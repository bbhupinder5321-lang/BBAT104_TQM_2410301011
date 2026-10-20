"""
OPD Queue Sequencing & Wait-Time Telemetry View for PySide6.
Matching Drittech Queue / City Care Hospital dashboard.

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Quality Goal: Q02 - Improve Performance (Reduce Patient Waiting Time < 15.0m)
"""

from datetime import date, datetime
from typing import Optional, List, Dict, Any, Callable
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDialog, QFormLayout, QMessageBox,
    QFrame, QMenu, QDateEdit, QTextEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QCursor

from src.models.appointment import (
    get_appointments_list, book_appointment, check_in_patient,
    start_consultation, complete_consultation, cancel_appointment,
    get_waiting_time_kpi
)
from src.models.doctor import get_all_doctors
from src.models.patient import fast_search_patients
from qt_app.widgets.stat_cards import KpiMetricCard
from qt_app.widgets.badge import Badge


class CompleteConsultationDialog(QDialog):
    """Modal dialog allowing physician to enter clinical consultation notes."""

    def __init__(self, appointment_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.appointment_data = appointment_data
        tok = appointment_data.get('token_number', 0)
        self.setWindowTitle(f"Finalize Consultation — Token #{tok:03d}")
        self.setFixedWidth(480)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
            QLabel {
                font-weight: 600;
                color: #334155;
                font-size: 12px;
            }
            QTextEdit {
                padding: 8px 10px;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                background-color: #F8FAFC;
                font-size: 12px;
            }
            QTextEdit:focus {
                border-color: #0284C7;
                background-color: #FFFFFF;
            }
            QPushButton#PrimaryBtn {
                background-color: #16A34A;
                color: white;
                font-weight: 700;
                padding: 9px 18px;
                border-radius: 6px;
                border: none;
            }
            QPushButton#PrimaryBtn:hover {
                background-color: #15803D;
            }
            QPushButton#CancelBtn {
                background-color: #F1F5F9;
                color: #475569;
                font-weight: 600;
                padding: 9px 18px;
                border-radius: 6px;
                border: 1px solid #E2E8F0;
            }
        """)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(12)

        lbl_head = QLabel("🩺 Finalize OPD Consultation")
        lbl_head.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        layout.addWidget(lbl_head)

        info_box = QFrame()
        info_box.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px;")
        i_lay = QVBoxLayout(info_box)
        i_lay.setSpacing(4)
        i_lay.addWidget(QLabel(f"Patient: <b>{self.appointment_data.get('patient_name')}</b> ({self.appointment_data.get('uhid')})"))
        i_lay.addWidget(QLabel(f"Doctor: <b>{self.appointment_data.get('doctor_name')}</b> ({self.appointment_data.get('specialization')})"))
        layout.addWidget(info_box)

        lbl_notes = QLabel("Clinical Notes & Prescriptions *:")
        layout.addWidget(lbl_notes)

        self.txt_notes = QTextEdit()
        self.txt_notes.setPlaceholderText("Enter diagnosis, medical observations, prescribed medications, and follow-up advice...")
        self.txt_notes.setFixedHeight(120)
        layout.addWidget(self.txt_notes)

        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("CancelBtn")
        btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Complete & Save Record  ➔")
        btn_save.setObjectName("PrimaryBtn")
        btn_save.setCursor(QCursor(Qt.PointingHandCursor))
        btn_save.clicked.connect(self.accept)

        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def get_notes(self) -> str:
        text = self.txt_notes.toPlainText().strip()
        return text if text else "Consultation completed successfully."


class TokenDetailsDialog(QDialog):
    """Modal View displaying comprehensive token info and wait telemetry."""

    def __init__(self, appointment_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.appointment_data = appointment_data
        tok = appointment_data.get('token_number', 0)
        self.setWindowTitle(f"Token Details: #{tok:03d}")
        self.setFixedWidth(460)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
        """)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 20)
        layout.setSpacing(12)

        top_row = QHBoxLayout()
        tok = self.appointment_data.get('token_number', 0)
        lbl_tok = QLabel(f"TOKEN #{tok:03d}")
        lbl_tok.setStyleSheet("font-size: 18px; font-weight: 800; color: #0284C7;")
        top_row.addWidget(lbl_tok)

        status = self.appointment_data.get("status", "Scheduled")
        badge_type = "green" if status == "In-Consultation" else ("amber" if status == "Waiting" else "cyan")
        badge = Badge(status, badge_type=badge_type)
        top_row.addWidget(badge, alignment=Qt.AlignRight | Qt.AlignVCenter)
        layout.addLayout(top_row)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: #E2E8F0;")
        layout.addWidget(divider)

        info_card = QFrame()
        info_card.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;")
        i_lay = QFormLayout(info_card)
        i_lay.setSpacing(8)

        i_lay.addRow("Appointment Code:", QLabel(str(self.appointment_data.get("appointment_number", "-"))))
        i_lay.addRow("Patient Name:", QLabel(f"{self.appointment_data.get('patient_name')} ({self.appointment_data.get('uhid')})"))
        i_lay.addRow("Attending Doctor:", QLabel(f"{self.appointment_data.get('doctor_name')} ({self.appointment_data.get('specialization')})"))
        i_lay.addRow("OPD Chamber:", QLabel(str(self.appointment_data.get("room_no", "OPD"))))
        i_lay.addRow("Appointment Date:", QLabel(str(self.appointment_data.get("appointment_date", "-"))))
        i_lay.addRow("Scheduled Time:", QLabel(str(self.appointment_data.get("appointment_time", "-"))))
        w = self.appointment_data.get("wait_time_minutes")
        w_str = f"{w:.1f} minutes" if w and w > 0 else "In Progress / Not checked in"
        i_lay.addRow("Recorded Wait Time:", QLabel(w_str))

        layout.addWidget(info_card)

        btn_row = QHBoxLayout()
        btn_close = QPushButton("Close")
        btn_close.setCursor(QCursor(Qt.PointingHandCursor))
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #0A1128;
                color: white;
                font-weight: 700;
                padding: 8px 18px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1E293B;
            }
        """)
        btn_close.clicked.connect(self.accept)
        btn_row.addStretch()
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)


class BookAppointmentDialog(QDialog):
    """Modal dialog for issuing a token / scheduling an outpatient appointment."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Issue OPD Token & Schedule Appointment")
        self.setFixedWidth(480)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
            QLabel {
                font-weight: 600;
                color: #334155;
                font-size: 12px;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 7px 10px;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                background-color: #F8FAFC;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #0284C7;
                background-color: #FFFFFF;
            }
            QPushButton#PrimaryBtn {
                background-color: #0A1128;
                color: white;
                font-weight: 700;
                padding: 9px 18px;
                border-radius: 6px;
            }
            QPushButton#PrimaryBtn:hover {
                background-color: #1E293B;
            }
            QPushButton#CancelBtn {
                background-color: #F1F5F9;
                color: #475569;
                font-weight: 600;
                padding: 9px 18px;
                border-radius: 6px;
                border: 1px solid #E2E8F0;
            }
        """)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        lbl_head = QLabel("🎫 Issue OPD Queue Token")
        lbl_head.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        layout.addWidget(lbl_head)

        form = QFormLayout()
        form.setSpacing(10)

        # Patient search / picker
        self.txt_patient_search = QLineEdit()
        self.txt_patient_search.setPlaceholderText("Search patient by UHID, Name, or Phone...")
        self.txt_patient_search.textChanged.connect(self._search_patients)

        self.cmb_patient = QComboBox()
        self.cmb_patient.setPlaceholderText("Select Patient...")

        self.cmb_doctor = QComboBox()
        doctors = get_all_doctors()
        for doc in doctors:
            self.cmb_doctor.addItem(
                f"{doc['full_name']} ({doc['specialization']}) - Room {doc['room_no']}",
                userData=doc["id"]
            )

        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setDisplayFormat("yyyy-MM-dd")

        self.txt_time = QLineEdit(datetime.now().strftime("%I:%M %p"))

        self.txt_notes = QLineEdit()
        self.txt_notes.setPlaceholderText("e.g. Follow-up consultation / Routine checkup")

        form.addRow("Search Patient:", self.txt_patient_search)
        form.addRow("Select Patient *:", self.cmb_patient)
        form.addRow("Attending Doctor *:", self.cmb_doctor)
        form.addRow("Appointment Date *:", self.date_picker)
        form.addRow("Scheduled Time:", self.txt_time)
        form.addRow("Clinical Notes:", self.txt_notes)

        layout.addLayout(form)

        # Buttons
        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("CancelBtn")
        btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Generate Token")
        btn_save.setObjectName("PrimaryBtn")
        btn_save.setCursor(QCursor(Qt.PointingHandCursor))
        btn_save.clicked.connect(self._validate_and_accept)

        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

        # Initial patient population
        self._search_patients()

    def _search_patients(self):
        query = self.txt_patient_search.text().strip()
        patients, _ = fast_search_patients(query, limit=20)
        self.cmb_patient.clear()
        for p in patients:
            self.cmb_patient.addItem(
                f"{p['full_name']} | UHID: {p['uhid']} | 📞 {p['phone']}",
                userData=p["id"]
            )

    def _validate_and_accept(self):
        if self.cmb_patient.currentIndex() < 0 or not self.cmb_patient.currentData():
            QMessageBox.warning(self, "Validation Error", "Please select a valid registered patient.")
            return
        if self.cmb_doctor.currentIndex() < 0 or not self.cmb_doctor.currentData():
            QMessageBox.warning(self, "Validation Error", "Please select an attending doctor.")
            return
        self.accept()

    def get_data(self) -> Dict[str, Any]:
        return {
            "patient_id": self.cmb_patient.currentData(),
            "doctor_id": self.cmb_doctor.currentData(),
            "appointment_date": self.date_picker.date().toString("yyyy-MM-dd"),
            "appointment_time": self.txt_time.text().strip(),
            "notes": self.txt_notes.text().strip()
        }


class AppointmentsView(QWidget):
    """
    OPD Queue Sequencing & Wait-Time Telemetry Interface.
    Directly addresses Core TQM Goal: Reduce Patient Waiting Time.
    """

    def __init__(self, on_open_billing: Optional[Callable] = None, parent=None):
        super().__init__(parent)
        self.on_open_billing = on_open_billing
        self.appointments_data: List[Dict[str, Any]] = []
        self._build_ui()
        self.load_appointments()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # 0. KPI Metrics Strip
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(14)

        self.kpi_total = KpiMetricCard("Today's Bookings", "0 Tokens", "Active Clinical Queue", "📅", "#0EA5E9")
        self.kpi_waiting = KpiMetricCard("Waiting Lounge", "0 Patients", "In Queue Awaiting Doctor", "⏳", "#F97316")
        self.kpi_consult = KpiMetricCard("In-Consultation", "0 Active", "In Doctor Chamber", "🩺", "#84CC16")
        self.kpi_wait_avg = KpiMetricCard("Avg OPD Wait", "0.0 min", "TQM Target < 15.0m (Q02)", "⏱️", "#EF4444")

        kpi_row.addWidget(self.kpi_total)
        kpi_row.addWidget(self.kpi_waiting)
        kpi_row.addWidget(self.kpi_consult)
        kpi_row.addWidget(self.kpi_wait_avg)
        main_layout.addLayout(kpi_row)

        # 1. Main Table Card Container
        card = QFrame()
        card.setObjectName("TableCard")
        card.setStyleSheet("""
            QFrame#TableCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 18)
        card_layout.setSpacing(14)

        # 1a. Toolbar: Filters & Actions
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        lbl_date = QLabel("Date:")
        lbl_date.setStyleSheet("font-size: 12px; font-weight: 700; color: #475569;")
        toolbar.addWidget(lbl_date)

        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setDisplayFormat("yyyy-MM-dd")
        self.date_filter.setFixedWidth(120)
        self.date_filter.setStyleSheet("""
            QDateEdit {
                padding: 6px 8px;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                background-color: #F8FAFC;
                font-size: 12px;
            }
        """)
        self.date_filter.dateChanged.connect(lambda: self.load_appointments())
        toolbar.addWidget(self.date_filter)

        btn_today = QPushButton("Today")
        btn_today.setCursor(QCursor(Qt.PointingHandCursor))
        btn_today.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9;
                color: #334155;
                font-weight: 600;
                font-size: 11px;
                padding: 6px 12px;
                border-radius: 6px;
                border: 1px solid #E2E8F0;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
        """)
        btn_today.clicked.connect(self._set_today)
        toolbar.addWidget(btn_today)

        lbl_status = QLabel("Status:")
        lbl_status.setStyleSheet("font-size: 12px; font-weight: 700; color: #475569;")
        toolbar.addWidget(lbl_status)

        self.cmb_status_filter = QComboBox()
        self.cmb_status_filter.addItems(["All", "Scheduled", "Waiting", "In-Consultation", "Completed", "Cancelled"])
        self.cmb_status_filter.setFixedWidth(130)
        self.cmb_status_filter.setStyleSheet("""
            QComboBox {
                padding: 6px 10px;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                background-color: #F8FAFC;
                font-size: 12px;
                font-weight: 600;
            }
        """)
        self.cmb_status_filter.currentTextChanged.connect(self._apply_filters)
        toolbar.addWidget(self.cmb_status_filter)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Filter patient name, doctor, or token...")
        self.txt_search.setFixedWidth(240)
        self.txt_search.setStyleSheet("""
            QLineEdit {
                padding: 6px 12px;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                background-color: #F8FAFC;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #0284C7;
                background-color: #FFFFFF;
            }
        """)
        self.txt_search.textChanged.connect(self._apply_filters)
        toolbar.addWidget(self.txt_search)

        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.setCursor(QCursor(Qt.PointingHandCursor))
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9;
                color: #334155;
                font-weight: 600;
                font-size: 12px;
                padding: 6px 14px;
                border-radius: 6px;
                border: 1px solid #E2E8F0;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
        """)
        btn_refresh.clicked.connect(self.load_appointments)
        toolbar.addWidget(btn_refresh)

        toolbar.addStretch()

        btn_book = QPushButton("➕ Book Appointment / Token")
        btn_book.setCursor(QCursor(Qt.PointingHandCursor))
        btn_book.setStyleSheet("""
            QPushButton {
                background-color: #0A1128;
                color: white;
                font-weight: 700;
                font-size: 12px;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1E293B;
            }
        """)
        btn_book.clicked.connect(self._on_book_appointment)
        toolbar.addWidget(btn_book)

        card_layout.addLayout(toolbar)

        # 1b. Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Token No", "Appt Code", "Patient Name (UHID)", "Doctor (Specialization)", "Room", "Status", "Wait (min)", "Time"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #F1F5F9;
                border-radius: 8px;
                background-color: #FFFFFF;
                gridline-color: #F8FAFC;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F1F5F9;
            }
            QTableWidget::item:selected {
                background-color: #F0F9FF;
                color: #0369A1;
            }
            QHeaderView::section {
                background-color: #F8FAFC;
                color: #475569;
                font-weight: 700;
                font-size: 11px;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #E2E8F0;
            }
        """)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.itemDoubleClicked.connect(self._on_table_double_clicked)
        card_layout.addWidget(self.table)

        # 1c. Queue Lifecycle Action Bar
        action_bar = QHBoxLayout()
        action_bar.setSpacing(10)

        lbl_step = QLabel("⚡ Queue Action:")
        lbl_step.setStyleSheet("font-weight: 700; font-size: 12px; color: #475569;")
        action_bar.addWidget(lbl_step)

        btn_view_details = QPushButton("📋 View Details")
        btn_view_details.setCursor(QCursor(Qt.PointingHandCursor))
        btn_view_details.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9;
                color: #334155;
                border: 1px solid #CBD5E1;
                font-weight: 700;
                font-size: 11px;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
        """)
        btn_view_details.clicked.connect(self._on_view_details)
        action_bar.addWidget(btn_view_details)

        btn_checkin = QPushButton("⏳ Check-In Patient")
        btn_checkin.setCursor(QCursor(Qt.PointingHandCursor))
        btn_checkin.setStyleSheet("""
            QPushButton {
                background-color: #FEF3C7;
                color: #D97706;
                border: 1px solid #FDE68A;
                font-weight: 700;
                font-size: 11px;
                padding: 6px 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #FDE68A;
            }
        """)
        btn_checkin.clicked.connect(self._on_check_in)
        action_bar.addWidget(btn_checkin)

        btn_start = QPushButton("🩺 Call Patient / Start")
        btn_start.setCursor(QCursor(Qt.PointingHandCursor))
        btn_start.setStyleSheet("""
            QPushButton {
                background-color: #E0F2FE;
                color: #0284C7;
                border: 1px solid #BAE6FD;
                font-weight: 700;
                font-size: 11px;
                padding: 6px 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #BAE6FD;
            }
        """)
        btn_start.clicked.connect(self._on_start_consultation)
        action_bar.addWidget(btn_start)

        btn_complete = QPushButton("✅ Complete Consultation")
        btn_complete.setCursor(QCursor(Qt.PointingHandCursor))
        btn_complete.setStyleSheet("""
            QPushButton {
                background-color: #DCFCE7;
                color: #16A34A;
                border: 1px solid #BBF7D0;
                font-weight: 700;
                font-size: 11px;
                padding: 6px 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #BBF7D0;
            }
        """)
        btn_complete.clicked.connect(self._on_complete_consultation)
        action_bar.addWidget(btn_complete)

        btn_cancel = QPushButton("❌ Cancel Token")
        btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #FEE2E2;
                color: #DC2626;
                border: 1px solid #FECACA;
                font-weight: 600;
                font-size: 11px;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #FECACA;
            }
        """)
        btn_cancel.clicked.connect(self._on_cancel_appointment)
        action_bar.addWidget(btn_cancel)

        action_bar.addStretch()
        card_layout.addLayout(action_bar)

        main_layout.addWidget(card)

    def _set_today(self):
        self.date_filter.setDate(QDate.currentDate())

    def load_appointments(self):
        """Fetch appointments from SQLite matching selected date."""
        target_date = self.date_filter.date().toString("yyyy-MM-dd")
        try:
            self.appointments_data = get_appointments_list(target_date=target_date)
            self._apply_filters()
            self._update_kpi_cards(target_date)
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load queue appointments: {e}")

    def _update_kpi_cards(self, target_date: str):
        total = len(self.appointments_data)
        waiting = sum(1 for a in self.appointments_data if a.get("status") == "Waiting")
        consult = sum(1 for a in self.appointments_data if a.get("status") == "In-Consultation")

        kpi_stats = get_waiting_time_kpi(target_date)
        avg_wait = kpi_stats.get("avg_wait_min", 0.0)

        self.kpi_total.update_value(f"{total} Tokens", "Total Scheduled Today")
        self.kpi_waiting.update_value(f"{waiting} Waiting", "Awaiting Consultation")
        self.kpi_consult.update_value(f"{consult} Active", "In Doctor Chamber")
        self.kpi_wait_avg.update_value(f"{avg_wait} min", "TQM Target < 15.0m")

    def _apply_filters(self):
        status_filter = self.cmb_status_filter.currentText()
        search_query = self.txt_search.text().strip().lower()

        filtered = []
        for a in self.appointments_data:
            if status_filter != "All" and a.get("status") != status_filter:
                continue
            if search_query:
                p_match = search_query in str(a.get("patient_name", "")).lower()
                uhid_match = search_query in str(a.get("uhid", "")).lower()
                d_match = search_query in str(a.get("doctor_name", "")).lower()
                tok_match = search_query in str(a.get("token_number", "")).lower()
                if not (p_match or uhid_match or d_match or tok_match):
                    continue
            filtered.append(a)

        self.table.setRowCount(len(filtered))
        for row_idx, appt in enumerate(filtered):
            # Token No (styled prominently)
            tok_num = appt.get("token_number", 0)
            item_token = QTableWidgetItem(f"#{tok_num:03d}")
            item_token.setFont(QFont("Segoe UI", 10, QFont.Bold))
            item_token.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 0, item_token)

            # Appointment Number
            item_num = QTableWidgetItem(str(appt.get("appointment_number", "")))
            item_num.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 1, item_num)

            # Patient Name + UHID
            p_text = f"{appt.get('patient_name', '')} ({appt.get('uhid', '')})"
            item_p = QTableWidgetItem(p_text)
            item_p.setFont(QFont("Segoe UI", 9, QFont.Bold))
            self.table.setItem(row_idx, 2, item_p)

            # Doctor
            d_text = f"{appt.get('doctor_name', '')} • {appt.get('specialization', '')}"
            item_d = QTableWidgetItem(d_text)
            self.table.setItem(row_idx, 3, item_d)

            # Room
            item_room = QTableWidgetItem(str(appt.get("room_no", "OPD")))
            item_room.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 4, item_room)

            # Status Pill Badge
            status = str(appt.get("status", "Scheduled"))
            if status == "Waiting":
                badge_type = "amber"
            elif status == "In-Consultation":
                badge_type = "green"
            elif status == "Completed":
                badge_type = "cyan"
            else:
                badge_type = "gray"

            badge = Badge(status, badge_type=badge_type)
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(4, 2, 4, 2)
            cell_layout.setAlignment(Qt.AlignCenter)
            cell_layout.addWidget(badge)
            self.table.setCellWidget(row_idx, 5, cell_widget)

            # Wait Time
            w_min = appt.get("wait_time_minutes")
            w_str = f"{w_min:.1f} m" if w_min is not None and w_min > 0 else "-"
            item_w = QTableWidgetItem(w_str)
            item_w.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 6, item_w)

            # Time
            item_time = QTableWidgetItem(str(appt.get("appointment_time", "")))
            item_time.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 7, item_time)

    def _get_selected_appointment(self) -> Optional[Dict[str, Any]]:
        row = self.table.currentRow()
        if row < 0:
            return None
        # Map row to filtered item
        tok_item = self.table.item(row, 1)  # appt code
        if not tok_item:
            return None
        appt_code = tok_item.text()
        for a in self.appointments_data:
            if a.get("appointment_number") == appt_code:
                return a
        return None

    def _on_book_appointment(self):
        dlg = BookAppointmentDialog(parent=self)
        if dlg.exec():
            data = dlg.get_data()
            try:
                appt_id, appt_num, token_num = book_appointment(
                    patient_id=data["patient_id"],
                    doctor_id=data["doctor_id"],
                    appointment_date=data["appointment_date"],
                    appointment_time=data["appointment_time"],
                    notes=data["notes"]
                )
                self.load_appointments()
                QMessageBox.information(
                    self, "Token Issued",
                    f"Token #{token_num:03d} issued successfully!\nAppointment ID: {appt_num}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to issue token: {e}")

    def _on_check_in(self):
        appt = self._get_selected_appointment()
        if not appt:
            QMessageBox.information(self, "Select Row", "Please select an appointment to check in.")
            return
        try:
            check_in_patient(appt["id"])
            self.load_appointments()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to check in patient: {e}")

    def _on_start_consultation(self):
        appt = self._get_selected_appointment()
        if not appt:
            QMessageBox.information(self, "Select Row", "Please select an appointment to start consultation.")
            return
        try:
            start_consultation(appt["id"])
            self.load_appointments()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start consultation: {e}")

    def _on_view_details(self):
        appt = self._get_selected_appointment()
        if not appt:
            QMessageBox.information(self, "Select Row", "Please select an appointment from the queue to view details.")
            return
        dlg = TokenDetailsDialog(appt, parent=self)
        dlg.exec()

    def _on_table_double_clicked(self, item):
        self._on_view_details()

    def _on_complete_consultation(self):
        appt = self._get_selected_appointment()
        if not appt:
            QMessageBox.information(self, "Select Row", "Please select an appointment to complete.")
            return

        dlg = CompleteConsultationDialog(appt, parent=self)
        if dlg.exec():
            notes = dlg.get_notes()
            try:
                wait_m = complete_consultation(appt["id"], notes)
                self.load_appointments()
                QMessageBox.information(
                    self, "Consultation Completed",
                    f"Consultation finalized and clinical notes logged!\n"
                    f"Recorded Patient Wait Time: {wait_m:.1f} minutes.\n"
                    f"TQM OPD cycle telemetry successfully recorded."
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to complete consultation: {e}")

    def _on_cancel_appointment(self):
        appt = self._get_selected_appointment()
        if not appt:
            QMessageBox.information(self, "Select Row", "Please select an appointment to cancel.")
            return
        confirm = QMessageBox.question(
            self, "Cancel Token",
            f"Are you sure you want to cancel appointment {appt['appointment_number']}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                cancel_appointment(appt["id"])
                self.load_appointments()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to cancel token: {e}")

    def _show_context_menu(self, pos):
        appt = self._get_selected_appointment()
        if not appt:
            return

        menu = QMenu(self)
        act_view = menu.addAction("📋 View Token & Clinical Details")
        act_in = menu.addAction("⏳ Check-In Patient")
        act_start = menu.addAction("🩺 Start Consultation")
        act_comp = menu.addAction("✅ Complete Consultation")
        menu.addSeparator()
        act_bill = menu.addAction("🧾 Settle Bill / Invoice")
        act_cancel = menu.addAction("❌ Cancel Token")

        chosen = menu.exec(self.table.viewport().mapToGlobal(pos))
        if chosen == act_view:
            self._on_view_details()
        elif chosen == act_in:
            self._on_check_in()
        elif chosen == act_start:
            self._on_start_consultation()
        elif chosen == act_comp:
            self._on_complete_consultation()
        elif chosen == act_bill and self.on_open_billing:
            self.on_open_billing()
        elif chosen == act_cancel:
            self._on_cancel_appointment()
