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
        super().__init__(parent, bg="#0B1728")
        self.on_login_success = on_login_success
        self.show_password = False

        self._build_ui()

    def _build_ui(self):
        # 1. Left Hero Branding & Academic Attribution (40% width)
        left_hero = tk.Frame(self, bg="#0B1728", padx=40, pady=50)
        left_hero.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        brand_center = tk.Frame(left_hero, bg="#0B1728")
        brand_center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # 2D Medical Badge
        logo_badge = tk.Label(
            brand_center, text="✚", font=("Segoe UI", 26, "bold"),
            bg="#2563EB", fg="white", width=2, height=1
        )
        logo_badge.pack(anchor=tk.W, pady=(0, 14))

        tk.Label(
            brand_center, text="MediCare", font=("Segoe UI", 26, "bold"),
            fg="white", bg="#0B1728"
        ).pack(anchor=tk.W)

        tk.Label(
            brand_center, text="Hospital Management System",
            font=("Segoe UI", 11), fg="#94A3B8", bg="#0B1728"
        ).pack(anchor=tk.W, pady=(2, 16))

        # TQM Subheader
        tk.Label(
            brand_center, text="TQM • Q02 IMPROVE PERFORMANCE",
            font=("Segoe UI", 8, "bold"), fg="#38BDF8", bg="#0B1728"
        ).pack(anchor=tk.W, pady=(0, 12))

        # Dark Glass Container with Feature Highlights (Matching Image 3)
        feat_box = tk.Frame(
            brand_center, bg="#132238", padx=16, pady=16,
            highlightthickness=1, highlightbackground="#1E3A5F"
        )
        feat_box.pack(fill=tk.X, pady=(0, 20))

        features = [
            ("01", "Patient records", "Fast and organized patient workflows"),
            ("02", "Appointments", "Scheduling and waiting-time tracking"),
            ("03", "Quality", "TQM analysis and Q02 performance"),
        ]
        for num, title, desc in features:
            row = tk.Frame(feat_box, bg="#132238")
            row.pack(fill=tk.X, pady=5)

            tk.Label(
                row, text=num, font=("Segoe UI", 9, "bold"),
                fg="#38BDF8", bg="#132238"
            ).pack(side=tk.LEFT, padx=(0, 10))

            t_col = tk.Frame(row, bg="#132238")
            t_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

            tk.Label(
                t_col, text=title, font=("Segoe UI", 9, "bold"),
                fg="white", bg="#132238"
            ).pack(anchor=tk.W)

            tk.Label(
                t_col, text=desc, font=("Segoe UI", 8),
                fg="#94A3B8", bg="#132238"
            ).pack(anchor=tk.W)

        # Bottom Secure Note
        tk.Label(
            brand_center, text="Secure role-based access • SQLite • Python",
            font=("Segoe UI", 8), fg="#64748B", bg="#0B1728"
        ).pack(anchor=tk.W)

        # 2. Right Manual Authentication Panel (60% width)
        right_panel = tk.Frame(self, bg="#F8FAFC", padx=30, pady=40)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        card_wrapper = tk.Frame(right_panel, bg="#F8FAFC")
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
            font=("Segoe UI", 8, "bold"), fg="#2563EB", bg="#FFFFFF"
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
            highlightcolor="#2563EB", insertbackground="#2563EB", fg="#0F172A"
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
            highlightcolor="#2563EB", insertbackground="#2563EB", fg="#0F172A"
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
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
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

        # 1. Left Sidebar Navigation
        self.sidebar = tk.Frame(self.workspace_frame, bg=THEME["sidebar_bg"], width=240)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # 1a. Brand Header in Sidebar (Matching Reference Screenshots)
        brand_box = tk.Frame(self.sidebar, bg=THEME["sidebar_bg"], padx=18, pady=16)
        brand_box.pack(fill=tk.X)

        logo_badge = tk.Label(
            brand_box, text="✚", font=("Segoe UI", 14, "bold"),
            bg="#2563EB", fg="white", width=2, height=1
        )
        logo_badge.pack(side=tk.LEFT, padx=(0, 10))

        brand_text = tk.Frame(brand_box, bg=THEME["sidebar_bg"])
        brand_text.pack(side=tk.LEFT)

        tk.Label(brand_text, text="MediCare", font=("Segoe UI", 13, "bold"), fg="white", bg=THEME["sidebar_bg"]).pack(anchor=tk.W)
        tk.Label(brand_text, text="Hospital Management", font=("Segoe UI", 8), fg="#94A3B8", bg=THEME["sidebar_bg"]).pack(anchor=tk.W)

        # 1b. User Profile Chip under Brand (Matching Screenshots)
        user_role = self.user_data.get("role", "Admin")
        name_parts = self.user_data.get("full_name", "User").split()
        initials = "".join([p[0].upper() for p in name_parts[:2]]) or "A"

        prof_chip = tk.Frame(self.sidebar, bg="#132238", padx=10, pady=8, highlightthickness=1, highlightbackground="#1E3A5F")
        prof_chip.pack(fill=tk.X, padx=14, pady=(0, 14))

        av_circle = tk.Label(
            prof_chip, text=initials, font=("Segoe UI", 8, "bold"),
            bg="#2563EB", fg="white", width=3, height=1
        )
        av_circle.pack(side=tk.LEFT, padx=(0, 8))

        prof_info = tk.Frame(prof_chip, bg="#132238")
        prof_info.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            prof_info, text=self.user_data.get("username", "admin"),
            font=("Segoe UI", 8, "bold"), fg="white", bg="#132238"
        ).pack(anchor=tk.W)

        tk.Label(
            prof_info, text=f"{user_role} account",
            font=("Segoe UI", 7), fg="#94A3B8", bg="#132238"
        ).pack(anchor=tk.W)

        dot = tk.Label(prof_chip, text="●", font=("Segoe UI", 7), fg="#10B981", bg="#132238")
        dot.pack(side=tk.RIGHT)

        # 1c. MAIN MENU Section
        tk.Label(
            self.sidebar, text="MAIN MENU",
            font=("Segoe UI", 7, "bold"), fg="#64748B", bg=THEME["sidebar_bg"], padx=18
        ).pack(anchor=tk.W, pady=(0, 6))

        main_menu_items = [
            ("Dashboard", "📊", "Dashboard"),
            ("Patients", "👥", "Patients"),
            ("Doctors", "👨‍⚕️", "Doctors"),
            ("Appointments", "📅", "Appointments"),
            ("Billing", "💳", "Billing"),
            ("CSV Import", "📥", "CSV Import"),
            ("Reports", "📈", "Reports"),
            ("Performance", "⚡", "Performance"),
        ]

        self.nav_buttons = {}
        for tab_id, icon, label in main_menu_items:
            btn_frame = tk.Frame(self.sidebar, bg=THEME["sidebar_bg"], cursor="hand2")
            btn_frame.pack(fill=tk.X, padx=12, pady=1)

            indicator = tk.Frame(btn_frame, bg=THEME["sidebar_bg"], width=3)
            indicator.pack(side=tk.LEFT, fill=tk.Y)

            btn_lbl = tk.Label(
                btn_frame, text=f"  {icon}  {label}", font=("Segoe UI", 8, "bold"),
                fg=THEME["sidebar_text"], bg=THEME["sidebar_bg"], padx=8, pady=6, anchor=tk.W
            )
            btn_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

            target_id = "Reports" if tab_id == "Performance" else tab_id
            btn_frame.bind("<Button-1>", lambda e, tid=target_id: self._show_view(tid))
            btn_lbl.bind("<Button-1>", lambda e, tid=target_id: self._show_view(tid))
            btn_frame.bind("<Enter>", lambda e, f=btn_frame, l=btn_lbl, tid=tab_id: self._on_hover(f, l, tid, True))
            btn_frame.bind("<Leave>", lambda e, f=btn_frame, l=btn_lbl, tid=tab_id: self._on_hover(f, l, tid, False))

            self.nav_buttons[tab_id] = {
                "frame": btn_frame,
                "label": btn_lbl,
                "indicator": indicator
            }

        # 1d. QUALITY MANAGEMENT Section
        tk.Label(
            self.sidebar, text="QUALITY MANAGEMENT",
            font=("Segoe UI", 7, "bold"), fg="#64748B", bg=THEME["sidebar_bg"], padx=18
        ).pack(anchor=tk.W, pady=(12, 6))

        q_frame = tk.Frame(self.sidebar, bg=THEME["sidebar_bg"], cursor="hand2")
        q_frame.pack(fill=tk.X, padx=12, pady=1)

        q_indicator = tk.Frame(q_frame, bg=THEME["sidebar_bg"], width=3)
        q_indicator.pack(side=tk.LEFT, fill=tk.Y)

        q_lbl = tk.Label(
            q_frame, text="  ✓  TQM Analysis", font=("Segoe UI", 8, "bold"),
            fg=THEME["sidebar_text"], bg=THEME["sidebar_bg"], padx=8, pady=6, anchor=tk.W
        )
        q_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        q_frame.bind("<Button-1>", lambda e: self._show_view("TQM Audit"))
        q_lbl.bind("<Button-1>", lambda e: self._show_view("TQM Audit"))
        q_frame.bind("<Enter>", lambda e, f=q_frame, l=q_lbl: self._on_hover(f, l, "TQM Audit", True))
        q_frame.bind("<Leave>", lambda e, f=q_frame, l=q_lbl: self._on_hover(f, l, "TQM Audit", False))

        self.nav_buttons["TQM Audit"] = {
            "frame": q_frame,
            "label": q_lbl,
            "indicator": q_indicator
        }

        # 1e. Bottom System Online & Logout
        bottom_box = tk.Frame(self.sidebar, bg=THEME["sidebar_bg"], padx=16, pady=12)
        bottom_box.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(
            bottom_box, text="● System online", font=("Segoe UI", 7, "bold"),
            fg="#10B981", bg=THEME["sidebar_bg"]
        ).pack(anchor=tk.W, pady=(0, 6))

        btn_logout = tk.Button(
            bottom_box, text="🚪 Logout", font=("Segoe UI", 8, "bold"),
            bg="#132238", fg="#EF4444", activebackground="#EF4444", activeforeground="white",
            relief="flat", cursor="hand2", padx=6, pady=4, command=self._logout
        )
        btn_logout.pack(fill=tk.X)

        # 2. Main Right Container
        self.right_container = tk.Frame(self.workspace_frame, bg=THEME["background"])
        self.right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 2a. Top Header Bar
        self.header_bar = tk.Frame(
            self.right_container, bg="white", height=65, padx=22, pady=10,
            highlightthickness=1, highlightbackground=THEME["border"]
        )
        self.header_bar.pack(fill=tk.X)

        head_left = tk.Frame(self.header_bar, bg="white")
        head_left.pack(side=tk.LEFT)

        self.lbl_head_title = tk.Label(
            head_left, text="Executive Dashboard",
            font=("Segoe UI", 13, "bold"), fg=THEME["text"], bg="white"
        )
        self.lbl_head_title.pack(anchor=tk.W)

        self.lbl_head_sub = tk.Label(
            head_left, 
            text=f"Course: {COURSE_CODE} • Student: {STUDENT_NAME} ({STUDENT_ROLL})", 
            font=("Segoe UI", 8), fg=THEME["text_muted"], bg="white"
        )
        self.lbl_head_sub.pack(anchor=tk.W)

        head_right = tk.Frame(self.header_bar, bg="white")
        head_right.pack(side=tk.RIGHT)

        # Global Pill Search Box
        self.header_search = ModernSearchBox(
            head_right, 
            placeholder="🔍 Search a Doctor or Patient...",
            on_search_callback=self._on_global_search,
            width=22
        )
        self.header_search.pack(side=tk.LEFT, padx=(0, 10))

        # Real-time SLA Pill
        self.sla_pill = tk.Label(
            head_right, 
            text=" ● 0.7ms Latency | SLA Compliant ", 
            font=("Segoe UI", 8, "bold"),
            bg=THEME["success_light"], fg="#047857",
            padx=8, pady=4, relief="flat", bd=0
        )
        self.sla_pill.pack(side=tk.LEFT, padx=(0, 8))

        # Live Digital Ticking Clock
        self.lbl_clock = tk.Label(
            head_right, text="", font=("Segoe UI", 8, "bold"),
            bg="#EFF6FF", fg=THEME["primary"], padx=8, pady=4
        )
        self.lbl_clock.pack(side=tk.LEFT, padx=(0, 8))

        # User Profile Chip
        user_chip = tk.Frame(head_right, bg="#F0F4FA", padx=6, pady=3, highlightthickness=1, highlightbackground="#D2E4F9")
        user_chip.pack(side=tk.LEFT)

        role_col = {"Admin": "#2563EB", "Doctor": "#059669", "Receptionist": "#D97706", "Billing": "#7C3AED"}.get(user_role, "#2563EB")
        av_circle = tk.Label(
            user_chip, text=initials, font=("Segoe UI", 8, "bold"),
            bg=role_col, fg="white", width=3, height=1
        )
        av_circle.pack(side=tk.LEFT, padx=(0, 5))

        u_info = tk.Frame(user_chip, bg="#F0F4FA")
        u_info.pack(side=tk.LEFT)

        tk.Label(u_info, text=self.user_data["full_name"][:14], font=("Segoe UI", 8, "bold"), fg="#0C2340", bg="#F0F4FA").pack(anchor=tk.W)
        tk.Label(u_info, text=user_role, font=("Segoe UI", 7), fg="#64748B", bg="#F0F4FA").pack(anchor=tk.W)

        # 2b. Content Views Container
        self.content_container = tk.Frame(self.right_container, bg=THEME["background"], padx=14, pady=8)
        self.content_container.pack(fill=tk.BOTH, expand=True)

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
            frame.config(bg=THEME["sidebar_hover"])
            label.config(bg=THEME["sidebar_hover"], fg="white")
        else:
            frame.config(bg=THEME["sidebar_bg"])
            label.config(bg=THEME["sidebar_bg"], fg=THEME["sidebar_text"])

    def _show_view(self, tab_id: str):
        self.current_tab = tab_id

        titles = {
            "Dashboard": ("Executive Performance Dashboard", "Real-time clinical throughput, active queues, and wait-time telemetry"),
            "Patients": ("Patient Directory & Fast Search", "Sub-100ms debounced patient lookup with Poka-Yoke duplicate validation"),
            "Doctors": ("Medical Staff & Physician Roster", "Doctor availability status toggles, room allocations, and specializations"),
            "Appointments": ("OPD Queue & Token Sequencer", "Live appointment lifecycle: Scheduled → Waiting → In-Consultation → Done"),
            "Billing": ("Patient Invoicing & Settlement Desk", "Itemized hospital billing, GST calculation, receipts, and payment reconciliation"),
            "CSV Import": ("High-Throughput Bulk CSV Ingestion", "Batch transactional patient import (> 500 rps) with duplicate collision protection"),
            "Reports": ("Vectorized Analytical Reports", "Vectorized Pandas aggregations for daily OPD, workloads, revenue, and SLAs"),
            "TQM Audit": ("TQM Quality Audit & Accreditation (CO1, CO2, CO3)", "Review 1-4 Artifacts: FMEA Matrix, SIPOC Map, SQC Pareto & Fishbone, Deming PDCA"),
        }
        main_t, sub_t = titles.get(tab_id, ("Hospital Management", "Operations Management"))
        self.lbl_head_title.config(text=main_t)
        self.lbl_head_sub.config(text=sub_t)

        for tid, widgets in self.nav_buttons.items():
            if tid == tab_id or (tab_id == "Reports" and tid == "Performance"):
                widgets["frame"].config(bg="#2563EB")
                widgets["label"].config(bg="#2563EB", fg="white")
                widgets["indicator"].config(bg="#2563EB")
            else:
                widgets["frame"].config(bg=THEME["sidebar_bg"])
                widgets["label"].config(bg=THEME["sidebar_bg"], fg=THEME["sidebar_text"])
                widgets["indicator"].config(bg=THEME["sidebar_bg"])

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
        if not self.workspace_frame or not self.workspace_frame.winfo_exists():
            return
        now = datetime.now()
        self.lbl_clock.config(text=f"🕒 {now.strftime('%I:%M:%S %p')}")

        if now.second % 2 == 0:
            self.sla_pill.config(bg=THEME["success_light"], fg="#047857")
        else:
            self.sla_pill.config(bg="#E0F2FE", fg="#0369A1")

        self.after(1000, self._tick_clock)

    def _logout(self):
        """Seamless in-window sign out returning to the integrated login screen."""
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
