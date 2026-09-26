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

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.title("Hospital Management System")
        self.geometry("1280x760")
        self.minsize(1100, 650)

        # Slightly darker background gives the
        # application a more professional appearance.
        ctk.set_appearance_mode("dark")

        self.create_layout()
        self.show_dashboard()

    # =========================================================
    # MAIN LAYOUT
    # =========================================================

    def create_layout(self):

        # -----------------------------------------------------
        # SIDEBAR
        # -----------------------------------------------------

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # Application branding
        brand_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        brand_frame.pack(
            fill="x",
            padx=20,
            pady=(28, 10)
        )

        hospital_icon = ctk.CTkLabel(
            brand_frame,
            text="✚",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        hospital_icon.pack(
            anchor="w"
        )

        title_label = ctk.CTkLabel(
            brand_frame,
            text="Hospital\nManagement",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            ),
            justify="left"
        )

        title_label.pack(
            anchor="w",
            pady=(4, 0)
        )

        subtitle_label = ctk.CTkLabel(
            brand_frame,
            text="TQM Performance System",
            font=ctk.CTkFont(size=11)
        )

        subtitle_label.pack(
            anchor="w",
            pady=(3, 0)
        )

        # -----------------------------------------------------
        # USER CARD
        # -----------------------------------------------------

        user_card = ctk.CTkFrame(
            self.sidebar,
            corner_radius=12
        )

        user_card.pack(
            fill="x",
            padx=15,
            pady=(15, 18)
        )

        username = self.user.get(
            "username",
            "admin"
        )

        role = self.user.get(
            "role",
            "admin"
        )

        user_icon = ctk.CTkLabel(
            user_card,
            text="●",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )

        user_icon.pack(
            side="left",
            padx=(12, 8),
            pady=12
        )

        user_text = ctk.CTkFrame(
            user_card,
            fg_color="transparent"
        )

        user_text.pack(
            side="left",
            pady=9
        )

        user_name_label = ctk.CTkLabel(
            user_text,
            text=username,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        user_name_label.pack(
            anchor="w"
        )

        role_label = ctk.CTkLabel(
            user_text,
            text=f"{role.title()} Account",
            font=ctk.CTkFont(size=10)
        )

        role_label.pack(
            anchor="w"
        )

        # -----------------------------------------------------
        # NAVIGATION LABEL
        # -----------------------------------------------------

        navigation_label = ctk.CTkLabel(
            self.sidebar,
            text="MAIN MENU",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        )

        navigation_label.pack(
            anchor="w",
            padx=22,
            pady=(0, 8)
        )

        # -----------------------------------------------------
        # NAVIGATION BUTTONS
        # -----------------------------------------------------

        self.create_sidebar_button(
            "Dashboard",
            self.show_dashboard
        )

        self.create_sidebar_button(
            "Patients",
            self.show_patients
        )

        self.create_sidebar_button(
            "Doctors",
            self.show_doctors
        )

        self.create_sidebar_button(
            "Appointments",
            self.show_appointments
        )

        self.create_sidebar_button(
            "Billing",
            self.show_billing
        )

        self.create_sidebar_button(
            "CSV Import",
            self.show_csv_import
        )

        self.create_sidebar_button(
            "Reports",
            self.show_reports
        )

        self.create_sidebar_button(
            "Performance",
            self.show_performance
        )

        # TQM Analysis
        self.create_sidebar_button(
            "TQM Analysis",
            self.show_tqm
        )

        # -----------------------------------------------------
        # SPACER
        # -----------------------------------------------------

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        spacer.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # LOGOUT
        # -----------------------------------------------------

        logout_button = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            height=40,
            corner_radius=9,
            command=self.logout
        )

        logout_button.pack(
            fill="x",
            padx=18,
            pady=(5, 20)
        )

        # -----------------------------------------------------
        # CONTENT AREA
        # -----------------------------------------------------

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

    # =========================================================
    # SIDEBAR BUTTON
    # =========================================================

    def create_sidebar_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=38,
            corner_radius=8,
            anchor="w",
            command=command
        )

        button.pack(
            fill="x",
            padx=18,
            pady=3
        )

    # =========================================================
    # CLEAR CONTENT
    # =========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.clear_content()

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

        self.clear_content()

        patient_frame = PatientFrame(
            self.content
        )

        patient_frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # DOCTORS
    # =========================================================

    def show_doctors(self):

        self.clear_content()

        doctor_frame = DoctorFrame(
            self.content
        )

        doctor_frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # APPOINTMENTS
    # =========================================================

    def show_appointments(self):

        self.clear_content()

        appointment_frame = AppointmentFrame(
            self.content
        )

        appointment_frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # BILLING
    # =========================================================

    def show_billing(self):

        self.clear_content()

        billing_frame = BillingFrame(
            self.content
        )

        billing_frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # CSV IMPORT
    # =========================================================

    def show_csv_import(self):

        self.clear_content()

        csv_frame = CSVImportFrame(
            self.content
        )

        csv_frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # REPORTS
    # =========================================================

    def show_reports(self):

        self.clear_content()

        report_frame = ReportFrame(
            self.content
        )

        report_frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # PERFORMANCE
    # =========================================================

    def show_performance(self):

        self.clear_content()

        performance_frame = PerformanceFrame(
            self.content
        )

        performance_frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # TQM ANALYSIS
    # =========================================================

    def show_tqm(self):

        self.clear_content()

        tqm_frame = TQMFrame(
            self.content
        )

        tqm_frame.pack(
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


# =============================================================
# APPLICATION ENTRY POINT
# =============================================================

def main():

    # Development user.
    # Login integration can be connected here later.

    user = {
        "user_id": 1,
        "username": "admin",
        "role": "admin"
    }

    app = MainApplication(user)

    app.mainloop()


if __name__ == "__main__":
    main()