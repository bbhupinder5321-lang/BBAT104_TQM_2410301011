import customtkinter as ctk
from tkinter import messagebox

from app.services.dashboard_service import DashboardService


class DashboardWindow(ctk.CTk):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.dashboard_service = DashboardService()

        self.title("Hospital Management System")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color="#F4F7FB")

        self.create_layout()
        self.load_dashboard()

    # ---------------------------------------------------------
    # MAIN LAYOUT
    # ---------------------------------------------------------

    def create_layout(self):

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color="#172033"
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # Main content
        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#F4F7FB"
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()
        self.create_dashboard_header()
        self.create_metric_cards()

    # ---------------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------------

    def create_sidebar(self):

        # Hospital title
        hospital_title = ctk.CTkLabel(
            self.sidebar,
            text="HOSPITAL",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color="white"
        )

        hospital_title.pack(
            pady=(35, 0)
        )

        system_title = ctk.CTkLabel(
            self.sidebar,
            text="Management System",
            font=ctk.CTkFont(size=12),
            text_color="#AEB8CC"
        )

        system_title.pack(
            pady=(0, 35)
        )

        # Navigation buttons
        self.create_nav_button(
            "▣   Dashboard",
            self.show_dashboard
        )

        self.create_nav_button(
            "●   Patients",
            self.module_not_ready
        )

        self.create_nav_button(
            "◉   Doctors",
            self.module_not_ready
        )

        self.create_nav_button(
            "▤   Appointments",
            self.module_not_ready
        )

        self.create_nav_button(
            "₹   Billing",
            self.module_not_ready
        )

        self.create_nav_button(
            "⇩   CSV Import",
            self.module_not_ready
        )

        self.create_nav_button(
            "▥   Reports",
            self.module_not_ready
        )

        self.create_nav_button(
            "◈   Performance",
            self.module_not_ready
        )

        # Bottom user section
        self.user_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="#202B40",
            corner_radius=12
        )

        self.user_frame.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=15
        )

        username = self.user.get(
            "username",
            "User"
        )

        role = self.user.get(
            "role",
            "staff"
        )

        self.user_label = ctk.CTkLabel(
            self.user_frame,
            text=username,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color="white"
        )

        self.user_label.pack(
            anchor="w",
            padx=15,
            pady=(12, 0)
        )

        self.role_label = ctk.CTkLabel(
            self.user_frame,
            text=role.title(),
            font=ctk.CTkFont(size=11),
            text_color="#AEB8CC"
        )

        self.role_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

        self.logout_button = ctk.CTkButton(
            self.user_frame,
            text="Logout",
            height=32,
            corner_radius=8,
            fg_color="#37445D",
            hover_color="#4A5872",
            command=self.logout
        )

        self.logout_button.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

    def create_nav_button(self, text, command):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            anchor="w",
            height=45,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#26344D",
            text_color="#E7EBF3",
            font=ctk.CTkFont(size=13),
            command=command
        )

        button.pack(
            fill="x",
            padx=12,
            pady=3
        )

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    def create_dashboard_header(self):

        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )

        title = ctk.CTkLabel(
            header,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color="#172033"
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Hospital performance overview",
            font=ctk.CTkFont(size=13),
            text_color="#6B7280"
        )

        subtitle.pack(
            anchor="w",
            pady=(2, 0)
        )

        self.refresh_button = ctk.CTkButton(
            header,
            text="↻  Refresh",
            width=100,
            height=35,
            corner_radius=8,
            command=self.load_dashboard
        )

        self.refresh_button.place(
            relx=1.0,
            y=5,
            anchor="ne"
        )

    # ---------------------------------------------------------
    # METRIC CARDS
    # ---------------------------------------------------------

    def create_metric_cards(self):

        self.cards_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.cards_frame.pack(
            fill="x",
            padx=30,
            pady=(10, 20)
        )

        for column in range(4):
            self.cards_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.patient_card = self.create_metric_card(
            self.cards_frame,
            0,
            "Today's Patients",
            "0"
        )

        self.appointment_card = self.create_metric_card(
            self.cards_frame,
            1,
            "Today's Appointments",
            "0"
        )

        self.pending_card = self.create_metric_card(
            self.cards_frame,
            2,
            "Pending Appointments",
            "0"
        )

        self.waiting_card = self.create_metric_card(
            self.cards_frame,
            3,
            "Average Waiting",
            "0 min"
        )

    def create_metric_card(
        self,
        parent,
        column,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            height=130,
            corner_radius=15,
            fg_color="white"
        )

        card.grid(
            row=0,
            column=column,
            padx=7,
            sticky="nsew"
        )

        card.grid_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        )

        title_label.pack(
            anchor="w",
            padx=18,
            pady=(20, 3)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            ),
            text_color="#172033"
        )

        value_label.pack(
            anchor="w",
            padx=18
        )

        return value_label

    # ---------------------------------------------------------
    # DASHBOARD DATA
    # ---------------------------------------------------------

    def load_dashboard(self):

        try:

            metrics = self.dashboard_service.get_dashboard_metrics()

            self.patient_card.configure(
                text=str(metrics["today_patients"])
            )

            self.appointment_card.configure(
                text=str(metrics["today_appointments"])
            )

            self.pending_card.configure(
                text=str(metrics["pending_appointments"])
            )

            self.waiting_card.configure(
                text=self.dashboard_service.format_waiting_time(
                    metrics["average_waiting_seconds"]
                )
            )

            self.create_lower_dashboard(metrics)

        except Exception as error:

            messagebox.showerror(
                "Dashboard Error",
                str(error)
            )

    # ---------------------------------------------------------
    # LOWER DASHBOARD
    # ---------------------------------------------------------

    def create_lower_dashboard(self, metrics):

        if hasattr(self, "lower_frame"):
            self.lower_frame.destroy()

        self.lower_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.lower_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 30)
        )

        self.lower_frame.grid_columnconfigure(
            0,
            weight=2
        )

        self.lower_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.lower_frame.grid_rowconfigure(
            0,
            weight=1
        )

        # Performance panel
        performance_card = ctk.CTkFrame(
            self.lower_frame,
            corner_radius=15,
            fg_color="white"
        )

        performance_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        performance_title = ctk.CTkLabel(
            performance_card,
            text="Performance Overview",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#172033"
        )

        performance_title.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        performance_subtitle = ctk.CTkLabel(
            performance_card,
            text="Key indicators for the Q02 performance goal",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        )

        performance_subtitle.pack(
            anchor="w",
            padx=25
        )

        self.create_performance_row(
            performance_card,
            "Average patient waiting time",
            self.dashboard_service.format_waiting_time(
                metrics["average_waiting_seconds"]
            )
        )

        self.create_performance_row(
            performance_card,
            "Today's appointment workload",
            str(metrics["today_appointments"])
        )

        self.create_performance_row(
            performance_card,
            "Pending appointments",
            str(metrics["pending_appointments"])
        )

        # Bed occupancy panel
        bed_card = ctk.CTkFrame(
            self.lower_frame,
            corner_radius=15,
            fg_color="white"
        )

        bed_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        bed_title = ctk.CTkLabel(
            bed_card,
            text="Bed Occupancy",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#172033"
        )

        bed_title.pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )

        occupied = metrics["occupied_beds"]
        total = metrics["total_beds"]

        percentage = self.dashboard_service.get_bed_occupancy_percentage(
            occupied,
            total
        )

        bed_value = ctk.CTkLabel(
            bed_card,
            text=f"{percentage}%",
            font=ctk.CTkFont(
                size=36,
                weight="bold"
            ),
            text_color="#172033"
        )

        bed_value.pack(
            pady=(15, 5)
        )

        bed_detail = ctk.CTkLabel(
            bed_card,
            text=f"{occupied} occupied / {total} total beds",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        )

        bed_detail.pack()

    def create_performance_row(
        self,
        parent,
        label,
        value
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="#F7F9FC",
            corner_radius=10,
            height=55
        )

        frame.pack(
            fill="x",
            padx=25,
            pady=7
        )

        frame.pack_propagate(False)

        label_widget = ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=12),
            text_color="#4B5563"
        )

        label_widget.pack(
            side="left",
            padx=15
        )

        value_widget = ctk.CTkLabel(
            frame,
            text=value,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color="#172033"
        )

        value_widget.pack(
            side="right",
            padx=15
        )

    # ---------------------------------------------------------
    # NAVIGATION
    # ---------------------------------------------------------

    def show_dashboard(self):
        self.load_dashboard()

    def module_not_ready(self):

        messagebox.showinfo(
            "Module",
            "This module will be connected to the main application next."
        )

    # ---------------------------------------------------------
    # LOGOUT
    # ---------------------------------------------------------

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if answer:
            self.destroy()


if __name__ == "__main__":

    test_user = {
        "user_id": 1,
        "username": "admin",
        "role": "admin"
    }

    app = DashboardWindow(test_user)
    app.mainloop()