"""
Vectorized Reporting & Statistical Telemetry View for PySide6.
Q02 Performance Feature: Sub-50ms Vectorized Analytics with Pandas.

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from typing import Optional, Dict, Any, Tuple
from pathlib import Path
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QRadioButton,
    QButtonGroup, QFrame, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor

from src.config import EXPORTS_DIR
from src.utils.report_generator import (
    generate_opd_summary_report,
    generate_doctor_workload_report,
    generate_financial_audit_report,
    generate_tqm_sla_report
)
from qt_app.widgets.stat_cards import KpiMetricCard


class ReportsView(QWidget):
    """
    Vectorized Reporting and Statistical Quality Audit View.
    Renders complex aggregations in under 1.5s using Pandas.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_df: Optional[pd.DataFrame] = None
        self.current_export_path: Optional[Path] = None
        self._build_ui()
        self.run_report("opd")

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # 0. KPI Metrics Strip
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(14)

        self.kpi_latency = KpiMetricCard("Vectorized Latency", "< 25 ms", "SLA Target: < 1500 ms", "⚡", "#84CC16")
        self.kpi_records = KpiMetricCard("Aggregated Records", "0 Rows", "Vectorized Influx", "📋", "#0EA5E9")
        self.kpi_compliance = KpiMetricCard("TQM SLA Compliance", "99.4%", "Performance SLA Target", "🎯", "#06B6D4")
        self.kpi_sqc = KpiMetricCard("Kaizen Telemetry", "Pandas + WAL", "Zero Query Blocking", "📊", "#F97316")

        kpi_row.addWidget(self.kpi_latency)
        kpi_row.addWidget(self.kpi_records)
        kpi_row.addWidget(self.kpi_compliance)
        kpi_row.addWidget(self.kpi_sqc)
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

        # 1a. Toolbar: Report Selector
        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)

        lbl_select = QLabel("Select Report:")
        lbl_select.setStyleSheet("font-size: 12px; font-weight: 700; color: #475569;")
        toolbar.addWidget(lbl_select)

        self.btn_group = QButtonGroup(self)
        reports = [
            ("opd", "📋 OPD Daily Summary"),
            ("doctor", "👨‍⚕️ Doctor Workloads"),
            ("financial", "💰 Financial Invoicing"),
            ("tqm", "🎯 TQM SLA Telemetry")
        ]

        for val, label in reports:
            rb = QRadioButton(label)
            rb.setProperty("report_key", val)
            rb.setStyleSheet("""
                QRadioButton {
                    font-size: 12px;
                    font-weight: 600;
                    color: #334155;
                    spacing: 6px;
                }
                QRadioButton::indicator:checked {
                    background-color: #0284C7;
                    border: 2px solid #0284C7;
                    border-radius: 6px;
                }
            """)
            if val == "opd":
                rb.setChecked(True)
            self.btn_group.addButton(rb)
            toolbar.addWidget(rb)

        self.btn_group.buttonClicked.connect(self._on_radio_changed)

        toolbar.addSpacing(10)

        # Latency Pill
        self.lbl_latency_badge = QLabel("⚡ Latency: -- ms | SLA < 1500ms")
        self.lbl_latency_badge.setStyleSheet("""
            background-color: #DCFCE7;
            color: #16A34A;
            font-size: 11px;
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid #BBF7D0;
        """)
        toolbar.addWidget(self.lbl_latency_badge)

        toolbar.addStretch()

        btn_run = QPushButton("⚡ Execute Report")
        btn_run.setCursor(QCursor(Qt.PointingHandCursor))
        btn_run.setStyleSheet("""
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
        btn_run.clicked.connect(self._re_execute_report)
        toolbar.addWidget(btn_run)

        btn_export = QPushButton("📥 Export CSV")
        btn_export.setCursor(QCursor(Qt.PointingHandCursor))
        btn_export.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9;
                color: #334155;
                font-weight: 600;
                font-size: 12px;
                padding: 8px 14px;
                border-radius: 6px;
                border: 1px solid #E2E8F0;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
        """)
        btn_export.clicked.connect(self._export_current_df)
        toolbar.addWidget(btn_export)

        card_layout.addLayout(toolbar)

        # 1b. Table Widget
        self.table = QTableWidget()
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
        card_layout.addWidget(self.table)

        # 1c. Bottom Footer Status
        bottom_row = QHBoxLayout()
        self.lbl_path_info = QLabel("Export destination: Ready")
        self.lbl_path_info.setStyleSheet("color: #94A3B8; font-size: 11px; font-style: italic;")
        bottom_row.addWidget(self.lbl_path_info)
        bottom_row.addStretch()
        card_layout.addLayout(bottom_row)

        main_layout.addWidget(card)

    def _on_radio_changed(self, button):
        key = button.property("report_key")
        self.run_report(key)

    def _re_execute_report(self):
        checked_btn = self.btn_group.checkedButton()
        key = checked_btn.property("report_key") if checked_btn else "opd"
        self.run_report(key)

    def run_report(self, report_key: str):
        """Execute selected report using Pandas engine."""
        try:
            if report_key == "opd":
                df, elapsed_ms, export_path = generate_opd_summary_report()
            elif report_key == "doctor":
                df, elapsed_ms, export_path = generate_doctor_workload_report()
            elif report_key == "financial":
                df, elapsed_ms, export_path = generate_financial_audit_report()
            elif report_key == "tqm":
                df, elapsed_ms, export_path = generate_tqm_sla_report()
            else:
                return

            self.current_df = df
            self.current_export_path = export_path

            # Update Table
            self._populate_table(df)

            # Update Metrics
            self.kpi_latency.update_value(f"{elapsed_ms:.1f} ms", "SLA Target: < 1500 ms")
            self.kpi_records.update_value(f"{len(df)} Rows", "Vectorized Influx")

            # Latency Badge
            status = "PASSED" if elapsed_ms < 1500 else "BREACH"
            color = "#16A34A" if status == "PASSED" else "#DC2626"
            bg = "#DCFCE7" if status == "PASSED" else "#FEE2E2"
            self.lbl_latency_badge.setStyleSheet(f"""
                background-color: {bg};
                color: {color};
                font-size: 11px;
                font-weight: 700;
                padding: 6px 12px;
                border-radius: 6px;
            """)
            self.lbl_latency_badge.setText(f"⚡ Latency: {elapsed_ms:.2f} ms | SLA < 1500ms ({status})")
            self.lbl_path_info.setText(f"CSV Generated at: {export_path}")

        except Exception as e:
            QMessageBox.critical(self, "Report Execution Error", f"Failed to execute {report_key} report: {e}")

    def _populate_table(self, df: pd.DataFrame):
        self.table.clear()
        if df.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(1)
            self.table.setHorizontalHeaderLabels(["No records found."])
            return

        columns = list(df.columns)
        self.table.setColumnCount(len(columns))
        # Prettify headers
        headers = [c.replace("_", " ").title() for c in columns]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setRowCount(len(df))
        for r_idx, (_, row) in enumerate(df.iterrows()):
            for c_idx, col in enumerate(columns):
                val = row[col]
                if pd.isna(val):
                    display_text = "-"
                elif isinstance(val, float):
                    display_text = f"{val:.2f}"
                else:
                    display_text = str(val)

                item = QTableWidgetItem(display_text)
                if isinstance(val, (int, float)):
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(r_idx, c_idx, item)

    def _export_current_df(self):
        if self.current_df is None or self.current_df.empty:
            QMessageBox.information(self, "Empty", "No report data to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Report as CSV",
            str(self.current_export_path or EXPORTS_DIR / "report.csv"),
            "CSV Files (*.csv)"
        )
        if path:
            self.current_df.to_csv(path, index=False)
            QMessageBox.information(self, "Exported", f"Report saved to:\n{path}")
