import customtkinter as ctk
from tkinter import ttk, messagebox

from app.services.report_service import ReportService


class ReportFrame(ctk.CTkFrame):

    BACKGROUND = "#F6F8FC"
    CARD = "#FFFFFF"
    BORDER = "#E6EAF0"
    TEXT_DARK = "#0F172A"
    SECONDARY = "#64748B"
    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color=self.BACKGROUND
        )

        self.service = ReportService()

        self.create_ui()
        self.load_reports()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def create_ui(self):

        # Page title
        title = ctk.CTkLabel(
            self,
            text="Hospital Reports",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color=self.TEXT_DARK
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Optimized reports for hospital performance monitoring",
            font=ctk.CTkFont(size=12),
            text_color=self.SECONDARY
        )

        subtitle.pack(
            anchor="w",
            padx=30,
            pady=(0, 15)
        )

        # Refresh button
        refresh_button = ctk.CTkButton(
            self,
            text="Refresh Reports",
            command=self.load_reports,
            width=150,
            height=38,
            fg_color=self.PRIMARY,
            hover_color=self.PRIMARY_HOVER
        )

        refresh_button.pack(
            anchor="e",
            padx=30,
            pady=(0, 15)
        )

        # Summary cards
        self.summary_frame = ctk.CTkFrame(
            self
        )

        self.summary_frame.pack(
            fill="x",
            padx=30,
            pady=5
        )

        for column in range(3):
            self.summary_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.patient_value = self.create_card(
            "Total Patients",
            0,
            0
        )

        self.doctor_value = self.create_card(
            "Total Doctors",
            0,
            1
        )

        self.appointment_value = self.create_card(
            "Appointments",
            0,
            2
        )

        self.bill_value = self.create_card(
            "Total Bills",
            1,
            0
        )

        self.revenue_value = self.create_card(
            "Total Revenue",
            1,
            1
        )

        self.average_bill_value = self.create_card(
            "Average Bill",
            1,
            2
        )

        # Notebook
        self.notebook = ttk.Notebook(
            self
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        # Doctor report tab
        self.doctor_tab = ctk.CTkFrame(
            self.notebook
        )

        self.notebook.add(
            self.doctor_tab,
            text="Doctor Report"
        )

        # Waiting-time tab
        self.waiting_tab = ctk.CTkFrame(
            self.notebook
        )

        self.notebook.add(
            self.waiting_tab,
            text="Waiting Time"
        )

        # Recent patients tab
        self.patient_tab = ctk.CTkFrame(
            self.notebook
        )

        self.notebook.add(
            self.patient_tab,
            text="Recent Patients"
        )

        # Appointment tab
        self.appointment_tab = ctk.CTkFrame(
            self.notebook
        )

        self.notebook.add(
            self.appointment_tab,
            text="Appointments"
        )

        self.create_doctor_table()
        self.create_waiting_table()
        self.create_patient_table()
        self.create_appointment_summary()

    # --------------------------------------------------
    # SUMMARY CARD
    # --------------------------------------------------

    def create_card(
        self,
        title,
        row,
        column
    ):

        card = ctk.CTkFrame(
            self.summary_frame,
            height=92,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=row,
            column=column,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=13
            )
        )

        title_label.pack(
            pady=(15, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text="0",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        value_label.pack(
            pady=(0, 12)
        )

        return value_label

    # --------------------------------------------------
    # DOCTOR TABLE
    # --------------------------------------------------

    def create_doctor_table(self):

        columns = (
            "doctor_id",
            "doctor_name",
            "specialization",
            "appointments"
        )

        self.doctor_tree = ttk.Treeview(
            self.doctor_tab,
            columns=columns,
            show="headings"
        )

        headings = {
            "doctor_id": "Doctor ID",
            "doctor_name": "Doctor Name",
            "specialization": "Specialization",
            "appointments": "Appointments"
        }

        for column in columns:

            self.doctor_tree.heading(
                column,
                text=headings[column]
            )

            self.doctor_tree.column(
                column,
                width=150
            )

        self.doctor_tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # --------------------------------------------------
    # WAITING TIME TABLE
    # --------------------------------------------------

    def create_waiting_table(self):

        columns = (
            "appointment_id",
            "patient",
            "doctor",
            "check_in",
            "consultation",
            "waiting"
        )

        self.waiting_tree = ttk.Treeview(
            self.waiting_tab,
            columns=columns,
            show="headings"
        )

        headings = {
            "appointment_id": "Appointment ID",
            "patient": "Patient",
            "doctor": "Doctor",
            "check_in": "Check In",
            "consultation": "Consultation",
            "waiting": "Waiting (min)"
        }

        for column in columns:

            self.waiting_tree.heading(
                column,
                text=headings[column]
            )

            self.waiting_tree.column(
                column,
                width=150
            )

        self.waiting_tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # --------------------------------------------------
    # PATIENT TABLE
    # --------------------------------------------------

    def create_patient_table(self):

        columns = (
            "patient_id",
            "name",
            "gender",
            "phone",
            "blood_group",
            "registration_date"
        )

        self.patient_tree = ttk.Treeview(
            self.patient_tab,
            columns=columns,
            show="headings"
        )

        headings = {
            "patient_id": "Patient ID",
            "name": "Patient Name",
            "gender": "Gender",
            "phone": "Phone",
            "blood_group": "Blood Group",
            "registration_date": "Registration Date"
        }

        for column in columns:

            self.patient_tree.heading(
                column,
                text=headings[column]
            )

            self.patient_tree.column(
                column,
                width=140
            )

        self.patient_tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # --------------------------------------------------
    # APPOINTMENT SUMMARY
    # --------------------------------------------------

    def create_appointment_summary(self):

        self.appointment_text = ctk.CTkLabel(
            self.appointment_tab,
            text="Loading...",
            font=ctk.CTkFont(
                size=20
            )
        )

        self.appointment_text.pack(
            pady=60
        )

    # --------------------------------------------------
    # LOAD REPORTS
    # --------------------------------------------------

    def load_reports(self):

        try:

            reports = self.service.get_all_reports()

            # ------------------------------
            # Summary
            # ------------------------------

            patient_report = reports["patients"]

            self.patient_value.configure(
                text=str(
                    patient_report["total_patients"]
                )
            )

            doctor_report = reports["doctors"]

            self.doctor_value.configure(
                text=str(
                    doctor_report["total_doctors"]
                )
            )

            appointment_report = reports["appointments"]

            self.appointment_value.configure(
                text=str(
                    appointment_report["total_appointments"]
                )
            )

            billing_report = reports["billing"]

            self.bill_value.configure(
                text=str(
                    billing_report["total_bills"]
                )
            )

            self.revenue_value.configure(
                text=f"₹{billing_report['total_revenue']:.2f}"
            )

            self.average_bill_value.configure(
                text=f"₹{billing_report['average_bill']:.2f}"
            )

            # ------------------------------
            # Doctor report
            # ------------------------------

            self.clear_tree(
                self.doctor_tree
            )

            for doctor in doctor_report["doctor_data"]:

                self.doctor_tree.insert(
                    "",
                    "end",
                    values=(
                        doctor["doctor_id"],
                        doctor["doctor_name"],
                        doctor["specialization"],
                        doctor["total_appointments"]
                    )
                )

            # ------------------------------
            # Waiting-time report
            # ------------------------------

            self.clear_tree(
                self.waiting_tree
            )

            for record in reports["waiting_time"]:

                self.waiting_tree.insert(
                    "",
                    "end",
                    values=(
                        record["appointment_id"],
                        record["patient_name"],
                        record["doctor_name"],
                        record["check_in_time"],
                        record["consultation_start_time"],
                        record["waiting_minutes"]
                    )
                )

            # ------------------------------
            # Recent patients
            # ------------------------------

            self.clear_tree(
                self.patient_tree
            )

            for patient in reports["recent_patients"]:

                self.patient_tree.insert(
                    "",
                    "end",
                    values=(
                        patient["patient_id"],
                        patient["full_name"],
                        patient["gender"],
                        patient["phone"],
                        patient["blood_group"],
                        patient["registration_date"]
                    )
                )

            # ------------------------------
            # Appointment summary
            # ------------------------------

            self.appointment_text.configure(
                text=(
                    f"Total Appointments: "
                    f"{appointment_report['total_appointments']}\n\n"
                    f"Scheduled: "
                    f"{appointment_report['scheduled']}\n\n"
                    f"Completed: "
                    f"{appointment_report['completed']}\n\n"
                    f"Cancelled: "
                    f"{appointment_report['cancelled']}"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Report Error",
                str(error)
            )

    # --------------------------------------------------
    # CLEAR TREE
    # --------------------------------------------------

    def clear_tree(self, tree):

        for item in tree.get_children():
            tree.delete(item)


# ------------------------------------------------------
# STANDALONE TEST
# ------------------------------------------------------

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    app.title(
        "Hospital Management System - Reports"
    )

    app.geometry(
        "1200x700"
    )

    frame = ReportFrame(
        app
    )

    frame.pack(
        fill="both",
        expand=True
    )

    app.mainloop()