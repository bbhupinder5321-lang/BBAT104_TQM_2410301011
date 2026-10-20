"""
Patients Directory View for PySide6 MedCare HMS.
Features sub-100ms debounced search, Poka-Yoke duplicate validation,
interactive patient registration, record editing, and detailed medical file modal.

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Quality Goal: Q02 - Improve Performance
"""

import time
from typing import Optional, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QComboBox, QMessageBox, QFrame, QMenu
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QCursor

from src.models.patient import (
    fast_search_patients, create_patient, update_patient,
    delete_patient, get_patient_by_id
)
from src.config import SLA_TARGETS
from qt_app.widgets.badge import Badge


class PatientFormDialog(QDialog):
    """Modal Form for Patient Registration or Editing with Real-Time Poka-Yoke."""

    def __init__(self, patient_data: Optional[Dict[str, Any]] = None, parent=None):
        super().__init__(parent)
        self.patient_data = patient_data
        self.is_edit = patient_data is not None

        title = f"Edit Patient: {patient_data.get('full_name')}" if self.is_edit else "Register New Patient (Poka-Yoke Shield)"
        self.setWindowTitle(title)
        self.setFixedSize(500, 520)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
            QLabel {
                font-size: 12px;
                color: #334155;
                font-weight: 600;
            }
            QLineEdit, QComboBox {
                background-color: #F8FAFC;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 7px 12px;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #0284C7;
                background-color: #FFFFFF;
            }
            QPushButton#PrimaryBtn {
                background-color: #0A1128;
                color: white;
                font-weight: 700;
                padding: 9px 18px;
                border-radius: 6px;
                border: none;
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
        self._build_form()

    def _build_form(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 22, 26, 22)
        layout.setSpacing(14)

        # Header Banner
        head_text = "✏️  Edit Patient Information" if self.is_edit else "✚  Register New Patient"
        head = QLabel(head_text)
        head.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 800;")
        layout.addWidget(head)

        lbl_sub = QLabel("Poka-Yoke Phone Uniqueness Validation Enforced (Q02 Quality Shield)")
        lbl_sub.setStyleSheet("color: #0284C7; font-size: 11px; font-weight: 600;")
        layout.addWidget(lbl_sub)

        form = QFormLayout()
        form.setSpacing(10)

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("e.g. Ramesh Verma")
        form.addRow("Full Name *", self.txt_name)

        self.cmb_gender = QComboBox()
        self.cmb_gender.addItems(["Male", "Female", "Other"])
        form.addRow("Gender *", self.cmb_gender)

        self.txt_age = QLineEdit()
        self.txt_age.setPlaceholderText("e.g. 35")
        form.addRow("Age *", self.txt_age)

        self.txt_phone = QLineEdit()
        self.txt_phone.setPlaceholderText("10-digit mobile number")
        form.addRow("Phone Number *", self.txt_phone)

        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("e.g. patient@gmail.com")
        form.addRow("Email Address", self.txt_email)

        self.cmb_blood = QComboBox()
        self.cmb_blood.addItems(["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-", "Unknown"])
        form.addRow("Blood Group", self.cmb_blood)

        self.txt_address = QLineEdit()
        self.txt_address.setPlaceholderText("e.g. Sector 12, Chandigarh")
        form.addRow("City / Address", self.txt_address)

        # Populate if editing
        if self.patient_data:
            p_name = self.patient_data.get("name") or self.patient_data.get("full_name", "")
            self.txt_name.setText(p_name)
            self.cmb_gender.setCurrentText(self.patient_data.get("gender", "Male"))
            self.txt_age.setText(str(self.patient_data.get("age", "")))
            self.txt_phone.setText(self.patient_data.get("phone", ""))
            self.txt_email.setText(self.patient_data.get("email", ""))
            self.cmb_blood.setCurrentText(self.patient_data.get("blood_group", "Unknown"))
            self.txt_address.setText(self.patient_data.get("address", ""))

        layout.addLayout(form)

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("CancelBtn")
        btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        btn_cancel.clicked.connect(self.reject)

        btn_save_text = "Save Changes" if self.is_edit else "Register Patient"
        btn_submit = QPushButton(btn_save_text)
        btn_submit.setObjectName("PrimaryBtn")
        btn_submit.setCursor(QCursor(Qt.PointingHandCursor))
        btn_submit.clicked.connect(self._validate_and_submit)

        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_submit)
        layout.addLayout(btn_row)

    def _validate_and_submit(self):
        name = self.txt_name.text().strip()
        age_str = self.txt_age.text().strip()
        phone = self.txt_phone.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Patient full name is required.")
            return

        try:
            age = int(age_str)
            if age <= 0 or age > 130:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid age (1-130).")
            return

        if len(phone) < 7:
            QMessageBox.warning(self, "Validation Error", "Phone number must be at least 7 digits.")
            return

        try:
            if self.is_edit:
                update_patient(
                    patient_id=self.patient_data["id"],
                    full_name=name,
                    gender=self.cmb_gender.currentText(),
                    age=age,
                    phone=phone,
                    email=self.txt_email.text().strip(),
                    address=self.txt_address.text().strip(),
                    blood_group=self.cmb_blood.currentText()
                )
                QMessageBox.information(self, "Success", f"Patient '{name}' details updated successfully.")
            else:
                p_id, uhid = create_patient(
                    full_name=name,
                    gender=self.cmb_gender.currentText(),
                    age=age,
                    phone=phone,
                    email=self.txt_email.text().strip(),
                    address=self.txt_address.text().strip(),
                    blood_group=self.cmb_blood.currentText()
                )
                QMessageBox.information(self, "Success", f"Patient registered successfully!\nGenerated UHID: {uhid}")

            self.accept()
        except ValueError as err:
            QMessageBox.critical(self, "Poka-Yoke Validation Shield", str(err))


class PatientDetailsDialog(QDialog):
    """Modal View for Comprehensive Patient Medical Card."""

    def __init__(self, patient_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.patient_data = patient_data
        p_name = patient_data.get("name") or patient_data.get("full_name", "")
        self.setWindowTitle(f"Patient File: {p_name}")
        self.setFixedSize(480, 420)
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

        # Header with UHID Pill
        top_row = QHBoxLayout()
        name_col = QVBoxLayout()
        name_col.setSpacing(2)

        p_name = self.patient_data.get("name") or self.patient_data.get("full_name", "")
        lbl_name = QLabel(p_name)
        lbl_name.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
        lbl_uhid = QLabel(f"UHID: {self.patient_data.get('uhid', '')}")
        lbl_uhid.setStyleSheet("font-size: 12px; font-weight: 700; color: #0284C7;")
        name_col.addWidget(lbl_name)
        name_col.addWidget(lbl_uhid)
        top_row.addLayout(name_col)

        bg = self.patient_data.get("blood_group") or "Unknown"
        badge_bg = Badge(f"🩸 {bg}", badge_type="red")
        top_row.addWidget(badge_bg, alignment=Qt.AlignRight | Qt.AlignVCenter)
        layout.addLayout(top_row)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: #E2E8F0;")
        layout.addWidget(divider)

        # Details Grid Card
        info_card = QFrame()
        info_card.setStyleSheet("""
            QFrame {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
            }
        """)
        i_lay = QFormLayout(info_card)
        i_lay.setContentsMargins(16, 14, 16, 14)
        i_lay.setSpacing(10)

        i_lay.addRow("Gender:", QLabel(str(self.patient_data.get("gender", "-"))))
        i_lay.addRow("Age:", QLabel(f"{self.patient_data.get('age', '-')} years"))
        i_lay.addRow("Contact Phone:", QLabel(str(self.patient_data.get("phone", "-"))))
        i_lay.addRow("Email Address:", QLabel(str(self.patient_data.get("email") or "Not registered")))
        i_lay.addRow("City / Address:", QLabel(str(self.patient_data.get("address") or "General OPD")))
        i_lay.addRow("Registered On:", QLabel(str(self.patient_data.get("created_at") or "-")))

        layout.addWidget(info_card)

        # Footer Buttons
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


class PatientsView(QWidget):
    """Modern Patients Directory with Fast Search, Full Editing, and SLA Telemetry."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.patients_cache = []
        self.debounce_timer = QTimer(self)
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.load_patients)

        self._build_ui()
        self.load_patients()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(16)

        # Header Row
        head_row = QHBoxLayout()
        lbl_title = QLabel("Patients Registry & Demographic Directory")
        lbl_title.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 800;")
        head_row.addWidget(lbl_title)

        btn_register = QPushButton("✚ Register Patient")
        btn_register.setCursor(QCursor(Qt.PointingHandCursor))
        btn_register.setStyleSheet("""
            QPushButton {
                background-color: #0A1128;
                color: white;
                font-size: 13px;
                font-weight: 700;
                padding: 8px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1E293B;
            }
        """)
        btn_register.clicked.connect(self._open_register_modal)
        head_row.addWidget(btn_register, alignment=Qt.AlignRight)
        layout.addLayout(head_row)

        # Search Bar + Latency Card
        search_card = QFrame()
        search_card.setObjectName("Card")
        search_card.setStyleSheet("""
            QFrame#Card {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        s_layout = QHBoxLayout(search_card)
        s_layout.setContentsMargins(16, 10, 16, 10)
        s_layout.setSpacing(14)

        lbl_icon = QLabel("🔍")
        lbl_icon.setStyleSheet("font-size: 16px;")
        s_layout.addWidget(lbl_icon)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Instant search by patient name, UHID, or phone number...")
        self.txt_search.setStyleSheet("""
            QLineEdit {
                border: none;
                background: transparent;
                font-size: 13px;
                color: #0F172A;
            }
        """)
        self.txt_search.textChanged.connect(self._on_search_changed)
        s_layout.addWidget(self.txt_search, 1)

        self.lbl_latency_badge = QLabel("⚡ Latency: 0.8ms | SLA: PASSED (<100ms)")
        self.lbl_latency_badge.setStyleSheet("""
            background-color: #DCFCE7;
            color: #15803D;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 700;
        """)
        s_layout.addWidget(self.lbl_latency_badge)
        layout.addWidget(search_card)

        # Table Card Container
        table_card = QFrame()
        table_card.setObjectName("TableCard")
        table_card.setStyleSheet("""
            QFrame#TableCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        t_layout = QVBoxLayout(table_card)
        t_layout.setContentsMargins(14, 14, 14, 14)
        t_layout.setSpacing(12)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "UHID", "Patient Name", "Gender", "Age", "Contact Phone", "Blood Group"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
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
        self.table.doubleClicked.connect(self._open_edit_modal)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        t_layout.addWidget(self.table)

        # Interactive Row Actions Footer
        act_row = QHBoxLayout()
        act_row.setSpacing(10)

        lbl_hint = QLabel("💡 Tip: Double-click any row to edit details, or use quick actions on right.")
        lbl_hint.setStyleSheet("color: #94A3B8; font-size: 11px; font-style: italic;")
        act_row.addWidget(lbl_hint)

        act_row.addStretch()

        btn_view_file = QPushButton("👁️ View Medical Card")
        btn_view_file.setCursor(QCursor(Qt.PointingHandCursor))
        btn_view_file.setStyleSheet("""
            QPushButton {
                background-color: #E0F2FE;
                color: #0284C7;
                font-weight: 700;
                font-size: 11px;
                padding: 6px 14px;
                border-radius: 6px;
                border: 1px solid #BAE6FD;
            }
            QPushButton:hover {
                background-color: #BAE6FD;
            }
        """)
        btn_view_file.clicked.connect(self._open_details_modal)
        act_row.addWidget(btn_view_file)

        btn_edit = QPushButton("✏️ Edit Record")
        btn_edit.setCursor(QCursor(Qt.PointingHandCursor))
        btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #F8FAFC;
                color: #334155;
                font-weight: 600;
                font-size: 11px;
                padding: 6px 14px;
                border-radius: 6px;
                border: 1px solid #CBD5E1;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
        """)
        btn_edit.clicked.connect(self._open_edit_modal)
        act_row.addWidget(btn_edit)

        btn_delete = QPushButton("🗑️ Remove Patient")
        btn_delete.setCursor(QCursor(Qt.PointingHandCursor))
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #FEE2E2;
                color: #DC2626;
                font-weight: 600;
                font-size: 11px;
                padding: 6px 14px;
                border-radius: 6px;
                border: 1px solid #FECACA;
            }
            QPushButton:hover {
                background-color: #FECACA;
            }
        """)
        btn_delete.clicked.connect(self._delete_patient)
        act_row.addWidget(btn_delete)

        t_layout.addLayout(act_row)
        layout.addWidget(table_card)

    def _on_search_changed(self):
        self.debounce_timer.start(120)

    def load_patients(self):
        query = self.txt_search.text().strip()
        records, latency_ms = fast_search_patients(query, limit=100)
        self.patients_cache = records

        self.table.setRowCount(len(records))
        for row, p in enumerate(records):
            item_id = QTableWidgetItem(str(p["id"]))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item_id)

            item_uhid = QTableWidgetItem(p["uhid"])
            item_uhid.setFont(QFont("Segoe UI", 9, QFont.Bold))
            item_uhid.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, item_uhid)

            name_item = QTableWidgetItem(p["full_name"])
            name_item.setFont(QFont("Segoe UI", 9, QFont.Bold))
            self.table.setItem(row, 2, name_item)

            item_g = QTableWidgetItem(p["gender"])
            item_g.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, item_g)

            item_a = QTableWidgetItem(str(p["age"]))
            item_a.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, item_a)

            self.table.setItem(row, 5, QTableWidgetItem(p["phone"]))

            bg = p.get("blood_group") or "-"
            badge = Badge(bg, badge_type="cyan" if bg != "-" else "gray")
            c_w = QWidget()
            c_l = QHBoxLayout(c_w)
            c_l.setContentsMargins(4, 2, 4, 2)
            c_l.setAlignment(Qt.AlignCenter)
            c_l.addWidget(badge)
            self.table.setCellWidget(row, 6, c_w)

        sla_pass = latency_ms <= SLA_TARGETS["SEARCH_MAX_MS"]
        status = "PASSED (<100ms)" if sla_pass else "BREACHED"
        bg = "#DCFCE7" if sla_pass else "#FEE2E2"
        fg = "#15803D" if sla_pass else "#DC2626"

        self.lbl_latency_badge.setText(f"⚡ Latency: {latency_ms:.2f}ms | {len(records)} found | SLA: {status}")
        self.lbl_latency_badge.setStyleSheet(f"""
            background-color: {bg};
            color: {fg};
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 700;
        """)

    def _get_selected_patient(self) -> Optional[Dict[str, Any]]:
        row = self.table.currentRow()
        if row < 0 or row >= len(self.patients_cache):
            return None
        return self.patients_cache[row]

    def _open_register_modal(self):
        dlg = PatientFormDialog(parent=self)
        if dlg.exec():
            self.load_patients()

    def _open_edit_modal(self):
        p = self._get_selected_patient()
        if not p:
            QMessageBox.information(self, "Select Row", "Please select a patient to edit details.")
            return

        # Fetch full demographic details
        full_p = get_patient_by_id(p["id"]) or p
        dlg = PatientFormDialog(patient_data=full_p, parent=self)
        if dlg.exec():
            self.load_patients()

    def _open_details_modal(self):
        p = self._get_selected_patient()
        if not p:
            QMessageBox.information(self, "Select Row", "Please select a patient to view medical file.")
            return

        full_p = get_patient_by_id(p["id"]) or p
        dlg = PatientDetailsDialog(patient_data=full_p, parent=self)
        dlg.exec()

    def _delete_patient(self):
        p = self._get_selected_patient()
        if not p:
            QMessageBox.information(self, "Select Row", "Please select a patient to remove.")
            return

        confirm = QMessageBox.question(
            self, "Confirm Patient Deletion",
            f"Are you sure you want to delete patient '{p['full_name']}' ({p['uhid']})?\n"
            "This will cascade delete all associated appointment and billing records.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                delete_patient(p["id"])
                self.load_patients()
                QMessageBox.information(self, "Deleted", f"Patient {p['full_name']} removed.")
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to delete patient: {e}")

    def _show_context_menu(self, pos):
        p = self._get_selected_patient()
        if not p:
            return

        menu = QMenu(self)
        act_view = menu.addAction("👁️ View Medical Card")
        act_edit = menu.addAction("✏️ Edit Patient Details")
        menu.addSeparator()
        act_del = menu.addAction("🗑️ Remove Patient Record")

        chosen = menu.exec(self.table.viewport().mapToGlobal(pos))
        if chosen == act_view:
            self._open_details_modal()
        elif chosen == act_edit:
            self._open_edit_modal()
        elif chosen == act_del:
            self._delete_patient()
