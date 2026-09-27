"""
Summary Spline Area Chart Widget for Patient Flow Trends.
Directly crafted after Reference Image 3 (KRL Health Care aesthetic):
- Smooth Catmull-Rom cubic spline curve in deep royal navy (#0C2B59)
- Translucent light blue pillar highlighting the peak at May 9
- Soft translucent gradient area fill below curve
- Circular dark navy badge floating at the peak with white label '82' and connecting pin
- Y-axis markers (40, 60, 80, 100) and May 5 - May 13 date labels
- Clean minimalist grid lines and borderless spines
"""

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.config import THEME


def catmull_rom_spline(pts, n_points: int = 100):
    """Generates butter-smooth Catmull-Rom cubic spline interpolation in pure NumPy."""
    P = np.asarray(pts, dtype=float)
    # Natural boundary extrapolation for start and end
    p_start = P[0] - (P[1] - P[0])
    p_end = P[-1] + (P[-1] - P[-2])
    P_pad = np.vstack([p_start, P, p_end])

    x_all = []
    y_all = []

    for i in range(len(P) - 1):
        p0, p1, p2, p3 = P_pad[i], P_pad[i+1], P_pad[i+2], P_pad[i+3]
        u = np.linspace(0.0, 1.0, n_points, endpoint=(i == len(P) - 2))
        u2 = u * u
        u3 = u2 * u

        # Standard Catmull-Rom blending functions
        f0 = -0.5 * u3 + 1.0 * u2 - 0.5 * u
        f1 =  1.5 * u3 - 2.5 * u2 + 1.0
        f2 = -1.5 * u3 + 2.0 * u2 + 0.5 * u
        f3 =  0.5 * u3 - 0.5 * u2

        x_seg = f0 * p0[0] + f1 * p1[0] + f2 * p2[0] + f3 * p3[0]
        y_seg = f0 * p0[1] + f1 * p1[1] + f2 * p2[1] + f3 * p3[1]
        x_all.extend(x_seg)
        y_all.extend(y_seg)

    return np.array(x_all), np.array(y_all)


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
        # High DPI for crisp modern rendering
        self.fig, self.ax = plt.subplots(figsize=(6.4, 2.6), dpi=100)
        self.fig.patch.set_facecolor("white")
        self.ax.set_facecolor("white")

        # 9 Dates matching Reference Image (May 5 - May 13)
        days_num = np.arange(9)
        day_labels = ["May 5", "May 6", "May 7", "May 8", "May 9", "May 10", "May 11", "May 12", "May 13"]
        # Wave data with peak at May 9 (index 4) = 82
        values = np.array([48.0, 54.0, 50.0, 62.0, 82.0, 53.0, 59.0, 56.0, 75.0])

        # Generate smooth cubic spline
        pts = np.column_stack([days_num, values])
        x_smooth, y_smooth = catmull_rom_spline(pts, n_points=80)
        y_smooth = np.clip(y_smooth, 0, None)

        # 1. Translucent highlight pillar behind the peak at May 9 (x = 4)
        peak_x = 4.0
        peak_y = 82.0
        self.ax.axvspan(peak_x - 0.28, peak_x + 0.28, ymin=0, ymax=peak_y / 115.0,
                        facecolor="#EBF4FE", edgecolor="none", alpha=0.95, zorder=1)

        # 2. Sleek royal navy spline curve (#0C2B59)
        line_color = "#0C2B59"
        self.ax.plot(x_smooth, y_smooth, color=line_color, linewidth=2.8, zorder=3)
        self.ax.fill_between(x_smooth, y_smooth, color="#1E5DB4", alpha=0.08, zorder=2)

        # 3. Peak marker and pin badge (82)
        # Dot on curve
        self.ax.plot(peak_x, peak_y, "o", color="#0C2B59", markersize=6.5,
                     markeredgecolor="white", markeredgewidth=2, zorder=5)

        # Dotted vertical connecting pin line
        badge_y = peak_y + 16.0
        self.ax.plot([peak_x, peak_x], [peak_y, badge_y - 4],
                     color="#0C2B59", linewidth=1.5, linestyle=":", zorder=4)

        # Dark navy circular badge with white "82"
        self.ax.text(
            peak_x, badge_y, "82",
            ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="white",
            bbox=dict(boxstyle="circle,pad=0.45", fc="#0C2B59", ec="#0C2B59", lw=1.5),
            zorder=6
        )

        # 4. Y-axis styling (40, 60, 80, 100)
        self.ax.set_yticks([40, 60, 80, 100])
        self.ax.set_yticklabels(["40", "60", "80", "100"], fontsize=8, color="#94A3B8")

        # 5. X-axis styling (May 5 - May 13)
        self.ax.set_xticks(days_num)
        self.ax.set_xticklabels(day_labels, fontsize=8, color="#64748B", fontweight="bold")
        self.ax.tick_params(axis="both", which="both", length=0, labelsize=8, colors="#64748B")
        self.ax.set_ylim(20, 115)
        self.ax.set_xlim(-0.4, 8.4)

        # 6. Horizontal light grid lines only
        self.ax.grid(axis="y", color="#F1F5F9", linestyle="-", linewidth=1)
        self.ax.grid(visible=False, axis="x")

        # 7. Remove border spines for clean minimalist presentation
        for spine in ["top", "right", "left", "bottom"]:
            self.ax.spines[spine].set_visible(False)

        self.fig.tight_layout(pad=0.8)

        # 8. Canvas embedding
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
