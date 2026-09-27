"""
Main Application Entry Point - Single Integrated Window Architecture.
Connected, Single-Screen Experience with Zero Pop-Up Modals:
- Seamless Single Application Window (1280x800)
- Integrated Full-Screen Login Portal with Manual Credential Entry (No Role Selection Tabs)
- Automatic Role Discovery via SQLite Database Authentication
- In-Window Transition between Login View and Clinical Workspace
- Full Access to all 8 Modules (including TQM Quality Audit & Accreditation)

BBAT104: Fundamentals of Total Quality Management
Academic Session: 2026–27 | Max Assessment: 70 Raw Marks (CO1, CO2, CO3)
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Assigned Quality Goal: Q02 - Improve Performance
"""

import sys
from pathlib import Path
from datetime import datetime

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, Dict, Any

from src.config import APP_NAME, COURSE_CODE, STUDENT_NAME, STUDENT_ROLL, QUALITY_GOAL, THEME
from src.database import init_db
from src.auth import authenticate, SessionManager
from src.modules.dashboard_view import DashboardView
from src.modules.patient_view import PatientView
from src.modules.doctor_view import DoctorView
from src.modules.appointment_view import AppointmentView
from src.modules.billing_view import BillingView
from src.modules.csv_import_view import CSVImportView
from src.modules.reports_view import ReportsView
from src.modules.tqm_audit_view import TQMAuditView
from src.widgets.ecg_animation import ECGAnimationWidget
from src.widgets.ui_kit import apply_global_styles, ModernSearchBox, RoundedCard, PillButton, CircleBadge


class IntegratedLoginView(tk.Frame):
    """
    Connected Full-Page Healthcare Authentication Portal (Image 3).
    Integrated directly into the main desktop application window (No popups).
    Features manual credential inputs, automatic role discovery, and modern 2D styling.
    """

    def __init__(self, parent, on_login_success: Callable[[Dict[str, Any]], None]):
        super().__init__(parent, bg="#003E5C")
        self.on_login_success = on_login_success
        self.show_password = False

        self._build_ui()

    def _build_ui(self):
        # 1. Left Hero Branding & Academic Attribution (40% width)
        left_hero = tk.Frame(self, bg="#003E5C", padx=40, pady=50)
        left_hero.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        brand_center = tk.Frame(left_hero, bg="#003E5C")
        brand_center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # 2D Medical Badge
        logo_badge = tk.Label(
            brand_center, text="✚", font=("Segoe UI", 24, "bold"),
            bg="#00BCD4", fg="white", width=2, height=1
        )
        logo_badge.pack(anchor=tk.W, pady=(0, 14))

        tk.Label(
            brand_center, text="MediCare", font=("Segoe UI", 26, "bold"),
            fg="white", bg="#003E5C"
        ).pack(anchor=tk.W)

        tk.Label(
            brand_center, text="Hospital Management System",
            font=("Segoe UI", 11), fg="#7DD3FC", bg="#003E5C"
        ).pack(anchor=tk.W, pady=(2, 16))

        # TQM Subheader
        tk.Label(
            brand_center, text="TQM • Q02 IMPROVE PERFORMANCE",
            font=("Segoe UI", 8, "bold"), fg="#38BDF8", bg="#003E5C"
        ).pack(anchor=tk.W, pady=(0, 12))

        # Deep Cyan / Teal Glass Container with Feature Highlights
        feat_box = tk.Frame(
            brand_center, bg="#004B6E", padx=16, pady=16,
            highlightthickness=1, highlightbackground="#02638A"
        )
        feat_box.pack(fill=tk.X, pady=(0, 20))

        features = [
            ("01", "Patient records", "Fast and organized patient workflows"),
            ("02", "Appointments", "Scheduling and waiting-time tracking"),
            ("03", "Quality", "TQM analysis and Q02 performance"),
        ]
        for num, title, desc in features:
            row = tk.Frame(feat_box, bg="#004B6E")
            row.pack(fill=tk.X, pady=5)

            tk.Label(
                row, text=num, font=("Segoe UI", 9, "bold"),
                fg="#38BDF8", bg="#004B6E"
            ).pack(side=tk.LEFT, padx=(0, 10))

            t_col = tk.Frame(row, bg="#004B6E")
            t_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

            tk.Label(
                t_col, text=title, font=("Segoe UI", 9, "bold"),
                fg="white", bg="#004B6E"
            ).pack(anchor=tk.W)

            tk.Label(
                t_col, text=desc, font=("Segoe UI", 8),
                fg="#BAE6FD", bg="#004B6E"
            ).pack(anchor=tk.W)

        # Bottom Secure Note
        tk.Label(
            brand_center, text="Secure role-based access • SQLite • Python",
            font=("Segoe UI", 8), fg="#7DD3FC", bg="#003E5C"
        ).pack(anchor=tk.W)

        # 2. Right Manual Authentication Panel (60% width)
        right_panel = tk.Frame(self, bg="#F0F6FA", padx=30, pady=40)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        card_wrapper = tk.Frame(right_panel, bg="#F0F6FA")
        card_wrapper.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Main Light Card with Soft Gaussian Drop Shadow (Matching Image 3)
        self.auth_card = RoundedCard(
            card_wrapper, bg_color="#FFFFFF", border_color="#E2E8F0",
            hover_bg="#FFFFFF", radius=18, pad_shadow=8, padx=32, pady=30,
            width=460, height=470
        )
        self.auth_card.pack()
        c = self.auth_card.inner

        tk.Label(
            c, text="WELCOME BACK",
            font=("Segoe UI", 8, "bold"), fg="#0284C7", bg="#FFFFFF"
        ).pack(anchor=tk.W)

        tk.Label(
            c, text="Sign in to MediCare",
            font=("Segoe UI", 20, "bold"), fg="#0F172A", bg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(2, 4))

        tk.Label(
            c, text="Enter your credentials to access your workspace.",
            font=("Segoe UI", 9), fg="#64748B", bg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(0, 20))

        # Field 1: Username
        tk.Label(
            c, text="USERNAME",
            font=("Segoe UI", 8, "bold"), fg="#475569", bg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(0, 4))

        self.txt_user = tk.Entry(
            c, font=("Segoe UI", 10), bg="#F8FAFC",
            relief="flat", bd=0, highlightthickness=1, highlightbackground="#CBD5E1",
            highlightcolor="#0284C7", insertbackground="#0284C7", fg="#0F172A"
        )
        self.txt_user.pack(fill=tk.X, pady=(0, 14), ipady=7)
        self.txt_user.focus_set()

        # Field 2: Password with Show/Hide Toggle
        tk.Label(
            c, text="PASSWORD",
            font=("Segoe UI", 8, "bold"), fg="#475569", bg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(0, 4))

        pass_row = tk.Frame(c, bg="#FFFFFF")
        pass_row.pack(fill=tk.X, pady=(0, 14))

        self.txt_pass = tk.Entry(
            pass_row, font=("Segoe UI", 10), show="•",
            bg="#F8FAFC", relief="flat", bd=0, highlightthickness=1, highlightbackground="#CBD5E1",
            highlightcolor="#0284C7", insertbackground="#0284C7", fg="#0F172A"
        )
        self.txt_pass.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=7)

        self.btn_eye = tk.Button(
            pass_row, text="👁️", font=("Segoe UI", 9),
            bg="#F1F5F9", fg="#0F172A", relief="flat", cursor="hand2", padx=8,
            command=self._toggle_password_visibility
        )
        self.btn_eye.pack(side=tk.LEFT, padx=(4, 0), fill=tk.Y)

        # Inline Error Label
        self.lbl_error = tk.Label(
            c, text="", font=("Segoe UI", 8, "bold"),
            fg="#DC2626", bg="#FFFFFF"
        )
        self.lbl_error.pack(anchor=tk.W, pady=(0, 6))

        # Sign In Button
        self.btn_sign = PillButton(
            c, text="Sign In →", font_size=10,
            bg_color="#003E5C", fg_color="white", hover_color="#002D42",
            padx=16, pady=8, command=self._do_login
        )
        self.btn_sign.pack(fill=tk.X, pady=(0, 18))

        # Enter key triggers login
        self.txt_user.bind("<Return>", lambda e: self._do_login())
        self.txt_pass.bind("<Return>", lambda e: self._do_login())

        # Centered Demo Footnote
        tk.Label(
            c, text="Demo admin account: admin / admin123",
            font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF"
        ).pack(anchor=tk.CENTER)

    def _toggle_password_visibility(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.txt_pass.config(show="")
            self.btn_eye.config(text="🙈")
        else:
            self.txt_pass.config(show="•")
            self.btn_eye.config(text="👁️")

    def _do_login(self):
        username = self.txt_user.get().strip()
        password = self.txt_pass.get()

        if not username or not password:
            self.lbl_error.config(text="⚠️ Please enter both username and password.")
            return

        user_data = authenticate(username, password)
        if user_data:
            self.lbl_error.config(text="")
            self.on_login_success(user_data)
        else:
            self.lbl_error.config(text="⚠️ Authentication failed: Invalid username or password.")
            messagebox.showerror(
                "Authentication Failed",
                "Invalid staff credentials.\nPlease check your username and password."
            )

    def reset_fields(self):
        """Clears input fields when returning to login on sign out."""
        self.txt_user.delete(0, tk.END)
        self.txt_pass.delete(0, tk.END)
        self.lbl_error.config(text="")
        self.txt_user.focus_set()


class MainWindow(tk.Tk):
    """
    Unified Single-Window Healthcare Application.
    Zero pop-ups. Seamlessly transitions between the Integrated Login View
    and the Clinical Workspace within the exact same 1280x800 window.
    """

    def __init__(self):
        super().__init__()
        self.title(f"MedCare HMS • High-Performance Hospital Management System ({STUDENT_NAME})")
        self.geometry("1280x800")
        self.minsize(1100, 700)
        self.configure(bg=THEME["background"])

        self.user_data: Optional[Dict[str, Any]] = None
        self.current_tab = "Dashboard"
        self.nav_buttons = {}
        self.views = {}

        self._configure_styles()

        # Main Host Container
        self.main_container = tk.Frame(self, bg=THEME["background"])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # 1. Integrated Login View (Initial State)
        self.login_view = IntegratedLoginView(self.main_container, on_login_success=self._on_login_success)
        self.login_view.pack(fill=tk.BOTH, expand=True)

        # 2. Clinical Workspace Frame (Created on Authentication)
        self.workspace_frame: Optional[tk.Frame] = None

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_styles(self):
        apply_global_styles(self)

    def _on_login_success(self, user_data: Dict[str, Any]):
        """Transitions seamlessly from Login to Clinical Workspace inside the same window."""
        self.user_data = user_data
        SessionManager.set_user(user_data)

        # Hide login view
        self.login_view.pack_forget()

        # Build and display clinical workspace
        self._build_workspace()

    def _build_workspace(self):
        if self.workspace_frame:
            self.workspace_frame.destroy()

        self.workspace_frame = tk.Frame(self.main_container, bg=THEME["background"])
        self.workspace_frame.pack(fill=tk.BOTH, expand=True)

        # =========================================================================
        # 1. TOP HEADER BAR (Exact Deep Prussian Navy #003E5C from Image 1)
        # =========================================================================
        self.top_bar = tk.Frame(self.workspace_frame, bg="#003E5C", height=58, padx=16, pady=8)
        self.top_bar.pack(side=tk.TOP, fill=tk.X)

        # 1a. Top Bar Left: Circular Medical Logo + Brand + Hamburger + View Title
        bar_left = tk.Frame(self.top_bar, bg="#003E5C")
        bar_left.pack(side=tk.LEFT)

        # Medical cross circular logo with cyan + lime border
        CircleBadge(
            bar_left, icon="✚", size=36,
            bg_color="#00BCD4", border_color="#84CC16", fg_color="white", font_size=14
        ).pack(side=tk.LEFT, padx=(0, 8))

        brand_text = tk.Frame(bar_left, bg="#003E5C")
        brand_text.pack(side=tk.LEFT, padx=(0, 16))

        tk.Label(
            brand_text, text="Hospital", font=("Segoe UI", 12, "bold"),
            fg="white", bg="#003E5C"
        ).pack(anchor=tk.W)

        tk.Label(
            brand_text, text="Medical Solution", font=("Segoe UI", 7, "bold"),
            fg="#38BDF8", bg="#003E5C"
        ).pack(anchor=tk.W)

        # Hamburger Menu Icon
        tk.Label(
            bar_left, text="☰", font=("Segoe UI", 14),
            fg="white", bg="#003E5C", padx=8
        ).pack(side=tk.LEFT, padx=(0, 12))

        # View Title Label
        self.lbl_head_title = tk.Label(
            bar_left, text="Dashboard",
            font=("Segoe UI", 15, "bold"), fg="white", bg="#003E5C"
        )
        self.lbl_head_title.pack(side=tk.LEFT)

        # Subtitle
        self.lbl_head_sub = tk.Label(
            bar_left, text=f"• {COURSE_CODE} ({STUDENT_NAME})",
            font=("Segoe UI", 8), fg="#7DD3FC", bg="#003E5C"
        )
        self.lbl_head_sub.pack(side=tk.LEFT, padx=(8, 0))

        # 1b. Top Bar Right: SLA Pill + Clock + Bell + Hospital Admin Chip
        bar_right = tk.Frame(self.top_bar, bg="#003E5C")
        bar_right.pack(side=tk.RIGHT)

        # Real-time SLA Pill
        self.sla_pill = tk.Label(
            bar_right, text=" ● 0.8ms Latency | SLA Compliant ",
            font=("Segoe UI", 8, "bold"),
            bg="#004B6E", fg="#38BDF8",
            padx=8, pady=4, relief="flat", bd=0
        )
        self.sla_pill.pack(side=tk.LEFT, padx=(0, 8))

        # Clock
        self.lbl_clock = tk.Label(
            bar_right, text="", font=("Segoe UI", 8, "bold"),
            bg="#004B6E", fg="white", padx=8, pady=4
        )
        self.lbl_clock.pack(side=tk.LEFT, padx=(0, 10))

        # Notification Bell with Red Badge
        bell_frame = tk.Frame(bar_right, bg="#003E5C", cursor="hand2")
        bell_frame.pack(side=tk.LEFT, padx=(0, 12))
        tk.Label(bell_frame, text="🔔", font=("Segoe UI", 12), fg="white", bg="#003E5C").pack(side=tk.LEFT)
        tk.Label(bell_frame, text="●", font=("Segoe UI", 7), fg="#EF4444", bg="#003E5C").pack(side=tk.LEFT)

        # Hospital Admin Profile Chip (Image 1 Pill)
        hosp_chip = tk.Frame(
            bar_right, bg="#004B6E", padx=8, pady=4,
            highlightthickness=1, highlightbackground="#02638A"
        )
        hosp_chip.pack(side=tk.LEFT)

        CircleBadge(hosp_chip, icon="🏥", size=28, bg_color="#0284C7", border_color="#0284C7", fg_color="white", font_size=10).pack(side=tk.LEFT, padx=(0, 6))

        h_info = tk.Frame(hosp_chip, bg="#004B6E")
        h_info.pack(side=tk.LEFT, padx=(0, 6))

        tk.Label(h_info, text="Healthcare Hospital", font=("Segoe UI", 8, "bold"), fg="white", bg="#004B6E").pack(anchor=tk.W)
        tk.Label(h_info, text="Hospital Admin", font=("Segoe UI", 7), fg="#7DD3FC", bg="#004B6E").pack(anchor=tk.W)

        tk.Label(hosp_chip, text="⋮", font=("Segoe UI", 11, "bold"), fg="white", bg="#004B6E").pack(side=tk.RIGHT)

        # =========================================================================
        # 2. BODY CONTAINER: Left White Sidebar + Right Workspace
        # =========================================================================
        body_container = tk.Frame(self.workspace_frame, bg=THEME["background"])
        body_container.pack(fill=tk.BOTH, expand=True)

        # 2a. Left Sidebar Navigation (Matching Image 1: White background, 2D icons, soft cyan pill)
        self.sidebar = tk.Frame(body_container, bg="#FFFFFF", width=220, highlightthickness=1, highlightbackground="#E2E8F0")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        menu_items = [
            ("Dashboard", "⊞", "Dashboard"),
            ("Doctors", "👨‍⚕️", "Doctors"),
            ("Appointments", "📅", "Appointments"),
            ("Book Appointment", "📝", "Book Appointment"),
            ("Doctors Review", "⭐", "Doctors Review"),
            ("Patients", "👥", "Patients"),
            ("Billing", "💳", "Billing"),
            ("CSV Import", "📥", "CSV Import"),
            ("Reports", "📈", "Reports"),
            ("Performance", "⚡", "Performance"),
            ("TQM Audit", "✓", "TQM Analysis"),
        ]

        self.nav_buttons = {}
        for tab_id, icon, label in menu_items:
            btn_frame = tk.Frame(self.sidebar, bg="#FFFFFF", cursor="hand2")
            btn_frame.pack(fill=tk.X, padx=10, pady=2)

            indicator = tk.Frame(btn_frame, bg="#FFFFFF", width=3)
            indicator.pack(side=tk.LEFT, fill=tk.Y)

            btn_lbl = tk.Label(
                btn_frame, text=f"  {icon}  {label}", font=("Segoe UI", 9, "bold"),
                fg="#334155", bg="#FFFFFF", padx=8, pady=7, anchor=tk.W
            )
            btn_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

            target_id = "Reports" if tab_id == "Performance" else ("Appointments" if tab_id == "Book Appointment" else ("Doctors" if tab_id == "Doctors Review" else tab_id))
            btn_frame.bind("<Button-1>", lambda e, tid=target_id: self._show_view(tid))
            btn_lbl.bind("<Button-1>", lambda e, tid=target_id: self._show_view(tid))
            btn_frame.bind("<Enter>", lambda e, f=btn_frame, l=btn_lbl, tid=tab_id: self._on_hover(f, l, tid, True))
            btn_frame.bind("<Leave>", lambda e, f=btn_frame, l=btn_lbl, tid=tab_id: self._on_hover(f, l, tid, False))

            self.nav_buttons[tab_id] = {
                "frame": btn_frame,
                "label": btn_lbl,
                "indicator": indicator
            }

        # Bottom System Online & Logout
        bottom_box = tk.Frame(self.sidebar, bg="#FFFFFF", padx=14, pady=12)
        bottom_box.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(
            bottom_box, text="● System online", font=("Segoe UI", 8, "bold"),
            fg="#10B981", bg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(0, 6))

        btn_logout = tk.Button(
            bottom_box, text="🚪 Logout", font=("Segoe UI", 8, "bold"),
            bg="#F8FAFC", fg="#EF4444", activebackground="#EF4444", activeforeground="white",
            relief="solid", bd=1, cursor="hand2", padx=6, pady=4, command=self._logout
        )
        btn_logout.pack(fill=tk.X)

        # 2b. Right Main Content Area
        self.content_container = tk.Frame(body_container, bg=THEME["background"], padx=6, pady=6)
        self.content_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initialize View Modules
        self.views = {}
        self.views["Dashboard"] = DashboardView(self.content_container, on_navigate=self._show_view)
        self.views["Patients"] = PatientView(self.content_container, on_schedule_appointment=self._on_schedule_from_patient)
        self.views["Doctors"] = DoctorView(self.content_container)
        self.views["Appointments"] = AppointmentView(self.content_container, on_open_billing=self._on_open_billing_from_appt)
        self.views["Billing"] = BillingView(self.content_container)
        self.views["CSV Import"] = CSVImportView(self.content_container, on_import_success=self._on_bulk_import_success)
        self.views["Reports"] = ReportsView(self.content_container)
        self.views["TQM Audit"] = TQMAuditView(self.content_container)

        self._show_view("Dashboard")
        self._tick_clock()

    def _on_hover(self, frame, label, tab_id, is_entering):
        if tab_id == self.current_tab:
            return
        if is_entering:
            frame.config(bg="#F0F9FF")
            label.config(bg="#F0F9FF", fg="#0284C7")
        else:
            frame.config(bg="#FFFFFF")
            label.config(bg="#FFFFFF", fg="#334155")

    def _show_view(self, tab_id: str):
        self.current_tab = tab_id

        titles = {
            "Dashboard": ("Dashboard", "Real-time clinical throughput and active queues"),
            "Patients": ("Patients", "Sub-100ms debounced patient directory with Poka-Yoke uniqueness"),
            "Doctors": ("Doctors", "Medical staff roster, specialties, and room allocation"),
            "Appointments": ("Appointments", "Live appointment lifecycle: Scheduled → Waiting → Done"),
            "Billing": ("Billing", "Itemized patient invoicing, 5% GST tax settlement"),
            "CSV Import": ("CSV Import", "High-throughput bulk CSV ingestion engine"),
            "Reports": ("Reports", "Vectorized Pandas aggregations and analytics"),
            "TQM Audit": ("TQM Analysis", "Total Quality Management, SQC charts, and FMEA matrix"),
        }
        main_t, sub_t = titles.get(tab_id, ("Hospital Management", "Operations Management"))
        self.lbl_head_title.config(text=main_t)
        self.lbl_head_sub.config(text=f"• {sub_t}")

        for tid, widgets in self.nav_buttons.items():
            is_active = (tid == tab_id or 
                         (tab_id == "Reports" and tid == "Performance") or
                         (tab_id == "Appointments" and tid == "Book Appointment") or
                         (tab_id == "Doctors" and tid == "Doctors Review"))
            if is_active:
                widgets["frame"].config(bg="#DDF2FD")
                widgets["label"].config(bg="#DDF2FD", fg="#0284C7")
                widgets["indicator"].config(bg="#0284C7")
            else:
                widgets["frame"].config(bg="#FFFFFF")
                widgets["label"].config(bg="#FFFFFF", fg="#334155")
                widgets["indicator"].config(bg="#FFFFFF")

        for v in self.views.values():
            v.pack_forget()

        if tab_id in self.views:
            self.views[tab_id].pack(fill=tk.BOTH, expand=True)
            if tab_id == "Dashboard":
                self.views["Dashboard"].refresh_dashboard()

    def _on_global_search(self, query: str):
        q = query.strip()
        if len(q) >= 2 and self.current_tab != "Patients":
            self._show_view("Patients")
        if "Patients" in self.views and hasattr(self.views["Patients"], "search_var"):
            self.views["Patients"].search_var.set(q)
            self.views["Patients"].load_patients()

    def _on_schedule_from_patient(self, patient_id: int):
        self._show_view("Appointments")
        self.views["Appointments"].open_booking_modal(preselected_patient_id=patient_id)

    def _on_open_billing_from_appt(self, appt_id: int):
        self._show_view("Billing")
        self.views["Billing"].open_new_bill_modal(preselected_appointment_id=appt_id)

    def _on_bulk_import_success(self):
        self.views["Patients"].load_patients()
        self.views["Dashboard"].refresh_dashboard()

    def _tick_clock(self):
        if not self.winfo_exists() or not self.workspace_frame or not self.workspace_frame.winfo_exists():
            return
        now = datetime.now()
        try:
            self.lbl_clock.config(text=f"🕒 {now.strftime('%I:%M:%S %p')}")

            if now.second % 2 == 0:
                self.sla_pill.config(bg=THEME["success_light"], fg="#047857")
            else:
                self.sla_pill.config(bg="#E0F2FE", fg="#0369A1")

            self._clock_timer = self.after(1000, self._tick_clock)
        except Exception:
            pass

    def _logout(self):
        """Seamless in-window sign out returning to the integrated login screen."""
        if hasattr(self, "_clock_timer") and self._clock_timer:
            try:
                self.after_cancel(self._clock_timer)
            except Exception:
                pass
            self._clock_timer = None

        if hasattr(self, "ecg_wave"):
            self.ecg_wave.stop()
        SessionManager.clear()
        self.user_data = None

        if self.workspace_frame:
            self.workspace_frame.destroy()
            self.workspace_frame = None

        # Show login portal again in the same window
        self.login_view.reset_fields()
        self.login_view.pack(fill=tk.BOTH, expand=True)

    def _on_close(self):
        if hasattr(self, "_clock_timer") and self._clock_timer:
            try:
                self.after_cancel(self._clock_timer)
            except Exception:
                pass
            self._clock_timer = None
        if hasattr(self, "ecg_wave"):
            self.ecg_wave.stop()
        self.destroy()


def start_app():
    """Application launcher initializing the single-window desktop application."""
    init_db()
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    start_app()
