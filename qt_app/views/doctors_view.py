"""
Doctor Management & Clinical Roster View for PySide6.
Matching Drittech Queue / City Care Hospital dashboard.

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from typing import Optional, List, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDialog, QFormLayout, QDoubleSpinBox, QMessageBox,
    QFrame, QMenu
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QCursor

from src.models.doctor import (
    get_all_doctors, create_doctor, update_doctor,
    toggle_doctor_status, delete_doctor, get_doctor_by_id
)
from qt_app.widgets.stat_cards import KpiMetricCard
from qt_app.widgets.badge import Badge


class DoctorProfileDialog(QDialog):
    """Modal dialog displaying comprehensive Doctor profile and clinical status."""

    def __init__(self, doctor_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.doctor_data = doctor_data
        self.setWindowTitle(f"Physician File: {doctor_data.get('full_name')}")
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
        layout.setSpacing(14)

        top_row = QHBoxLayout()
        name_col = QVBoxLayout()
        name_col.setSpacing(2)

        lbl_name = QLabel(self.doctor_data.get("full_name", ""))
        lbl_name.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
        lbl_code = QLabel(f"Code: {self.doctor_data.get('doctor_code', '')} • {self.doctor_data.get('specialization', '')}")
        lbl_code.setStyleSheet("font-size: 12px; font-weight: 700; color: #0284C7;")
        name_col.addWidget(lbl_name)
        name_col.addWidget(lbl_code)
        top_row.addLayout(name_col)

        status = self.doctor_data.get("status", "Available")
        b_type = "green" if status == "Available" else ("amber" if status in ["On Leave", "In Surgery"] else "gray")
        badge = Badge(status, badge_type=b_type)
        top_row.addWidget(badge, alignment=Qt.AlignRight | Qt.AlignVCenter)
        layout.addLayout(top_row)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: #E2E8F0;")
        layout.addWidget(divider)

        # Info Box
        info_card = QFrame()
        info_card.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;")
        i_lay = QFormLayout(info_card)
        i_lay.setSpacing(10)

        i_lay.addRow("Specialization:", QLabel(str(self.doctor_data.get("specialization", "-"))))
        i_lay.addRow("OPD Room:", QLabel(str(self.doctor_data.get("room_no", "-"))))
        fee = float(self.doctor_data.get("consultation_fee", 0.0))
        i_lay.addRow("Consultation Fee:", QLabel(f"₹ {fee:.2f}"))
        i_lay.addRow("Phone Number:", QLabel(str(self.doctor_data.get("phone", "-"))))
        i_lay.addRow("Email Address:", QLabel(str(self.doctor_data.get("email") or "Not registered")))

        layout.addWidget(info_card)

        # Quick Status Change Buttons
        lbl_st = QLabel("⚡ Quick Duty Status Update:")
        lbl_st.setStyleSheet("font-size: 11px; font-weight: 700; color: #475569;")
        layout.addWidget(lbl_st)

        st_row = QHBoxLayout()
        st_row.setSpacing(6)

        for s_text, col in [("Available", "#16A34A"), ("In Surgery", "#EA580C"), ("On Leave", "#D97706"), ("Inactive", "#64748B")]:
            btn_s = QPushButton(s_text)
            btn_s.setCursor(QCursor(Qt.PointingHandCursor))
            btn_s.setStyleSheet(f"""
                QPushButton {{
                    background-color: #F8FAFC;
                    color: {col};
                    border: 1px solid #CBD5E1;
                    font-size: 11px;
                    font-weight: 700;
                    padding: 5px 8px;
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    background-color: {col}15;
                    border-color: {col};
                }}
            """)
            btn_s.clicked.connect(lambda checked=False, st=s_text: self._set_status(st))
            st_row.addWidget(btn_s)

        layout.addLayout(st_row)

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

    def _set_status(self, new_status: str):
        toggle_doctor_status(self.doctor_data["id"], new_status)
        self.doctor_data["status"] = new_status
        self.accept()


class DoctorFormDialog(QDialog):
    """Modal dialog for onboarding or updating a physician."""

    def __init__(self, doctor_data: Optional[Dict[str, Any]] = None, parent=None):
        super().__init__(parent)
        self.doctor_data = doctor_data
        self.setWindowTitle("Onboard New Doctor" if not doctor_data else f"Edit Doctor: {doctor_data.get('full_name')}")
        self.setFixedWidth(460)
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
            QLineEdit, QComboBox, QDoubleSpinBox {
                padding: 7px 10px;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                background-color: #F8FAFC;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
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

        # Dialog Title
        lbl_head = QLabel(self.windowTitle())
        lbl_head.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        layout.addWidget(lbl_head)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignLeft)

        self.txt_code = QLineEdit()
        self.txt_code.setPlaceholderText("e.g. DOC-011")

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Dr. Full Name")

        self.cmb_spec = QComboBox()
        self.cmb_spec.addItems([
            "Cardiology", "Neurology", "Pediatrics", "Orthopedics",
            "Dermatology", "General Medicine", "Oncology", "ENT"
        ])
        self.cmb_spec.setEditable(True)

        self.txt_phone = QLineEdit()
        self.txt_phone.setPlaceholderText("10-digit mobile number")

        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("doctor@citycare.org")

        self.txt_room = QLineEdit()
        self.txt_room.setPlaceholderText("e.g. Room 104 / OPD 3")

        self.spn_fee = QDoubleSpinBox()
        self.spn_fee.setRange(0, 50000)
        self.spn_fee.setValue(800.0)
        self.spn_fee.setPrefix("₹ ")

        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["Available", "In Surgery", "On Leave", "Inactive"])

        # Populate if editing
        if self.doctor_data:
            self.txt_code.setText(self.doctor_data.get("doctor_code", ""))
            self.txt_code.setEnabled(False)  # Read-only code on edit
            self.txt_name.setText(self.doctor_data.get("full_name", ""))
            self.cmb_spec.setCurrentText(self.doctor_data.get("specialization", "General Medicine"))
            self.txt_phone.setText(self.doctor_data.get("phone", ""))
            self.txt_email.setText(self.doctor_data.get("email", ""))
            self.txt_room.setText(self.doctor_data.get("room_no", ""))
            self.spn_fee.setValue(float(self.doctor_data.get("consultation_fee", 800.0)))
            self.cmb_status.setCurrentText(self.doctor_data.get("status", "Available"))

        form.addRow("Doctor Code *", self.txt_code)
        form.addRow("Full Name *", self.txt_name)
        form.addRow("Specialization *", self.cmb_spec)
        form.addRow("Contact Phone *", self.txt_phone)
        form.addRow("Email Address", self.txt_email)
        form.addRow("Assigned OPD Room", self.txt_room)
        form.addRow("Consultation Fee (₹)", self.spn_fee)
        form.addRow("Current Status", self.cmb_status)

        layout.addLayout(form)

        # Buttons
        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("CancelBtn")
        btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Save Doctor Record")
        btn_save.setObjectName("PrimaryBtn")
        btn_save.setCursor(QCursor(Qt.PointingHandCursor))
        btn_save.clicked.connect(self._validate_and_accept)

        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _validate_and_accept(self):
        code = self.txt_code.text().strip()
        name = self.txt_name.text().strip()
        if not code or not name:
            QMessageBox.warning(self, "Validation Error", "Doctor Code and Full Name are mandatory.")
            return
        self.accept()

    def get_data(self) -> Dict[str, Any]:
        return {
            "doctor_code": self.txt_code.text().strip(),
            "full_name": self.txt_name.text().strip(),
            "specialization": self.cmb_spec.currentText().strip(),
            "phone": self.txt_phone.text().strip(),
            "email": self.txt_email.text().strip(),
            "room_no": self.txt_room.text().strip(),
            "consultation_fee": self.spn_fee.value(),
            "status": self.cmb_status.currentText().strip()
        }


class DoctorsView(QWidget):
    """
    Physician Roster, Specialization & Real-Time Availability View.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.doctors_data: List[Dict[str, Any]] = []
        self._build_ui()
        self.load_doctors()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # 0. KPI Metrics Strip
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(14)

        self.kpi_total = KpiMetricCard("Medical Faculty", "0 Doctors", "Certified Clinical Specialists", "👨‍⚕️", "#06B6D4")
        self.kpi_avail = KpiMetricCard("Active On Duty", "0 On Duty", "Ready for Consultations", "🟢", "#84CC16")
        self.kpi_surgery = KpiMetricCard("In Procedure / OT", "0 Active", "Operating Theaters Active", "🏥", "#F97316")
        self.kpi_fee = KpiMetricCard("Avg OPD Tariff", "₹0.00", "Standard Consultation Fee", "💰", "#0EA5E9")

        kpi_row.addWidget(self.kpi_total)
        kpi_row.addWidget(self.kpi_avail)
        kpi_row.addWidget(self.kpi_surgery)
        kpi_row.addWidget(self.kpi_fee)
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

        # 1a. Toolbar: Filter and Actions
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        lbl_filter = QLabel("Status:")
        lbl_filter.setStyleSheet("font-size: 12px; font-weight: 700; color: #475569;")
        toolbar.addWidget(lbl_filter)

        self.cmb_status_filter = QComboBox()
        self.cmb_status_filter.addItems(["All", "Available", "In Surgery", "On Leave", "Inactive"])
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
        self.txt_search.setPlaceholderText("🔍 Quick filter by doctor name or specialization...")
        self.txt_search.setFixedWidth(280)
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

        btn_refresh = QPushButton("🔄 Refresh Roster")
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
        btn_refresh.clicked.connect(self.load_doctors)
        toolbar.addWidget(btn_refresh)

        toolbar.addStretch()

        btn_add = QPushButton("➕ Onboard New Doctor")
        btn_add.setCursor(QCursor(Qt.PointingHandCursor))
        btn_add.setStyleSheet("""
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
        btn_add.clicked.connect(self._on_add_doctor)
        toolbar.addWidget(btn_add)

        card_layout.addLayout(toolbar)

        # 1b. Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Code", "Doctor Name", "Specialization", "Contact Phone", "OPD Room", "Consultation Fee", "Duty Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
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
        self.table.doubleClicked.connect(self._view_profile)
        card_layout.addWidget(self.table)

        # 1c. Bottom Actions Strip
        bottom_bar = QHBoxLayout()
        lbl_hint = QLabel("💡 Tip: Double-click or right-click any row to edit details, toggle duty status, or remove record.")
        lbl_hint.setStyleSheet("color: #94A3B8; font-size: 11px; font-style: italic;")
        bottom_bar.addWidget(lbl_hint)

        bottom_bar.addStretch()

        btn_profile = QPushButton("👁️ View Profile")
        btn_profile.setCursor(QCursor(Qt.PointingHandCursor))
        btn_profile.setStyleSheet("""
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
        btn_profile.clicked.connect(self._view_profile)
        bottom_bar.addWidget(btn_profile)

        btn_toggle_duty = QPushButton("🔄 Toggle Status")
        btn_toggle_duty.setCursor(QCursor(Qt.PointingHandCursor))
        btn_toggle_duty.setStyleSheet("""
            QPushButton {
                background-color: #F0FDF4;
                color: #16A34A;
                border: 1px solid #BBF7D0;
                font-weight: 700;
                font-size: 11px;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #DCFCE7;
            }
        """)
        btn_toggle_duty.clicked.connect(self._on_toggle_status)
        bottom_bar.addWidget(btn_toggle_duty)

        btn_edit = QPushButton("✏️ Edit Doctor")
        btn_edit.setCursor(QCursor(Qt.PointingHandCursor))
        btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #F8FAFC;
                color: #334155;
                border: 1px solid #CBD5E1;
                font-weight: 600;
                font-size: 11px;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
        """)
        btn_edit.clicked.connect(self._on_edit_doctor)
        bottom_bar.addWidget(btn_edit)

        card_layout.addLayout(bottom_bar)
        main_layout.addWidget(card)

    def load_doctors(self):
        """Fetch all doctors from SQLite database and populate table."""
        try:
            self.doctors_data = get_all_doctors()
            self._apply_filters()
            self._update_kpi_cards()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load doctor roster: {e}")

    def _update_kpi_cards(self):
        total = len(self.doctors_data)
        avail = sum(1 for d in self.doctors_data if d.get("status") == "Available")
        surgery = sum(1 for d in self.doctors_data if d.get("status") == "In Surgery")
        avg_fee = sum(float(d.get("consultation_fee", 0.0)) for d in self.doctors_data) / max(1, total)

        self.kpi_total.update_value(f"{total} Doctors", "Total Medical Faculty")
        self.kpi_avail.update_value(f"{avail} On Duty", "Ready for Consultations")
        self.kpi_surgery.update_value(f"{surgery} In Surgery", "Operating Theaters Active")
        self.kpi_fee.update_value(f"₹{avg_fee:.2f}", "Standard OPD Tariff")

    def _apply_filters(self):
        status_filter = self.cmb_status_filter.currentText()
        search_query = self.txt_search.text().strip().lower()

        filtered = []
        for d in self.doctors_data:
            if status_filter != "All" and d.get("status") != status_filter:
                continue
            if search_query:
                name_match = search_query in str(d.get("full_name", "")).lower()
                spec_match = search_query in str(d.get("specialization", "")).lower()
                code_match = search_query in str(d.get("doctor_code", "")).lower()
                if not (name_match or spec_match or code_match):
                    continue
            filtered.append(d)

        self.table.setRowCount(len(filtered))
        for row_idx, doc in enumerate(filtered):
            # ID
            item_id = QTableWidgetItem(str(doc.get("id", "")))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 0, item_id)

            # Code
            item_code = QTableWidgetItem(str(doc.get("doctor_code", "")))
            item_code.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 1, item_code)

            # Name
            item_name = QTableWidgetItem(str(doc.get("full_name", "")))
            item_name.setFont(QFont("Segoe UI", 9, QFont.Bold))
            self.table.setItem(row_idx, 2, item_name)

            # Specialization
            item_spec = QTableWidgetItem(str(doc.get("specialization", "")))
            self.table.setItem(row_idx, 3, item_spec)

            # Phone
            item_phone = QTableWidgetItem(str(doc.get("phone", "")))
            self.table.setItem(row_idx, 4, item_phone)

            # Room
            item_room = QTableWidgetItem(str(doc.get("room_no", "")))
            item_room.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 5, item_room)

            # Fee
            fee_val = float(doc.get("consultation_fee", 0.0))
            item_fee = QTableWidgetItem(f"₹ {fee_val:.2f}")
            item_fee.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 6, item_fee)

            # Status Pill Badge
            status = str(doc.get("status", "Available"))
            badge_type = "green" if status == "Available" else ("amber" if status in ["On Leave", "In Surgery"] else "gray")
            badge = Badge(status, badge_type=badge_type)
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(4, 2, 4, 2)
            cell_layout.setAlignment(Qt.AlignCenter)
            cell_layout.addWidget(badge)
            self.table.setCellWidget(row_idx, 7, cell_widget)

    def _get_selected_doctor(self) -> Optional[Dict[str, Any]]:
        row = self.table.currentRow()
        if row < 0:
            return None
        doc_id_item = self.table.item(row, 0)
        if not doc_id_item:
            return None
        doc_id = int(doc_id_item.text())
        for d in self.doctors_data:
            if d.get("id") == doc_id:
                return d
        return None

    def _on_add_doctor(self):
        dlg = DoctorFormDialog(parent=self)
        if dlg.exec():
            data = dlg.get_data()
            try:
                create_doctor(
                    doctor_code=data["doctor_code"],
                    full_name=data["full_name"],
                    specialization=data["specialization"],
                    phone=data["phone"],
                    email=data["email"],
                    room_no=data["room_no"],
                    consultation_fee=data["consultation_fee"],
                    status=data["status"]
                )
                self.load_doctors()
                QMessageBox.information(self, "Success", f"Doctor {data['full_name']} onboarded successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to create doctor: {e}")

    def _on_edit_doctor(self):
        doc = self._get_selected_doctor()
        if not doc:
            QMessageBox.information(self, "Select Row", "Please select a doctor to edit.")
            return

        dlg = DoctorFormDialog(doctor_data=doc, parent=self)
        if dlg.exec():
            data = dlg.get_data()
            try:
                update_doctor(
                    doctor_id=doc["id"],
                    full_name=data["full_name"],
                    specialization=data["specialization"],
                    phone=data["phone"],
                    email=data["email"],
                    room_no=data["room_no"],
                    consultation_fee=data["consultation_fee"],
                    status=data["status"]
                )
                self.load_doctors()
                QMessageBox.information(self, "Success", f"Doctor {data['full_name']} updated.")
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to update doctor: {e}")

    def _on_toggle_status(self):
        doc = self._get_selected_doctor()
        if not doc:
            QMessageBox.information(self, "Select Row", "Please select a doctor to toggle status.")
            return

        cur = doc.get("status", "Available")
        next_status = "In Surgery" if cur == "Available" else ("On Leave" if cur == "In Surgery" else "Available")
        try:
            toggle_doctor_status(doc["id"], next_status)
            self.load_doctors()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to toggle status: {e}")

    def _view_profile(self):
        doc = self._get_selected_doctor()
        if not doc:
            QMessageBox.information(self, "Select Row", "Please select a doctor to view profile.")
            return
        dlg = DoctorProfileDialog(doctor_data=doc, parent=self)
        dlg.exec()
        self.load_doctors()

    def _show_context_menu(self, pos):
        doc = self._get_selected_doctor()
        if not doc:
            return

        menu = QMenu(self)
        act_prof = menu.addAction("👁️ View Physician File")
        act_edit = menu.addAction("✏️ Edit Details")
        menu.addSeparator()
        act_avail = menu.addAction("Set Status: Available")
        act_surg = menu.addAction("Set Status: In Surgery")
        act_leave = menu.addAction("Set Status: On Leave")
        act_inact = menu.addAction("Set Status: Inactive")
        menu.addSeparator()
        act_del = menu.addAction("🗑️ Remove Doctor")

        chosen = menu.exec(self.table.viewport().mapToGlobal(pos))
        if chosen == act_prof:
            self._view_profile()
        elif chosen == act_edit:
            self._on_edit_doctor()
            toggle_doctor_status(doc["id"], "Available")
            self.load_doctors()
        elif chosen == act_surg:
            toggle_doctor_status(doc["id"], "In Surgery")
            self.load_doctors()
        elif chosen == act_leave:
            toggle_doctor_status(doc["id"], "On Leave")
            self.load_doctors()
        elif chosen == act_inact:
            toggle_doctor_status(doc["id"], "Inactive")
            self.load_doctors()
        elif chosen == act_edit:
            self._on_edit_doctor()
        elif chosen == act_del:
            confirm = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete {doc['full_name']}? This action cannot be undone.",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                try:
                    delete_doctor(doc["id"])
                    self.load_doctors()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete doctor: {e}")
