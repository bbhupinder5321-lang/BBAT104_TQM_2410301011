"""
Modern Embedded Charts for PySide6:
1. Average Wait Time Area Spline Chart
2. Department Queue Donut Chart

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

import logging
import numpy as np
import matplotlib
matplotlib.use("QtAgg")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QWidget, QGridLayout
)
from PySide6.QtCore import Qt


class WaitTimeAreaChartCard(QFrame):
    """
    Middle-Right Card: "Average Wait Time" Area Spline Chart
    Matches Drittech Queue screenshot with smooth cyan curve and gradient area fill.
    """

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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 12)
        layout.setSpacing(6)

        # Header Row
        head_row = QHBoxLayout()
        lbl_title = QLabel("Average Wait Time")
        lbl_title.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;")
        head_row.addWidget(lbl_title)

        self.cmb_filter = QComboBox()
        self.cmb_filter.addItems(["Today", "This Week", "This Month"])
        self.cmb_filter.setStyleSheet("""
            QComboBox {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 600;
                color: #475569;
            }
        """)
        head_row.addWidget(self.cmb_filter, alignment=Qt.AlignRight)
        layout.addLayout(head_row)

        # Embedded Matplotlib Canvas
        self.fig, self.ax = plt.subplots(figsize=(6.2, 2.5), dpi=95)
        self.fig.patch.set_facecolor("#FFFFFF")
        self.ax.set_facecolor("#FFFFFF")

        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setStyleSheet("background: transparent;")
        layout.addWidget(self.canvas)

        self._draw_spline_chart()

    def _draw_spline_chart(self):
        self.ax.clear()

        # Data points matching photo: 8 AM (15m), 9 AM (20m), 10 AM (32m), 11 AM (45m peak), 12 PM (38m), 1 PM (22m), 2 PM (15m)
        hours = np.array([8, 9, 10, 11, 12, 13, 14])
        wait_times = np.array([14, 21, 33, 46, 36, 23, 15])
        hour_labels = ["08 AM", "09 AM", "10 AM", "11 AM", "12 PM", "01 PM", "02 PM"]

        # Smooth spline interpolation (120 points) using pure numpy polynomial fit
        x_smooth = np.linspace(hours.min(), hours.max(), 120)
        poly = np.poly1d(np.polyfit(hours, wait_times, 4))
        y_smooth = np.clip(poly(x_smooth), 0, 60)

        # Plot Cyan Area Fill
        self.ax.fill_between(x_smooth, y_smooth, color="#00BCD4", alpha=0.15)
        # Plot Spline Line
        self.ax.plot(x_smooth, y_smooth, color="#00BCD4", linewidth=2.4)
        # Plot Scatter Markers
        self.ax.scatter(hours, wait_times, color="#00BCD4", s=32, zorder=5, edgecolors="#FFFFFF", linewidth=1.8)

        # Styling & Axis
        self.ax.set_xticks(hours)
        self.ax.set_xticklabels(hour_labels, fontsize=8, color="#94A3B8")
        self.ax.set_yticks([0, 15, 30, 45, 60])
        self.ax.set_yticklabels(["0", "15", "30", "45", "60"], fontsize=8, color="#94A3B8")
        self.ax.set_ylabel("Minutes", fontsize=8, color="#94A3B8", labelpad=2)
        self.ax.set_ylim(0, 65)

        self.ax.grid(axis="y", color="#F1F5F9", linestyle="-", linewidth=1, zorder=1)
        self.ax.grid(visible=False, axis="x")

        for s in ["top", "right", "left", "bottom"]:
            self.ax.spines[s].set_visible(False)

        self.fig.tight_layout(pad=0.4)
        self.canvas.draw()


class DepartmentQueueDonutCard(QFrame):
    """
    Bottom-Middle Card: "Department Queue" Donut Chart with Legend.
    Matches Drittech Queue screenshot with donut pie chart and colored breakdown.
    """

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
        main_layout.setSpacing(10)

        # Title
        lbl_title = QLabel("Department Queue")
        lbl_title.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;")
        main_layout.addWidget(lbl_title)

        body_layout = QHBoxLayout()
        body_layout.setSpacing(10)

        # 1. Left Donut Chart
        self.fig, self.ax = plt.subplots(figsize=(2.6, 2.6), dpi=95)
        self.fig.patch.set_facecolor("#FFFFFF")
        self.ax.set_facecolor("#FFFFFF")

        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setFixedSize(190, 190)
        body_layout.addWidget(self.canvas)

        # 2. Right Legend Grid
        legend_widget = QWidget()
        leg_layout = QVBoxLayout(legend_widget)
        leg_layout.setContentsMargins(0, 4, 0, 4)
        leg_layout.setSpacing(6)
        leg_layout.setAlignment(Qt.AlignVCenter)

        departments_data = [
            ("General OPD", "68 (48%)", "#00BCD4"),
            ("Cardiology", "22 (15%)", "#0284C7"),
            ("Orthopedics", "18 (13%)", "#38BDF8"),
            ("Dermatology", "12 (8%)", "#F59E0B"),
            ("Neurology", "10 (7%)", "#8B5CF6"),
            ("Others", "12 (8%)", "#94A3B8"),
        ]

        for dept, count_pct, color in departments_data:
            row = QHBoxLayout()
            row.setSpacing(8)

            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 13px; background: transparent;")
            row.addWidget(dot)

            lbl_dept = QLabel(dept)
            lbl_dept.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 500;")
            row.addWidget(lbl_dept)

            lbl_val = QLabel(count_pct)
            lbl_val.setStyleSheet("color: #0F172A; font-size: 12px; font-weight: 700;")
            lbl_val.setAlignment(Qt.AlignRight)
            row.addWidget(lbl_val)

            leg_layout.addLayout(row)

        body_layout.addWidget(legend_widget)
        main_layout.addLayout(body_layout)

        self._draw_donut(departments_data)

    def _draw_donut(self, data):
        self.ax.clear()

        counts = [68, 22, 18, 12, 10, 12]
        colors = [item[2] for item in data]

        wedges, _ = self.ax.pie(
            counts, colors=colors, startangle=90, counterclock=False,
            wedgeprops=dict(width=0.38, edgecolor="white", linewidth=2.0)
        )

        # Center Label: 142 Total
        self.ax.text(0, 0.08, "142", ha="center", va="center", fontsize=15, fontweight="800", color="#0F172A")
        self.ax.text(0, -0.15, "Total", ha="center", va="center", fontsize=9, color="#94A3B8", fontweight="600")

        self.ax.axis("equal")
        self.fig.tight_layout(pad=0.2)
        self.canvas.draw()
