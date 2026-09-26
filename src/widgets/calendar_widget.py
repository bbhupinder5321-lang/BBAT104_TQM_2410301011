"""
Interactive Calendar Widget for OPD Appointment Scheduling.
Inspired by Reference Images 1 & 3 (Admin Portal & Arck University).
Provides a modern day-grid with active day circles and appointment markers.
"""

import calendar
from datetime import date, datetime
import tkinter as tk
from typing import Optional, Callable
from src.config import THEME


class AppointmentCalendar(tk.Frame):
    """
    Modern Clinical Calendar Widget with Month Navigation and Date Highlighting.
    """

    def __init__(self, parent, on_date_selected: Optional[Callable[[str], None]] = None, bg_color: str = "white"):
        super().__init__(parent, bg=bg_color)
        self.on_date_selected = on_date_selected
        self.bg_color = bg_color

        today = date.today()
        self.current_year = today.year
        self.current_month = today.month
        self.selected_day = today.day

        self._build_ui()
        self._render_calendar()

    def _build_ui(self):
        # 1. Month Header & Navigation Row
        header_row = tk.Frame(self, bg=self.bg_color)
        header_row.pack(fill=tk.X, pady=(0, 10))

        self.lbl_month = tk.Label(
            header_row, text="", font=("Segoe UI", 11, "bold"),
            fg=THEME["text"], bg=self.bg_color
        )
        self.lbl_month.pack(side=tk.LEFT)

        nav_box = tk.Frame(header_row, bg=self.bg_color)
        nav_box.pack(side=tk.RIGHT)

        btn_prev = tk.Button(
            nav_box, text="‹", font=("Segoe UI", 12, "bold"),
            bg="#F1F5F9", fg=THEME["text"], relief="flat", cursor="hand2",
            padx=8, pady=0, command=self._prev_month
        )
        btn_prev.pack(side=tk.LEFT, padx=2)

        btn_next = tk.Button(
            nav_box, text="›", font=("Segoe UI", 12, "bold"),
            bg="#F1F5F9", fg=THEME["text"], relief="flat", cursor="hand2",
            padx=8, pady=0, command=self._next_month
        )
        btn_next.pack(side=tk.LEFT, padx=2)

        # 2. Weekday Header Labels
        days_row = tk.Frame(self, bg=self.bg_color)
        days_row.pack(fill=tk.X, pady=(0, 4))

        day_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for d in day_names:
            tk.Label(
                days_row, text=d, font=("Segoe UI", 8, "bold"),
                fg="#94A3B8", bg=self.bg_color, width=4
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 3. Days Grid Container
        self.grid_container = tk.Frame(self, bg=self.bg_color)
        self.grid_container.pack(fill=tk.BOTH, expand=True)

    def _render_calendar(self):
        # Update month label
        month_name = calendar.month_name[self.current_month]
        self.lbl_month.config(text=f"{month_name} {self.current_year}")

        # Clear existing buttons
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        cal = calendar.monthcalendar(self.current_year, self.current_month)
        today = date.today()

        for r_idx, week in enumerate(cal):
            week_row = tk.Frame(self.grid_container, bg=self.bg_color)
            week_row.pack(fill=tk.X, pady=2)

            for d_idx, day_num in enumerate(week):
                cell_box = tk.Frame(week_row, bg=self.bg_color, width=32, height=30)
                cell_box.pack(side=tk.LEFT, fill=tk.X, expand=True)
                cell_box.pack_propagate(False)

                if day_num == 0:
                    continue

                is_today = (self.current_year == today.year and 
                            self.current_month == today.month and 
                            day_num == today.day)
                is_selected = (day_num == self.selected_day)

                if is_selected:
                    bg_c = THEME["primary"]
                    fg_c = "white"
                elif is_today:
                    bg_c = THEME["primary_light"]
                    fg_c = THEME["primary"]
                else:
                    bg_c = self.bg_color
                    fg_c = THEME["text"]

                btn_day = tk.Button(
                    cell_box, text=str(day_num), font=("Segoe UI", 8, "bold" if (is_today or is_selected) else "normal"),
                    bg=bg_c, fg=fg_c, relief="flat", cursor="hand2", bd=0,
                    activebackground=THEME["primary_light"], activeforeground=THEME["primary"],
                    command=lambda d=day_num: self._select_day(d)
                )
                btn_day.pack(fill=tk.BOTH, expand=True, padx=2, pady=1)

    def _select_day(self, day: int):
        self.selected_day = day
        self._render_calendar()
        sel_date_str = f"{self.current_year:04d}-{self.current_month:02d}-{day:02d}"
        if self.on_date_selected:
            self.on_date_selected(sel_date_str)

    def _prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.selected_day = 1
        self._render_calendar()

    def _next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.selected_day = 1
        self._render_calendar()
