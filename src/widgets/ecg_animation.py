"""
Animated ECG Heartbeat / Vital Telemetry Widget.
Inspired by Reference Image 2 (KRL Health Care ECG wave branding).
Renders a live pulsing electrocardiogram wave on a Tkinter Canvas.
"""

import math
import tkinter as tk
from src.config import THEME


class ECGAnimationWidget(tk.Frame):
    """
    Live Animated Heartbeat / ECG Waveform Widget with moving pulse beam.
    """

    def __init__(self, parent, width: int = 180, height: int = 40, bg_color: str = "#0F172A"):
        super().__init__(parent, bg=bg_color)
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.cursor_x = 0
        self.is_running = True

        self.canvas = tk.Canvas(
            self, width=width, height=height, bg=bg_color,
            highlightthickness=0, bd=0
        )
        self.canvas.pack(side=tk.LEFT)

        # Precompute ECG waveform points
        self.wave_points = self._generate_ecg_points()
        self._animate()

    def _generate_ecg_points(self):
        mid_y = self.height // 2
        pts = []
        for x in range(self.width):
            # Normalize to 0..1 cycle every 90 pixels
            phase = (x % 90) / 90.0
            if 0.0 <= phase < 0.2:
                y = mid_y
            elif 0.2 <= phase < 0.3:
                # P wave
                y = mid_y - 4 * math.sin((phase - 0.2) / 0.1 * math.pi)
            elif 0.3 <= phase < 0.38:
                y = mid_y
            elif 0.38 <= phase < 0.42:
                # Q dip
                y = mid_y + 6
            elif 0.42 <= phase < 0.48:
                # R spike
                y = mid_y - 18
            elif 0.48 <= phase < 0.54:
                # S dip
                y = mid_y + 10
            elif 0.54 <= phase < 0.65:
                y = mid_y
            elif 0.65 <= phase < 0.8:
                # T wave
                y = mid_y - 7 * math.sin((phase - 0.65) / 0.15 * math.pi)
            else:
                y = mid_y
            pts.append((x, int(y)))
        return pts

    def _animate(self):
        if not self.winfo_exists() or not self.is_running:
            return

        self.canvas.delete("all")
        mid_y = self.height // 2

        # Draw faint baseline grid line
        self.canvas.create_line(0, mid_y, self.width, mid_y, fill="#1E293B", width=1)

        # Draw ECG line with trailing fade
        prev_pt = None
        for x, y in self.wave_points:
            if prev_pt is not None:
                # Distance from cursor
                dist = (self.cursor_x - x) % self.width
                if dist < 80:
                    alpha_ratio = 1.0 - (dist / 80.0)
                    color = "#38BDF8" if alpha_ratio > 0.6 else "#0284C7"
                    line_w = 2 if alpha_ratio > 0.6 else 1
                    self.canvas.create_line(prev_pt[0], prev_pt[1], x, y, fill=color, width=line_w)
                elif dist > self.width - 15:
                    self.canvas.create_line(prev_pt[0], prev_pt[1], x, y, fill="#0F3559", width=1)
            prev_pt = (x, y)

        # Draw pulsing lead dot
        curr_y = self.wave_points[self.cursor_x][1]
        self.canvas.create_oval(
            self.cursor_x - 3, curr_y - 3, self.cursor_x + 3, curr_y + 3,
            fill="#38BDF8", outline="#E0F2FE", width=1
        )

        # Step cursor
        self.cursor_x = (self.cursor_x + 2) % self.width
        self.after(25, self._animate)

    def stop(self):
        self.is_running = False
