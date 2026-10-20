"""
Billing, Invoicing & Payment Settlement Desk for PySide6.
Matching Drittech Queue / City Care Hospital dashboard.

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from datetime import date
from typing import Optional, List, Dict, Any
from pathlib import Path
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDialog, QFormLayout, QDoubleSpinBox, QMessageBox,
    QFrame, QMenu, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor

from src.config import EXPORTS_DIR, STUDENT_NAME, STUDENT_ROLL, COURSE_CODE
from src.models.billing import get_invoices, create_invoice, update_payment_status
from src.models.patient import fast_search_patients
from qt_app.widgets.stat_cards import KpiMetricCard
from qt_app.widgets.badge import Badge


class PaymentSettlementDialog(QDialog):
    """Modal dialog for settling invoice payment with payment mode selection."""

    def __init__(self, invoice_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.invoice_data = invoice_data
        self.setWindowTitle(f"Settle Payment: {invoice_data.get('invoice_number')}")
        self.setFixedWidth(420)
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
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                background-color: #F8FAFC;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton#PrimaryBtn {
                background-color: #16A34A;
                color: white;
                font-weight: 700;
                padding: 10px 18px;
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
                padding: 10px 18px;
                border-radius: 6px;
                border: 1px solid #E2E8F0;
            }
        """)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        lbl_head = QLabel("💳 Confirm Payment Settlement")
        lbl_head.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        layout.addWidget(lbl_head)

        info_card = QFrame()
        info_card.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;")
        i_lay = QVBoxLayout(info_card)
        i_lay.setSpacing(4)

        i_lay.addWidget(QLabel(f"Invoice Number: <b>{self.invoice_data.get('invoice_number')}</b>"))
        i_lay.addWidget(QLabel(f"Patient Name: <b>{self.invoice_data.get('patient_name')}</b> ({self.invoice_data.get('uhid')})"))
        total = float(self.invoice_data.get('total_amount', 0.0))
        lbl_amt = QLabel(f"Total Amount Due: ₹{total:.2f}")
        lbl_amt.setStyleSheet("color: #16A34A; font-size: 15px; font-weight: 800; margin-top: 4px;")
        i_lay.addWidget(lbl_amt)
        layout.addWidget(info_card)

        lbl_m = QLabel("Select Settlement Mode:")
        layout.addWidget(lbl_m)

        self.cmb_mode = QComboBox()
        self.cmb_mode.addItems(["UPI / QR (Instant)", "Cash Counter", "Credit / Debit Card (POS)", "Health Insurance / TPA"])
        layout.addWidget(self.cmb_mode)

        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("CancelBtn")
        btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        btn_cancel.clicked.connect(self.reject)

        btn_confirm = QPushButton("Confirm Payment  ➔")
        btn_confirm.setObjectName("PrimaryBtn")
        btn_confirm.setCursor(QCursor(Qt.PointingHandCursor))
        btn_confirm.clicked.connect(self.accept)

        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_confirm)
        layout.addLayout(btn_row)

    def get_payment_mode(self) -> str:
        return self.cmb_mode.currentText()


class InvoiceReceiptDialog(QDialog):
    """Modal View for Complete Hospital Tax Invoice Receipt."""

    def __init__(self, invoice_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.invoice_data = invoice_data
        self.setWindowTitle(f"Tax Invoice Receipt: {invoice_data.get('invoice_number')}")
        self.setFixedWidth(480)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
        """)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(12)

        # Header with Hospital Branding
        top_row = QHBoxLayout()
        brand_col = QVBoxLayout()
        brand_col.setSpacing(2)

        lbl_hosp = QLabel("CITY CARE HOSPITAL")
        lbl_hosp.setStyleSheet("font-size: 16px; font-weight: 800; color: #0A1128;")
        lbl_sub = QLabel("Official Outpatient Tax Invoice & Receipt")
        lbl_sub.setStyleSheet("font-size: 11px; font-weight: 600; color: #0284C7;")
        brand_col.addWidget(lbl_hosp)
        brand_col.addWidget(lbl_sub)
        top_row.addLayout(brand_col)

        status = self.invoice_data.get("payment_status", "Pending")
        badge = Badge(status, badge_type="green" if status == "Paid" else "amber")
        top_row.addWidget(badge, alignment=Qt.AlignRight | Qt.AlignVCenter)
        layout.addLayout(top_row)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: #E2E8F0;")
        layout.addWidget(divider)

        # Invoice Metadata Row
        meta_row = QHBoxLayout()
        lbl_inv_no = QLabel(f"<b>Invoice #:</b> {self.invoice_data.get('invoice_number')}")
        lbl_date = QLabel(f"<b>Date:</b> {self.invoice_data.get('invoice_date')}")
        lbl_inv_no.setStyleSheet("font-size: 11px; color: #475569;")
        lbl_date.setStyleSheet("font-size: 11px; color: #475569;")
        meta_row.addWidget(lbl_inv_no)
        meta_row.addStretch()
        meta_row.addWidget(lbl_date)
        layout.addLayout(meta_row)

        lbl_pat = QLabel(f"<b>Patient:</b> {self.invoice_data.get('patient_name')} (UHID: {self.invoice_data.get('uhid')})")
        lbl_pat.setStyleSheet("font-size: 12px; color: #1E293B;")
        layout.addWidget(lbl_pat)

        # Itemized Charges Breakdown Box
        box = QFrame()
        box.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px;")
        b_lay = QFormLayout(box)
        b_lay.setSpacing(8)

        c_amt = float(self.invoice_data.get('consultation_amount', 0.0))
        m_amt = float(self.invoice_data.get('medicine_amount', 0.0))
        l_amt = float(self.invoice_data.get('lab_amount', 0.0))
        t_amt = float(self.invoice_data.get('tax_amount', 0.0))
        tot_amt = float(self.invoice_data.get('total_amount', 0.0))

        b_lay.addRow("OPD Doctor Consultation Fee:", QLabel(f"₹ {c_amt:.2f}"))
        b_lay.addRow("Pharmacy / Medicine Tariff:", QLabel(f"₹ {m_amt:.2f}"))
        b_lay.addRow("Laboratory & Diagnostic Charges:", QLabel(f"₹ {l_amt:.2f}"))
        b_lay.addRow("Healthcare GST (5% Combined):", QLabel(f"₹ {t_amt:.2f}"))

        layout.addWidget(box)

        # Total Highlight Box
        tot_card = QFrame()
        tot_card.setStyleSheet("background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px;")
        t_lay = QHBoxLayout(tot_card)
        t_lay.setContentsMargins(14, 10, 14, 10)

        lbl_t_text = QLabel("TOTAL AMOUNT:")
        lbl_t_text.setStyleSheet("font-size: 13px; font-weight: 800; color: #16A34A;")
        t_lay.addWidget(lbl_t_text)

        lbl_t_val = QLabel(f"₹ {tot_amt:.2f}")
        lbl_t_val.setStyleSheet("font-size: 18px; font-weight: 800; color: #16A34A;")
        t_lay.addWidget(lbl_t_val, alignment=Qt.AlignRight)
        layout.addWidget(tot_card)

        # Footer Actions
        btn_row = QHBoxLayout()
        lbl_foot = QLabel(f"Payment Mode: {self.invoice_data.get('payment_mode', 'Pending')}")
        lbl_foot.setStyleSheet("color: #64748B; font-size: 11px; font-style: italic;")
        btn_row.addWidget(lbl_foot)

        btn_row.addStretch()

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
        btn_row.addWidget(btn_close)

        layout.addLayout(btn_row)


class CreateInvoiceDialog(QDialog):
    """Modal dialog for itemized patient billing with automatic 5% GST computation."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generate New Patient Bill")
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
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        lbl_head = QLabel("🧾 Generate Itemized Patient Invoice")
        lbl_head.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        layout.addWidget(lbl_head)

        form = QFormLayout()
        form.setSpacing(10)

        # Patient picker
        self.txt_patient_search = QLineEdit()
        self.txt_patient_search.setPlaceholderText("Search patient name, UHID, or phone...")
        self.txt_patient_search.textChanged.connect(self._search_patients)

        self.cmb_patient = QComboBox()

        # Fee inputs
        self.spn_consult = QDoubleSpinBox()
        self.spn_consult.setRange(0, 100000)
        self.spn_consult.setValue(800.0)
        self.spn_consult.setPrefix("₹ ")
        self.spn_consult.valueChanged.connect(self._recalc_total)

        self.spn_medicine = QDoubleSpinBox()
        self.spn_medicine.setRange(0, 100000)
        self.spn_medicine.setValue(0.0)
        self.spn_medicine.setPrefix("₹ ")
        self.spn_medicine.valueChanged.connect(self._recalc_total)

        self.spn_lab = QDoubleSpinBox()
        self.spn_lab.setRange(0, 100000)
        self.spn_lab.setValue(0.0)
        self.spn_lab.setPrefix("₹ ")
        self.spn_lab.valueChanged.connect(self._recalc_total)

        # Payment options
        self.cmb_mode = QComboBox()
        self.cmb_mode.addItems(["UPI / QR (Instant)", "Cash Counter", "Credit / Debit Card (POS)", "Health Insurance / TPA"])

        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["Paid", "Pending"])

        # Calculated total label
        self.lbl_summary = QLabel("Subtotal: ₹800.00 | GST (5%): ₹40.00 | Total: ₹840.00")
        self.lbl_summary.setStyleSheet("background-color: #F0FDF4; color: #16A34A; font-weight: 700; padding: 8px; border-radius: 6px;")

        form.addRow("Search Patient:", self.txt_patient_search)
        form.addRow("Select Patient *:", self.cmb_patient)
        form.addRow("Consultation Fee (₹):", self.spn_consult)
        form.addRow("Pharmacy Charges (₹):", self.spn_medicine)
        form.addRow("Laboratory Tests (₹):", self.spn_lab)
        form.addRow("Payment Mode:", self.cmb_mode)
        form.addRow("Payment Status:", self.cmb_status)
        form.addRow("Calculated Total:", self.lbl_summary)

        layout.addLayout(form)

        # Buttons
        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("CancelBtn")
        btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Issue Invoice")
        btn_save.setObjectName("PrimaryBtn")
        btn_save.setCursor(QCursor(Qt.PointingHandCursor))
        btn_save.clicked.connect(self._validate_and_accept)

        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

        self._search_patients()
        self._recalc_total()

    def _search_patients(self):
        query = self.txt_patient_search.text().strip()
        patients, _ = fast_search_patients(query, limit=20)
        self.cmb_patient.clear()
        for p in patients:
            self.cmb_patient.addItem(
                f"{p['full_name']} | UHID: {p['uhid']} | 📞 {p['phone']}",
                userData=p["id"]
            )

    def _recalc_total(self):
        subtotal = self.spn_consult.value() + self.spn_medicine.value() + self.spn_lab.value()
        gst = round(subtotal * 0.05, 2)
        total = round(subtotal + gst, 2)
        self.lbl_summary.setText(f"Subtotal: ₹{subtotal:.2f} | GST (5%): ₹{gst:.2f} | Total: ₹{total:.2f}")

    def _validate_and_accept(self):
        if self.cmb_patient.currentIndex() < 0 or not self.cmb_patient.currentData():
            QMessageBox.warning(self, "Validation Error", "Please select a registered patient.")
            return
        self.accept()

    def get_data(self) -> Dict[str, Any]:
        return {
            "patient_id": self.cmb_patient.currentData(),
            "consultation_amount": self.spn_consult.value(),
            "medicine_amount": self.spn_medicine.value(),
            "lab_amount": self.spn_lab.value(),
            "payment_mode": self.cmb_mode.currentText(),
            "payment_status": self.cmb_status.currentText()
        }


class BillingView(QWidget):
    """
    Hospital Billing, Invoicing & Payment Settlement Desk.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.invoices_data: List[Dict[str, Any]] = []
        self._build_ui()
        self.load_invoices()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # 0. KPI Metrics Strip
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(14)

        self.kpi_settled = KpiMetricCard("Settled Revenue", "₹0.00", "Collected Hospital Funds", "💰", "#84CC16")
        self.kpi_pending = KpiMetricCard("Pending Invoices", "₹0.00", "Awaiting Patient Settlement", "⏳", "#F97316")
        self.kpi_count = KpiMetricCard("Invoices Issued", "0 Invoices", "Itemized Bills with 5% GST", "🧾", "#0EA5E9")
        self.kpi_rate = KpiMetricCard("Collection Rate", "0.0%", "Settlement Clearance Ratio", "📈", "#06B6D4")

        kpi_row.addWidget(self.kpi_settled)
        kpi_row.addWidget(self.kpi_pending)
        kpi_row.addWidget(self.kpi_count)
        kpi_row.addWidget(self.kpi_rate)
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

        lbl_filter = QLabel("Status:")
        lbl_filter.setStyleSheet("font-size: 12px; font-weight: 700; color: #475569;")
        toolbar.addWidget(lbl_filter)

        self.cmb_filter = QComboBox()
        self.cmb_filter.addItems(["All", "Paid", "Pending"])
        self.cmb_filter.setFixedWidth(120)
        self.cmb_filter.setStyleSheet("""
            QComboBox {
                padding: 6px 10px;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                background-color: #F8FAFC;
                font-size: 12px;
                font-weight: 600;
            }
        """)
        self.cmb_filter.currentTextChanged.connect(self._apply_filters)
        toolbar.addWidget(self.cmb_filter)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Search invoice no, patient name, UHID...")
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
        btn_refresh.clicked.connect(self.load_invoices)
        toolbar.addWidget(btn_refresh)

        # Revenue Summary Pill
        self.lbl_revenue_pill = QLabel("💰 Settled: ₹0.00 | Pending: ₹0.00")
        self.lbl_revenue_pill.setStyleSheet("""
            background-color: #E0F2FE;
            color: #0369A1;
            font-size: 11px;
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 6px;
        """)
        toolbar.addWidget(self.lbl_revenue_pill)

        toolbar.addStretch()

        btn_new_bill = QPushButton("🧾 Generate New Patient Bill")
        btn_new_bill.setCursor(QCursor(Qt.PointingHandCursor))
        btn_new_bill.setStyleSheet("""
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
        btn_new_bill.clicked.connect(self._on_new_bill)
        toolbar.addWidget(btn_new_bill)

        card_layout.addLayout(toolbar)

        # 1b. Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Invoice No", "Date", "Patient Name (UHID)", "Doctor", "Consultation", "Med/Lab", "GST (5%)", "Total Amount", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)
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
        self.table.doubleClicked.connect(self._view_receipt)
        card_layout.addWidget(self.table)

        # 1c. Bottom Actions Strip
        bottom_bar = QHBoxLayout()
        bottom_bar.setSpacing(10)

        lbl_hint = QLabel("💡 Tip: Double-click any row to view itemized receipt. Right-click to settle or export.")
        lbl_hint.setStyleSheet("color: #94A3B8; font-size: 11px; font-style: italic;")
        bottom_bar.addWidget(lbl_hint)

        bottom_bar.addStretch()

        btn_receipt = QPushButton("🧾 View Tax Receipt")
        btn_receipt.setCursor(QCursor(Qt.PointingHandCursor))
        btn_receipt.setStyleSheet("""
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
        btn_receipt.clicked.connect(self._view_receipt)
        bottom_bar.addWidget(btn_receipt)

        btn_settle = QPushButton("💳 Settle Payment")
        btn_settle.setCursor(QCursor(Qt.PointingHandCursor))
        btn_settle.setStyleSheet("""
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
        btn_settle.clicked.connect(self._on_settle_invoice)
        bottom_bar.addWidget(btn_settle)

        btn_export = QPushButton("📥 Export CSV")
        btn_export.setCursor(QCursor(Qt.PointingHandCursor))
        btn_export.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9;
                color: #334155;
                border: 1px solid #E2E8F0;
                font-weight: 600;
                font-size: 11px;
                padding: 6px 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
        """)
        btn_export.clicked.connect(self._export_csv)
        bottom_bar.addWidget(btn_export)

        card_layout.addLayout(bottom_bar)
        main_layout.addWidget(card)

    def load_invoices(self):
        """Fetch invoices from SQLite database."""
        try:
            self.invoices_data = get_invoices()
            self._apply_filters()
            self._update_kpi_cards()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load billing invoices: {e}")

    def _update_kpi_cards(self):
        total_invoices = len(self.invoices_data)
        settled_rev = sum(float(b.get("total_amount", 0.0)) for b in self.invoices_data if b.get("payment_status") == "Paid")
        pending_rev = sum(float(b.get("total_amount", 0.0)) for b in self.invoices_data if b.get("payment_status") == "Pending")
        total_rev = settled_rev + pending_rev
        rate = (settled_rev / total_rev * 100.0) if total_rev > 0 else 0.0

        self.kpi_settled.update_value(f"₹{settled_rev:,.2f}", "Collected Hospital Revenue")
        self.kpi_pending.update_value(f"₹{pending_rev:,.2f}", "Pending Collection")
        self.kpi_count.update_value(f"{total_invoices} Bills", "Itemized Invoices with GST")
        self.kpi_rate.update_value(f"{rate:.1f}%", "Settlement Clearance Rate")

        self.lbl_revenue_pill.setText(f"💰 Settled: ₹{settled_rev:,.2f} | Pending: ₹{pending_rev:,.2f}")

    def _apply_filters(self):
        status_filter = self.cmb_filter.currentText()
        search_query = self.txt_search.text().strip().lower()

        filtered = []
        for inv in self.invoices_data:
            if status_filter != "All" and inv.get("payment_status") != status_filter:
                continue
            if search_query:
                num_match = search_query in str(inv.get("invoice_number", "")).lower()
                p_match = search_query in str(inv.get("patient_name", "")).lower()
                uhid_match = search_query in str(inv.get("uhid", "")).lower()
                if not (num_match or p_match or uhid_match):
                    continue
            filtered.append(inv)

        self.table.setRowCount(len(filtered))
        for row_idx, inv in enumerate(filtered):
            # Invoice No
            item_no = QTableWidgetItem(str(inv.get("invoice_number", "")))
            item_no.setFont(QFont("Segoe UI", 9, QFont.Bold))
            item_no.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 0, item_no)

            # Date
            item_date = QTableWidgetItem(str(inv.get("invoice_date", "")))
            item_date.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 1, item_date)

            # Patient Name
            p_text = f"{inv.get('patient_name', '')} ({inv.get('uhid', '')})"
            item_p = QTableWidgetItem(p_text)
            self.table.setItem(row_idx, 2, item_p)

            # Doctor
            item_doc = QTableWidgetItem(str(inv.get("doctor_name", "OPD Duty")))
            self.table.setItem(row_idx, 3, item_doc)

            # Consultation
            c_val = float(inv.get("consultation_amount", 0.0))
            item_c = QTableWidgetItem(f"₹ {c_val:.2f}")
            item_c.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 4, item_c)

            # Med/Lab
            ml_val = float(inv.get("medicine_amount", 0.0)) + float(inv.get("lab_amount", 0.0))
            item_ml = QTableWidgetItem(f"₹ {ml_val:.2f}")
            item_ml.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 5, item_ml)

            # Tax Amount
            tax_val = float(inv.get("tax_amount", 0.0))
            item_tax = QTableWidgetItem(f"₹ {tax_val:.2f}")
            item_tax.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 6, item_tax)

            # Total
            tot_val = float(inv.get("total_amount", 0.0))
            item_tot = QTableWidgetItem(f"₹ {tot_val:.2f}")
            item_tot.setFont(QFont("Segoe UI", 9, QFont.Bold))
            item_tot.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 7, item_tot)

            # Status Pill Badge
            status = str(inv.get("payment_status", "Pending"))
            badge_type = "green" if status == "Paid" else "amber"
            badge = Badge(status, badge_type=badge_type)
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(4, 2, 4, 2)
            cell_layout.setAlignment(Qt.AlignCenter)
            cell_layout.addWidget(badge)
            self.table.setCellWidget(row_idx, 8, cell_widget)

    def _get_selected_invoice(self) -> Optional[Dict[str, Any]]:
        row = self.table.currentRow()
        if row < 0:
            return None
        inv_no_item = self.table.item(row, 0)
        if not inv_no_item:
            return None
        inv_no = inv_no_item.text()
        for b in self.invoices_data:
            if b.get("invoice_number") == inv_no:
                return b
        return None

    def _on_new_bill(self):
        dlg = CreateInvoiceDialog(parent=self)
        if dlg.exec():
            data = dlg.get_data()
            try:
                bill_id, inv_num, total = create_invoice(
                    patient_id=data["patient_id"],
                    appointment_id=None,
                    consultation_amount=data["consultation_amount"],
                    medicine_amount=data["medicine_amount"],
                    lab_amount=data["lab_amount"],
                    payment_mode=data["payment_mode"],
                    payment_status=data["payment_status"]
                )
                self.load_invoices()
                QMessageBox.information(
                    self, "Invoice Created",
                    f"Invoice {inv_num} generated successfully!\nTotal Billed: ₹{total:.2f}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to generate invoice: {e}")

    def _on_settle_invoice(self):
        inv = self._get_selected_invoice()
        if not inv:
            QMessageBox.information(self, "Select Row", "Please select an invoice to settle.")
            return

        if inv.get("payment_status") == "Paid":
            QMessageBox.information(self, "Already Settled", f"Invoice {inv['invoice_number']} is already paid.")
            return

        dlg = PaymentSettlementDialog(invoice_data=inv, parent=self)
        if dlg.exec():
            mode = dlg.get_payment_mode()
            try:
                update_payment_status(inv["id"], "Paid", payment_mode=mode)
                self.load_invoices()
                QMessageBox.information(self, "Settled", f"Invoice {inv['invoice_number']} settled via {mode}.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to settle invoice: {e}")

    def _view_receipt(self):
        inv = self._get_selected_invoice()
        if not inv:
            QMessageBox.information(self, "Select Row", "Please select an invoice to view receipt.")
            return

        dlg = InvoiceReceiptDialog(invoice_data=inv, parent=self)
        dlg.exec()

    def _export_csv(self):
        if not self.invoices_data:
            QMessageBox.information(self, "Empty", "No invoice data available to export.")
            return

        out_path = EXPORTS_DIR / f"Billing_Invoices_{date.today().strftime('%Y%m%d')}.csv"
        df = pd.DataFrame(self.invoices_data)
        df.to_csv(out_path, index=False)
        QMessageBox.information(self, "Exported", f"Exported {len(df)} invoices to:\n{out_path}")

    def _show_context_menu(self, pos):
        inv = self._get_selected_invoice()
        if not inv:
            return

        menu = QMenu(self)
        act_receipt = menu.addAction("🧾 View Full Tax Receipt")
        if inv.get("payment_status") != "Paid":
            act_settle = menu.addAction("💳 Settle Payment (Choose Mode)")
        else:
            act_settle = None
        menu.addSeparator()
        act_csv = menu.addAction("📥 Export Invoices to CSV")

        chosen = menu.exec(self.table.viewport().mapToGlobal(pos))
        if chosen == act_receipt:
            self._view_receipt()
        elif act_settle and chosen == act_settle:
            self._on_settle_invoice()
        elif chosen == act_csv:
            self._export_csv()
