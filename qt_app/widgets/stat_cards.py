"""
Live Overview 4-Metric Strip Widget for PySide6.
Matching Drittech Queue / City Care Hospital dashboard.

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from datetime import datetime
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QWidget
)
from PySide6.QtCore import Qt
from qt_app.widgets.badge import CircleIconBadge


class MetricItem(QWidget):
    """Single metric item with circular icon badge, value, and label."""

    def __init__(self, icon: str, val: str, label: str,
                 icon_bg: str = "#E0F2FE", icon_fg: str = "#0284C7", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Circular Badge
        badge = CircleIconBadge(icon, bg_color=icon_bg, fg_color=icon_fg, size=44, font_size=18)
        layout.addWidget(badge, alignment=Qt.AlignCenter)

        # Value
        self.lbl_val = QLabel(val)
        self.lbl_val.setStyleSheet("color: #0F172A; font-size: 22px; font-weight: 800;")
        self.lbl_val.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_val)

        # Subtitle
        lbl_sub = QLabel(label)
        lbl_sub.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 500;")
        lbl_sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_sub)

    def setValue(self, val: str):
        self.lbl_val.setText(val)


class LiveOverviewCard(QFrame):
    """White card containing the 4 circular stat overview metrics."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.setStyleSheet("""
            QFrame#Card {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(12)

        # Header
        top_row = QHBoxLayout()
        lbl_title = QLabel("Live Overview")
        lbl_title.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;")
        top_row.addWidget(lbl_title)

        self.lbl_timestamp = QLabel(f"Last updated: {datetime.now().strftime('%I:%M:%S %p')}")
        self.lbl_timestamp.setStyleSheet("color: #94A3B8; font-size: 11px;")
        top_row.addWidget(self.lbl_timestamp, alignment=Qt.AlignRight)
        main_layout.addLayout(top_row)

        # Metrics Horizontal Row
        metrics_row = QHBoxLayout()
        metrics_row.setContentsMargins(0, 4, 0, 0)
        metrics_row.setSpacing(16)

        self.m_patients = MetricItem("👥", "142", "Total Patients\nToday", "#E0F2FE", "#0284C7")
        self.m_served = MetricItem("👤", "42", "Served\nToday", "#DCFCE7", "#16A34A")
        self.m_waiting = MetricItem("⏳", "68", "Waiting\nNow", "#FEF3C7", "#D97706")
        self.m_wait_time = MetricItem("🕒", "28 min", "Avg. Wait Time\nToday", "#EDE9FE", "#8B5CF6")

        metrics_row.addWidget(self.m_patients)
        metrics_row.addWidget(self.m_served)
        metrics_row.addWidget(self.m_waiting)
        metrics_row.addWidget(self.m_wait_time)

        main_layout.addLayout(metrics_row)

    def update_metrics(self, total: int = 142, served: int = 42, waiting: int = 68, avg_wait: str = "28 min"):
        self.m_patients.setValue(str(total))
        self.m_served.setValue(str(served))
        self.m_waiting.setValue(str(waiting))
        self.m_wait_time.setValue(avg_wait)
        self.lbl_timestamp.setText(f"Last updated: {datetime.now().strftime('%I:%M:%S %p')}")


class KpiMetricCard(QFrame):
    """
    Modern SaaS Metric Card with Left Accent Stripe, Icon Badge, and Dynamic Value.
    Used across Doctors, OPD Queue, Billing, TQM, and Analytics views.
    """

    def __init__(self, title: str, value: str, sub: str, icon: str,
                 accent_color: str = "#0EA5E9", parent=None):
        super().__init__(parent)
        self.accent_color = accent_color
        self.setObjectName("KpiCard")
        self.setStyleSheet(f"""
            QFrame#KpiCard {{
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-left: 4px solid {accent_color};
                border-radius: 12px;
            }}
        """)
        self._build_ui(title, value, sub, icon)

    def _build_ui(self, title: str, value: str, sub: str, icon: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)

        # Left text column
        text_col = QVBoxLayout()
        text_col.setSpacing(4)

        self.lbl_title = QLabel(title.upper())
        self.lbl_title.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        text_col.addWidget(self.lbl_title)

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet("color: #0F172A; font-size: 22px; font-weight: 800;")
        text_col.addWidget(self.lbl_value)

        self.lbl_sub = QLabel(sub)
        self.lbl_sub.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 500;")
        text_col.addWidget(self.lbl_sub)

        layout.addLayout(text_col, stretch=1)

        # Right icon badge
        badge = CircleIconBadge(icon, bg_color=self.accent_color + "22", fg_color=self.accent_color, size=42, font_size=16)
        layout.addWidget(badge, alignment=Qt.AlignRight | Qt.AlignVCenter)

    def update_value(self, val: str, sub: str = None):
        self.lbl_value.setText(val)
        if sub is not None:
            self.lbl_sub.setText(sub)

