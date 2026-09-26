"""
Main Application Entry Point - Modern Behance / Dribbble Healthcare UI.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Quality Goal: Q02 - Improve Performance
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
from src.widgets.ui_kit import apply_global_styles, ModernSearchBox, RoundedCard


class LoginWindow(tk.Tk):
    """Ultra-Modern Role-Based Healthcare Authentication Gateway."""

    ROLES_INFO = {
        "Admin": {
            "icon": "🛡️",
            "name": "Super Admin",
            "tagline": "System Administrator — Full TQM SLA controls, DB indexing & audit telemetry",
            "user": "admin",
            "pass": "admin123",
            "color": "#2563EB",
            "light_bg": "#EFF6FF",
            "border": "#BFDBFE"
        },
        "Doctor": {
            "icon": "🩺",
            "name": "Physician",
            "tagline": "Clinical Medical Officer — OPD patient queue, consultations & diagnosis",
            "user": "doctor",
            "pass": "doc123",
            "color": "#059669",
            "light_bg": "#ECFDF5",
            "border": "#A7F3D0"
        },
        "Reception": {
            "icon": "👩‍💼",
            "name": "Front Desk",
            "tagline": "OPD Admissions Desk — Token issuance, patient check-ins & fast search",
            "user": "reception",
            "pass": "rec123",
            "color": "#D97706",
            "light_bg": "#FFFBEB",
            "border": "#FDE68A"
        },
        "Billing": {
            "icon": "💳",
            "name": "Cashier",
            "tagline": "Financial Billing Desk — Invoicing, GST tax receipts & payment settlement",
            "user": "billing",
            "pass": "bill123",
            "color": "#7C3AED",
            "light_bg": "#F5F3FF",
            "border": "#DDD6FE"
        }
    }

    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.title("MedCare HMS • Secure Role-Based Gateway")
        self.geometry("520x680")
        self.resizable(False, False)
        self.configure(bg=THEME["sidebar_bg"])

        self.active_role = "Admin"
        self.role_buttons = {}
        self.show_password = False

        self._build_ui()
        self._select_role("Admin")

    def _build_ui(self):
        container = tk.Frame(self, bg=THEME["sidebar_bg"], padx=26, pady=22)
        container.pack(fill=tk.BOTH, expand=True)

        # 1. Top Brand Header
        brand_frame = tk.Frame(container, bg=THEME["sidebar_bg"])
        brand_frame.pack(fill=tk.X, pady=(0, 15))

        logo_box = tk.Label(
            brand_frame, text="✚", font=("Segoe UI", 22, "bold"),
            bg="#2563EB", fg="white", width=2, height=1
        )
        logo_box.pack(side=tk.LEFT, padx=(0, 12))

        title_box = tk.Frame(brand_frame, bg=THEME["sidebar_bg"])
        title_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            title_box, text="MedCare HMS Portal", font=("Segoe UI", 16, "bold"),
            fg="white", bg=THEME["sidebar_bg"]
        ).pack(anchor=tk.W)

        tk.Label(
            title_box, text=f"{COURSE_CODE} • TQM {QUALITY_GOAL} - Improve Performance", font=("Segoe UI", 8),
            fg="#94A3B8", bg=THEME["sidebar_bg"]
        ).pack(anchor=tk.W)

        # Pulse status badge
        tk.Label(
            brand_frame, text="● 24/7 OPD ONLINE", font=("Segoe UI", 7, "bold"),
            fg="#10B981", bg="#0B132B", padx=8, pady=3
        ).pack(side=tk.RIGHT)

        # 2. Main White Card with Soft Drop Shadow
        self.login_card = RoundedCard(
            container, bg_color="#FFFFFF", border_color="#E2E8F0",
            hover_bg="#FFFFFF", radius=18, pad_shadow=6, padx=22, pady=18
        )
        self.login_card.pack(fill=tk.BOTH, expand=True)
        card = self.login_card.inner

        tk.Label(
            card, text="Role-Based Authentication", font=("Segoe UI", 13, "bold"),
            fg=THEME["text"], bg="white"
        ).pack(anchor=tk.W)

        tk.Label(
            card, text="Select your clinical staff role below to configure authentication:",
            font=("Segoe UI", 8), fg=THEME["text_muted"], bg="white"
        ).pack(anchor=tk.W, pady=(2, 12))

        # 3. Role Selector Segmented Bar (4 Tabs)
        role_strip = tk.Frame(card, bg="#F1F5F9", padx=3, pady=3)
        role_strip.pack(fill=tk.X, pady=(0, 12))

        for r_key, r_data in self.ROLES_INFO.items():
            btn = tk.Button(
                role_strip, text=f"{r_data['icon']} {r_data['name']}",
                font=("Segoe UI", 8, "bold"),
                relief="flat", cursor="hand2", padx=6, pady=6, bd=0,
                command=lambda k=r_key: self._select_role(k)
            )
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            self.role_buttons[r_key] = btn

        # 4. Dynamic Role Description Banner
        self.role_banner = tk.Frame(card, bg="#EFF6FF", padx=10, pady=8, highlightthickness=1, highlightbackground="#BFDBFE")
        self.role_banner.pack(fill=tk.X, pady=(0, 14))

        self.lbl_role_desc = tk.Label(
            self.role_banner, text="", font=("Segoe UI", 8, "bold"),
            fg="#1D4ED8", bg="#EFF6FF", wraplength=420, justify=tk.LEFT
        )
        self.lbl_role_desc.pack(anchor=tk.W)

        # 5. Username Field
        lbl_user_frame = tk.Frame(card, bg="white")
        lbl_user_frame.pack(fill=tk.X, pady=(0, 3))
        tk.Label(lbl_user_frame, text="👤 Staff ID / Username", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(side=tk.LEFT)
        self.lbl_user_hint = tk.Label(lbl_user_frame, text="(admin)", font=("Segoe UI", 8), fg="#64748B", bg="white")
        self.lbl_user_hint.pack(side=tk.RIGHT)

        self.txt_user = tk.Entry(card, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_user.pack(fill=tk.X, pady=(0, 12), ipady=5)

        # 6. Password Field with Show/Hide Toggle
        lbl_pass_frame = tk.Frame(card, bg="white")
        lbl_pass_frame.pack(fill=tk.X, pady=(0, 3))
        tk.Label(lbl_pass_frame, text="🔒 Password", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(side=tk.LEFT)

        pass_row = tk.Frame(card, bg="white")
        pass_row.pack(fill=tk.X, pady=(0, 14))

        self.txt_pass = tk.Entry(pass_row, font=("Segoe UI", 10), show="•", bg="#F8FAFC", relief="solid", bd=1)
        self.txt_pass.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)

        self.btn_toggle_eye = tk.Button(
            pass_row, text="👁️", font=("Segoe UI", 9),
            bg="#F1F5F9", fg=THEME["text"], relief="flat", cursor="hand2", padx=8,
            command=self._toggle_password_visibility
        )
        self.btn_toggle_eye.pack(side=tk.LEFT, padx=(4, 0), fill=tk.Y)

        # Error notification label (hidden when no error)
        self.lbl_error = tk.Label(card, text="", font=("Segoe UI", 8, "bold"), fg="#DC2626", bg="white")
        self.lbl_error.pack(fill=tk.X, pady=(0, 8))

        # 7. Sign In Button
        self.btn_sign = tk.Button(
            card, text="🚀 Authenticate & Enter Portal →", font=("Segoe UI", 10, "bold"),
            bg=THEME["primary"], fg="white", activebackground=THEME["primary_dark"], activeforeground="white",
            relief="flat", cursor="hand2", command=self._do_login
        )
        self.btn_sign.pack(fill=tk.X, ipady=8, pady=(0, 10))

        # 8. Footer Student Attribution
        footer_box = tk.Frame(container, bg=THEME["sidebar_bg"])
        footer_box.pack(fill=tk.X, pady=(10, 0))

        tk.Label(
            footer_box, 
            text=f"Developed by {STUDENT_NAME} | Roll No: {STUDENT_ROLL} | CSE - A",
            font=("Segoe UI", 8), fg="#94A3B8", bg=THEME["sidebar_bg"]
        ).pack(anchor=tk.CENTER)
        tk.Label(
            footer_box, 
            text="Assigned Goal: Q02 (Improve Performance) • SQLite WAL Mode & B-Tree Optimization",
            font=("Segoe UI", 7), fg="#64748B", bg=THEME["sidebar_bg"]
        ).pack(anchor=tk.CENTER)

    def _select_role(self, role_key: str):
        self.active_role = role_key
        r_info = self.ROLES_INFO[role_key]

        # Update Tab Button styles
        for k, btn in self.role_buttons.items():
            if k == role_key:
                btn.config(bg="white", fg=r_info["color"], relief="solid")
            else:
                btn.config(bg="#F1F5F9", fg="#64748B", relief="flat")

        # Update Role Description Banner
        self.role_banner.config(bg=r_info["light_bg"], highlightbackground=r_info["border"])
        self.lbl_role_desc.config(text=f"{r_info['icon']} {r_info['tagline']}", fg=r_info["color"], bg=r_info["light_bg"])
        self.btn_sign.config(bg=r_info["color"])

        # Populate Credentials
        self.txt_user.delete(0, tk.END)
        self.txt_user.insert(0, r_info["user"])
        self.lbl_user_hint.config(text=f"({r_info['user']})")

        self.txt_pass.delete(0, tk.END)
        self.txt_pass.insert(0, r_info["pass"])
        self.lbl_error.config(text="")

    def _toggle_password_visibility(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.txt_pass.config(show="")
            self.btn_toggle_eye.config(text="🙈")
        else:
            self.txt_pass.config(show="•")
            self.btn_toggle_eye.config(text="👁️")

    def _do_login(self):
        user = self.txt_user.get().strip()
        pwd = self.txt_pass.get()
        user_data = authenticate(user, pwd)
        if user_data:
            self.destroy()
            self.on_login_success(user_data)
        else:
            self.lbl_error.config(text="⚠️ Authentication failed: Invalid username or password for this role.")
            messagebox.showerror("Authentication Failed", f"Invalid credentials for {self.active_role} role.\nPlease check username and password.")


class MainWindow(tk.Tk):
    """
    Modern Behance / Dribbble Healthcare Architecture:
    - Deep Slate Left Sidebar Navigation with active pill state
    - Clean Top Header with Breadcrumbs, Live Clock & Real-time SLA Pill
    - Card-based Content Views with Smooth Swapping
    """

    def __init__(self, user_data: dict):
        super().__init__()
        self.user_data = user_data
        self.title(f"MedCare HMS • High-Performance Hospital Management System ({STUDENT_NAME})")
        self.geometry("1280x800")
        self.minsize(1100, 700)
        self.configure(bg=THEME["background"])

        self.current_tab = "Dashboard"
        self.nav_buttons = {}
        self.views = {}

        self._configure_styles()
        self._build_layout()
        self._show_view("Dashboard")
        self._tick_clock()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_styles(self):
        apply_global_styles(self)

    def _build_layout(self):
        # 1. Left Sidebar Navigation (240px)
        self.sidebar = tk.Frame(self, bg=THEME["sidebar_bg"], width=240)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # 1a. Sidebar Brand Header
        brand_box = tk.Frame(self.sidebar, bg=THEME["sidebar_bg"], padx=18, pady=22)
        brand_box.pack(fill=tk.X)

        logo_badge = tk.Label(
            brand_box, text="✦", font=("Segoe UI", 16, "bold"),
            bg=THEME["primary"], fg="white", width=2, height=1
        )
        logo_badge.pack(side=tk.LEFT, padx=(0, 10))

        brand_text = tk.Frame(brand_box, bg=THEME["sidebar_bg"])
        brand_text.pack(side=tk.LEFT)

        tk.Label(brand_text, text="MedCare HMS", font=("Segoe UI", 13, "bold"), fg="white", bg=THEME["sidebar_bg"]).pack(anchor=tk.W)
        tk.Label(brand_text, text="Q02 Performance Pro", font=("Segoe UI", 8), fg="#94A3B8", bg=THEME["sidebar_bg"]).pack(anchor=tk.W)

        # Divider
        tk.Frame(self.sidebar, bg="#1E293B", height=1).pack(fill=tk.X, padx=15, pady=(0, 10))

        # 1a-2. Live Animated Heartbeat ECG Vitals Widget (Reference Image 2)
        ecg_card = tk.Frame(self.sidebar, bg="#0B132B", padx=10, pady=8)
        ecg_card.pack(fill=tk.X, padx=12, pady=(0, 12))

        ecg_top = tk.Frame(ecg_card, bg="#0B132B")
        ecg_top.pack(fill=tk.X)

        tk.Label(ecg_top, text="● LIVE VITALS", font=("Segoe UI", 7, "bold"), fg="#10B981", bg="#0B132B").pack(side=tk.LEFT)
        tk.Label(ecg_top, text="74 BPM", font=("Segoe UI", 7, "bold"), fg="#38BDF8", bg="#0B132B").pack(side=tk.RIGHT)

        self.ecg_wave = ECGAnimationWidget(ecg_card, width=200, height=32, bg_color="#0B132B")
        self.ecg_wave.pack(anchor=tk.CENTER, pady=(4, 0))

        # 1b. Navigation Menu (Role-Based Access Filtering)
        user_role = self.user_data.get("role", "Admin")
        tk.Label(self.sidebar, text=f"MENU • {user_role.upper()}", font=("Segoe UI", 7, "bold"), fg="#64748B", bg=THEME["sidebar_bg"], padx=20).pack(anchor=tk.W, pady=(0, 6))

        role_menus = {
            "Admin": ["Dashboard", "Patients", "Doctors", "Appointments", "Billing", "CSV Import", "Reports", "TQM Audit"],
            "Doctor": ["Dashboard", "Appointments", "Patients", "Doctors", "TQM Audit"],
            "Receptionist": ["Dashboard", "Patients", "Appointments", "Billing", "Doctors"],
            "Billing": ["Dashboard", "Billing", "Patients", "Reports"]
        }
        allowed_tabs = role_menus.get(user_role, role_menus["Admin"])
        all_nav = [
            ("Dashboard", "📊", "Overview Dashboard"),
            ("Patients", "👥", "Patients & Search"),
            ("Doctors", "👨‍⚕️", "Doctor Directory"),
            ("Appointments", "📅", "OPD Queue & Tokens"),
            ("Billing", "💳", "Billing & Invoicing"),
            ("CSV Import", "📥", "Bulk CSV Ingestion"),
            ("Reports", "📈", "Analytics & Reports"),
            ("TQM Audit", "🎯", "TQM Quality Audit"),
        ]
        nav_items = [item for item in all_nav if item[0] in allowed_tabs]

        for tab_id, icon, label in nav_items:
            btn_frame = tk.Frame(self.sidebar, bg=THEME["sidebar_bg"], cursor="hand2")
            btn_frame.pack(fill=tk.X, padx=10, pady=2)

            # Left active accent line (indicator)
            indicator = tk.Frame(btn_frame, bg=THEME["sidebar_bg"], width=4)
            indicator.pack(side=tk.LEFT, fill=tk.Y)

            btn_lbl = tk.Label(
                btn_frame, text=f"  {icon}  {label}", font=("Segoe UI", 9, "bold"),
                fg=THEME["sidebar_text"], bg=THEME["sidebar_bg"], padx=10, pady=8, anchor=tk.W
            )
            btn_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Bind events for hover and click
            btn_frame.bind("<Button-1>", lambda e, tid=tab_id: self._show_view(tid))
            btn_lbl.bind("<Button-1>", lambda e, tid=tab_id: self._show_view(tid))
            btn_frame.bind("<Enter>", lambda e, f=btn_frame, l=btn_lbl, tid=tab_id: self._on_hover(f, l, tid, True))
            btn_frame.bind("<Leave>", lambda e, f=btn_frame, l=btn_lbl, tid=tab_id: self._on_hover(f, l, tid, False))

            self.nav_buttons[tab_id] = {
                "frame": btn_frame,
                "label": btn_lbl,
                "indicator": indicator
            }

        # 1c. Bottom Profile & SLA Widget
        bottom_box = tk.Frame(self.sidebar, bg="#0B132B", padx=15, pady=15)
        bottom_box.pack(side=tk.BOTTOM, fill=tk.X)

        prof_row = tk.Frame(bottom_box, bg="#0B132B")
        prof_row.pack(fill=tk.X)

        # Avatar circle with user initials
        name_parts = self.user_data.get("full_name", "User").split()
        initials = "".join([p[0].upper() for p in name_parts[:2]]) or "BS"
        role_colors = {"Admin": "#2563EB", "Doctor": "#059669", "Receptionist": "#D97706", "Billing": "#7C3AED"}
        avatar_col = role_colors.get(user_role, THEME["primary"])

        avatar = tk.Label(prof_row, text=initials, font=("Segoe UI", 9, "bold"), bg=avatar_col, fg="white", width=3, height=1)
        avatar.pack(side=tk.LEFT, padx=(0, 10))

        prof_info = tk.Frame(prof_row, bg="#0B132B")
        prof_info.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(prof_info, text=self.user_data["full_name"][:14], font=("Segoe UI", 9, "bold"), fg="white", bg="#0B132B").pack(anchor=tk.W)
        role_badge = tk.Label(
            prof_info, text=f"● {self.user_data['role']}", font=("Segoe UI", 7, "bold"),
            fg=avatar_col, bg="#0B132B"
        )
        role_badge.pack(anchor=tk.W)

        # Logout button
        btn_logout = tk.Button(
            bottom_box, text="🚪 Sign Out", font=("Segoe UI", 8, "bold"),
            bg="#1E293B", fg="#EF4444", activebackground="#EF4444", activeforeground="white",
            relief="flat", cursor="hand2", padx=6, pady=3, command=self._logout
        )
        btn_logout.pack(fill=tk.X, pady=(10, 0))

        # 2. Main Right Container
        self.right_container = tk.Frame(self, bg=THEME["background"])
        self.right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 2a. Top Modern Header Bar (Height 65px)
        self.header_bar = tk.Frame(self.right_container, bg="white", height=65, padx=25, pady=12, highlightthickness=1, highlightbackground=THEME["border"])
        self.header_bar.pack(fill=tk.X)

        # Breadcrumbs / Title
        head_left = tk.Frame(self.header_bar, bg="white")
        head_left.pack(side=tk.LEFT)

        self.lbl_head_title = tk.Label(head_left, text="Executive Dashboard", font=("Segoe UI", 14, "bold"), fg=THEME["text"], bg="white")
        self.lbl_head_title.pack(anchor=tk.W)

        self.lbl_head_sub = tk.Label(
            head_left, 
            text=f"Course: {COURSE_CODE} • Student: {STUDENT_NAME} ({STUDENT_ROLL})", 
            font=("Segoe UI", 8), fg=THEME["text_muted"], bg="white"
        )
        self.lbl_head_sub.pack(anchor=tk.W)

        # Right Telemetry, Global Search & Profile Badges
        head_right = tk.Frame(self.header_bar, bg="white")
        head_right.pack(side=tk.RIGHT)

        # Global Pill Search Box (KRL Health Care Reference Image)
        self.header_search = ModernSearchBox(
            head_right, 
            placeholder="🔍 Search a Doctor or Patient...",
            on_search_callback=self._on_global_search,
            width=24
        )
        self.header_search.pack(side=tk.LEFT, padx=(0, 10))

        # Real-time SLA Pill
        self.sla_pill = tk.Label(
            head_right, 
            text=" ● 0.7ms Latency | SLA Compliant ", 
            font=("Segoe UI", 8, "bold"),
            bg=THEME["success_light"], fg="#047857",
            padx=10, pady=4, relief="flat", bd=0
        )
        self.sla_pill.pack(side=tk.LEFT, padx=(0, 8))

        # Live Digital Ticking Clock
        self.lbl_clock = tk.Label(
            head_right, text="", font=("Segoe UI", 8, "bold"),
            bg="#EFF6FF", fg=THEME["primary"], padx=8, pady=4
        )
        self.lbl_clock.pack(side=tk.LEFT, padx=(0, 10))

        # Modern User Profile Chip (Reference Image top-right)
        user_chip = tk.Frame(head_right, bg="#F0F4FA", padx=8, pady=4, highlightthickness=1, highlightbackground="#D2E4F9")
        user_chip.pack(side=tk.LEFT)

        name_parts = self.user_data.get("full_name", "User").split()
        initials = "".join([p[0].upper() for p in name_parts[:2]]) or "BS"
        role_col = {"Admin": "#1E5DB4", "Doctor": "#059669", "Receptionist": "#D97706", "Billing": "#7C3AED"}.get(self.user_data.get("role", "Admin"), "#1E5DB4")

        av_circle = tk.Label(
            user_chip, text=initials, font=("Segoe UI", 8, "bold"),
            bg=role_col, fg="white", width=3, height=1
        )
        av_circle.pack(side=tk.LEFT, padx=(0, 6))

        u_info = tk.Frame(user_chip, bg="#F0F4FA")
        u_info.pack(side=tk.LEFT)

        tk.Label(u_info, text=self.user_data.get("full_name", "Dr. Alex")[:14], font=("Segoe UI", 8, "bold"), fg="#0C2340", bg="#F0F4FA").pack(anchor=tk.W)
        tk.Label(u_info, text=self.user_data.get("role", "Admin"), font=("Segoe UI", 7), fg="#64748B", bg="#F0F4FA").pack(anchor=tk.W)

        # 2b. Content Views Container
        self.content_container = tk.Frame(self.right_container, bg=THEME["background"], padx=15, pady=10)
        self.content_container.pack(fill=tk.BOTH, expand=True)

        # Initialize View Modules
        self.views["Dashboard"] = DashboardView(self.content_container, on_navigate=self._show_view)
        self.views["Patients"] = PatientView(self.content_container, on_schedule_appointment=self._on_schedule_from_patient)
        self.views["Doctors"] = DoctorView(self.content_container)
        self.views["Appointments"] = AppointmentView(self.content_container, on_open_billing=self._on_open_billing_from_appt)
        self.views["Billing"] = BillingView(self.content_container)
        self.views["CSV Import"] = CSVImportView(self.content_container, on_import_success=self._on_bulk_import_success)
        self.views["Reports"] = ReportsView(self.content_container)
        self.views["TQM Audit"] = TQMAuditView(self.content_container)

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

        # Update Header Title
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

        # Update Nav Sidebar Active States
        for tid, widgets in self.nav_buttons.items():
            if tid == tab_id:
                widgets["frame"].config(bg=THEME["sidebar_active"])
                widgets["label"].config(bg=THEME["sidebar_active"], fg="white")
                widgets["indicator"].config(bg="white")
            else:
                widgets["frame"].config(bg=THEME["sidebar_bg"])
                widgets["label"].config(bg=THEME["sidebar_bg"], fg=THEME["sidebar_text"])
                widgets["indicator"].config(bg=THEME["sidebar_bg"])

        # Hide all views and display target
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
        now = datetime.now()
        self.lbl_clock.config(text=f"🕒 {now.strftime('%I:%M:%S %p')}")

        # Subtle pulsing animation on SLA pill
        if now.second % 2 == 0:
            self.sla_pill.config(bg=THEME["success_light"], fg="#047857")
        else:
            self.sla_pill.config(bg="#E0F2FE", fg="#0369A1")

        self.after(1000, self._tick_clock)

    def _logout(self):
        if hasattr(self, "ecg_wave"):
            self.ecg_wave.stop()
        SessionManager.clear()
        self.destroy()
        start_app()

    def _on_close(self):
        if hasattr(self, "ecg_wave"):
            self.ecg_wave.stop()
        self.destroy()


def start_app():
    """Application launcher."""
    init_db()

    def on_login(user_data):
        main_win = MainWindow(user_data)
        main_win.mainloop()

    login = LoginWindow(on_login)
    login.mainloop()


if __name__ == "__main__":
    start_app()
