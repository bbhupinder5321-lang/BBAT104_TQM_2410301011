import customtkinter as ctk
from tkinter import messagebox


from app.services.dashboard_service import DashboardService


class DashboardFrame(ctk.CTkFrame):

    # =========================================================
    # COLORS
    # =========================================================

    SIDEBAR = "#111827"
    SIDEBAR_HOVER = "#1F2937"

    BACKGROUND = "#F4F7FB"
    CARD = "#FFFFFF"

    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"

    TEXT = "#111827"
    SECONDARY_TEXT = "#6B7280"
    BORDER = "#E5E7EB"

    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, parent, user=None):

        super().__init__(
            parent,
            fg_color=self.BACKGROUND
        )

        self.user = user or {
            "username": "admin",
            "role": "admin"
        }

        self.service = DashboardService()

        self.metrics = {}

        self.create_widgets()

    # =========================================================
    # MAIN UI
    # =========================================================

    def create_widgets(self):

        # Main scroll area
        self.main = ctk.CTkScrollableFrame(
            self,
            fg_color=self.BACKGROUND,
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0
        )

        self.load_metrics()

        self.create_header()

        self.create_stat_cards()

        self.create_middle_section()

        self.create_bottom_section()

    # =========================================================
    # LOAD DATA
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
                f"Unable to load dashboard:\n{error}"
            )

            self.metrics = {
                "today_patients": 0,
                "today_appointments": 0,
                "pending_appointments": 0,
                "total_beds": 0,
                "occupied_beds": 0,
                "average_waiting_seconds": 0
            }

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self.main,
            fg_color=self.BACKGROUND
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        # Left side
        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.pack(
            side="left"
        )

        title = ctk.CTkLabel(
            left,
            text="Dashboard",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            left,
            text=(
                "Welcome back! Here's what's happening "
                "in your hospital today."
            ),
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=14
            )
        )

        subtitle.pack(
            anchor="w",
            pady=(4, 0)
        )

        # Right side
        right = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        right.pack(
            side="right"
        )

        username = self.user.get(
            "username",
            "admin"
        )

        role = self.user.get(
            "role",
            "admin"
        )

        profile = ctk.CTkFrame(
            right,
            fg_color=self.CARD,
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER
        )

        profile.pack(
            padx=(10, 0),
            pady=2
        )

        avatar = ctk.CTkFrame(
            profile,
            width=38,
            height=38,
            corner_radius=19,
            fg_color=self.PRIMARY
        )

        avatar.pack(
            side="left",
            padx=(10, 8),
            pady=9
        )

        avatar.pack_propagate(False)

        avatar_label = ctk.CTkLabel(
            avatar,
            text=username[0].upper(),
            text_color="white",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        avatar_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        profile_text = ctk.CTkFrame(
            profile,
            fg_color="transparent"
        )

        profile_text.pack(
            side="left",
            padx=(0, 15),
            pady=8
        )

        name_label = ctk.CTkLabel(
            profile_text,
            text=username,
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        name_label.pack(
            anchor="w"
        )

        role_label = ctk.CTkLabel(
            profile_text,
            text=f"{role.title()}",
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=10
            )
        )

        role_label.pack(
            anchor="w"
        )

    # =========================================================
    # STAT CARDS
    # =========================================================

    def create_stat_cards(self):

        cards_container = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        cards_container.pack(
            fill="x",
            padx=30,
            pady=5
        )

        for column in range(4):

            cards_container.grid_columnconfigure(
                column,
                weight=1
            )

        cards = [
            (
                "Patients",
                self.metrics["today_patients"],
                "Registered today",
                "P",
                self.PRIMARY
            ),
            (
                "Appointments",
                self.metrics["today_appointments"],
                "Scheduled today",
                "A",
                "#7C3AED"
            ),
            (
                "Pending",
                self.metrics["pending_appointments"],
                "Awaiting consultation",
                "W",
                self.WARNING
            ),
            (
                "Beds",
                self.metrics["total_beds"],
                "Total hospital beds",
                "B",
                self.SUCCESS
            )
        ]

        for column, data in enumerate(cards):

            self.create_stat_card(
                cards_container,
                data,
                column
            )

    def create_stat_card(
        self,
        parent,
        data,
        column
    ):

        title, value, description, icon_text, accent = data

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=column,
            padx=6,
            pady=6,
            sticky="nsew"
        )

        # Top row
        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=18,
            pady=(18, 8)
        )

        icon = ctk.CTkFrame(
            top,
            width=42,
            height=42,
            corner_radius=11,
            fg_color=accent
        )

        icon.pack(
            side="left"
        )

        icon.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            icon,
            text=icon_text,
            text_color="white",
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

        # Value
        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=29,
                weight="bold"
            )
        )

        value_label.pack(
            anchor="w",
            padx=18
        )

        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        title_label.pack(
            anchor="w",
            padx=18
        )

        # Description
        description_label = ctk.CTkLabel(
            card,
            text=description,
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=10
            )
        )

        description_label.pack(
            anchor="w",
            padx=18,
            pady=(2, 18)
        )

    # =========================================================
    # MIDDLE SECTION
    # =========================================================

    def create_middle_section(self):

        middle = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        middle.pack(
            fill="x",
            padx=30,
            pady=(18, 8)
        )

        middle.grid_columnconfigure(
            0,
            weight=3
        )

        middle.grid_columnconfigure(
            1,
            weight=2
        )

        self.create_waiting_card(
            middle
        )

        self.create_bed_card(
            middle
        )

    # =========================================================
    # WAITING TIME
    # =========================================================

    def create_waiting_card(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=0,
            padx=(0, 7),
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
            text="Patient Waiting Time",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.pack(
            side="left"
        )

        badge = ctk.CTkLabel(
            header,
            text="Q02",
            text_color=self.PRIMARY,
            fg_color="#EFF6FF",
            corner_radius=7,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            padx=8,
            pady=4
        )

        badge.pack(
            side="right"
        )

        wait_time = self.service.format_waiting_time(
            self.metrics[
                "average_waiting_seconds"
            ]
        )

        value = ctk.CTkLabel(
            card,
            text=wait_time,
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=34,
                weight="bold"
            )
        )

        value.pack(
            anchor="w",
            padx=22,
            pady=(20, 0)
        )

        description = ctk.CTkLabel(
            card,
            text=(
                "Average time from patient check-in "
                "until consultation begins."
            ),
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=11
            )
        )

        description.pack(
            anchor="w",
            padx=22,
            pady=(2, 20)
        )

    # =========================================================
    # BED OCCUPANCY
    # =========================================================

    def create_bed_card(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=1,
            padx=(7, 0),
            sticky="nsew"
        )

        title = ctk.CTkLabel(
            card,
            text="Bed Occupancy",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=22,
            pady=(20, 10)
        )

        occupied = self.metrics[
            "occupied_beds"
        ]

        total = self.metrics[
            "total_beds"
        ]

        percentage = (
            self.service
            .get_bed_occupancy_percentage(
                occupied,
                total
            )
        )

        percentage_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        percentage_frame.pack(
            fill="x",
            padx=22
        )

        percentage_label = ctk.CTkLabel(
            percentage_frame,
            text=f"{percentage}%",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        percentage_label.pack(
            side="left"
        )

        occupancy_text = ctk.CTkLabel(
            percentage_frame,
            text=f"{occupied} / {total} beds",
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=11
            )
        )

        occupancy_text.pack(
            side="right",
            pady=(10, 0)
        )

        progress = ctk.CTkProgressBar(
            card,
            height=10,
            corner_radius=5,
            progress_color=self.SUCCESS,
            fg_color="#E5E7EB"
        )

        progress.pack(
            fill="x",
            padx=22,
            pady=(12, 5)
        )

        progress.set(
            percentage / 100
            if total > 0
            else 0
        )

        description = ctk.CTkLabel(
            card,
            text="Current hospital bed utilization",
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=10
            )
        )

        description.pack(
            anchor="w",
            padx=22,
            pady=(2, 20)
        )

    # =========================================================
    # BOTTOM SECTION
    # =========================================================

    def create_bottom_section(self):

        bottom = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            padx=30,
            pady=(8, 25)
        )

        bottom.grid_columnconfigure(
            0,
            weight=1
        )

        bottom.grid_columnconfigure(
            1,
            weight=1
        )

        # Quick actions
        self.create_quick_actions(
            bottom
        )

        # System performance
        self.create_performance_card(
            bottom
        )

    # =========================================================
    # QUICK ACTIONS
    # =========================================================

    def create_quick_actions(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=0,
            padx=(0, 7),
            sticky="nsew"
        )

        title = ctk.CTkLabel(
            card,
            text="Quick Actions",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=22,
            pady=(20, 12)
        )

        buttons = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=18,
            pady=(0, 20)
        )

        buttons.grid_columnconfigure(
            0,
            weight=1
        )

        buttons.grid_columnconfigure(
            1,
            weight=1
        )

        add_patient = ctk.CTkButton(
            buttons,
            text="+  Add Patient",
            height=38,
            corner_radius=9,
            fg_color=self.PRIMARY,
            hover_color=self.PRIMARY_HOVER,
            command=self.show_not_available
        )

        add_patient.grid(
            row=0,
            column=0,
            padx=4,
            pady=4,
            sticky="ew"
        )

        refresh = ctk.CTkButton(
            buttons,
            text="↻  Refresh",
            height=38,
            corner_radius=9,
            fg_color="#E8EEF7",
            hover_color="#DCE5F2",
            text_color=self.TEXT,
            command=self.refresh_dashboard
        )

        refresh.grid(
            row=0,
            column=1,
            padx=4,
            pady=4,
            sticky="ew"
        )

    # =========================================================
    # SYSTEM PERFORMANCE
    # =========================================================

    def create_performance_card(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=1,
            padx=(7, 0),
            sticky="nsew"
        )

        title = ctk.CTkLabel(
            card,
            text="System Performance",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=22,
            pady=(20, 4)
        )

        status = ctk.CTkLabel(
            card,
            text="●  System operating normally",
            text_color=self.SUCCESS,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        status.pack(
            anchor="w",
            padx=22,
            pady=(0, 5)
        )

        description = ctk.CTkLabel(
            card,
            text=(
                "Optimized SQL queries and database "
                "indexes are enabled for Q02."
            ),
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=11
            ),
            justify="left"
        )

        description.pack(
            anchor="w",
            padx=22,
            pady=(0, 20)
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_dashboard(self):

        for widget in self.winfo_children():
            widget.destroy()

        self.create_widgets()

    # =========================================================
    # TEMPORARY QUICK ACTION
    # =========================================================

    def show_not_available(self):

        messagebox.showinfo(
            "Quick Action",
            "Use the Patients section to add a new patient."
        )