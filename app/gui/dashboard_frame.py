import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox


from app.services.dashboard_service import DashboardService


class DashboardFrame(ctk.CTkFrame):

    # =========================================================
    # PREMIUM HOSPITAL DASHBOARD
    # =========================================================
    #
    # The dashboard intentionally keeps the existing
    # DashboardService as the single source of real metrics.
    #
    # GUI shows -> Service decides -> Repository queries
    # -> Database stores
    #
    # No fake clinical/revenue/history data is generated here.
    # =========================================================

    # ---------------------------------------------------------
    # SURFACE COLORS
    # ---------------------------------------------------------

    BACKGROUND = "#F6F8FC"
    CARD = "#FFFFFF"
    CARD_SOFT = "#F8FAFD"
    CARD_DARK = "#111827"

    # ---------------------------------------------------------
    # BRAND / ACCENTS
    # ---------------------------------------------------------

    PRIMARY = "#2563EB"
    PRIMARY_DARK = "#1D4ED8"
    PRIMARY_SOFT = "#EFF6FF"

    INDIGO = "#4F46E5"
    INDIGO_SOFT = "#EEF2FF"

    CYAN = "#0891B2"
    CYAN_SOFT = "#ECFEFF"

    GREEN = "#10B981"
    GREEN_DARK = "#059669"
    GREEN_SOFT = "#ECFDF5"

    ORANGE = "#F59E0B"
    ORANGE_DARK = "#D97706"
    ORANGE_SOFT = "#FFF7ED"

    RED = "#EF4444"
    RED_SOFT = "#FEF2F2"

    PURPLE = "#7C3AED"
    PURPLE_SOFT = "#F5F3FF"

    # ---------------------------------------------------------
    # TEXT
    # ---------------------------------------------------------

    TEXT = "#111827"
    TEXT_DARK = "#0F172A"
    SECONDARY_TEXT = "#64748B"
    MUTED_TEXT = "#94A3B8"
    WHITE = "#FFFFFF"

    # ---------------------------------------------------------
    # BORDERS / CHARTS
    # ---------------------------------------------------------

    BORDER = "#E6EAF0"
    BORDER_DARK = "#D8DEE8"
    GRID = "#EEF2F7"
    TRACK = "#E9EEF5"

    # ---------------------------------------------------------
    # SIZING
    # ---------------------------------------------------------

    PAGE_PAD_X = 30
    PAGE_PAD_TOP = 24
    PAGE_PAD_BOTTOM = 34

    def __init__(self, parent, user=None):

        super().__init__(
            parent,
            fg_color=self.BACKGROUND,
            corner_radius=0
        )

        self.user = user or {
            "username": "admin",
            "role": "admin"
        }

        self.service = DashboardService()
        self.metrics = {}

        # Animation state
        self.animation_jobs = []
        self.chart_animation_jobs = []

        # Widget references used by refresh/animation
        self.kpi_value_labels = {}
        self.kpi_sub_labels = {}
        self.occupancy_canvas = None
        self.occupancy_arc = None
        self.flow_canvas = None
        self.flow_bars = []
        self.wait_value_label = None
        self.refresh_button = None
        self.refresh_icon_label = None

        # Navigation target is resolved from the top-level window.
        self.window = self.winfo_toplevel()

        self.create_widgets()

    # =========================================================
    # MAIN BUILD
    # =========================================================

    def create_widgets(self):

        self.cancel_animations()

        self.main = ctk.CTkScrollableFrame(
            self,
            fg_color=self.BACKGROUND,
            corner_radius=0,
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        self.load_metrics()

        self.create_header()

        self.create_kpi_section()

        self.create_analytics_section()

        self.create_operations_section()

        self.create_quality_section()

        self.create_footer()

        self.after(
            80,
            self.start_entrance_animation
        )

    # =========================================================
    # DATA
    # =========================================================

    def load_metrics(self):

        try:

            self.metrics = (
                self.service
                .get_dashboard_metrics()
            )

        except Exception as error:

            messagebox.showerror(
                "Dashboard Error",
                f"Unable to load dashboard data.\n\n{error}"
            )

            self.metrics = {
                "today_patients": 0,
                "today_appointments": 0,
                "pending_appointments": 0,
                "total_beds": 0,
                "occupied_beds": 0,
                "average_waiting_seconds": 0
            }

        # Make every expected metric safe even if the service
        # returns a partial dictionary in the future.
        for key in (
            "today_patients",
            "today_appointments",
            "pending_appointments",
            "total_beds",
            "occupied_beds",
            "average_waiting_seconds"
        ):
            self.metrics.setdefault(key, 0)

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=self.PAGE_PAD_X,
            pady=(self.PAGE_PAD_TOP, 8)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        # -----------------------------------------------------
        # LEFT: GREETING + CONTEXT
        # -----------------------------------------------------

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.grid(
            row=0,
            column=0,
            sticky="w"
        )

        username = self.user.get(
            "username",
            "admin"
        )

        display_name = str(username).strip().title()

        greeting = ctk.CTkLabel(
            left,
            text=f"Good day, {display_name}  👋",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            )
        )

        greeting.pack(
            anchor="w"
        )

        today_text = datetime.now().strftime(
            "%A, %d %B %Y"
        )

        subtitle = ctk.CTkLabel(
            left,
            text=(
                f"{today_text}  •  Hospital operations overview"
            ),
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=12
            )
        )

        subtitle.pack(
            anchor="w",
            pady=(5, 0)
        )

        # -----------------------------------------------------
        # RIGHT: Q02 + REFRESH
        # -----------------------------------------------------

        right = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        right.grid(
            row=0,
            column=1,
            sticky="e"
        )

        quality_badge = ctk.CTkFrame(
            right,
            fg_color=self.PRIMARY_SOFT,
            corner_radius=10,
            border_width=1,
            border_color="#DBEAFE"
        )

        quality_badge.pack(
            side="left",
            padx=(0, 9)
        )

        quality_label = ctk.CTkLabel(
            quality_badge,
            text="Q02  •  IMPROVE PERFORMANCE",
            text_color=self.PRIMARY,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        )

        quality_label.pack(
            padx=12,
            pady=8
        )

        self.refresh_button = ctk.CTkButton(
            right,
            text="↻  Refresh",
            width=105,
            height=36,
            corner_radius=10,
            fg_color=self.CARD,
            hover_color="#F1F5F9",
            text_color=self.TEXT,
            border_width=1,
            border_color=self.BORDER,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.refresh_dashboard
        )

        self.refresh_button.pack(
            side="left"
        )

    # =========================================================
    # KPI SECTION
    # =========================================================

    def create_kpi_section(self):

        section = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        section.pack(
            fill="x",
            padx=self.PAGE_PAD_X,
            pady=(13, 5)
        )

        for column in range(4):

            section.grid_columnconfigure(
                column,
                weight=1,
                uniform="kpi"
            )

        cards = [
            {
                "key": "patients",
                "title": "Patients",
                "value": self.metrics["today_patients"],
                "caption": "Registered today",
                "icon": "P",
                "accent": self.PRIMARY,
                "soft": self.PRIMARY_SOFT,
                "action": self.go_patients
            },
            {
                "key": "appointments",
                "title": "Appointments",
                "value": self.metrics["today_appointments"],
                "caption": "Scheduled today",
                "icon": "A",
                "accent": self.PURPLE,
                "soft": self.PURPLE_SOFT,
                "action": self.go_appointments
            },
            {
                "key": "pending",
                "title": "Pending",
                "value": self.metrics["pending_appointments"],
                "caption": "Awaiting consultation",
                "icon": "W",
                "accent": self.ORANGE,
                "soft": self.ORANGE_SOFT,
                "action": self.go_appointments
            },
            {
                "key": "beds",
                "title": "Beds",
                "value": self.metrics["total_beds"],
                "caption": "Total hospital beds",
                "icon": "B",
                "accent": self.GREEN,
                "soft": self.GREEN_SOFT,
                "action": None
            }
        ]

        for column, data in enumerate(cards):

            self.create_kpi_card(
                section,
                data,
                column
            )

    def create_kpi_card(
        self,
        parent,
        data,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=18,
            border_width=1,
            border_color=self.BORDER,
            cursor="hand2" if data["action"] else "arrow"
        )

        card.grid(
            row=0,
            column=column,
            padx=5,
            pady=5,
            sticky="nsew"
        )

        # A small colored top accent gives the cards a
        # commercial dashboard feel without adding noise.
        accent_strip = ctk.CTkFrame(
            card,
            height=4,
            corner_radius=2,
            fg_color=data["accent"]
        )

        accent_strip.pack(
            fill="x",
            padx=20,
            pady=(14, 0)
        )

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=20,
            pady=(13, 0)
        )

        icon = ctk.CTkFrame(
            top,
            width=42,
            height=42,
            corner_radius=12,
            fg_color=data["soft"]
        )

        icon.pack(
            side="left"
        )

        icon.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            icon,
            text=data["icon"],
            text_color=data["accent"],
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        icon_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        title = ctk.CTkLabel(
            top,
            text=data["title"].upper(),
            text_color=self.MUTED_TEXT,
            font=ctk.CTkFont(
                size=9,
                weight="bold"
            )
        )

        title.pack(
            side="left",
            padx=11,
            pady=(1, 0)
        )

        # Click hint for cards that navigate.
        if data["action"]:

            arrow = ctk.CTkLabel(
                top,
                text="↗",
                text_color=self.MUTED_TEXT,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                )
            )

            arrow.pack(
                side="right"
            )

        value_label = ctk.CTkLabel(
            card,
            text="0",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        value_label.pack(
            anchor="w",
            padx=20,
            pady=(13, 0)
        )

        caption = ctk.CTkLabel(
            card,
            text=data["caption"],
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=10
            )
        )

        caption.pack(
            anchor="w",
            padx=20,
            pady=(1, 18)
        )

        self.kpi_value_labels[data["key"]] = (
            value_label,
            int(data["value"])
        )

        self.kpi_sub_labels[data["key"]] = caption

        if data["action"]:

            self.bind_recursive(
                card,
                "<Button-1>",
                lambda event, command=data["action"]: command()
            )

            self.bind_recursive(
                card,
                "<Enter>",
                lambda event, widget=card, color="#F8FBFF":
                    widget.configure(fg_color=color)
            )

            self.bind_recursive(
                card,
                "<Leave>",
                lambda event, widget=card:
                    widget.configure(fg_color=self.CARD)
            )

    # =========================================================
    # ANALYTICS SECTION
    # =========================================================

    def create_analytics_section(self):

        section = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        section.pack(
            fill="x",
            padx=self.PAGE_PAD_X,
            pady=(18, 6)
        )

        section.grid_columnconfigure(
            0,
            weight=7,
            uniform="analytics"
        )

        section.grid_columnconfigure(
            1,
            weight=3,
            uniform="analytics"
        )

        self.create_flow_card(
            section
        )

        self.create_occupancy_card(
            section
        )

    # =========================================================
    # PATIENT / APPOINTMENT FLOW
    # =========================================================

    def create_flow_card(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=18,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=0,
            padx=(0, 6),
            sticky="nsew"
        )

        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=22,
            pady=(20, 0)
        )

        title_area = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_area.pack(
            side="left"
        )

        title = ctk.CTkLabel(
            title_area,
            text="Patient & Appointment Flow",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            title_area,
            text="Today's operational volume",
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=10
            )
        )

        subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        legend = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        legend.pack(
            side="right",
            anchor="n"
        )

        self.create_legend_item(
            legend,
            "Patients",
            self.PRIMARY
        )

        self.create_legend_item(
            legend,
            "Appointments",
            self.PURPLE
        )

        self.create_legend_item(
            legend,
            "Pending",
            self.ORANGE
        )

        self.flow_canvas = ctk.CTkCanvas(
            card,
            width=640,
            height=245,
            bg=self.CARD,
            highlightthickness=0,
            bd=0
        )

        self.flow_canvas.pack(
            fill="x",
            expand=True,
            padx=16,
            pady=(12, 18)
        )

        self.flow_canvas.bind(
            "<Configure>",
            lambda event: self.draw_flow_chart()
        )

        self.flow_canvas.after(
            40,
            self.draw_flow_chart
        )

    def create_legend_item(
        self,
        parent,
        text,
        color
    ):

        item = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        item.pack(
            side="left",
            padx=(8, 0)
        )

        dot = ctk.CTkLabel(
            item,
            text="●",
            text_color=color,
            font=ctk.CTkFont(
                size=8
            )
        )

        dot.pack(
            side="left"
        )

        label = ctk.CTkLabel(
            item,
            text=text,
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=9
            )
        )

        label.pack(
            side="left",
            padx=(3, 0)
        )

    def draw_flow_chart(self):

        if not self.flow_canvas:
            return

        canvas = self.flow_canvas

        try:
            width = max(
                canvas.winfo_width(),
                500
            )

            height = max(
                canvas.winfo_height(),
                220
            )

        except Exception:
            return

        canvas.delete("all")

        values = [
            (
                "Patients",
                int(self.metrics.get("today_patients", 0)),
                self.PRIMARY
            ),
            (
                "Appointments",
                int(self.metrics.get("today_appointments", 0)),
                self.PURPLE
            ),
            (
                "Pending",
                int(self.metrics.get("pending_appointments", 0)),
                self.ORANGE
            )
        ]

        maximum = max(
            [item[1] for item in values] + [1]
        )

        left = 45
        right = width - 25
        top = 24
        bottom = height - 42

        plot_width = right - left
        plot_height = bottom - top

        # Horizontal guide lines.
        for step in range(5):

            ratio = step / 4

            y = bottom - (
                plot_height * ratio
            )

            canvas.create_line(
                left,
                y,
                right,
                y,
                fill=self.GRID,
                width=1
            )

            tick = int(
                maximum * ratio
            )

            canvas.create_text(
                left - 10,
                y,
                text=str(tick),
                fill=self.MUTED_TEXT,
                font=("Segoe UI", 8),
                anchor="e"
            )

        group_width = plot_width / 3

        bar_width = min(
            62,
            group_width * 0.35
        )

        self.flow_bars = []

        for index, (label, value, color) in enumerate(values):

            center_x = (
                left
                + group_width * index
                + group_width / 2
            )

            target_height = (
                0
                if maximum <= 0
                else (value / maximum) * plot_height
            )

            x1 = center_x - bar_width / 2
            x2 = center_x + bar_width / 2

            # Track
            canvas.create_rectangle(
                x1,
                top,
                x2,
                bottom,
                fill="#F3F6FA",
                outline=""
            )

            bar = canvas.create_rectangle(
                x1,
                bottom,
                x2,
                bottom,
                fill=color,
                outline=""
            )

            value_text = canvas.create_text(
                center_x,
                bottom - target_height - 12,
                text=str(value),
                fill=self.TEXT_DARK,
                font=("Segoe UI", 10, "bold")
            )

            canvas.create_text(
                center_x,
                bottom + 19,
                text=label,
                fill=self.SECONDARY_TEXT,
                font=("Segoe UI", 9)
            )

            self.flow_bars.append(
                {
                    "bar": bar,
                    "value_text": value_text,
                    "x1": x1,
                    "x2": x2,
                    "bottom": bottom,
                    "target_height": target_height,
                    "target_y": bottom - target_height - 12
                }
            )

        self.animate_flow_chart()

    def animate_flow_chart(self):

        self.cancel_chart_animation()

        steps = 18

        for step in range(steps + 1):

            job = self.after(
                step * 24,
                lambda progress=step / steps:
                    self.update_flow_animation(progress)
            )

            self.chart_animation_jobs.append(
                job
            )

    def update_flow_animation(self, progress):

        # Smooth ease-out curve.
        eased = 1 - ((1 - progress) ** 3)

        for item in self.flow_bars:

            current_height = (
                item["target_height"] * eased
            )

            top_y = (
                item["bottom"] - current_height
            )

            self.flow_canvas.coords(
                item["bar"],
                item["x1"],
                top_y,
                item["x2"],
                item["bottom"]
            )

            value_y = (
                top_y - 12
            )

            self.flow_canvas.coords(
                item["value_text"],
                (item["x1"] + item["x2"]) / 2,
                value_y
            )

    # =========================================================
    # BED OCCUPANCY
    # =========================================================

    def create_occupancy_card(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=18,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=1,
            padx=(6, 0),
            sticky="nsew"
        )

        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=22,
            pady=(20, 0)
        )

        title = ctk.CTkLabel(
            header,
            text="Bed Occupancy",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.pack(
            side="left"
        )

        live = ctk.CTkLabel(
            header,
            text="LIVE",
            text_color=self.GREEN_DARK,
            fg_color=self.GREEN_SOFT,
            corner_radius=6,
            font=ctk.CTkFont(
                size=8,
                weight="bold"
            )
        )

        live.pack(
            side="right",
            padx=0,
            pady=1
        )

        self.occupancy_canvas = ctk.CTkCanvas(
            card,
            width=230,
            height=180,
            bg=self.CARD,
            highlightthickness=0,
            bd=0
        )

        self.occupancy_canvas.pack(
            pady=(8, 0)
        )

        self.occupancy_canvas.bind(
            "<Configure>",
            lambda event: self.draw_occupancy()
        )

        percentage = self.get_occupancy_percentage()

        summary = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        summary.pack(
            fill="x",
            padx=22,
            pady=(2, 20)
        )

        left = ctk.CTkFrame(
            summary,
            fg_color="transparent"
        )

        left.pack(
            side="left"
        )

        occupied_label = ctk.CTkLabel(
            left,
            text=f"{self.metrics['occupied_beds']} occupied",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        occupied_label.pack(
            anchor="w"
        )

        available = max(
            0,
            int(self.metrics["total_beds"])
            - int(self.metrics["occupied_beds"])
        )

        available_label = ctk.CTkLabel(
            left,
            text=f"{available} available",
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=9
            )
        )

        available_label.pack(
            anchor="w",
            pady=(2, 0)
        )

        percentage_label = ctk.CTkLabel(
            summary,
            text=f"{percentage:.0f}%",
            text_color=self.GREEN_DARK,
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        percentage_label.pack(
            side="right"
        )

        self.after(
            80,
            self.draw_occupancy
        )

    def get_occupancy_percentage(self):

        occupied = int(
            self.metrics.get(
                "occupied_beds",
                0
            )
        )

        total = int(
            self.metrics.get(
                "total_beds",
                0
            )
        )

        try:

            return float(
                self.service.get_bed_occupancy_percentage(
                    occupied,
                    total
                )
            )

        except Exception:

            if total <= 0:
                return 0.0

            return round(
                (occupied / total) * 100,
                1
            )

    def draw_occupancy(self):

        if not self.occupancy_canvas:
            return

        canvas = self.occupancy_canvas

        width = max(
            canvas.winfo_width(),
            230
        )

        height = max(
            canvas.winfo_height(),
            180
        )

        canvas.delete("all")

        percentage = self.get_occupancy_percentage()

        center_x = width / 2
        center_y = height / 2

        size = min(
            width,
            height
        ) - 34

        left = center_x - size / 2
        top = center_y - size / 2
        right = center_x + size / 2
        bottom = center_y + size / 2

        # Background track.
        canvas.create_arc(
            left,
            top,
            right,
            bottom,
            start=90,
            extent=-359.9,
            style="arc",
            outline=self.TRACK,
            width=16
        )

        self.occupancy_arc = canvas.create_arc(
            left,
            top,
            right,
            bottom,
            start=90,
            extent=0,
            style="arc",
            outline=self.GREEN,
            width=16
        )

        canvas.create_text(
            center_x,
            center_y - 3,
            text="0%",
            fill=self.TEXT_DARK,
            font=("Segoe UI", 23, "bold"),
            tags="occupancy_value"
        )

        canvas.create_text(
            center_x,
            center_y + 25,
            text="occupied",
            fill=self.SECONDARY_TEXT,
            font=("Segoe UI", 8),
            tags="occupancy_caption"
        )

        self.animate_occupancy(
            percentage
        )

    def animate_occupancy(self, target):

        steps = 24

        for step in range(steps + 1):

            self.after(
                25 + step * 22,
                lambda progress=step / steps:
                    self.update_occupancy_animation(
                        target,
                        progress
                    )
            )

    def update_occupancy_animation(
        self,
        target,
        progress
    ):

        if not self.occupancy_canvas:
            return

        eased = 1 - ((1 - progress) ** 3)

        current = target * eased

        self.occupancy_canvas.itemconfigure(
            self.occupancy_arc,
            extent=-(
                359.9 * current / 100
            )
        )

        self.occupancy_canvas.itemconfigure(
            "occupancy_value",
            text=f"{current:.0f}%"
        )

    # =========================================================
    # OPERATIONS SECTION
    # =========================================================

    def create_operations_section(self):

        section = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        section.pack(
            fill="x",
            padx=self.PAGE_PAD_X,
            pady=(12, 6)
        )

        section.grid_columnconfigure(
            0,
            weight=4,
            uniform="operations"
        )

        section.grid_columnconfigure(
            1,
            weight=6,
            uniform="operations"
        )

        self.create_waiting_card(
            section
        )

        self.create_quick_actions_card(
            section
        )

    # =========================================================
    # WAITING TIME
    # =========================================================

    def create_waiting_card(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD_DARK,
            corner_radius=18
        )

        card.grid(
            row=0,
            column=0,
            padx=(0, 6),
            sticky="nsew"
        )

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=22,
            pady=(20, 0)
        )

        title_area = ctk.CTkFrame(
            top,
            fg_color="transparent"
        )

        title_area.pack(
            side="left"
        )

        title = ctk.CTkLabel(
            title_area,
            text="Average Waiting Time",
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            title_area,
            text="Check-in → consultation",
            text_color="#9CA3AF",
            font=ctk.CTkFont(
                size=9
            )
        )

        subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        badge = ctk.CTkLabel(
            top,
            text="Q02",
            text_color="#BFDBFE",
            fg_color="#1E3A8A",
            corner_radius=7,
            font=ctk.CTkFont(
                size=8,
                weight="bold"
            )
        )

        badge.pack(
            side="right",
            padx=0,
            pady=2
        )

        self.wait_value_label = ctk.CTkLabel(
            card,
            text="0 min",
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=31,
                weight="bold"
            )
        )

        self.wait_value_label.pack(
            anchor="w",
            padx=22,
            pady=(22, 0)
        )

        neutral = ctk.CTkLabel(
            card,
            text="Measured from recorded check-in to consultation start.",
            text_color="#9CA3AF",
            font=ctk.CTkFont(
                size=9
            )
        )

        neutral.pack(
            anchor="w",
            padx=22,
            pady=(3, 18)
        )

        # Visual scale. This is deliberately a neutral
        # measurement scale, not an invented clinical target.
        scale = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        scale.pack(
            fill="x",
            padx=22,
            pady=(0, 18)
        )

        scale.grid_columnconfigure(
            0,
            weight=1
        )

        track = ctk.CTkFrame(
            scale,
            height=7,
            corner_radius=4,
            fg_color="#273449"
        )

        track.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        value = max(
            0,
            int(
                self.metrics.get(
                    "average_waiting_seconds",
                    0
                )
            )
        )

        # The bar represents the measured value on a
        # 30-minute visual window. It is not a quality target.
        ratio = min(
            value / (30 * 60),
            1
        )

        fill = ctk.CTkFrame(
            track,
            height=7,
            corner_radius=4,
            fg_color=self.PRIMARY
        )

        fill.place(
            relx=0,
            rely=0,
            relwidth=ratio,
            relheight=1
        )

        labels = ctk.CTkFrame(
            scale,
            fg_color="transparent"
        )

        labels.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(6, 0)
        )

        labels.grid_columnconfigure(
            0,
            weight=1
        )

        labels.grid_columnconfigure(
            1,
            weight=1
        )

        labels.grid_columnconfigure(
            2,
            weight=1
        )

        for column, text in enumerate(
            ("0 min", "15 min", "30+ min")
        ):

            label = ctk.CTkLabel(
                labels,
                text=text,
                text_color="#64748B",
                font=ctk.CTkFont(
                    size=8
                )
            )

            label.grid(
                row=0,
                column=column,
                sticky="w" if column == 0 else (
                    "e" if column == 2 else "ew"
                )
            )

        self.after(
            140,
            self.animate_waiting_time
        )

    def animate_waiting_time(self):

        if not self.wait_value_label:
            return

        target = max(
            0,
            int(
                self.metrics.get(
                    "average_waiting_seconds",
                    0
                )
            )
        )

        steps = 20

        for step in range(steps + 1):

            self.after(
                step * 28,
                lambda progress=step / steps:
                    self.update_waiting_time_animation(
                        target,
                        progress
                    )
            )

    def update_waiting_time_animation(
        self,
        target,
        progress
    ):

        if not self.wait_value_label:
            return

        eased = 1 - ((1 - progress) ** 3)

        current = int(
            target * eased
        )

        self.wait_value_label.configure(
            text=self.service.format_waiting_time(
                current
            )
        )

    # =========================================================
    # QUICK ACTIONS
    # =========================================================

    def create_quick_actions_card(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=18,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=1,
            padx=(6, 0),
            sticky="nsew"
        )

        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=22,
            pady=(20, 4)
        )

        title = ctk.CTkLabel(
            header,
            text="Quick Actions",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        title.pack(
            side="left"
        )

        hint = ctk.CTkLabel(
            header,
            text="Open a workspace",
            text_color=self.MUTED_TEXT,
            font=ctk.CTkFont(
                size=9
            )
        )

        hint.pack(
            side="right"
        )

        actions = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        actions.pack(
            fill="x",
            padx=16,
            pady=(7, 18)
        )

        for column in range(4):

            actions.grid_columnconfigure(
                column,
                weight=1,
                uniform="quick"
            )

        items = [
            (
                "P",
                "Patients",
                "Manage records",
                self.PRIMARY,
                self.PRIMARY_SOFT,
                self.go_patients
            ),
            (
                "A",
                "Appointments",
                "View schedule",
                self.PURPLE,
                self.PURPLE_SOFT,
                self.go_appointments
            ),
            (
                "R",
                "Reports",
                "View analytics",
                self.CYAN,
                self.CYAN_SOFT,
                self.go_reports
            ),
            (
                "↻",
                "Refresh",
                "Update metrics",
                self.GREEN,
                self.GREEN_SOFT,
                self.refresh_dashboard
            )
        ]

        for column, item in enumerate(items):

            self.create_action_tile(
                actions,
                item,
                column
            )

    def create_action_tile(
        self,
        parent,
        item,
        column
    ):

        icon_text, title, subtitle, accent, soft, command = item

        tile = ctk.CTkFrame(
            parent,
            fg_color=self.CARD_SOFT,
            corner_radius=13,
            border_width=1,
            border_color="#EEF1F5",
            cursor="hand2"
        )

        tile.grid(
            row=0,
            column=column,
            padx=4,
            pady=4,
            sticky="nsew"
        )

        icon = ctk.CTkFrame(
            tile,
            width=35,
            height=35,
            corner_radius=10,
            fg_color=soft
        )

        icon.pack(
            pady=(12, 8)
        )

        icon.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            icon,
            text=icon_text,
            text_color=accent,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        icon_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        title_label = ctk.CTkLabel(
            tile,
            text=title,
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        )

        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            tile,
            text=subtitle,
            text_color=self.MUTED_TEXT,
            font=ctk.CTkFont(
                size=8
            )
        )

        subtitle_label.pack(
            pady=(2, 12)
        )

        self.bind_recursive(
            tile,
            "<Button-1>",
            lambda event, action=command: action()
        )

        self.bind_recursive(
            tile,
            "<Enter>",
            lambda event, widget=tile:
                widget.configure(
                    fg_color="#F1F5FA"
                )
        )

        self.bind_recursive(
            tile,
            "<Leave>",
            lambda event, widget=tile:
                widget.configure(
                    fg_color=self.CARD_SOFT
                )
        )

    # =========================================================
    # QUALITY / Q02 SECTION
    # =========================================================

    def create_quality_section(self):

        card = ctk.CTkFrame(
            self.main,
            fg_color=self.CARD,
            corner_radius=18,
            border_width=1,
            border_color=self.BORDER
        )

        card.pack(
            fill="x",
            padx=self.PAGE_PAD_X,
            pady=(12, 8)
        )

        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=22,
            pady=(20, 8)
        )

        title_area = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_area.pack(
            side="left"
        )

        title = ctk.CTkLabel(
            title_area,
            text="Q02 Performance",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            title_area,
            text="Performance improvements built into this hospital system",
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=9
            )
        )

        subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        badge = ctk.CTkLabel(
            header,
            text="QUALITY GOAL  •  IMPROVE PERFORMANCE",
            text_color=self.PRIMARY,
            fg_color=self.PRIMARY_SOFT,
            corner_radius=7,
            font=ctk.CTkFont(
                size=8,
                weight="bold"
            )
        )

        badge.pack(
            side="right",
            pady=1
        )

        features = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        features.pack(
            fill="x",
            padx=16,
            pady=(2, 20)
        )

        for column in range(4):

            features.grid_columnconfigure(
                column,
                weight=1,
                uniform="quality"
            )

        feature_data = [
            (
                "01",
                "Fast Search",
                "Patient lookup by name, ID or phone",
                self.PRIMARY
            ),
            (
                "02",
                "Optimized Reports",
                "Faster report-oriented database queries",
                self.PURPLE
            ),
            (
                "03",
                "Duplicate Prevention",
                "Unique patient phone constraint",
                self.GREEN
            ),
            (
                "04",
                "CSV Import",
                "Bulk patient record workflow",
                self.ORANGE
            )
        ]

        for column, data in enumerate(feature_data):

            self.create_quality_feature(
                features,
                data,
                column
            )

    def create_quality_feature(
        self,
        parent,
        data,
        column
    ):

        number, title, description, accent = data

        item = ctk.CTkFrame(
            parent,
            fg_color=self.CARD_SOFT,
            corner_radius=12,
            border_width=1,
            border_color="#EEF1F5"
        )

        item.grid(
            row=0,
            column=column,
            padx=4,
            pady=4,
            sticky="nsew"
        )

        top = ctk.CTkFrame(
            item,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=13,
            pady=(12, 7)
        )

        number_label = ctk.CTkLabel(
            top,
            text=number,
            text_color=accent,
            font=ctk.CTkFont(
                size=9,
                weight="bold"
            )
        )

        number_label.pack(
            side="left"
        )

        active = ctk.CTkLabel(
            top,
            text="ACTIVE",
            text_color=self.GREEN_DARK,
            fg_color=self.GREEN_SOFT,
            corner_radius=5,
            font=ctk.CTkFont(
                size=7,
                weight="bold"
            )
        )

        active.pack(
            side="right"
        )

        title_label = ctk.CTkLabel(
            item,
            text=title,
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        )

        title_label.pack(
            anchor="w",
            padx=13
        )

        description_label = ctk.CTkLabel(
            item,
            text=description,
            text_color=self.MUTED_TEXT,
            font=ctk.CTkFont(
                size=8
            ),
            justify="left",
            wraplength=180
        )

        description_label.pack(
            anchor="w",
            padx=13,
            pady=(3, 13)
        )

    # =========================================================
    # FOOTER
    # =========================================================

    def create_footer(self):

        footer = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        footer.pack(
            fill="x",
            padx=self.PAGE_PAD_X,
            pady=(3, self.PAGE_PAD_BOTTOM)
        )

        left = ctk.CTkLabel(
            footer,
            text="MediCare  •  Hospital Management System",
            text_color=self.MUTED_TEXT,
            font=ctk.CTkFont(
                size=9
            )
        )

        left.pack(
            side="left"
        )

        right = ctk.CTkLabel(
            footer,
            text="Q02  •  Performance dashboard",
            text_color=self.MUTED_TEXT,
            font=ctk.CTkFont(
                size=9
            )
        )

        right.pack(
            side="right"
        )

    # =========================================================
    # ANIMATIONS
    # =========================================================

    def start_entrance_animation(self):

        self.animate_kpi(
            "patients",
            delay=0
        )

        self.animate_kpi(
            "appointments",
            delay=90
        )

        self.animate_kpi(
            "pending",
            delay=180
        )

        self.animate_kpi(
            "beds",
            delay=270
        )

    def animate_kpi(
        self,
        key,
        delay=0
    ):

        if key not in self.kpi_value_labels:
            return

        label, target = self.kpi_value_labels[key]

        steps = 20

        for step in range(steps + 1):

            self.after(
                delay + step * 25,
                lambda progress=step / steps,
                       widget=label,
                       value=target:
                    self.update_kpi_animation(
                        widget,
                        value,
                        progress
                    )
            )

    def update_kpi_animation(
        self,
        widget,
        target,
        progress
    ):

        eased = 1 - ((1 - progress) ** 3)

        current = int(
            target * eased
        )

        widget.configure(
            text=f"{current:,}"
        )

    # =========================================================
    # ANIMATION CLEANUP
    # =========================================================

    def cancel_chart_animation(self):

        for job in self.chart_animation_jobs:

            try:
                self.after_cancel(job)

            except Exception:
                pass

        self.chart_animation_jobs = []

    def cancel_animations(self):

        self.cancel_chart_animation()

        # We intentionally do not try to cancel every generic
        # after() call from child widgets because the complete
        # dashboard is destroyed during refresh. The Tk widgets
        # are then removed together safely.

    # =========================================================
    # INTERACTION HELPERS
    # =========================================================

    def bind_recursive(
        self,
        widget,
        event,
        command
    ):

        widget.bind(
            event,
            command,
            add="+"
        )

        for child in widget.winfo_children():

            try:

                self.bind_recursive(
                    child,
                    event,
                    command
                )

            except Exception:
                pass

    def go_patients(self):

        try:

            if hasattr(
                self.window,
                "show_patients"
            ):
                self.window.show_patients()

        except Exception as error:

            messagebox.showerror(
                "Navigation Error",
                f"Unable to open Patients.\n\n{error}"
            )

    def go_appointments(self):

        try:

            if hasattr(
                self.window,
                "show_appointments"
            ):
                self.window.show_appointments()

        except Exception as error:

            messagebox.showerror(
                "Navigation Error",
                f"Unable to open Appointments.\n\n{error}"
            )

    def go_reports(self):

        try:

            if hasattr(
                self.window,
                "show_reports"
            ):
                self.window.show_reports()

        except Exception as error:

            messagebox.showerror(
                "Navigation Error",
                f"Unable to open Reports.\n\n{error}"
            )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_dashboard(self):

        if self.refresh_button:

            try:

                self.refresh_button.configure(
                    state="disabled",
                    text="↻  Updating..."
                )

            except Exception:
                pass

        self.cancel_animations()

        # Small visual delay makes the refresh interaction
        # feel deliberate without blocking the UI.
        self.after(
            140,
            self.rebuild_dashboard
        )

    def rebuild_dashboard(self):

        for widget in self.winfo_children():

            try:
                widget.destroy()

            except Exception:
                pass

        self.kpi_value_labels = {}
        self.kpi_sub_labels = {}
        self.occupancy_canvas = None
        self.occupancy_arc = None
        self.flow_canvas = None
        self.flow_bars = []
        self.wait_value_label = None
        self.refresh_button = None

        self.create_widgets()
