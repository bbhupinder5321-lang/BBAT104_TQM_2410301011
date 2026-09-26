"""
Radial / Donut Circular Progress Ring Widget.
Inspired by modern SaaS dashboards (Reference Image 3).
Renders smooth animated circular gauges on a Tkinter Canvas.
"""

import tkinter as tk
from src.config import THEME


class CircularGauge(tk.Frame):
    """
    Circular Donut Progress Gauge with animated filling effect.
    """

    def __init__(self, parent, size: int = 120, ring_width: int = 10,
                 bg_color: str = "white", track_color: str = "#E2E8F0",
                 fill_color: str = "#2563EB", label: str = "Progress",
                 initial_val: float = 0.0, max_val: float = 100.0,
                 suffix: str = "%"):
        super().__init__(parent, bg=bg_color)
        self.size = size
        self.ring_width = ring_width
        self.bg_color = bg_color
        self.track_color = track_color
        self.fill_color = fill_color
        self.label_text = label
        self.current_val = 0.0
        self.target_val = initial_val
        self.max_val = max_val
        self.suffix = suffix

        self.canvas = tk.Canvas(
            self, width=size, height=size, bg=bg_color,
            highlightthickness=0, bd=0
        )
        self.canvas.pack(anchor=tk.CENTER)

        self.lbl_title = tk.Label(
            self, text=label, font=("Segoe UI", 9, "bold"),
            fg=THEME["text_muted"], bg=bg_color
        )
        self.lbl_title.pack(anchor=tk.CENTER, pady=(2, 0))

        self.draw_gauge()
        if initial_val > 0:
            self.animate_to(initial_val)

    def draw_gauge(self):
        self.canvas.delete("all")
        pad = self.ring_width + 4
        x0, y0 = pad, pad
        x1, y1 = self.size - pad, self.size - pad

        # 1. Background Track Ring
        self.canvas.create_oval(
            x0, y0, x1, y1,
            outline=self.track_color,
            width=self.ring_width
        )

        # 2. Value Arc
        pct = max(0.0, min(1.0, self.current_val / self.max_val))
        extent = - (pct * 360.0)

        if pct > 0:
            self.canvas.create_arc(
                x0, y0, x1, y1,
                start=90, extent=extent,
                outline=self.fill_color,
                style=tk.ARC,
                width=self.ring_width
            )

        # 3. Center Value Text
        display_val = f"{int(self.current_val)}{self.suffix}" if self.suffix == "%" else f"{self.current_val:.1f}{self.suffix}"
        self.canvas.create_text(
            self.size // 2, self.size // 2,
            text=display_val,
            font=("Segoe UI", 13, "bold"),
            fill=THEME["text"]
        )

    def animate_to(self, target: float):
        """Smoothly animate progress ring from current to target."""
        self.target_val = max(0.0, min(self.max_val, target))
        if hasattr(self, "_anim_job") and self._anim_job:
            try:
                self.after_cancel(self._anim_job)
            except Exception:
                pass
        self._step_animation()

    def _step_animation(self):
        try:
            if not self.winfo_exists():
                return
            diff = self.target_val - self.current_val
            if abs(diff) > 0.5:
                step = diff * 0.2
                self.current_val += step
                self.draw_gauge()
                self._anim_job = self.after(16, self._step_animation)
            else:
                self.current_val = self.target_val
                self.draw_gauge()
                self._anim_job = None
        except Exception:
            return
