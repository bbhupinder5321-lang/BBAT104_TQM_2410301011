"""
Summary Spline Area Chart Widget for Patient Flow Trends.
Inspired by Reference Image (KRL Health Care aesthetic):
- Smooth curved spline line in deep royal navy (#0C2B59)
- Soft translucent gradient area fill below curve
- Circular dark navy badge floating at the peak with white label '82' and connecting pin
- Clean minimalist grid lines and borderless spines
"""

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.config import THEME


class PatientTrendChart(tk.Frame):
    """
    Embedded Spline Area Chart matching the KRL Health Care 'Summary' graph.
    Features the circular peak badge (82) with connecting pin.
    """

    def __init__(self, parent, bg_color: str = "#FFFFFF"):
        super().__init__(parent, bg=bg_color)
        self.bg_color = bg_color
        self._build_chart()

    def _build_chart(self):
        plt.style.use("default")
        # High DPI for crisp rendering
        self.fig, self.ax = plt.subplots(figsize=(6.4, 2.5), dpi=100)
        self.fig.patch.set_facecolor("white")
        self.ax.set_facecolor("white")

        # Days of the week data with peak at 82
        days_num = np.array([1, 2, 3, 4, 5, 6, 7])
        day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        values = np.array([28, 45, 82, 58, 64, 42, 30])  # Peak at 82 on Wednesday

        # Smooth spline interpolation
        x_smooth = np.linspace(days_num.min(), days_num.max(), 300)
        try:
            from scipy.interpolate import make_interp_spline
            spline = make_interp_spline(days_num, values, k=3)
            y_smooth = np.clip(spline(x_smooth), 0, None)
        except Exception:
            # Polyfit fallback
            z = np.polyfit(days_num, values, 4)
            p = np.poly1d(z)
            y_smooth = np.clip(p(x_smooth), 0, None)

        # Plot sleek royal navy curve
        line_color = "#0C2B59"
        self.ax.plot(x_smooth, y_smooth, color=line_color, linewidth=2.8, zorder=3)
        self.ax.fill_between(x_smooth, y_smooth, color="#1E5DB4", alpha=0.10, zorder=2)

        # Secondary subtle comparison line (e.g. previous week)
        y_prev = values * 0.72 + np.array([4, 6, -5, 8, 3, 2, 5])
        try:
            from scipy.interpolate import make_interp_spline
            spline_prev = make_interp_spline(days_num, y_prev, k=3)
            y_prev_smooth = np.clip(spline_prev(x_smooth), 0, None)
        except Exception:
            z_prev = np.polyfit(days_num, y_prev, 4)
            p_prev = np.poly1d(z_prev)
            y_prev_smooth = np.clip(p_prev(x_smooth), 0, None)

        self.ax.plot(x_smooth, y_prev_smooth, color="#CBD5E1", linewidth=1.8, linestyle="--", alpha=0.8, zorder=2)

        # Find exact peak coordinates
        peak_idx = np.argmax(y_smooth)
        px, py = x_smooth[peak_idx], y_smooth[peak_idx]

        # Draw connecting pin line from curve to circular badge
        badge_y = py + 12
        self.ax.plot([px, px], [py, badge_y - 3], color="#0C2B59", linewidth=1.5, linestyle=":", zorder=4)

        # Draw dark navy circular peak badge with text "82"
        self.ax.plot(px, py, "o", color="#0C2B59", markersize=6, markeredgecolor="white", markeredgewidth=2, zorder=5)
        self.ax.text(
            px, badge_y, "82",
            ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="white",
            bbox=dict(boxstyle="circle,pad=0.45", fc="#0C2B59", ec="#0C2B59", lw=1.5),
            zorder=6
        )

        # Minimalist X-axis styling
        self.ax.set_xticks(days_num)
        self.ax.set_xticklabels(day_labels, fontsize=8, color="#64748B", fontweight="semibold")
        self.ax.tick_params(axis="both", which="both", length=0, labelsize=8, colors="#64748B")
        self.ax.set_ylim(0, 110)

        # Horizontal light grid lines only
        self.ax.grid(axis="y", color="#F1F5F9", linestyle="-", linewidth=1)
        self.ax.grid(visible=False, axis="x")

        # Spines removal
        for spine in ["top", "right", "left", "bottom"]:
            self.ax.spines[spine].set_visible(False)

        self.fig.tight_layout(pad=0.8)

        # Canvas embedding
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
