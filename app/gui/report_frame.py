import customtkinter as ctk
from tkinter import ttk, messagebox

from app.services.report_service import ReportService


class ReportFrame(ctk.CTkFrame):

    BACKGROUND = "#F6F8FC"
    CARD = "#FFFFFF"
    CARD_SOFT = "#F8FAFD"
    BORDER = "#E6EAF0"
    TEXT_DARK = "#0F172A"
    SECONDARY = "#64748B"
    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    PURPLE = "#7C3AED"

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color=self.BACKGROUND)
        self.service = ReportService()
        self.configure_tree_style()
        self.create_ui()
        self.load_reports()

    def configure_tree_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Hospital.Treeview",
            background="#FFFFFF",
            foreground=self.TEXT_DARK,
            fieldbackground="#FFFFFF",
            rowheight=38,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Hospital.Treeview.Heading",
            background="#F1F5F9",
            foreground="#334155",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(10, 10)
        )
        style.map(
            "Hospital.Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#1E3A8A")]
        )

    def create_ui(self):
        self.main = ctk.CTkScrollableFrame(
            self,
            fg_color=self.BACKGROUND,
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )
        self.main.pack(fill="both", expand=True)

        self.create_header()
        self.create_summary()
        self.create_reports_area()
        self.create_footer()

    def create_header(self):
        header = ctk.CTkFrame(
            self.main,
            fg_color=self.CARD,
            corner_radius=20,
            border_width=1,
            border_color=self.BORDER
        )
        header.pack(fill="x", padx=30, pady=(25, 15))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=24, pady=20)

        ctk.CTkLabel(
            left,
            text="REPORT CENTER  /  HOSPITAL OPERATIONS",
            text_color=self.PRIMARY,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Hospital Reports",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", pady=(4, 2))

        ctk.CTkLabel(
            left,
            text="Monitor patients, appointments, doctors, billing and waiting-time performance.",
            text_color=self.SECONDARY,
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=24, pady=20)

        ctk.CTkLabel(
            right,
            text="●  DATA READY",
            text_color=self.SUCCESS,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="e", pady=(0, 8))

        ctk.CTkButton(
            right,
            text="↻  Refresh Reports",
            width=155,
            height=38,
            corner_radius=10,
            fg_color=self.PRIMARY,
            hover_color=self.PRIMARY_HOVER,
            command=self.load_reports
        ).pack(anchor="e")

    def create_summary(self):
        section = ctk.CTkFrame(self.main, fg_color="transparent")
        section.pack(fill="x", padx=30, pady=(0, 15))

        for column in range(6):
            section.grid_columnconfigure(column, weight=1)

        cards = [
            ("PATIENTS", "0", "Registered patients", self.PRIMARY),
            ("DOCTORS", "0", "Medical staff", self.PURPLE),
            ("APPOINTMENTS", "0", "Total appointments", "#0891B2"),
            ("BILLS", "0", "Generated bills", self.WARNING),
            ("REVENUE", "₹0.00", "Total collected", self.SUCCESS),
            ("AVG BILL", "₹0.00", "Average bill value", "#EC4899")
        ]

        self.summary_values = []

        for column, data in enumerate(cards):
            value_label = self.create_metric_card(section, data, column)
            self.summary_values.append(value_label)

        (
            self.patient_value,
            self.doctor_value,
            self.appointment_value,
            self.bill_value,
            self.revenue_value,
            self.average_bill_value
        ) = self.summary_values

    def create_metric_card(self, parent, data, column):
        title, value, description, accent = data

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
            padx=5,
            sticky="nsew"
        )

        ctk.CTkFrame(
            card,
            width=4,
            height=58,
            corner_radius=2,
            fg_color=accent
        ).pack(side="left", padx=(12, 9), pady=14)

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=(0, 10), pady=11)

        ctk.CTkLabel(
            body,
            text=title,
            text_color=self.SECONDARY,
            font=ctk.CTkFont(size=9, weight="bold")
        ).pack(anchor="w")

        value_label = ctk.CTkLabel(
            body,
            text=value,
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(size=21, weight="bold")
        )
        value_label.pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            body,
            text=description,
            text_color="#94A3B8",
            font=ctk.CTkFont(size=8)
        ).pack(anchor="w")

        return value_label

    def create_reports_area(self):
        card = ctk.CTkFrame(
            self.main,
            fg_color=self.CARD,
            corner_radius=20,
            border_width=1,
            border_color=self.BORDER
        )
        card.pack(fill="both", expand=True, padx=30, pady=(0, 15))

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(18, 8))

        ctk.CTkLabel(
            top,
            text="Operational Reports",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text="Select a report to inspect detailed records",
            text_color=self.SECONDARY,
            font=ctk.CTkFont(size=10)
        ).pack(side="right", pady=4)

        self.notebook = ttk.Notebook(card)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=(0, 18))

        self.doctor_tab = ctk.CTkFrame(self.notebook, fg_color=self.CARD)
        self.waiting_tab = ctk.CTkFrame(self.notebook, fg_color=self.CARD)
        self.patient_tab = ctk.CTkFrame(self.notebook, fg_color=self.CARD)
        self.appointment_tab = ctk.CTkFrame(self.notebook, fg_color=self.CARD)

        self.notebook.add(self.doctor_tab, text="  Doctor Report  ")
        self.notebook.add(self.waiting_tab, text="  Waiting Time  ")
        self.notebook.add(self.patient_tab, text="  Recent Patients  ")
        self.notebook.add(self.appointment_tab, text="  Appointments  ")

        self.create_doctor_table()
        self.create_waiting_table()
        self.create_patient_table()
        self.create_appointment_summary()

    def create_table_shell(self, parent):
        shell = ctk.CTkFrame(
            parent,
            fg_color=self.CARD_SOFT,
            corner_radius=14,
            border_width=1,
            border_color=self.BORDER
        )
        shell.pack(fill="both", expand=True, padx=10, pady=10)
        return shell

    def create_doctor_table(self):
        shell = self.create_table_shell(self.doctor_tab)
        columns = ("doctor_id", "doctor_name", "specialization", "appointments")

        self.doctor_tree = ttk.Treeview(
            shell,
            columns=columns,
            show="headings",
            style="Hospital.Treeview"
        )

        headings = {
            "doctor_id": "Doctor ID",
            "doctor_name": "Doctor Name",
            "specialization": "Specialization",
            "appointments": "Appointments"
        }

        widths = {"doctor_id": 120, "doctor_name": 250, "specialization": 250, "appointments": 140}
        self.configure_tree(self.doctor_tree, headings, widths)

    def create_waiting_table(self):
        shell = self.create_table_shell(self.waiting_tab)
        columns = ("appointment_id", "patient", "doctor", "check_in", "consultation", "waiting")

        self.waiting_tree = ttk.Treeview(
            shell,
            columns=columns,
            show="headings",
            style="Hospital.Treeview"
        )

        headings = {
            "appointment_id": "Appointment ID",
            "patient": "Patient",
            "doctor": "Doctor",
            "check_in": "Check In",
            "consultation": "Consultation",
            "waiting": "Waiting (min)"
        }

        widths = {
            "appointment_id": 125,
            "patient": 190,
            "doctor": 190,
            "check_in": 170,
            "consultation": 170,
            "waiting": 130
        }
        self.configure_tree(self.waiting_tree, headings, widths)

    def create_patient_table(self):
        shell = self.create_table_shell(self.patient_tab)
        columns = ("patient_id", "name", "gender", "phone", "blood_group", "registration_date")

        self.patient_tree = ttk.Treeview(
            shell,
            columns=columns,
            show="headings",
            style="Hospital.Treeview"
        )

        headings = {
            "patient_id": "Patient ID",
            "name": "Patient Name",
            "gender": "Gender",
            "phone": "Phone",
            "blood_group": "Blood Group",
            "registration_date": "Registration Date"
        }

        widths = {
            "patient_id": 120,
            "name": 230,
            "gender": 100,
            "phone": 170,
            "blood_group": 120,
            "registration_date": 170
        }
        self.configure_tree(self.patient_tree, headings, widths)

    def configure_tree(self, tree, headings, widths):
        for column, heading in headings.items():
            tree.heading(column, text=heading)
            tree.column(
                column,
                width=widths.get(column, 150),
                minwidth=80,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            tree.master,
            orient="vertical",
            command=tree.yview
        )
        scrollbar.pack(side="right", fill="y")

        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True, padx=6, pady=6)

    def create_appointment_summary(self):
        container = ctk.CTkFrame(
            self.appointment_tab,
            fg_color="transparent"
        )
        container.pack(fill="both", expand=True, padx=25, pady=25)

        self.appointment_total = self.create_status_block(
            container,
            "TOTAL APPOINTMENTS",
            "0",
            self.PRIMARY,
            0
        )
        self.appointment_scheduled = self.create_status_block(
            container,
            "SCHEDULED",
            "0",
            "#0891B2",
            1
        )
        self.appointment_completed = self.create_status_block(
            container,
            "COMPLETED",
            "0",
            self.SUCCESS,
            2
        )
        self.appointment_cancelled = self.create_status_block(
            container,
            "CANCELLED",
            "0",
            self.DANGER,
            3
        )

    def create_status_block(self, parent, title, value, accent, column):
        parent.grid_columnconfigure(column, weight=1)

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD_SOFT,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )
        card.grid(row=0, column=column, padx=8, sticky="nsew")

        ctk.CTkFrame(
            card,
            height=5,
            corner_radius=2,
            fg_color=accent
        ).pack(fill="x", padx=18, pady=(18, 15))

        ctk.CTkLabel(
            card,
            text=title,
            text_color=self.SECONDARY,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", padx=18)

        label = ctk.CTkLabel(
            card,
            text=value,
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(size=30, weight="bold")
        )
        label.pack(anchor="w", padx=18, pady=(5, 20))
        return label

    def create_footer(self):
        footer = ctk.CTkFrame(self.main, fg_color="transparent")
        footer.pack(fill="x", padx=30, pady=(0, 25))

        ctk.CTkLabel(
            footer,
            text="Q02  •  Improve Performance",
            text_color=self.PRIMARY,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(side="left")

        ctk.CTkLabel(
            footer,
            text="Reports use live hospital database records",
            text_color="#94A3B8",
            font=ctk.CTkFont(size=9)
        ).pack(side="right")

    def load_reports(self):
        try:
            reports = self.service.get_all_reports()

            patient_report = reports["patients"]
            doctor_report = reports["doctors"]
            appointment_report = reports["appointments"]
            billing_report = reports["billing"]

            self.patient_value.configure(
                text=str(patient_report["total_patients"])
            )
            self.doctor_value.configure(
                text=str(doctor_report["total_doctors"])
            )
            self.appointment_value.configure(
                text=str(appointment_report["total_appointments"])
            )
            self.bill_value.configure(
                text=str(billing_report["total_bills"])
            )
            self.revenue_value.configure(
                text=f"₹{billing_report['total_revenue']:.2f}"
            )
            self.average_bill_value.configure(
                text=f"₹{billing_report['average_bill']:.2f}"
            )

            self.clear_tree(self.doctor_tree)
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

            self.clear_tree(self.waiting_tree)
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

            self.clear_tree(self.patient_tree)
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

            self.appointment_total.configure(
                text=str(appointment_report["total_appointments"])
            )
            self.appointment_scheduled.configure(
                text=str(appointment_report["scheduled"])
            )
            self.appointment_completed.configure(
                text=str(appointment_report["completed"])
            )
            self.appointment_cancelled.configure(
                text=str(appointment_report["cancelled"])
            )

        except Exception as error:
            messagebox.showerror("Report Error", str(error))

    def clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Hospital Management System - Reports")
    app.geometry("1400x850")

    frame = ReportFrame(app)
    frame.pack(fill="both", expand=True)

    app.mainloop()
