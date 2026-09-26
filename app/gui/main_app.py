import customtkinter as ctk
from tkinter import messagebox


from app.gui.dashboard_frame import DashboardFrame
from app.gui.patient_frame import PatientFrame
from app.gui.doctor_frame import DoctorFrame
from app.gui.appointment_frame import AppointmentFrame
from app.gui.billing_frame import BillingFrame
from app.gui.csv_import_frame import CSVImportFrame
from app.gui.report_frame import ReportFrame
from app.gui.performance_frame import PerformanceFrame
from app.gui.tqm_frame import TQMFrame


class MainApplication(ctk.CTk):

    # =========================================================
    # MEDICARE HOSPITAL MANAGEMENT APPLICATION SHELL
    # =========================================================

    SIDEBAR = "#111827"
    SIDEBAR_HOVER = "#1F2937"
    SIDEBAR_ACTIVE = "#2563EB"

    CONTENT = "#F6F8FC"
    WHITE = "#FFFFFF"
    BORDER = "#263244"

    TEXT = "#F8FAFC"
    MUTED = "#94A3B8"

    GREEN = "#10B981"

    def __init__(self, user):

        super().__init__()

        self.user = user or {
            "user_id": 1,
            "username": "admin",
            "role": "admin"
        }

        self.role = self.user.get("role", "admin")

        self.ROLE_THEME = {
            "admin": {
                "accent": "#2563EB",
                "accent_hover": "#1D4ED8",
                "soft": "#EFF6FF",
                "workspace": "Administrator Console"
            },
            "staff": {
                "accent": "#10B981",
                "accent_hover": "#059669",
                "soft": "#ECFDF5",
                "workspace": "Staff Operations"
            }
        }.get(self.role, {
            "accent": "#2563EB",
            "accent_hover": "#1D4ED8",
            "soft": "#EFF6FF",
            "workspace": "Hospital Workspace"
        })

        self.title(
            f"MediCare  •  {self.ROLE_THEME['workspace']}"
        )

        self.geometry(
            "1440x900"
        )

        self.minsize(
            1180,
            760
        )

        ctk.set_appearance_mode(
            "light"
        )

        ctk.set_default_color_theme(
            "blue"
        )

        self.after(120, self._maximize_window)

        self.current_page = None
        self.sidebar_buttons = {}

        self.create_layout()

        self.show_dashboard()

    def _maximize_window(self):
        try:
            self.state("zoomed")
        except Exception:
            pass

    # =========================================================
    # APPLICATION LAYOUT
    # =========================================================

    def create_layout(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=244,
            corner_radius=0,
            fg_color=self.SIDEBAR
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )

        self.create_brand()

        self.create_user_card()

        self.create_navigation()

        self.create_sidebar_footer()

        # -----------------------------------------------------
        # CONTENT AREA
        # -----------------------------------------------------

        self.content_shell = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.CONTENT
        )

        self.content_shell.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.content = ctk.CTkFrame(
            self.content_shell,
            corner_radius=0,
            fg_color=self.CONTENT
        )

        self.content.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # BRAND
    # =========================================================

    def create_brand(self):

        brand = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        brand.pack(
            fill="x",
            padx=20,
            pady=(25, 10)
        )

        icon = ctk.CTkFrame(
            brand,
            width=44,
            height=44,
            corner_radius=13,
            fg_color=self.ROLE_THEME["accent"]
        )

        icon.pack(
            side="left"
        )

        icon.pack_propagate(
            False
        )

        icon_label = ctk.CTkLabel(
            icon,
            text="+",
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            )
        )

        icon_label.place(
            relx=0.5,
            rely=0.47,
            anchor="center"
        )

        text_area = ctk.CTkFrame(
            brand,
            fg_color="transparent"
        )

        text_area.pack(
            side="left",
            padx=(11, 0)
        )

        title = ctk.CTkLabel(
            text_area,
            text="MediCare",
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            text_area,
            text="Hospital Management",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=9
            )
        )

        subtitle.pack(
            anchor="w",
            pady=(1, 0)
        )

    # =========================================================
    # USER CARD
    # =========================================================

    def create_user_card(self):

        username = str(
            self.user.get(
                "username",
                "admin"
            )
        )

        role = str(
            self.user.get(
                "role",
                "admin"
            )
        )

        card = ctk.CTkFrame(
            self.sidebar,
            fg_color="#182234",
            corner_radius=14,
            border_width=1,
            border_color="#223047"
        )

        card.pack(
            fill="x",
            padx=15,
            pady=(12, 19)
        )

        avatar = ctk.CTkFrame(
            card,
            width=38,
            height=38,
            corner_radius=19,
            fg_color="#DBEAFE"
        )

        avatar.pack(
            side="left",
            padx=(11, 9),
            pady=11
        )

        avatar.pack_propagate(
            False
        )

        avatar_label = ctk.CTkLabel(
            avatar,
            text=username[:1].upper(),
            text_color="#1D4ED8",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        avatar_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        text_area = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        text_area.pack(
            side="left",
            pady=9
        )

        name = ctk.CTkLabel(
            text_area,
            text=username,
            text_color=self.WHITE,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        name.pack(
            anchor="w"
        )

        role_label = ctk.CTkLabel(
            text_area,
            text=f"{role.title()} account",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=9
            )
        )

        role_label.pack(
            anchor="w",
            pady=(2, 0)
        )

    # =========================================================
    # NAVIGATION
    # =========================================================

    def create_navigation(self):

        main_label = ctk.CTkLabel(
            self.sidebar,
            text="MAIN MENU",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=9,
                weight="bold"
            )
        )

        main_label.pack(
            anchor="w",
            padx=21,
            pady=(0, 7)
        )

        self.create_sidebar_button(
            "⌂",
            "Dashboard",
            self.show_dashboard,
            "dashboard"
        )

        self.create_sidebar_button(
            "♙",
            "Patients",
            self.show_patients,
            "manage_patients"
        )

        self.create_sidebar_button(
            "⚕",
            "Doctors",
            self.show_doctors,
            "manage_doctors"
        )

        self.create_sidebar_button(
            "◷",
            "Appointments",
            self.show_appointments,
            "manage_appointments"
        )

        self.create_sidebar_button(
            "▣",
            "Billing",
            self.show_billing,
            "manage_billing"
        )

        self.create_sidebar_button(
            "⇧",
            "CSV Import",
            self.show_csv_import,
            "import_csv"
        )

        self.create_sidebar_button(
            "▤",
            "Reports",
            self.show_reports,
            "view_reports"
        )

        self.create_sidebar_button(
            "⌁",
            "Performance",
            self.show_performance,
            "view_performance"
        )

        quality_label = ctk.CTkLabel(
            self.sidebar,
            text="QUALITY MANAGEMENT",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=9,
                weight="bold"
            )
        )

        quality_label.pack(
            anchor="w",
            padx=21,
            pady=(17, 7)
        )

        self.create_sidebar_button(
            "✓",
            "TQM Analysis",
            self.show_tqm,
            "view_reports"
        )

    def create_sidebar_button(
        self,
        icon,
        text,
        command,
        permission
    ):

        role = self.user.get(
            "role",
            "admin"
        )

        allowed = self.has_permission(
            role,
            permission
        )

        if not allowed:
            return

        button = ctk.CTkButton(
            self.sidebar,
            text=f"  {icon}     {text}",
            height=40,
            corner_radius=10,
            anchor="w",
            fg_color="transparent",
            hover_color=self.ROLE_THEME["accent_hover"],
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=lambda name=text,
                   action=command:
                self.navigate(
                    name,
                    action
                )
        )

        button.pack(
            fill="x",
            padx=13,
            pady=2
        )

        def on_enter(_event):
            if self.current_page != text:
                button.configure(
                    fg_color=self.SIDEBAR_HOVER,
                    text_color=self.WHITE
                )

        def on_leave(_event):
            if self.current_page != text:
                button.configure(
                    fg_color="transparent",
                    text_color="#CBD5E1"
                )

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        self.sidebar_buttons[text] = button

    def has_permission(
        self,
        role,
        permission
    ):

        permissions = {

            "admin": {
                "dashboard",
                "manage_patients",
                "manage_doctors",
                "manage_appointments",
                "manage_billing",
                "import_csv",
                "view_reports",
                "view_performance"
            },

            "staff": {
                "dashboard",
                "manage_patients",
                "manage_appointments",
                "manage_billing",
                "view_reports"
            }
        }

        return permission in permissions.get(
            role,
            set()
        )

    # =========================================================
    # SIDEBAR FOOTER
    # =========================================================

    def create_sidebar_footer(self):

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        spacer.pack(
            fill="both",
            expand=True
        )

        system = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        system.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        dot = ctk.CTkLabel(
            system,
            text="●",
            text_color=self.GREEN,
            font=ctk.CTkFont(
                size=9
            )
        )

        dot.pack(
            side="left"
        )

        status = ctk.CTkLabel(
            system,
            text=" System online",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=9
            )
        )

        status.pack(
            side="left"
        )

        logout = ctk.CTkButton(
            self.sidebar,
            text="⇥   Logout",
            height=40,
            corner_radius=10,
            anchor="w",
            fg_color="#182234",
            hover_color="#273449",
            text_color="#E2E8F0",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=self.logout
        )

        logout.pack(
            fill="x",
            padx=13,
            pady=(0, 18)
        )

    # =========================================================
    # NAVIGATION ENGINE
    # =========================================================

    def navigate(
        self,
        name,
        command
    ):

        self.set_active_navigation(
            name
        )

        command()

    def set_active_navigation(
        self,
        active_name
    ):

        for name, button in self.sidebar_buttons.items():

            if name == active_name:

                button.configure(
                    fg_color=self.ROLE_THEME["accent"],
                    text_color=self.WHITE
                )

            else:

                button.configure(
                    fg_color="transparent",
                    text_color="#CBD5E1"
                )

        self.current_page = active_name

    # =========================================================
    # CLEAR CONTENT
    # =========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():

            try:
                widget.destroy()

            except Exception:
                pass

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.clear_content()

        self.set_active_navigation(
            "Dashboard"
        )

        dashboard = DashboardFrame(
            self.content,
            self.user
        )

        dashboard.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # PATIENTS
    # =========================================================

    def show_patients(self):

        if not self.has_permission(
            self.user.get("role", "admin"),
            "manage_patients"
        ):
            return

        self.clear_content()

        self.set_active_navigation(
            "Patients"
        )

        frame = PatientFrame(
            self.content
        )

        frame.user = self.user
        frame.role = self.role

        frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # DOCTORS
    # =========================================================

    def show_doctors(self):

        if not self.has_permission(
            self.user.get("role", "admin"),
            "manage_doctors"
        ):
            return

        self.clear_content()

        self.set_active_navigation(
            "Doctors"
        )

        frame = DoctorFrame(
            self.content
        )

        frame.user = self.user
        frame.role = self.role

        frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # APPOINTMENTS
    # =========================================================

    def show_appointments(self):

        if not self.has_permission(
            self.user.get("role", "admin"),
            "manage_appointments"
        ):
            return

        self.clear_content()

        self.set_active_navigation(
            "Appointments"
        )

        frame = AppointmentFrame(
            self.content
        )

        frame.user = self.user
        frame.role = self.role

        frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # BILLING
    # =========================================================

    def show_billing(self):

        if not self.has_permission(
            self.user.get("role", "admin"),
            "manage_billing"
        ):
            return

        self.clear_content()

        self.set_active_navigation(
            "Billing"
        )

        frame = BillingFrame(
            self.content
        )

        frame.user = self.user
        frame.role = self.role

        frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # CSV IMPORT
    # =========================================================

    def show_csv_import(self):

        if not self.has_permission(
            self.user.get("role", "admin"),
            "import_csv"
        ):
            return

        self.clear_content()

        self.set_active_navigation(
            "CSV Import"
        )

        frame = CSVImportFrame(
            self.content
        )

        frame.user = self.user
        frame.role = self.role

        frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # REPORTS
    # =========================================================

    def show_reports(self):

        if not self.has_permission(
            self.user.get("role", "admin"),
            "view_reports"
        ):
            return

        self.clear_content()

        self.set_active_navigation(
            "Reports"
        )

        frame = ReportFrame(
            self.content
        )

        frame.user = self.user
        frame.role = self.role

        frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # PERFORMANCE
    # =========================================================

    def show_performance(self):

        if not self.has_permission(
            self.user.get("role", "admin"),
            "view_performance"
        ):
            return

        self.clear_content()

        self.set_active_navigation(
            "Performance"
        )

        frame = PerformanceFrame(
            self.content
        )

        frame.user = self.user
        frame.role = self.role

        frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # TQM
    # =========================================================

    def show_tqm(self):

        if not self.has_permission(
            self.user.get("role", "admin"),
            "view_reports"
        ):
            return

        self.clear_content()

        self.set_active_navigation(
            "TQM Analysis"
        )

        frame = TQMFrame(
            self.content
        )

        frame.user = self.user
        frame.role = self.role

        frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if not answer:
            return

        self.destroy()

        from app.gui.login_gui import LoginWindow

        login = LoginWindow()
        login.mainloop()


# =============================================================
# DEVELOPMENT ENTRY POINT
# =============================================================

def main():

    user = {
        "user_id": 1,
        "username": "admin",
        "role": "admin"
    }

    app = MainApplication(
        user
    )

    app.mainloop()


if __name__ == "__main__":
    main()
