import tkinter as tk
from tkinter import ttk, messagebox

import customtkinter as ctk

from app.gui.ui_kit import HospitalFrame

from app.services.appointment_service import AppointmentService
from app.services.patient_service import PatientService
from app.services.doctor_service import DoctorService


class AppointmentFrame(HospitalFrame):

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

        self.appointment_service = AppointmentService()
        self.patient_service = PatientService()
        self.doctor_service = DoctorService()

        self.selected_appointment_id = None
        self.patient_map = {}
        self.doctor_map = {}

        self.create_ui()
        self.load_patients()
        self.load_doctors()
        self.load_appointments()

    # =========================================================
    # UI
    # =========================================================

    def create_ui(self):
        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = ctk.CTkFrame(
            self,
            fg_color=self.CARD,
            corner_radius=20,
            border_width=1,
            border_color=self.BORDER
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        title = ctk.CTkLabel(
            header,
            text="◷  Appointment Management",
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
            text="Schedule appointments and measure patient waiting time",
            font=ctk.CTkFont(size=11),
            text_color=self.SECONDARY
        )

        subtitle.pack(
            anchor="w",
            pady=(2, 0)
        )

        # -----------------------------------------------------
        # Live operations snapshot
        snapshot = ctk.CTkFrame(self, fg_color="transparent")
        snapshot.pack(fill="x", padx=30, pady=(0, 15))
        for column in range(4):
            snapshot.grid_columnconfigure(column, weight=1, uniform="uxstats")
        self.ux_stat_labels = {}
        card = ctk.CTkFrame(snapshot, fg_color=self.CARD, corner_radius=15, border_width=1, border_color=self.BORDER)
        card.grid(row=0, column=0, padx=(0 if 0==0 else 5, 5 if 0<3 else 0), sticky="ew")
        ctk.CTkLabel(card, text="◷  TOTAL", text_color=self.SECONDARY, font=ctk.CTkFont(size=8, weight="bold")).pack(anchor="w", padx=13, pady=(11, 3))
        self.ux_stat_labels["total"] = ctk.CTkLabel(card, text="0", text_color=self.TEXT_DARK, font=ctk.CTkFont(size=20, weight="bold"))
        self.ux_stat_labels["total"].pack(anchor="w", padx=13, pady=(0, 11))
        card = ctk.CTkFrame(snapshot, fg_color=self.CARD, corner_radius=15, border_width=1, border_color=self.BORDER)
        card.grid(row=0, column=1, padx=(0 if 1==0 else 5, 5 if 1<3 else 0), sticky="ew")
        ctk.CTkLabel(card, text="◷  SCHEDULED", text_color=self.SECONDARY, font=ctk.CTkFont(size=8, weight="bold")).pack(anchor="w", padx=13, pady=(11, 3))
        self.ux_stat_labels["scheduled"] = ctk.CTkLabel(card, text="0", text_color=self.TEXT_DARK, font=ctk.CTkFont(size=20, weight="bold"))
        self.ux_stat_labels["scheduled"].pack(anchor="w", padx=13, pady=(0, 11))
        card = ctk.CTkFrame(snapshot, fg_color=self.CARD, corner_radius=15, border_width=1, border_color=self.BORDER)
        card.grid(row=0, column=2, padx=(0 if 2==0 else 5, 5 if 2<3 else 0), sticky="ew")
        ctk.CTkLabel(card, text="◷  COMPLETED", text_color=self.SECONDARY, font=ctk.CTkFont(size=8, weight="bold")).pack(anchor="w", padx=13, pady=(11, 3))
        self.ux_stat_labels["completed"] = ctk.CTkLabel(card, text="0", text_color=self.TEXT_DARK, font=ctk.CTkFont(size=20, weight="bold"))
        self.ux_stat_labels["completed"].pack(anchor="w", padx=13, pady=(0, 11))
        card = ctk.CTkFrame(snapshot, fg_color=self.CARD, corner_radius=15, border_width=1, border_color=self.BORDER)
        card.grid(row=0, column=3, padx=(0 if 3==0 else 5, 5 if 3<3 else 0), sticky="ew")
        ctk.CTkLabel(card, text="◷  WAITING", text_color=self.SECONDARY, font=ctk.CTkFont(size=8, weight="bold")).pack(anchor="w", padx=13, pady=(11, 3))
        self.ux_stat_labels["waiting"] = ctk.CTkLabel(card, text="0", text_color=self.TEXT_DARK, font=ctk.CTkFont(size=20, weight="bold"))
        self.ux_stat_labels["waiting"].pack(anchor="w", padx=13, pady=(0, 11))

        # Form Card
        # -----------------------------------------------------

        form_card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER
        )

        form_card.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        for column in range(3):
            form_card.grid_columnconfigure(
                column,
                weight=1
            )

        form_title = ctk.CTkLabel(
            form_card,
            text="Appointment Details",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color="#172033"
        )

        form_title.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=20,
            pady=(18, 12)
        )

        # -----------------------------------------------------
        # Patient
        # -----------------------------------------------------

        self.create_label(
            form_card,
            "Patient",
            1,
            0
        )

        self.patient_combo = ctk.CTkComboBox(
            form_card,
            height=36,
            values=["No patients available"]
        )

        self.patient_combo.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 12)
        )

        # -----------------------------------------------------
        # Doctor
        # -----------------------------------------------------

        self.create_label(
            form_card,
            "Doctor",
            1,
            1
        )

        self.doctor_combo = ctk.CTkComboBox(
            form_card,
            height=36,
            values=["No doctors available"]
        )

        self.doctor_combo.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=(0, 12)
        )

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        self.create_label(
            form_card,
            "Status",
            1,
            2
        )

        self.status_combo = ctk.CTkComboBox(
            form_card,
            height=36,
            values=[
                "Scheduled",
                "Completed",
                "Cancelled"
            ]
        )

        self.status_combo.set(
            "Scheduled"
        )

        self.status_combo.grid(
            row=2,
            column=2,
            sticky="ew",
            padx=(10, 20),
            pady=(0, 12)
        )

        # -----------------------------------------------------
        # Date
        # -----------------------------------------------------

        self.create_label(
            form_card,
            "Appointment Date",
            3,
            0
        )

        self.date_entry = ctk.CTkEntry(
            form_card,
            height=36,
            placeholder_text="YYYY-MM-DD"
        )

        self.date_entry.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 12)
        )

        # -----------------------------------------------------
        # Time
        # -----------------------------------------------------

        self.create_label(
            form_card,
            "Appointment Time",
            3,
            1
        )

        self.time_entry = ctk.CTkEntry(
            form_card,
            height=36,
            placeholder_text="HH:MM"
        )

        self.time_entry.grid(
            row=4,
            column=1,
            sticky="ew",
            padx=10,
            pady=(0, 12)
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        button_frame = ctk.CTkFrame(
            form_card,
            fg_color="transparent"
        )

        button_frame.grid(
            row=5,
            column=0,
            columnspan=3,
            sticky="w",
            padx=20,
            pady=(2, 18)
        )

        add_button = ctk.CTkButton(
            button_frame,
            text="＋  Book Appointment",
            width=135,
            height=36,
            command=self.add_appointment
        )

        add_button.pack(
            side="left",
            padx=(0, 8)
        )

        update_button = ctk.CTkButton(
            button_frame,
            text="Update",
            width=100,
            height=36,
            fg_color="#37445D",
            hover_color="#4A5872",
            command=self.update_appointment
        )

        update_button.pack(
            side="left",
            padx=8
        )

        cancel_button = ctk.CTkButton(
            button_frame,
            text="×  Cancel Appointment",
            width=145,
            height=36,
            fg_color="#B42318",
            hover_color="#912018",
            command=self.cancel_appointment
        )

        cancel_button.pack(
            side="left",
            padx=8
        )

        checkin_button = ctk.CTkButton(
            button_frame,
            text="Check In",
            width=100,
            height=36,
            fg_color="#176B5B",
            hover_color="#125447",
            command=self.check_in
        )

        checkin_button.pack(
            side="left",
            padx=8
        )

        consultation_button = ctk.CTkButton(
            button_frame,
            text="Start Consultation",
            width=140,
            height=36,
            fg_color="#176B5B",
            hover_color="#125447",
            command=self.start_consultation
        )

        consultation_button.pack(
            side="left",
            padx=8
        )

        clear_button = ctk.CTkButton(
            button_frame,
            text="↺  Clear",
            width=90,
            height=36,
            fg_color="#E5E7EB",
            hover_color="#D1D5DB",
            text_color="#172033",
            command=self.clear_form
        )

        clear_button.pack(
            side="left",
            padx=8
        )

        # -----------------------------------------------------
        # Table Card
        # -----------------------------------------------------

        table_card = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER
        )

        table_card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        # Search row
        search_frame = ctk.CTkFrame(
            table_card,
            fg_color="transparent"
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=(18, 12)
        )

        table_title = ctk.CTkLabel(
            search_frame,
            text="Appointment Records",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color="#172033"
        )

        table_title.pack(
            side="left"
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            height=36,
            placeholder_text="Search patient, doctor or ID..."
        )

        self.search_entry.pack(
            side="right",
            padx=(10, 0)
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_appointments
        )

        refresh_button = ctk.CTkButton(
            search_frame,
            text="↻ Refresh",
            width=90,
            height=36,
            command=self.refresh_appointments
        )

        refresh_button.pack(
            side="right"
        )

        # -----------------------------------------------------
        # Treeview
        # -----------------------------------------------------

        tree_frame = ctk.CTkFrame(
            table_card,
            fg_color="transparent"
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        columns = (
            "id",
            "patient",
            "doctor",
            "date",
            "time",
            "status",
            "waiting"
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading(
            "id",
            text="ID"
        )

        self.tree.heading(
            "patient",
            text="Patient"
        )

        self.tree.heading(
            "doctor",
            text="Doctor"
        )

        self.tree.heading(
            "date",
            text="Date"
        )

        self.tree.heading(
            "time",
            text="Time"
        )

        self.tree.heading(
            "status",
            text="Status"
        )

        self.tree.heading(
            "waiting",
            text="Waiting Time"
        )

        self.tree.column(
            "id",
            width=55,
            anchor="center"
        )

        self.tree.column(
            "patient",
            width=170
        )

        self.tree.column(
            "doctor",
            width=180
        )

        self.tree.column(
            "date",
            width=105,
            anchor="center"
        )

        self.tree.column(
            "time",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "status",
            width=110,
            anchor="center"
        )

        self.tree.column(
            "waiting",
            width=120,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<Double-1>",
            self.select_appointment
        )

        # Treeview style
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Segoe UI", 10),
            background="white",
            fieldbackground="white"
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    def update_ux_stats(self):
        try:
            items = self.tree.get_children()
            self.ux_stat_labels["total"].configure(text=str(len(items)))
            vals=[self.tree.item(i, "values") for i in items]
            joined=" ".join(str(v) for row in vals for v in row).lower()
            self.ux_stat_labels["scheduled"].configure(text=str(joined.count("scheduled")))
            self.ux_stat_labels["completed"].configure(text=str(joined.count("completed")))
            self.ux_stat_labels["waiting"].configure(text=str(joined.count("waiting")))
            selected = self.selected_appointment_id
            self.ux_stat_labels["selected"].configure(text="Ready" if selected else "None")
        except Exception:
            pass

    def create_label(
        self,
        parent,
        text,
        row,
        column
    ):
        label = ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color="#4B5563"
        )

        label.grid(
            row=row,
            column=column,
            sticky="w",
            padx=20 if column == 0 else 10,
            pady=(0, 5)
        )

    # =========================================================
    # Patient / Doctor Dropdowns
    # =========================================================

    def load_patients(self):
        try:
            patients = self.patient_service.get_all_patients()

            self.patient_map = {}

            values = []

            for patient in patients:
                display = (
                    f"{patient['patient_id']} - "
                    f"{patient['full_name']}"
                )

                values.append(display)

                self.patient_map[display] = patient[
                    "patient_id"
                ]

            if values:
                self.patient_combo.configure(
                    values=values
                )
                self.patient_combo.set(
                    values[0]
                )
            else:
                self.patient_combo.configure(
                    values=["No patients available"]
                )
                self.patient_combo.set(
                    "No patients available"
                )

        except Exception as error:
            messagebox.showerror(
                "Patient Loading Error",
                str(error)
            )

    def load_doctors(self):
        try:
            doctors = self.doctor_service.get_all_doctors()

            self.doctor_map = {}

            values = []

            for doctor in doctors:
                display = (
                    f"{doctor['doctor_id']} - "
                    f"{doctor['full_name']} - "
                    f"{doctor['specialization']}"
                )

                values.append(display)

                self.doctor_map[display] = doctor[
                    "doctor_id"
                ]

            if values:
                self.doctor_combo.configure(
                    values=values
                )
                self.doctor_combo.set(
                    values[0]
                )
            else:
                self.doctor_combo.configure(
                    values=["No doctors available"]
                )
                self.doctor_combo.set(
                    "No doctors available"
                )

        except Exception as error:
            messagebox.showerror(
                "Doctor Loading Error",
                str(error)
            )

    # =========================================================
    # CRUD
    # =========================================================

    def get_selected_patient_id(self):
        selected = self.patient_combo.get()

        if selected not in self.patient_map:
            raise ValueError(
                "Please select a valid patient."
            )

        return self.patient_map[selected]

    def get_selected_doctor_id(self):
        selected = self.doctor_combo.get()

        if selected not in self.doctor_map:
            raise ValueError(
                "Please select a valid doctor."
            )

        return self.doctor_map[selected]

    def add_appointment(self):
        try:
            patient_id = self.get_selected_patient_id()
            doctor_id = self.get_selected_doctor_id()

            appointment_id = (
                self.appointment_service.add_appointment(
                    patient_id,
                    doctor_id,
                    self.date_entry.get(),
                    self.time_entry.get(),
                    self.status_combo.get()
                )
            )

            self.show_toast("Operation completed")

        messagebox.showinfo(
                "Success",
                (
                    "Appointment booked successfully.
"
                    f"Appointment ID: {appointment_id}"
                )
            )

            self.clear_form()
            self.load_appointments()

        except Exception as error:
            messagebox.showerror(
                "Unable to Book Appointment",
                str(error)
            )

    def update_appointment(self):
        if not self.selected_appointment_id:
            messagebox.showwarning(
                "Select Appointment",
                "Double-click an appointment record first."
            )
            return

        try:
            patient_id = self.get_selected_patient_id()
            doctor_id = self.get_selected_doctor_id()

            self.appointment_service.update_appointment(
                self.selected_appointment_id,
                patient_id,
                doctor_id,
                self.date_entry.get(),
                self.time_entry.get(),
                self.status_combo.get()
            )

            self.show_toast("Operation completed")

        messagebox.showinfo(
                "Success",
                "Appointment updated successfully."
            )

            self.clear_form()
            self.load_appointments()

        except Exception as error:
            messagebox.showerror(
                "Unable to Update Appointment",
                str(error)
            )

    def cancel_appointment(self):
        if not self.selected_appointment_id:
            messagebox.showwarning(
                "Select Appointment",
                "Double-click an appointment record first."
            )
            return

        answer = messagebox.askyesno(
            "Cancel Appointment",
            "Are you sure you want to cancel this appointment?"
        )

        if not answer:
            return

        try:
            appointment = (
                self.appointment_service.get_appointment(
                    self.selected_appointment_id
                )
            )

            if appointment is None:
                raise ValueError(
                    "Appointment record not found."
                )

            patient_id = appointment["patient_id"]
            doctor_id = appointment["doctor_id"]
            appointment_date = appointment["appointment_date"]
            appointment_time = appointment["appointment_time"]

            self.appointment_service.update_appointment(
                self.selected_appointment_id,
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                "Cancelled"
            )

            self.show_toast("Operation completed")

        messagebox.showinfo(
                "Success",
                "Appointment cancelled successfully."
            )

            self.clear_form()
            self.load_appointments()

        except Exception as error:
            messagebox.showerror(
                "Unable to Cancel Appointment",
                str(error)
            )

    # =========================================================
    # Waiting Time
    # =========================================================

    def check_in(self):
        if not self.selected_appointment_id:
            messagebox.showwarning(
                "Select Appointment",
                "Double-click an appointment record first."
            )
            return

        try:
            self.appointment_service.check_in_patient(
                self.selected_appointment_id
            )

            self.show_toast("Operation completed")

        messagebox.showinfo(
                "Check-in Recorded",
                "Patient check-in time recorded."
            )

            self.load_appointments()

        except Exception as error:
            messagebox.showerror(
                "Check-in Error",
                str(error)
            )

    def start_consultation(self):
        if not self.selected_appointment_id:
            messagebox.showwarning(
                "Select Appointment",
                "Double-click an appointment record first."
            )
            return

        try:
            self.appointment_service.start_consultation(
                self.selected_appointment_id
            )

            self.show_toast("Operation completed")

        messagebox.showinfo(
                "Consultation Started",
                "Consultation start time recorded."
            )

            self.load_appointments()

        except Exception as error:
            messagebox.showerror(
                "Consultation Error",
                str(error)
            )

    # =========================================================
    # Loading / Search
    # =========================================================

    def load_appointments(self):
        try:
            appointments = (
                self.appointment_service.get_all_appointments()
            )

            self.display_appointments(
                appointments
            )

        except Exception as error:
            messagebox.showerror(
                "Loading Error",
                str(error)
            )

    def search_appointments(self, event=None):
        search_text = self.search_entry.get().strip()

        try:
            if search_text:
                appointments = (
                    self.appointment_service.search_appointments(
                        search_text
                    )
                )
            else:
                appointments = (
                    self.appointment_service.get_all_appointments()
                )

            self.display_appointments(
                appointments
            )

        except Exception as error:
            messagebox.showerror(
                "Search Error",
                str(error)
            )

    def display_appointments(self, appointments):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for appointment in appointments:

            waiting_seconds = (
                self.appointment_service.calculate_waiting_time(
                    appointment["check_in_time"],
                    appointment["consultation_start_time"]
                )
            )

            if waiting_seconds is None:
                waiting_text = "-"
            else:
                waiting_text = (
                    self.appointment_service
                    .format_waiting_time(waiting_seconds)
                    if hasattr(
                        self.appointment_service,
                        "format_waiting_time"
                    )
                    else self.format_waiting_time(
                        waiting_seconds
                    )
                )

            self.tree.insert(
                "",
                "end",
                values=(
                    appointment["appointment_id"],
                    appointment["patient_name"],
                    appointment["doctor_name"],
                    appointment["appointment_date"],
                    appointment["appointment_time"],
                    appointment["status"],
                    waiting_text
                )
            )

        self.update_ux_stats()

    def format_waiting_time(self, seconds):
        if seconds is None:
            return "-"

        if seconds < 60:
            return f"{int(seconds)} sec"

        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)

        if remaining_seconds == 0:
            return f"{minutes} min"

        return (
            f"{minutes} min "
            f"{remaining_seconds} sec"
        )

    def refresh_appointments(self):
        self.search_entry.unbind(
            "<KeyRelease>"
        )

        self.search_entry.delete(
            0,
            "end"
        )

        self.clear_form()
        self.load_patients()
        self.load_doctors()
        self.load_appointments()

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_appointments
        )

    # =========================================================
    # Selection / Form
    # =========================================================

    def select_appointment(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        self.selected_appointment_id = int(
            values[0]
        )

        # Find patient
        patient_found = False

        for display, patient_id in self.patient_map.items():
            if str(patient_id) == str(
                self.get_patient_id_from_row(values[1])
            ):
                self.patient_combo.set(
                    display
                )
                patient_found = True
                break

        # Find doctor
        doctor_found = False

        for display, doctor_id in self.doctor_map.items():
            if values[2] in display:
                self.doctor_combo.set(
                    display
                )
                doctor_found = True
                break

        # Date
        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            values[3]
        )

        # Time
        self.time_entry.delete(
            0,
            "end"
        )

        self.time_entry.insert(
            0,
            values[4]
        )

        # Status
        self.status_combo.set(
            values[5]
        )

    def get_patient_id_from_row(
        self,
        patient_name
    ):
        for display, patient_id in self.patient_map.items():
            if display.endswith(
                f"- {patient_name}"
            ):
                return patient_id

        return None

    def clear_form(self):
        self.selected_appointment_id = None

        self.date_entry.delete(
            0,
            "end"
        )

        self.time_entry.delete(
            0,
            "end"
        )

        self.status_combo.set(
            "Scheduled"
        )

        for item in self.tree.selection():
            self.tree.selection_remove(item)


# =============================================================
# Standalone Test
# =============================================================

if __name__ == "__main__":
    root = ctk.CTk()

    root.title(
        "Appointment Management"
    )

    root.geometry(
        "1280x760"
    )

    frame = AppointmentFrame(root)

    frame.pack(
        fill="both",
        expand=True
    )

    root.mainloop()