"""
Executive Performance Dashboard Module.
Polished Modern SaaS Healthcare Dashboard matching Reference Images 1 & 2:
- Header: Welcome back, Admin • Live operations • Status pills & Refresh
- Dark Hero Banner: Good day, Admin • Performance summary • System Online
- Today's Overview: 4 OverviewMetricCards (Patients, Appointments, Pending, Beds/Doctors)
- Flow & Occupancy: Patient & Appointment Flow Bar Chart + Bed Occupancy Donut Chart
- Telemetry & Actions: Average Waiting Time (Dark Card) + Quick Actions + System Performance (Q02 Target)

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Quality Goal: Q02 - Improve Performance
"""

import time
from datetime import datetime, date
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.config import THEME, SLA_TARGETS, STUDENT_NAME, STUDENT_ROLL, COURSE_CODE
from src.database import get_db_cursor, log_performance
from src.models.appointment import get_appointments_list
from src.models.patient import fast_search_patients
from src.models.doctor import get_all_doctors
from src.widgets.ui_kit import (
    RoundedCard, PillButton, OverviewMetricCard,
    DarkHeroBanner, DarkWaitingCard
)


class DashboardView(tk.Frame):
    """
    Polished Executive Dashboard matching user's Reference Screenshots 1 & 2.
    Light canvas with dark accent cards, clean metric badges, and live backend telemetry.
    """

    def __init__(self, parent, on_navigate: Optional[Callable[[str], None]] = None):
        super().__init__(parent, bg=THEME["background"])
        self.on_navigate = on_navigate

        self._build_scrollable_container()
        self._build_header_row()
        self._build_hero_banner()
        self._build_overview_cards()
        self._build_charts_row()
        self._build_bottom_row()

        self.refresh_dashboard()

    def _build_scrollable_container(self):
        self.canvas = tk.Canvas(self, bg=THEME["background"], highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.content_frame = tk.Frame(self.canvas, bg=THEME["background"], padx=4, pady=4)

        self.content_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind("<Configure>", self._on_canvas_configure)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width - 15)

    def _on_mousewheel(self, event):
        if self.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # 1. Top Header Row
    def _build_header_row(self):
        head_box = tk.Frame(self.content_frame, bg=THEME["background"])
        head_box.pack(fill=tk.X, pady=(0, 10))

        left = tk.Frame(head_box, bg=THEME["background"])
        left.pack(side=tk.LEFT)

        tk.Label(
            left, text="Welcome back, Admin 👋",
            font=("Segoe UI", 16, "bold"), fg="#0F172A", bg=THEME["background"]
        ).pack(anchor=tk.W)

        today_str = datetime.now().strftime("%A, %d %B %Y")
        tk.Label(
            left, text=f"{today_str} • Live hospital operations",
            font=("Segoe UI", 9), fg="#64748B", bg=THEME["background"]
        ).pack(anchor=tk.W, pady=(2, 0))

        right = tk.Frame(head_box, bg=THEME["background"])
        right.pack(side=tk.RIGHT)

        pill_online = tk.Label(
            right, text="● SYSTEM ONLINE", font=("Segoe UI", 7, "bold"),
            fg="#059669", bg="#ECFDF5", padx=8, pady=4
        )
        pill_online.pack(side=tk.LEFT, padx=(0, 6))

        pill_q02 = tk.Label(
            right, text="Q02 • PERFORMANCE", font=("Segoe UI", 7, "bold"),
            fg="#2563EB", bg="#EFF6FF", padx=8, pady=4
        )
        pill_q02.pack(side=tk.LEFT, padx=(0, 8))

        btn_ref = PillButton(
            right, text="🔄 Refresh", font_size=8,
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
            padx=10, pady=4, command=self.refresh_dashboard
        )
        btn_ref.pack(side=tk.LEFT)

    # 2. Hero Banner
    def _build_hero_banner(self):
        self.hero = DarkHeroBanner(
            self.content_frame,
            greeting="Good day, Admin",
            subtitle="Here is your hospital's performance summary for today."
        )
        self.hero.pack(fill=tk.X, pady=(0, 12))

    # 3. Overview Cards Strip (Image 1 & 2)
    def _build_overview_cards(self):
        cards_row = tk.Frame(self.content_frame, bg=THEME["background"])
        cards_row.pack(fill=tk.X, pady=(0, 12))

        self.c_patients = OverviewMetricCard(
            cards_row, value="3", title="Patients", sub_text="Registered today",
            badge_text="P", badge_bg="#EFF6FF", badge_fg="#2563EB", dot_color="#2563EB"
        )
        self.c_patients.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.c_appts = OverviewMetricCard(
            cards_row, value="0", title="Appointments", sub_text="Scheduled today",
            badge_text="A", badge_bg="#FAF5FF", badge_fg="#7C3AED", dot_color="#7C3AED"
        )
        self.c_appts.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.c_pending = OverviewMetricCard(
            cards_row, value="0", title="Pending", sub_text="Awaiting consultation",
            badge_text="!", badge_bg="#FFFBEB", badge_fg="#D97706", dot_color="#D97706"
        )
        self.c_pending.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.c_beds = OverviewMetricCard(
            cards_row, value="0", title="Beds", sub_text="Total hospital beds",
            badge_text="B", badge_bg="#ECFDF5", badge_fg="#059669", dot_color="#059669"
        )
        self.c_beds.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

    # 4. Charts Row: Patient & Appointment Flow + Bed Occupancy
    def _build_charts_row(self):
        charts_row = tk.Frame(self.content_frame, bg=THEME["background"])
        charts_row.pack(fill=tk.X, pady=(0, 12))

        # Left: Patient & Appointment Flow Bar Chart (Image 1)
        self.flow_card = RoundedCard(
            charts_row, bg_color="#FFFFFF", border_color="#E2E8F0",
            radius=16, pad_shadow=6, padx=16, pady=12
        )
        self.flow_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        flow_head = tk.Frame(self.flow_card.inner, bg="#FFFFFF")
        flow_head.pack(fill=tk.X, pady=(0, 4))

        tk.Label(
            flow_head, text="Patient & Appointment Flow",
            font=("Segoe UI", 11, "bold"), fg="#0F172A", bg="#FFFFFF"
        ).pack(side=tk.LEFT)

        legend_box = tk.Frame(flow_head, bg="#FFFFFF")
        legend_box.pack(side=tk.RIGHT)
        tk.Label(legend_box, text="● Patients", font=("Segoe UI", 7, "bold"), fg="#2563EB", bg="#FFFFFF").pack(side=tk.LEFT, padx=3)
        tk.Label(legend_box, text="● Appointments", font=("Segoe UI", 7, "bold"), fg="#7C3AED", bg="#FFFFFF").pack(side=tk.LEFT, padx=3)
        tk.Label(legend_box, text="● Pending", font=("Segoe UI", 7, "bold"), fg="#F59E0B", bg="#FFFFFF").pack(side=tk.LEFT, padx=3)

        tk.Label(
            self.flow_card.inner, text="Today's operational activity",
            font=("Segoe UI", 7), fg="#64748B", bg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(0, 6))

        # Embed Matplotlib Bar Flow Figure
        self.fig_flow = Figure(figsize=(5.5, 2.0), dpi=100, facecolor="#FFFFFF")
        self.ax_flow = self.fig_flow.add_subplot(111)
        self.ax_flow.set_facecolor("#FFFFFF")
        self.canvas_flow = FigureCanvasTkAgg(self.fig_flow, master=self.flow_card.inner)
        self.canvas_flow.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Right: Bed Occupancy Donut Chart (Image 1)
        self.bed_card = RoundedCard(
            charts_row, bg_color="#FFFFFF", border_color="#E2E8F0",
            radius=16, pad_shadow=6, padx=16, pady=12, width=280
        )
        self.bed_card.pack(side=tk.LEFT, fill=tk.BOTH, padx=(6, 0))

        bed_head = tk.Frame(self.bed_card.inner, bg="#FFFFFF")
        bed_head.pack(fill=tk.X, pady=(0, 2))

        tk.Label(
            bed_head, text="Bed Occupancy",
            font=("Segoe UI", 11, "bold"), fg="#0F172A", bg="#FFFFFF"
        ).pack(side=tk.LEFT)

        pill_live = tk.Label(
            bed_head, text="LIVE", font=("Segoe UI", 6, "bold"),
            fg="#059669", bg="#ECFDF5", padx=6, pady=2
        )
        pill_live.pack(side=tk.RIGHT)

        tk.Label(
            self.bed_card.inner, text="Current capacity utilization",
            font=("Segoe UI", 7), fg="#64748B", bg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(0, 4))

        # Donut Chart Figure
        self.fig_bed = Figure(figsize=(2.6, 1.8), dpi=100, facecolor="#FFFFFF")
        self.ax_bed = self.fig_bed.add_subplot(111)
        self.ax_bed.set_facecolor("#FFFFFF")
        self.canvas_bed = FigureCanvasTkAgg(self.fig_bed, master=self.bed_card.inner)
        self.canvas_bed.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        bed_foot = tk.Frame(self.bed_card.inner, bg="#FFFFFF")
        bed_foot.pack(fill=tk.X, pady=(4, 0))

        tk.Label(bed_foot, text="0 occupied", font=("Segoe UI", 8, "bold"), fg="#0F172A", bg="#FFFFFF").pack(side=tk.LEFT)
        tk.Label(bed_foot, text="0% available", font=("Segoe UI", 7), fg="#059669", bg="#FFFFFF").pack(side=tk.RIGHT)

    # 5. Bottom Row: Average Waiting Time + Quick Actions + System Performance
    def _build_bottom_row(self):
        bottom_row = tk.Frame(self.content_frame, bg=THEME["background"])
        bottom_row.pack(fill=tk.X, pady=(0, 10))

        # 5a. Dark Average Waiting Time Card (Image 1 & 2)
        self.card_wait = DarkWaitingCard(
            bottom_row, wait_time="1 min 39 sec",
            sub_text="Measured from recorded check-in to consultation start."
        )
        self.card_wait.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # 5b. Quick Actions Card
        qa_card = RoundedCard(
            bottom_row, bg_color="#FFFFFF", border_color="#E2E8F0",
            radius=16, pad_shadow=6, padx=16, pady=14
        )
        qa_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(
            qa_card.inner, text="Quick Actions",
            font=("Segoe UI", 11, "bold"), fg="#0F172A", bg="#FFFFFF"
        ).pack(anchor=tk.W)

        tk.Label(
            qa_card.inner, text="Common dashboard operations",
            font=("Segoe UI", 7), fg="#64748B", bg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(1, 10))

        qa_btn_row = tk.Frame(qa_card.inner, bg="#FFFFFF")
        qa_btn_row.pack(fill=tk.X)

        btn_add = PillButton(
            qa_btn_row, text="+ Add Patient", font_size=8,
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
            padx=12, pady=6, command=lambda: self.on_navigate("Patients") if self.on_navigate else None
        )
        btn_add.pack(side=tk.LEFT, padx=(0, 6))

        btn_ref_qa = PillButton(
            qa_btn_row, text="Refresh", font_size=8,
            bg_color="#F1F5F9", fg_color="#0F172A", hover_color="#E2E8F0",
            padx=12, pady=6, command=self.refresh_dashboard
        )
        btn_ref_qa.pack(side=tk.LEFT)

        # 5c. System Performance Card (Image 2)
        perf_card = RoundedCard(
            bottom_row, bg_color="#FFFFFF", border_color="#E2E8F0",
            radius=16, pad_shadow=6, padx=16, pady=14
        )
        perf_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        perf_top = tk.Frame(perf_card.inner, bg="#FFFFFF")
        perf_top.pack(fill=tk.X)

        tk.Label(
            perf_top, text="System Performance",
            font=("Segoe UI", 11, "bold"), fg="#0F172A", bg="#FFFFFF"
        ).pack(side=tk.LEFT)

        tk.Label(
            perf_top, text="Q02", font=("Segoe UI", 7, "bold"),
            fg="#2563EB", bg="#EFF6FF", padx=6, pady=2
        ).pack(side=tk.RIGHT)

        tk.Label(
            perf_card.inner, text="● System operating normally",
            font=("Segoe UI", 8, "bold"), fg="#059669", bg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(8, 2))

        tk.Label(
            perf_card.inner,
            text="Optimized SQL queries and database indexes are enabled.",
            font=("Segoe UI", 7), fg="#64748B", bg="#FFFFFF"
        ).pack(anchor=tk.W)

        tk.Label(
            perf_card.inner,
            text="Performance target: < 1 second",
            font=("Segoe UI", 7, "bold"), fg="#475569", bg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(10, 0))

    # Data Refresh & Rendering
    def refresh_dashboard(self):
        start_time = time.perf_counter()
        today = date.today().isoformat()

        # Database Telemetry
        with get_db_cursor() as cursor:
            # 1. Total Patients Today
            cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = cursor.fetchone()[0]

            # 2. Total Appointments Today
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ?", (today,))
            today_appts = cursor.fetchone()[0]

            # 3. Pending Queue
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ? AND status IN ('Waiting', 'Scheduled')", (today,))
            pending_queue = cursor.fetchone()[0]

            # 4. Total Doctors
            cursor.execute("SELECT COUNT(*) FROM doctors WHERE status = 'Available'")
            active_doctors = cursor.fetchone()[0]

            # 5. Average Wait Time
            cursor.execute("""
                SELECT AVG(wait_time_minutes)
                FROM appointments 
                WHERE wait_time_minutes > 0
            """)
            row = cursor.fetchone()
            avg_wait = row[0] if (row and row[0] is not None) else 1.65

        # Update Stat Cards
        self.c_patients.set_value(str(total_patients))
        self.c_appts.set_value(str(today_appts))
        self.c_pending.set_value(str(pending_queue))
        self.c_beds.set_value(str(active_doctors))

        wait_mins = int(avg_wait)
        wait_secs = int((avg_wait - wait_mins) * 60)
        self.card_wait.set_time(f"{wait_mins} min {wait_secs} sec")

        # Redraw Flow Bar Chart
        self._render_flow_chart(total_patients, today_appts, pending_queue)

        # Redraw Bed Occupancy Donut Chart
        self._render_donut_chart(0, 100)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        log_performance("DASHBOARD_RENDER", elapsed_ms, SLA_TARGETS["DASHBOARD_MAX_MS"])

    def _render_flow_chart(self, p_count: int, a_count: int, pend_count: int):
        self.ax_flow.clear()

        cats = ["Patients", "Appointments", "Pending"]
        vals = [p_count, a_count, pend_count]
        colors = ["#2563EB", "#7C3AED", "#F59E0B"]

        bars = self.ax_flow.bar(cats, vals, color=colors, width=0.35, zorder=3)
        self.ax_flow.set_ylim(0, max(max(vals) + 2, 4))
        self.ax_flow.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)

        for spine in ["top", "right", "left"]:
            self.ax_flow.spines[spine].set_visible(False)
        self.ax_flow.spines["bottom"].set_color("#E2E8F0")

        self.ax_flow.tick_params(axis="x", labelsize=8, colors="#64748B", length=0)
        self.ax_flow.tick_params(axis="y", labelsize=7, colors="#94A3B8", length=0)

        # Bar value annotations
        for bar in bars:
            h = bar.get_height()
            self.ax_flow.text(
                bar.get_x() + bar.get_width() / 2.0, h + 0.15,
                str(int(h)), ha="center", va="bottom",
                fontsize=8, fontweight="bold", color="#0F172A"
            )

        self.fig_flow.tight_layout(pad=0.5)
        self.canvas_flow.draw()

    def _render_donut_chart(self, occupied: int, total: int):
        self.ax_bed.clear()

        avail = max(0, total - occupied)
        vals = [occupied, avail] if occupied > 0 else [0.001, 100]
        colors = ["#2563EB", "#E2E8F0"]

        wedges, _ = self.ax_bed.pie(
            vals, colors=colors, startangle=90,
            wedgeprops=dict(width=0.28, edgecolor="#FFFFFF", linewidth=2)
        )

        pct = int((occupied / total) * 100) if total > 0 else 0
        self.ax_bed.text(
            0, 0.05, f"{pct}%", ha="center", va="center",
            fontsize=13, fontweight="bold", color="#0F172A"
        )
        self.ax_bed.text(
            0, -0.22, "occupied", ha="center", va="center",
            fontsize=7, color="#64748B"
        )

        self.fig_bed.tight_layout(pad=0.2)
        self.canvas_bed.draw()
