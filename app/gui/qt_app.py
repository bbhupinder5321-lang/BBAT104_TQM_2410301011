"""PySide6 interface for MediCare Hospital Management System.

This module introduces the Qt interface without deleting the legacy Tkinter
screens. Business rules and database access remain in the existing services.
Run with: python -m app.gui.qt_main
"""
from __future__ import annotations

import csv
import os
from datetime import date
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QDialogButtonBox, QFileDialog,
    QFormLayout, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMessageBox, QPushButton, QScrollArea, QSizePolicy,
    QSpinBox, QDoubleSpinBox, QStackedWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget, QTextEdit
)

from app.services.auth_service import AuthService
from app.services.patient_service import PatientService
from app.services.doctor_service import DoctorService
from app.services.appointment_service import AppointmentService
from app.services.bill_service import BillService
from app.services.dashboard_service import DashboardService
from app.services.report_service import ReportService
from app.services.performance_service import PerformanceService
from app.services.csv_import_service import CSVImportService
from app.services.tqm_service import TQMService


APP_STYLE = """
QWidget {
    background: #F4F7FB; color: #172033;
    font-family: "Segoe UI"; font-size: 10pt;
}
QMainWindow { background: #F4F7FB; }
QFrame#Sidebar { background: #111827; border: none; }
QFrame#Sidebar QLabel { background: transparent; color: #D7DFEA; }
QLabel#Brand { color: #FFFFFF; font-size: 19pt; font-weight: 700; }
QLabel#BrandSub { color: #94A3B8; font-size: 8pt; }
QLabel#TopbarTitle { font-size: 15pt; font-weight: 700; color: #101828; }
QFrame#Topbar { background: #FFFFFF; border: none; border-bottom: 1px solid #E3EAF3; }
QLineEdit#WorkspaceSearch { background: #F8FAFC; border: 1px solid #E2E8F0; }
QLineEdit#WorkspaceSearch:focus { background: #FFFFFF; border: 1px solid #2563EB; }
QLabel#PageTitle { font-size: 23pt; font-weight: 700; color: #101828; }
QLabel#PageSub { color: #667085; font-size: 10pt; }
QLabel#CardTitle { color: #667085; font-size: 9pt; font-weight: 600; }
QLabel#MetricValue { color: #101828; font-size: 23pt; font-weight: 700; }
QFrame#Card, QFrame#Panel {
    background: #FFFFFF; border: 1px solid #E3EAF3; border-radius: 13px;
}
QPushButton {
    background: #2563EB; color: #FFFFFF; border: none;
    border-radius: 8px; padding: 9px 14px; font-weight: 600;
}
QPushButton:hover { background: #1D4ED8; }
QPushButton:disabled { background: #AAB8CC; color: #F5F7FA; }
QPushButton#NavButton {
    background: transparent; color: #CBD5E1; text-align: left;
    padding: 11px 14px; border-radius: 8px; font-weight: 500;
}
QPushButton#NavButton:hover { background: #1F2937; color: #FFFFFF; }
QPushButton#NavButton[active="true"] { background: #2563EB; color: #FFFFFF; }
QPushButton#Secondary {
    background: #EAF0F8; color: #24334A;
}
QPushButton#Secondary:hover { background: #DCE6F3; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
    background: #FFFFFF; border: 1px solid #D5DEEA; border-radius: 7px;
    padding: 8px; selection-background-color: #2563EB;
}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus { border: 1px solid #2563EB; }
QTableWidget {
    background: #FFFFFF; alternate-background-color: #F8FAFD;
    border: 1px solid #E3EAF3; border-radius: 8px; gridline-color: #EEF2F7;
    selection-background-color: #E3EDFF; selection-color: #14213D;
}
QHeaderView::section {
    background: #F1F5FA; color: #526176; border: none;
    border-bottom: 1px solid #E0E7F0; padding: 10px; font-weight: 700;
}
QScrollArea { border: none; background: transparent; }
QDialog { background: #F4F7FB; }
"""


def as_dict(row):
    if row is None:
        return {}
    try:
        return dict(row)
    except (TypeError, ValueError):
        return row if isinstance(row, dict) else {}


def make_label(text, object_name=None):
    label = QLabel(str(text))
    if object_name:
        label.setObjectName(object_name)
    return label


def make_panel():
    panel = QFrame()
    panel.setObjectName("Panel")
    return panel


class RecordDialog(QDialog):
    """Reusable, validated form dialog for service-backed records."""

    def __init__(self, title, fields, initial=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(470)
        self.fields = fields
        self.inputs = {}
        initial = initial or {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 20)
        heading = make_label(title, "PageTitle")
        heading.setStyleSheet("font-size: 17pt;")
        layout.addWidget(heading)
        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(13)

        for key, label, kind, options in fields:
            if kind == "combo":
                widget = QComboBox()
                for display, value in options:
                    widget.addItem(str(display), value)
                existing = initial.get(key)
                if existing is not None:
                    idx = widget.findData(existing)
                    if idx < 0:
                        idx = widget.findText(str(existing))
                    if idx >= 0:
                        widget.setCurrentIndex(idx)
            elif kind == "amount":
                widget = QDoubleSpinBox()
                widget.setRange(0, 999999999)
                widget.setDecimals(2)
                widget.setPrefix("₹ ")
                widget.setValue(float(initial.get(key) or 0))
            elif kind == "multiline":
                widget = QTextEdit()
                widget.setFixedHeight(82)
                widget.setPlainText(str(initial.get(key, "")))
            else:
                widget = QLineEdit()
                widget.setPlaceholderText(label)
                widget.setText(str(initial.get(key, "")))
                if kind == "date":
                    widget.setPlaceholderText("YYYY-MM-DD")
                elif kind == "time":
                    widget.setPlaceholderText("HH:MM")
            self.inputs[key] = widget
            form.addRow(label, widget)

        layout.addLayout(form)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def values(self):
        result = {}
        for key, _label, kind, _options in self.fields:
            widget = self.inputs[key]
            if kind == "combo":
                result[key] = widget.currentData()
            elif kind == "amount":
                result[key] = widget.value()
            elif kind == "multiline":
                result[key] = widget.toPlainText().strip()
            else:
                result[key] = widget.text().strip()
        return result


class DataPage(QWidget):
    """Searchable table with service-backed add, edit, and delete actions."""

    def __init__(self, title, subtitle, columns, loader, fields, add_fn, edit_fn,
                 delete_fn, parent=None, search_hint="Search records...", extra_actions=None):
        super().__init__(parent)
        self.page_title = title
        self.columns = columns
        self.loader = loader
        self.fields = fields
        self.add_fn = add_fn
        self.edit_fn = edit_fn
        self.delete_fn = delete_fn
        self.extra_actions = extra_actions or []
        self.records = []
        self.search = QLineEdit()
        self.search.setPlaceholderText(search_hint)
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self.apply_filter)

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 26, 30, 26)
        root.setSpacing(18)
        root.addWidget(make_label(title, "PageTitle"))
        root.addWidget(make_label(subtitle, "PageSub"))

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.search, 1)
        self.add_button = QPushButton("+  Add record")
        self.add_button.clicked.connect(self.add_record)
        toolbar.addWidget(self.add_button)
        edit_button = QPushButton("Edit selected")
        edit_button.setObjectName("Secondary")
        edit_button.clicked.connect(self.edit_record)
        toolbar.addWidget(edit_button)
        delete_button = QPushButton("Delete")
        delete_button.setObjectName("Secondary")
        delete_button.clicked.connect(self.delete_record)
        toolbar.addWidget(delete_button)
        for action_label, _action in self.extra_actions:
            action_button = QPushButton(action_label)
            action_button.setObjectName("Secondary")
            action_button.clicked.connect(
                lambda _checked=False, action=_action: self.run_extra_action(action)
            )
            toolbar.addWidget(action_button)
        refresh_button = QPushButton("Refresh")
        refresh_button.setObjectName("Secondary")
        refresh_button.clicked.connect(self.refresh)
        toolbar.addWidget(refresh_button)
        root.addLayout(toolbar)

        panel = make_panel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(12, 12, 12, 12)
        self.table = QTableWidget(0, len(columns))
        self.table.setHorizontalHeaderLabels([label for _key, label in columns])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setMinimumSectionSize(90)
        self.table.setSortingEnabled(True)
        panel_layout.addWidget(self.table)
        root.addWidget(panel, 1)
        self.footer = make_label("Loading records…", "PageSub")
        root.addWidget(self.footer)
        self.refresh()

    def refresh(self):
        try:
            self.records = [as_dict(row) for row in self.loader()]
            self.apply_filter()
        except Exception as error:
            QMessageBox.critical(self, "Unable to load records", str(error))
            self.footer.setText("Records could not be loaded.")

    def apply_filter(self, *_):
        query = self.search.text().strip().casefold()
        rows = [
            row for row in self.records
            if not query or any(query in str(value or "").casefold() for value in row.values())
        ]
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(rows))
        for row_index, record in enumerate(rows):
            for column_index, (key, _label) in enumerate(self.columns):
                value = record.get(key, "")
                if key == "amount" and value not in ("", None):
                    try:
                        value = f"₹ {float(value):,.2f}"
                    except (ValueError, TypeError):
                        pass
                item = QTableWidgetItem("" if value is None else str(value))
                item.setData(Qt.ItemDataRole.UserRole, record)
                self.table.setItem(row_index, column_index, item)
        self.table.setSortingEnabled(True)
        self.footer.setText(f"{len(rows)} records shown · {len(self.records)} total")

    def selected_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Select a record", "Choose a row in the table first.")
            return None
        item = self.table.item(row, 0)
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def add_record(self):
        dialog = RecordDialog(f"Add {self.page_title.rstrip('s')}", self.fields, parent=self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            self.add_fn(dialog.values())
            self.refresh()
            QMessageBox.information(self, "Saved", "The record was added successfully.")
        except Exception as error:
            QMessageBox.warning(self, "Could not save record", str(error))

    def edit_record(self):
        record = self.selected_record()
        if not record:
            return
        dialog = RecordDialog(f"Edit {self.page_title.rstrip('s')}", self.fields, record, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            self.edit_fn(record, dialog.values())
            self.refresh()
            QMessageBox.information(self, "Saved", "The record was updated successfully.")
        except Exception as error:
            QMessageBox.warning(self, "Could not update record", str(error))

    def run_extra_action(self, action):
        record = self.selected_record()
        if not record:
            return
        try:
            message = action(record)
            self.refresh()
            if message:
                QMessageBox.information(self, "Appointment updated", message)
        except Exception as error:
            QMessageBox.warning(self, "Action failed", str(error))

    def delete_record(self):
        record = self.selected_record()
        if not record:
            return
        primary_key = self.columns[0][0]
        if QMessageBox.question(
            self, "Confirm deletion",
            f"Delete record #{record.get(primary_key, '')}? This cannot be undone."
        ) != QMessageBox.StandardButton.Yes:
            return
        try:
            self.delete_fn(record)
            self.refresh()
        except Exception as error:
            QMessageBox.warning(self, "Could not delete record", str(error))


class MetricCard(QFrame):
    def __init__(self, title, value, hint="", accent="#2563EB", parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 17, 18, 17)
        layout.setSpacing(7)
        stripe = QFrame()
        stripe.setFixedHeight(4)
        stripe.setStyleSheet(f"background:{accent}; border-radius:2px;")
        layout.addWidget(stripe)
        layout.addWidget(make_label(title, "CardTitle"))
        layout.addWidget(make_label(value, "MetricValue"))
        if hint:
            layout.addWidget(make_label(hint, "PageSub"))


class DashboardPage(QWidget):
    def __init__(self, user, navigate, parent=None):
        super().__init__(parent)
        self.user = user
        self.navigate = navigate
        self.service = DashboardService()
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(30, 26, 30, 28)
        self.root.setSpacing(18)
        self.build()

    def build(self):
        top = QHBoxLayout()
        title_area = QVBoxLayout()
        title_area.addWidget(make_label("Good day, " + self.user.get("username", "User"), "PageTitle"))
        title_area.addWidget(make_label("Here’s the operational overview for your hospital today.", "PageSub"))
        top.addLayout(title_area, 1)
        refresh = QPushButton("↻  Refresh dashboard")
        refresh.clicked.connect(self.refresh)
        top.addWidget(refresh, 0, Qt.AlignmentFlag.AlignTop)
        self.root.addLayout(top)

        self.metrics_area = QGridLayout()
        self.metrics_area.setSpacing(14)
        self.root.addLayout(self.metrics_area)
        self.dynamic_area = QHBoxLayout()
        self.dynamic_area.setSpacing(16)
        self.root.addLayout(self.dynamic_area, 1)
        self.quick_area = QHBoxLayout()
        self.quick_area.setSpacing(10)
        self.root.addLayout(self.quick_area)
        self.refresh()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child = item.layout()
            if widget:
                widget.deleteLater()
            if child:
                self.clear_layout(child)

    def refresh(self):
        try:
            metrics = self.service.get_dashboard_metrics()
        except Exception as error:
            QMessageBox.critical(self, "Dashboard error", str(error))
            return
        self.clear_layout(self.metrics_area)
        cards = [
            ("New patients today", metrics.get("today_patients", 0), "Registrations today", "#2563EB"),
            ("Appointments today", metrics.get("today_appointments", 0), "All scheduled visits", "#7C3AED"),
            ("Waiting in queue", metrics.get("checked_in_appointments", 0), "Checked in, not yet seen", "#D97706"),
            ("Average wait", self.service.format_waiting_time(metrics.get("average_waiting_seconds", 0)), "Measured check-in to consultation", "#0891B2"),
        ]
        for i, (title, value, hint, color) in enumerate(cards):
            self.metrics_area.addWidget(MetricCard(title, value, hint, color), 0, i)

        self.clear_layout(self.dynamic_area)
        queue_panel = make_panel()
        queue_layout = QVBoxLayout(queue_panel)
        queue_layout.setContentsMargins(18, 16, 18, 16)
        queue_layout.addWidget(make_label("Today’s appointment queue", "PageTitle"))
        queue_layout.addWidget(make_label("A quick view of patient flow and consultation status.", "PageSub"))
        queue = QTableWidget(0, 4)
        queue.setHorizontalHeaderLabels(["Time", "Patient", "Doctor", "Status"])
        queue.verticalHeader().setVisible(False)
        queue.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        queue.setAlternatingRowColors(True)
        items = metrics.get("queue", [])
        queue.setRowCount(len(items))
        for ri, item in enumerate(items):
            item = as_dict(item)
            values = [item.get("appointment_time", ""), item.get("patient_name", ""),
                      item.get("doctor_name", ""), item.get("status", "")]
            for ci, value in enumerate(values):
                queue.setItem(ri, ci, QTableWidgetItem(str(value or "")))
        queue.horizontalHeader().setStretchLastSection(True)
        queue_layout.addWidget(queue, 1)
        self.dynamic_area.addWidget(queue_panel, 3)

        capacity_panel = make_panel()
        capacity_layout = QVBoxLayout(capacity_panel)
        capacity_layout.setContentsMargins(20, 18, 20, 18)
        capacity_layout.addWidget(make_label("Hospital capacity", "PageTitle"))
        capacity_layout.addWidget(make_label("Bed utilization snapshot", "PageSub"))
        total = int(metrics.get("total_beds", 0))
        occupied = int(metrics.get("occupied_beds", 0))
        available = int(metrics.get("available_beds", 0))
        pct = self.service.get_bed_occupancy_percentage(occupied, total)
        capacity_layout.addWidget(MetricCard("Occupied beds", f"{occupied} / {total}", f"{pct}% occupancy", "#10B981"))
        capacity_layout.addWidget(MetricCard("Available beds", available, "Based on current bed records", "#0891B2"))
        for ward in metrics.get("bed_wards", []):
            ward = as_dict(ward)
            cap = f"{ward.get('occupied_beds', 0)} of {ward.get('total_beds', 0)} beds occupied"
            capacity_layout.addWidget(make_label(f"{ward.get('ward', 'Ward')}: {cap}", "PageSub"))
        self.dynamic_area.addWidget(capacity_panel, 2)

        self.clear_layout(self.quick_area)
        actions = [
            ("Register patient", "Patients"),
            ("Book appointment", "Appointments"),
            ("Create bill", "Billing"),
            ("View reports", "Reports"),
        ]
        for text, page in actions:
            button = QPushButton(text + "  →")
            button.setObjectName("Secondary")
            button.clicked.connect(lambda _checked=False, name=page: self.navigate(name))
            self.quick_area.addWidget(button)
        self.root.addStretch(0)


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.auth = AuthService()
        self.setWindowTitle("MediCare | Secure sign in")
        self.setMinimumSize(900, 590)
        self.resize(1050, 680)

        base = QWidget()
        base.setStyleSheet("background:#F4F7FB;")
        layout = QHBoxLayout(base)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        brand = QFrame()
        brand.setMinimumWidth(380)
        brand.setStyleSheet("background:#111827;")
        brand_layout = QVBoxLayout(brand)
        brand_layout.setContentsMargins(42, 48, 42, 42)
        brand_layout.addStretch()
        logo = make_label("✚", None)
        logo.setStyleSheet("color:#FFFFFF;background:#2563EB;font-size:28pt;font-weight:700;border-radius:16px;padding:12px;")
        logo.setFixedSize(74, 74)
        brand_layout.addWidget(logo, 0, Qt.AlignmentFlag.AlignLeft)
        brand_layout.addSpacing(18)
        name = make_label("MediCare", None)
        name.setStyleSheet("color:#FFFFFF;font-size:28pt;font-weight:700;")
        brand_layout.addWidget(name)
        tagline = make_label("Hospital Management System", None)
        tagline.setStyleSheet("color:#AAB7CA;font-size:12pt;")
        brand_layout.addWidget(tagline)
        brand_layout.addSpacing(30)
        statement = make_label("Better patient flow.\nClearer decisions.\nContinuous improvement.", None)
        statement.setStyleSheet("color:#E2E8F0;font-size:16pt;line-height:1.4;")
        brand_layout.addWidget(statement)
        brand_layout.addStretch()
        brand_layout.addWidget(make_label("Q02 · Improve Performance", None))

        form_wrap = QWidget()
        form_layout = QVBoxLayout(form_wrap)
        form_layout.setContentsMargins(58, 52, 58, 48)
        form_layout.addStretch()
        form_layout.addWidget(make_label("Welcome back", "PageTitle"))
        form_layout.addWidget(make_label("Sign in to your hospital workspace.", "PageSub"))
        form_layout.addSpacing(28)
        form_layout.addWidget(make_label("Username"))
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        self.username.setText("admin")
        self.username.setMinimumHeight(44)
        form_layout.addWidget(self.username)
        form_layout.addSpacing(12)
        form_layout.addWidget(make_label("Password"))
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setText("")
        self.password.setMinimumHeight(44)
        self.password.returnPressed.connect(self.sign_in)
        form_layout.addWidget(self.password)
        form_layout.addSpacing(18)
        login = QPushButton("Sign in  →")
        login.setMinimumHeight(46)
        login.clicked.connect(self.sign_in)
        form_layout.addWidget(login)
        form_layout.addSpacing(18)
        form_layout.addWidget(make_label("Access is controlled by your assigned account role.", "PageSub"))
        form_layout.addStretch()
        layout.addWidget(brand, 2)
        layout.addWidget(form_wrap, 3)
        self.setCentralWidget(base)

    def sign_in(self):
        try:
            user = self.auth.login(self.username.text(), self.password.text())
        except Exception as error:
            QMessageBox.warning(self, "Sign in failed", str(error))
            self.password.selectAll()
            self.password.setFocus()
            return
        self.app_window = HospitalWindow(user)
        self.app_window.show()
        self.close()


class HospitalWindow(QMainWindow):
    NAV_ITEMS = [
        ("Dashboard", "Overview", "dashboard"),
        ("Patients", "Patient records", "manage_patients"),
        ("Doctors", "Doctor directory", "manage_doctors"),
        ("Appointments", "Patient flow", "manage_appointments"),
        ("Billing", "Payments and invoices", "manage_billing"),
        ("CSV Import", "Bulk patient import", "import_csv"),
        ("Reports", "Operational reports", "view_reports"),
        ("Performance", "Q02 performance", "view_performance"),
        ("TQM Analysis", "Quality improvement", "view_reports"),
    ]

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.role = user.get("role", "staff")
        self.setWindowTitle(f"MediCare · {self.role.title()} workspace")
        self.resize(1440, 900)
        self.setMinimumSize(1120, 720)
        self.pages = {}
        self.nav_buttons = {}

        shell = QWidget()
        shell_layout = QHBoxLayout(shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(245)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(15, 24, 15, 18)
        side_layout.setSpacing(7)
        brand_row = QHBoxLayout()
        brand_icon = make_label("✚")
        brand_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_icon.setFixedSize(43, 43)
        brand_icon.setStyleSheet("background:#2563EB;color:white;font-size:22pt;font-weight:700;border-radius:12px;")
        brand_row.addWidget(brand_icon)
        brand_text = QVBoxLayout()
        brand_text.addWidget(make_label("MediCare", "Brand"))
        brand_text.addWidget(make_label("HOSPITAL MANAGEMENT", "BrandSub"))
        brand_row.addLayout(brand_text, 1)
        side_layout.addLayout(brand_row)
        side_layout.addSpacing(18)

        profile = QFrame()
        profile.setStyleSheet("background:#1D2939;border:1px solid #2B3A4F;border-radius:10px;")
        profile_layout = QVBoxLayout(profile)
        profile_layout.setContentsMargins(13, 12, 13, 12)
        profile_layout.addWidget(make_label(user.get("username", "User")))
        profile_layout.addWidget(make_label(f"{self.role.title()} account"))
        side_layout.addWidget(profile)
        side_layout.addSpacing(16)
        side_layout.addWidget(make_label("WORKSPACE"))
        for title, subtitle, permission in self.NAV_ITEMS:
            if not self.allowed(permission):
                continue
            button = QPushButton(title)
            button.setObjectName("NavButton")
            button.setProperty("active", False)
            button.clicked.connect(lambda _checked=False, name=title: self.show_page(name))
            self.nav_buttons[title] = button
            side_layout.addWidget(button)
        side_layout.addStretch()
        online = make_label("●  System ready")
        online.setStyleSheet("color:#34D399;")
        side_layout.addWidget(online)
        logout = QPushButton("↪  Sign out")
        logout.setObjectName("NavButton")
        logout.clicked.connect(self.logout)
        side_layout.addWidget(logout)

        # Main workspace: persistent top bar + the existing page stack.
        # Keeping the stack intact means every service-backed page and action remains available.
        workspace = QWidget()
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)

        topbar = QFrame()
        topbar.setObjectName("Topbar")
        topbar.setStyleSheet(
            "QFrame#Topbar { background:#FFFFFF; border:0; "
            "border-bottom:1px solid #E3EAF3; }"
        )
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(28, 15, 28, 15)
        topbar_layout.setSpacing(18)

        heading_group = QVBoxLayout()
        heading_group.setSpacing(2)
        self.page_heading = make_label("Dashboard", "TopbarTitle")
        self.page_heading.setStyleSheet(
            "font-size:15pt;font-weight:700;color:#101828;background:transparent;"
        )
        self.page_breadcrumb = make_label("Workspace  /  Overview", "PageSub")
        heading_group.addWidget(self.page_heading)
        heading_group.addWidget(self.page_breadcrumb)
        topbar_layout.addLayout(heading_group, 1)

        self.page_search = QLineEdit()
        self.page_search.setObjectName("WorkspaceSearch")
        self.page_search.setPlaceholderText("Quick jump to a page…")
        self.page_search.setClearButtonEnabled(True)
        self.page_search.setMaximumWidth(300)
        self.page_search.setMinimumHeight(38)
        self.page_search.returnPressed.connect(self.navigate_from_search)
        topbar_layout.addWidget(self.page_search)

        user_chip = QFrame()
        user_chip.setStyleSheet(
            "QFrame { background:#F1F5F9;border:1px solid #E2E8F0;border-radius:10px; }"
        )
        chip_layout = QHBoxLayout(user_chip)
        chip_layout.setContentsMargins(11, 7, 11, 7)
        chip_layout.setSpacing(9)
        avatar = make_label(self.user.get("username", "U")[:1].upper())
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setFixedSize(31, 31)
        avatar.setStyleSheet(
            "background:#DBEAFE;color:#1D4ED8;border-radius:8px;font-weight:700;"
        )
        chip_layout.addWidget(avatar)
        identity = QVBoxLayout()
        identity.setSpacing(0)
        identity.addWidget(make_label(self.user.get("username", "User")))
        role_label = make_label(self.role.title() + " account", "PageSub")
        identity.addWidget(role_label)
        chip_layout.addLayout(identity)
        topbar_layout.addWidget(user_chip)

        self.stack = QStackedWidget()
        self.stack.setContentsMargins(0, 0, 0, 0)
        workspace_layout.addWidget(topbar)
        workspace_layout.addWidget(self.stack, 1)
        shell_layout.addWidget(sidebar)
        shell_layout.addWidget(workspace, 1)
        self.setCentralWidget(shell)
        self.statusBar().showMessage("MediCare · Q02 Improve Performance")
        self.show_page("Dashboard")

    def allowed(self, permission):
        permissions = {
            "admin": {"dashboard", "manage_patients", "manage_doctors", "manage_appointments",
                      "manage_billing", "import_csv", "view_reports", "view_performance"},
            "staff": {"dashboard", "manage_patients", "manage_appointments",
                      "manage_billing", "view_reports"}
        }
        return permission in permissions.get(self.role, set())

    def show_page(self, name):
        if name not in self.pages:
            page = self.build_page(name)
            if page is None:
                return
            self.pages[name] = page
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(self.pages[name])
        if hasattr(self, "page_heading"):
            self.page_heading.setText(name)
            self.page_breadcrumb.setText("Workspace  /  " + name)
        if hasattr(self, "page_search"):
            self.page_search.clear()
        for label, button in self.nav_buttons.items():
            button.setProperty("active", label == name)
            button.style().unpolish(button)
            button.style().polish(button)
        self.statusBar().showMessage(f"{name} · Signed in as {self.user.get('username', 'User')}")

    def build_page(self, name):
        if name == "Dashboard":
            return DashboardPage(self.user, self.show_page)
        if name == "Patients":
            service = PatientService()
            fields = [
                ("full_name", "Full name", "text", None),
                ("dob", "Date of birth", "date", None),
                ("gender", "Gender", "combo", [("Female", "Female"), ("Male", "Male"), ("Other", "Other")]),
                ("phone", "Phone (10 digits)", "text", None),
                ("address", "Address", "multiline", None),
                ("blood_group", "Blood group", "combo", [(x, x) for x in ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]]),
            ]
            return DataPage(name, "Maintain accurate patient information and reduce duplicate records.",
                [("patient_id", "ID"), ("full_name", "Patient"), ("dob", "Date of birth"),
                 ("gender", "Gender"), ("phone", "Phone"), ("blood_group", "Blood group"),
                 ("registration_date", "Registered")],
                service.get_all_patients, fields,
                lambda v: service.add_patient(v["full_name"], v["dob"], v["gender"], v["phone"],
                    v["address"], v["blood_group"], date.today().isoformat()),
                lambda r, v: service.update_patient(r["patient_id"], v["full_name"], v["dob"], v["gender"],
                    v["phone"], v["address"], v["blood_group"]),
                lambda r: service.delete_patient(r["patient_id"]), search_hint="Search name, phone, or patient ID…")
        if name == "Doctors":
            service = DoctorService()
            fields = [
                ("full_name", "Full name", "text", None),
                ("specialization", "Specialization", "text", None),
                ("phone", "Phone (10 digits)", "text", None),
                ("status", "Status", "combo", [("Active", "Active"), ("Inactive", "Inactive")]),
            ]
            return DataPage(name, "Manage the doctor directory and availability.",
                [("doctor_id", "ID"), ("full_name", "Doctor"), ("specialization", "Specialization"),
                 ("phone", "Phone"), ("status", "Status")],
                service.get_all_doctors, fields,
                lambda v: service.add_doctor(v["full_name"], v["specialization"], v["phone"], v["status"]),
                lambda r, v: service.update_doctor(r["doctor_id"], v["full_name"], v["specialization"], v["phone"], v["status"]),
                lambda r: service.delete_doctor(r["doctor_id"]), search_hint="Search doctor, specialty, phone…")
        if name == "Appointments":
            service = AppointmentService()
            patients = [as_dict(x) for x in PatientService().get_all_patients()]
            doctors = [as_dict(x) for x in DoctorService().get_all_doctors()]
            patient_options = [(f"{p.get('full_name')} · #{p.get('patient_id')}", p.get("patient_id")) for p in patients]
            doctor_options = [(f"{d.get('full_name')} · {d.get('specialization')}", d.get("doctor_id")) for d in doctors]
            fields = [
                ("patient_id", "Patient", "combo", patient_options),
                ("doctor_id", "Doctor", "combo", doctor_options),
                ("appointment_date", "Date", "date", None),
                ("appointment_time", "Time", "time", None),
                ("status", "Status", "combo", [(x, x) for x in ["Scheduled", "Checked In", "Completed", "Cancelled"]]),
            ]
            def add(v):
                if not v["patient_id"] or not v["doctor_id"]:
                    raise ValueError("Add a patient and a doctor before booking.")
                service.add_appointment(v["patient_id"], v["doctor_id"], v["appointment_date"],
                                       v["appointment_time"], v["status"])
            def edit(r, v):
                service.update_appointment(r["appointment_id"], v["patient_id"], v["doctor_id"],
                                           v["appointment_date"], v["appointment_time"], v["status"])
            return DataPage(name, "Schedule visits and track check-in to consultation wait times.",
                [("appointment_id", "ID"), ("patient_name", "Patient"), ("doctor_name", "Doctor"),
                 ("appointment_date", "Date"), ("appointment_time", "Time"), ("status", "Status"),
                 ("check_in_time", "Checked in"), ("consultation_start_time", "Consultation started")],
                service.get_all_appointments, fields, add, edit,
                lambda r: service.delete_appointment(r["appointment_id"]),
                search_hint="Search patient, doctor, or appointment ID…",
                extra_actions=[
                    ("Record check-in", lambda r: (
                        service.check_in_patient(r["appointment_id"])
                        and f"Check-in recorded for appointment #{r['appointment_id']}."
                    )),
                    ("Start consultation", lambda r: (
                        service.start_consultation(r["appointment_id"])
                        and f"Consultation start recorded for appointment #{r['appointment_id']}."
                    )),
                ])
        if name == "Billing":
            service = BillService()
            patients = [as_dict(x) for x in PatientService().get_all_patients()]
            patient_options = [(f"{p.get('full_name')} · #{p.get('patient_id')}", p.get("patient_id")) for p in patients]
            fields = [
                ("patient_id", "Patient", "combo", patient_options),
                ("bill_date", "Bill date", "date", None),
                ("description", "Description", "text", None),
                ("amount", "Amount", "amount", None),
            ]
            def add(v):
                if not v["patient_id"]:
                    raise ValueError("Add a patient before creating a bill.")
                service.add_bill(v["patient_id"], v["bill_date"], v["description"], v["amount"])
            def edit(r, v):
                service.update_bill(r["bill_id"], v["patient_id"], v["bill_date"], v["description"], v["amount"])
            return DataPage(name, "Create and maintain patient bills with clear totals.",
                [("bill_id", "Bill ID"), ("patient_name", "Patient"), ("bill_date", "Date"),
                 ("description", "Description"), ("amount", "Amount (INR)")],
                service.get_all_bills, fields, add, edit,
                lambda r: service.delete_bill(r["bill_id"]), search_hint="Search patient, date, or bill…")
        if name == "CSV Import":
            return CSVPage()
        if name == "Reports":
            return ReportsPage()
        if name == "Performance":
            return PerformancePage()
        if name == "TQM Analysis":
            return TQMPage()
        return None

    def navigate_from_search(self):
        query = self.page_search.text().strip().casefold()
        if not query:
            return
        available = list(self.nav_buttons.keys())
        exact = next((name for name in available if name.casefold() == query), None)
        matches = [name for name in available if query in name.casefold()]
        if exact:
            self.show_page(exact)
        elif len(matches) == 1:
            self.show_page(matches[0])
        elif matches:
            QMessageBox.information(
                self, "Choose a page",
                "More than one page matches. Enter a more specific name:\n\n"
                + "\n".join(matches)
            )
        else:
            QMessageBox.information(
                self, "Page not found",
                "No available page matches that search. Try Dashboard, Patients, "
                "Doctors, Appointments, Billing, CSV Import, Reports, Performance, "
                "or TQM Analysis."
            )

    def logout(self):
        answer = QMessageBox.question(self, "Sign out", "Return to the sign-in screen?")
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class CSVPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = CSVImportService()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 26, 30, 28)
        layout.setSpacing(16)
        layout.addWidget(make_label("CSV Patient Import", "PageTitle"))
        layout.addWidget(make_label("Import multiple patient records with validation and duplicate detection.", "PageSub"))
        panel = make_panel()
        box = QVBoxLayout(panel)
        box.setContentsMargins(22, 22, 22, 22)
        box.addWidget(make_label("Import patient spreadsheet", "PageTitle"))
        box.addWidget(make_label("Required columns: full_name, dob, gender, phone, address, blood_group", "PageSub"))
        self.path_label = make_label("No file selected", "PageSub")
        box.addWidget(self.path_label)
        choose = QPushButton("Choose CSV file")
        choose.clicked.connect(self.choose_file)
        box.addWidget(choose, 0, Qt.AlignmentFlag.AlignLeft)
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setMinimumHeight(230)
        self.result.setPlaceholderText("Import summary and rejected rows will appear here.")
        box.addWidget(self.result)
        layout.addWidget(panel)
        layout.addStretch()

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose patient CSV", "", "CSV files (*.csv)")
        if not path:
            return
        self.path_label.setText(path)
        if QMessageBox.question(self, "Confirm import", f"Import patient records from:\n{path}?") != QMessageBox.StandardButton.Yes:
            return
        try:
            result = self.service.import_patients(path)
            summary = (
                f"Import complete\n\nImported: {result.get('imported', 0)}\n"
                f"Duplicates skipped: {result.get('duplicates', 0)}\n"
                f"Rejected rows: {result.get('rejected', 0)}"
            )
            rejected = result.get("rejected_rows", [])
            if rejected:
                summary += "\n\nRejected rows:\n" + "\n".join(
                    f"Row {row.get('row')}: {row.get('reason')}" for row in rejected[:100]
                )
            self.result.setPlainText(summary)
        except Exception as error:
            QMessageBox.warning(self, "Import failed", str(error))


class ReportsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = ReportService()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 26, 30, 28)
        layout.setSpacing(16)
        layout.addWidget(make_label("Operational Reports", "PageTitle"))
        layout.addWidget(make_label("A concise view of patient, appointment, billing, and waiting-time performance.", "PageSub"))
        refresh = QPushButton("Refresh reports")
        refresh.clicked.connect(self.load)
        layout.addWidget(refresh, 0, Qt.AlignmentFlag.AlignLeft)
        self.content = QVBoxLayout()
        layout.addLayout(self.content)
        layout.addStretch()
        self.load()

    def load(self):
        while self.content.count():
            item = self.content.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        try:
            data = self.service.get_all_reports()
        except Exception as error:
            QMessageBox.warning(self, "Reports unavailable", str(error))
            return
        cards = QGridLayout()
        layout = QVBoxLayout()
        for title, value, hint, color in [
            ("Total patients", data["patients"]["total_patients"], "Registered patients", "#2563EB"),
            ("Total doctors", data["doctors"]["total_doctors"], "Doctor directory", "#7C3AED"),
            ("Appointments", data["appointments"]["total_appointments"], "All appointment records", "#0891B2"),
            ("Total revenue", f"₹ {data['billing']['total_revenue']:,.2f}", f"{data['billing']['total_bills']} bills", "#059669"),
            ("Average bill", f"₹ {data['billing']['average_bill']:,.2f}", "Per bill", "#D97706"),
            ("Completed visits", data["appointments"]["completed"], "Appointment status", "#0D9488"),
        ]:
            layout.addWidget(MetricCard(title, value, hint, color))
        panel = make_panel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(18, 18, 18, 18)
        panel_layout.addWidget(make_label("Appointment status summary", "PageTitle"))
        status = data["appointments"]
        for key in ["scheduled", "completed", "cancelled"]:
            panel_layout.addWidget(make_label(f"{key.title()}: {status.get(key, 0)}", "PageSub"))
        self.content.addLayout(layout)
        self.content.addWidget(panel)


class PerformancePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = PerformanceService()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 26, 30, 28)
        layout.setSpacing(16)
        layout.addWidget(make_label("Performance Lab", "PageTitle"))
        layout.addWidget(make_label("Measure the application’s database, patient-search, dashboard, and report paths for Q02.", "PageSub"))
        self.cards = QGridLayout()
        layout.addLayout(self.cards)
        run = QPushButton("Run performance checks")
        run.clicked.connect(self.run_checks)
        layout.addWidget(run, 0, Qt.AlignmentFlag.AlignLeft)
        self.details = QTextEdit()
        self.details.setReadOnly(True)
        self.details.setPlaceholderText("Results will appear here.")
        layout.addWidget(self.details, 1)

    def run_checks(self):
        try:
            results = self.service.measure_all()
            rows = []
            for key, value in results.items():
                label = key.replace("_", " ").title()
                rows.append(f"{label}: {value:.2f} ms")
            rows.append("")
            rows.append("Dashboard target: under 1,000 ms under normal local conditions.")
            rows.append("These measurements describe this run and machine; they are not universal benchmarks.")
            self.details.setPlainText("\n".join(rows))
        except Exception as error:
            QMessageBox.warning(self, "Performance check failed", str(error))


class TQMPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = TQMService()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 26, 30, 28)
        layout.setSpacing(16)
        layout.addWidget(make_label("TQM Analysis", "PageTitle"))
        layout.addWidget(make_label("Quality tools focused on Q02 — Improve Performance.", "PageSub"))
        self.tabs = QStackedWidget()
        tab_bar = QHBoxLayout()
        for label, index in [("SIPOC", 0), ("FMEA", 1), ("PDCA overview", 2)]:
            button = QPushButton(label)
            button.setObjectName("Secondary")
            button.clicked.connect(lambda _checked=False, i=index: self.tabs.setCurrentIndex(i))
            tab_bar.addWidget(button)
        layout.addLayout(tab_bar)
        self.tabs.addWidget(self.build_sipoc())
        self.tabs.addWidget(self.build_fmea())
        self.tabs.addWidget(self.build_pdca())
        layout.addWidget(self.tabs, 1)

    def build_sipoc(self):
        data = self.service.get_sipoc_data()
        page = QWidget()
        grid = QGridLayout(page)
        for i, key in enumerate(["suppliers", "inputs", "process", "outputs", "customers"]):
            panel = make_panel()
            box = QVBoxLayout(panel)
            box.setContentsMargins(16, 16, 16, 16)
            box.addWidget(make_label(key.title(), "PageTitle"))
            for entry in data[key]:
                box.addWidget(make_label("•  " + entry, "PageSub"))
            grid.addWidget(panel, 0, i)
        return page

    def build_fmea(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        rows = self.service.get_fmea_priority()
        table = QTableWidget(len(rows), 5)
        table.setHorizontalHeaderLabels(["Failure mode", "Effect", "RPN", "Risk", "Improvement"])
        table.verticalHeader().setVisible(False)
        for i, row in enumerate(rows):
            values = [row["failure_mode"], row["effect"], row["rpn"],
                      self.service.get_risk_level(row["rpn"]), row["improvement"]]
            for j, value in enumerate(values):
                table.setItem(i, j, QTableWidgetItem(str(value)))
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        return page

    def build_pdca(self):
        page = QWidget()
        grid = QGridLayout(page)
        steps = [
            ("PLAN", "Define the current waiting-time baseline, duplicate-record causes, and measurable targets.", "#2563EB"),
            ("DO", "Apply indexed search, duplicate validation, streamlined check-in, and bulk CSV import.", "#7C3AED"),
            ("CHECK", "Compare average waiting time, search latency, import duplicates, and report generation.", "#0891B2"),
            ("ACT", "Standardize successful changes and revise the improvement plan when results miss target.", "#059669"),
        ]
        for i, (title, body, color) in enumerate(steps):
            panel = make_panel()
            box = QVBoxLayout(panel)
            box.setContentsMargins(20, 20, 20, 20)
            box.addWidget(make_label(title, "PageTitle"))
            box.addWidget(make_label(body, "PageSub"))
            panel.setStyleSheet(f"QFrame#Panel{{border-top:4px solid {color};}}")
            grid.addWidget(panel, i // 2, i % 2)
        return page
