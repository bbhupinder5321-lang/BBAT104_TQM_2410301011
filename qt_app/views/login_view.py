"""
Modern Role-Based Authentication & Login View for PySide6.
Matches the Drittech Queue / City Care Hospital SaaS aesthetic.

BBAT104: Fundamentals of Total Quality Management
Academic Session: 2026–27 | Max Assessment: 70 Raw Marks (CO1, CO2, CO3)
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Assigned Quality Goal: Q02 - Improve Performance
"""

from typing import Optional, Callable, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor, QColor

from src.auth import authenticate, SessionManager
from src.config import STUDENT_NAME, STUDENT_ROLL, COURSE_CODE, QUALITY_GOAL


class LoginView(QWidget):
    """
    Modern Clinical SaaS Login Screen with 1-Click Role Autofill Chips,
    Student Accreditation Banner, and Secure SHA-256 Authentication.
    """
    login_successful = Signal(dict)  # Emitted with user_data dict on successful login

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        # Full-window outer container
        outer_layout = QHBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # -------------------------------------------------------------
        # LEFT SIDE: Deep Navy Branding & Hospital Telemetry Hero (#0A1128)
        # -------------------------------------------------------------
        left_panel = QFrame()
        left_panel.setFixedWidth(520)
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #0A1128;
                border-right: 1px solid #1E293B;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(44, 48, 44, 40)
        left_layout.setSpacing(18)

        # Hospital Logo & Brand Title
        brand_row = QHBoxLayout()
        brand_row.setSpacing(14)

        logo_badge = QLabel("🏥")
        logo_badge.setFixedSize(56, 56)
        logo_badge.setAlignment(Qt.AlignCenter)
        logo_badge.setStyleSheet("""
            background-color: #00E5FF22;
            color: #00E5FF;
            font-size: 28px;
            border-radius: 12px;
            border: 1px solid #00E5FF55;
        """)
        brand_row.addWidget(logo_badge)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        lbl_h_name = QLabel("City Care Hospital")
        lbl_h_name.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: 800; letter-spacing: 0.5px;")
        lbl_sub = QLabel("Drittech Clinical Queue & HMS OS")
        lbl_sub.setStyleSheet("color: #00E5FF; font-size: 13px; font-weight: 600;")
        title_box.addWidget(lbl_h_name)
        title_box.addWidget(lbl_sub)
        brand_row.addLayout(title_box)
        left_layout.addLayout(brand_row)

        left_layout.addSpacing(16)

        # Hero Tagline
        lbl_tagline = QLabel("Advanced Hospital Queue Sequencing,\nSub-1ms Triage & TQM Statistical Audit")
        lbl_tagline.setStyleSheet("color: #F8FAFC; font-size: 16px; font-weight: 700; line-height: 1.4;")
        left_layout.addWidget(lbl_tagline)

        # Feature Highlights Cards
        features = [
            ("⚡ Sub-1ms Query Engine", "SQLite WAL Mode with 10 Composite B-Tree Indexes for zero lag."),
            ("🛡️ Poka-Yoke Safeguards", "Instant duplicate phone & UHID detection prevents triage errors."),
            ("📊 TQM Quality Accreditation", "Integrated Deming PDCA, Pareto 80/20, Ishikawa & FMEA matrix."),
            ("🔐 Role-Based Access Control", "Granular permissions for Admins, Physicians, Triage & Cashiers.")
        ]

        for title, desc in features:
            f_box = QFrame()
            f_box.setStyleSheet("""
                QFrame {
                    background-color: #0F172A;
                    border: 1px solid #1E293B;
                    border-left: 3px solid #00E5FF;
                    border-radius: 8px;
                    padding: 10px 14px;
                }
            """)
            f_lay = QVBoxLayout(f_box)
            f_lay.setContentsMargins(12, 8, 12, 8)
            f_lay.setSpacing(2)

            f_t = QLabel(title)
            f_t.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: 700;")
            f_d = QLabel(desc)
            f_d.setStyleSheet("color: #94A3B8; font-size: 11px;")
            f_d.setWordWrap(True)
            f_lay.addWidget(f_t)
            f_lay.addWidget(f_d)
            left_layout.addWidget(f_box)

        left_layout.addStretch()

        # Student Accreditation Badge in Left Footer
        student_badge = QFrame()
        student_badge.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 8px 12px;
            }
        """)
        sb_lay = QVBoxLayout(student_badge)
        sb_lay.setContentsMargins(12, 10, 12, 10)
        sb_lay.setSpacing(4)

        sb_head = QLabel("ACADEMIC EVALUATION ACCREDITATION")
        sb_head.setStyleSheet("color: #00E5FF; font-size: 10px; font-weight: 800; letter-spacing: 0.5px;")
        sb_info = QLabel(f"Student: {STUDENT_NAME} | Roll: {STUDENT_ROLL}\nClass: CSE - A | Course: {COURSE_CODE}\nAssigned TQM Goal: {QUALITY_GOAL}")
        sb_info.setStyleSheet("color: #E2E8F0; font-size: 11px; line-height: 1.3;")
        sb_lay.addWidget(sb_head)
        sb_lay.addWidget(sb_info)
        left_layout.addWidget(student_badge)

        outer_layout.addWidget(left_panel)

        # -------------------------------------------------------------
        # RIGHT SIDE: Modern Clean Authentication Card (#F4F7FB background)
        # -------------------------------------------------------------
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #F4F7FB;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(60, 40, 60, 40)
        right_layout.setAlignment(Qt.AlignCenter)

        # Center Card Container
        card = QFrame()
        card.setFixedWidth(460)
        card.setStyleSheet("""
            QFrame#AuthCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
        """)
        card.setObjectName("AuthCard")

        # Soft drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)

        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(36, 36, 36, 36)
        c_layout.setSpacing(14)

        # Form Header
        lbl_welcome = QLabel("Welcome Back")
        lbl_welcome.setStyleSheet("color: #0F172A; font-size: 22px; font-weight: 800;")
        c_layout.addWidget(lbl_welcome)

        lbl_instruct = QLabel("Sign in with your role credentials to access City Care Hospital operations.")
        lbl_instruct.setStyleSheet("color: #64748B; font-size: 12px;")
        lbl_instruct.setWordWrap(True)
        c_layout.addWidget(lbl_instruct)

        c_layout.addSpacing(6)

        # Quick Demo Role Autofill Chips
        lbl_roles = QLabel("⚡ Quick Demo Roles (1-Click Fill):")
        lbl_roles.setStyleSheet("color: #475569; font-size: 11px; font-weight: 700;")
        c_layout.addWidget(lbl_roles)

        chips_row = QHBoxLayout()
        chips_row.setSpacing(6)

        roles_config = [
            ("👑 Admin", "admin", "admin123", "#0284C7", "#E0F2FE"),
            ("📋 Reception", "reception", "rec123", "#16A34A", "#DCFCE7"),
            ("🩺 Doctor", "doctor", "doc123", "#D97706", "#FEF3C7"),
            ("💳 Billing", "billing", "bill123", "#8B5CF6", "#EDE9FE"),
        ]

        for label, u, p, color, bg in roles_config:
            btn_chip = QPushButton(label)
            btn_chip.setCursor(QCursor(Qt.PointingHandCursor))
            btn_chip.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg};
                    color: {color};
                    font-size: 11px;
                    font-weight: 700;
                    padding: 5px 8px;
                    border: 1px solid {color}44;
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    background-color: {color}22;
                }}
            """)
            btn_chip.clicked.connect(lambda checked=False, user=u, pwd=p: self._fill_credentials(user, pwd))
            chips_row.addWidget(btn_chip)

        c_layout.addLayout(chips_row)
        c_layout.addSpacing(6)

        # Input 1: Username
        lbl_u = QLabel("Username / User ID")
        lbl_u.setStyleSheet("color: #334155; font-size: 12px; font-weight: 700;")
        c_layout.addWidget(lbl_u)

        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Enter username (e.g. admin)")
        self.txt_username.setText("admin")  # Default to admin for fast evaluation
        self.txt_username.setStyleSheet("""
            QLineEdit {
                padding: 10px 14px;
                border: 1.5px solid #CBD5E1;
                border-radius: 8px;
                background-color: #F8FAFC;
                font-size: 13px;
                color: #0F172A;
            }
            QLineEdit:focus {
                border-color: #0284C7;
                background-color: #FFFFFF;
            }
        """)
        c_layout.addWidget(self.txt_username)

        # Input 2: Password
        lbl_p = QLabel("Password")
        lbl_p.setStyleSheet("color: #334155; font-size: 12px; font-weight: 700;")
        c_layout.addWidget(lbl_p)

        pwd_row = QHBoxLayout()
        pwd_row.setSpacing(6)

        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setPlaceholderText("Enter your password")
        self.txt_password.setText("admin123")  # Default to admin123
        self.txt_password.setStyleSheet("""
            QLineEdit {
                padding: 10px 14px;
                border: 1.5px solid #CBD5E1;
                border-radius: 8px;
                background-color: #F8FAFC;
                font-size: 13px;
                color: #0F172A;
            }
            QLineEdit:focus {
                border-color: #0284C7;
                background-color: #FFFFFF;
            }
        """)
        self.txt_password.returnPressed.connect(self._do_login)
        pwd_row.addWidget(self.txt_password, stretch=1)

        self.btn_toggle_pwd = QPushButton("👁️")
        self.btn_toggle_pwd.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_toggle_pwd.setFixedSize(38, 38)
        self.btn_toggle_pwd.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9;
                border: 1.5px solid #CBD5E1;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
        """)
        self.btn_toggle_pwd.clicked.connect(self._toggle_password_visibility)
        pwd_row.addWidget(self.btn_toggle_pwd)

        c_layout.addLayout(pwd_row)

        # Error Banner Label (hidden by default)
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet("""
            background-color: #FEE2E2;
            color: #DC2626;
            font-size: 12px;
            font-weight: 600;
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid #FECACA;
        """)
        self.lbl_error.setVisible(False)
        c_layout.addWidget(self.lbl_error)

        c_layout.addSpacing(6)

        # Sign In Button
        self.btn_login = QPushButton("Sign In to Clinical Suite  ➔")
        self.btn_login.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_login.setFixedHeight(44)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #0A1128;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 800;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1E293B;
            }
            QPushButton:pressed {
                background-color: #0284C7;
            }
        """)
        self.btn_login.clicked.connect(self._do_login)
        c_layout.addWidget(self.btn_login)

        # System Status Pill in Card Footer
        lbl_engine_note = QLabel("🟢 SQLite WAL Mode Active • B-Tree Accelerated")
        lbl_engine_note.setStyleSheet("color: #16A34A; font-size: 11px; font-weight: 600; text-align: center;")
        lbl_engine_note.setAlignment(Qt.AlignCenter)
        c_layout.addWidget(lbl_engine_note)

        right_layout.addWidget(card)
        outer_layout.addWidget(right_panel, stretch=1)

    def _fill_credentials(self, u: str, p: str):
        self.txt_username.setText(u)
        self.txt_password.setText(p)
        self.lbl_error.setVisible(False)

    def _toggle_password_visibility(self):
        if self.txt_password.echoMode() == QLineEdit.Password:
            self.txt_password.setEchoMode(QLineEdit.Normal)
            self.btn_toggle_pwd.setText("🔒")
        else:
            self.txt_password.setEchoMode(QLineEdit.Password)
            self.btn_toggle_pwd.setText("👁️")

    def _do_login(self):
        u = self.txt_username.text().strip()
        p = self.txt_password.text().strip()

        if not u or not p:
            self.lbl_error.setText("⚠️ Please enter both username and password.")
            self.lbl_error.setVisible(True)
            return

        user_data = authenticate(u, p)
        if user_data:
            self.lbl_error.setVisible(False)
            self.login_successful.emit(user_data)
        else:
            self.lbl_error.setText("❌ Invalid username or password. Check role chips above.")
            self.lbl_error.setVisible(True)
