import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import customtkinter as ctk

from app.services.appointment_service import AppointmentService
from app.services.patient_service import PatientService
from app.services.doctor_service import DoctorService


class AppointmentGUI(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.appointment_service = AppointmentService()
        self.patient_service = PatientService()
        self.doctor_service = DoctorService()

        self.selected_appointment_id = None

        self.patient_map = {}
        self.doctor_map = {}

        self.create_widgets()
        self.load_patients()
        self.load_doctors()
        self.load_appointments()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Appointment Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(anchor="w", padx=25, pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Book, manage and monitor patient appointments",
            font=ctk.CTkFont(size=13)
        )
        subtitle.pack(anchor="w", padx=25, pady=(0, 15))

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=25, pady=10)

        # Patient
        ctk.CTkLabel(
            form_frame,
            text="Patient"
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        self.patient_menu = ctk.CTkOptionMenu(
            form_frame,
            width=240,
            values=["No patients available"]
        )
        self.patient_menu.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15)
        )

        # Doctor
        ctk.CTkLabel(
            form_frame,
            text="Doctor"
        ).grid(row=0, column=1, padx=15, pady=(15, 5), sticky="w")

        self.doctor_menu = ctk.CTkOptionMenu(
            form_frame,
            width=240,
            values=["No doctors available"]
        )
        self.doctor_menu.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 15)
        )

        # Date
        ctk.CTkLabel(
            form_frame,
            text="Date (YYYY-MM-DD)"
        ).grid(row=0, column=2, padx=15, pady=(15, 5), sticky="w")

        self.date_entry = ctk.CTkEntry(
            form_frame,
            width=180,
            placeholder_text="2026-09-26"
        )
        self.date_entry.grid(
            row=1,
            column=2,
            padx=15,
            pady=(0, 15)
        )

        # Time
        ctk.CTkLabel(
            form_frame,
            text="Time (HH:MM)"
        ).grid(row=0, column=3, padx=15, pady=(15, 5), sticky="w")

        self.time_entry = ctk.CTkEntry(
            form_frame,
            width=150,
            placeholder_text="10:30"
        )
        self.time_entry.grid(
            row=1,
            column=3,
            padx=15,
            pady=(0, 15)
        )

        # Status
        ctk.CTkLabel(
            form_frame,
            text="Status"
        ).grid(row=0, column=4, padx=15, pady=(15, 5), sticky="w")

        self.status_menu = ctk.CTkOptionMenu(
            form_frame,
            width=170,
            values=[
                "Scheduled",
                "Checked In",
                "In Consultation",
                "Completed",
                "Cancelled"
            ]
        )
        self.status_menu.set("Scheduled")
        self.status_menu.grid(
            row=1,
            column=4,
            padx=15,
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=25, pady=10)

        ctk.CTkButton(
            button_frame,
            text="Book Appointment",
            command=self.add_appointment
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            button_frame,
            text="Update",
            command=self.update_appointment
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            button_frame,
            text="Cancel Appointment",
            command=self.cancel_appointment
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            button_frame,
            text="Check In",
            command=self.check_in
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            button_frame,
            text="Start Consultation",
            command=self.start_consultation
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_form
        ).pack(side="left", padx=8)

        # -----------------------------------------------------
        # Search
        # -----------------------------------------------------

        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=25, pady=(10, 5))

        ctk.CTkLabel(
            search_frame,
            text="Search"
        ).pack(side="left", padx=(15, 8))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=350,
            placeholder_text="Patient, doctor, specialization or appointment ID"
        )
        self.search_entry.pack(
            side="left",
            padx=5,
            pady=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_appointments
        )

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            command=self.refresh_appointments
        ).pack(side="left", padx=10)

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(5, 20)
        )

        columns = (
            "appointment_id",
            "patient",
            "doctor",
            "date",
            "time",
            "status",
            "waiting"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "appointment_id",
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
            "appointment_id",
            width=60,
            anchor="center"
        )

        self.tree.column(
            "patient",
            width=180
        )

        self.tree.column(
            "doctor",
            width=180
        )

        self.tree.column(
            "date",
            width=110,
            anchor="center"
        )

        self.tree.column(
            "time",
            width=90,
            anchor="center"
        )

        self.tree.column(
            "status",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "waiting",
            width=120,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
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

    # ---------------------------------------------------------
    # Patient / Doctor dropdowns
    # ---------------------------------------------------------

    def load_patients(self):

        patients = self.patient_service.get_all_patients()

        self.patient_map.clear()

        values = []

        for patient in patients:

            patient_id = patient["patient_id"]
            name = patient["full_name"]

            display_value = f"{patient_id} - {name}"

            self.patient_map[display_value] = patient_id

            values.append(display_value)

        if not values:
            values = ["No patients available"]

        self.patient_menu.configure(
            values=values
        )

        self.patient_menu.set(
            values[0]
        )

    def load_doctors(self):

        doctors = self.doctor_service.get_all_doctors()

        self.doctor_map.clear()

        values = []

        for doctor in doctors:

            doctor_id = doctor["doctor_id"]
            name = doctor["full_name"]
            specialization = doctor["specialization"]

            display_value = (
                f"{doctor_id} - {name} ({specialization})"
            )

            self.doctor_map[display_value] = doctor_id

            values.append(display_value)

        if not values:
            values = ["No doctors available"]

        self.doctor_menu.configure(
            values=values
        )

        self.doctor_menu.set(
            values[0]
        )

    # ---------------------------------------------------------
    # Add appointment
    # ---------------------------------------------------------

    def add_appointment(self):

        try:

            patient_display = self.patient_menu.get()
            doctor_display = self.doctor_menu.get()

            patient_id = self.patient_map.get(
                patient_display
            )

            doctor_id = self.doctor_map.get(
                doctor_display
            )

            date = self.date_entry.get().strip()
            time = self.time_entry.get().strip()
            status = self.status_menu.get()

            appointment_id = (
                self.appointment_service.add_appointment(
                    patient_id,
                    doctor_id,
                    date,
                    time,
                    status
                )
            )

            messagebox.showinfo(
                "Success",
                f"Appointment booked successfully.\n\n"
                f"Appointment ID: {appointment_id}"
            )

            self.clear_form()
            self.load_appointments()

        except ValueError as error:

            messagebox.showerror(
                "Validation Error",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not book appointment.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Load appointments
    # ---------------------------------------------------------

    def load_appointments(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        appointments = (
            self.appointment_service.get_all_appointments()
        )

        for appointment in appointments:

            waiting_time = (
                self.get_waiting_time_text(appointment)
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
                    waiting_time
                )
            )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search_appointments(self, event=None):

        search_text = (
            self.search_entry.get().strip()
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not search_text:

            self.load_appointments()
            return

        appointments = (
            self.appointment_service.search_appointments(
                search_text
            )
        )

        for appointment in appointments:

            waiting_time = (
                self.get_waiting_time_text(appointment)
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
                    waiting_time
                )
            )

    # ---------------------------------------------------------
    # Select appointment
    # ---------------------------------------------------------

    def select_appointment(self, event=None):

        selected_item = self.tree.focus()

        if not selected_item:
            return

        values = self.tree.item(
            selected_item,
            "values"
        )

        if not values:
            return

        appointment_id = values[0]

        try:

            appointment = (
                self.appointment_service.get_appointment(
                    appointment_id
                )
            )

            if appointment is None:
                return

            self.selected_appointment_id = appointment_id

            # Patient
            for display_value, patient_id in self.patient_map.items():

                if patient_id == appointment["patient_id"]:

                    self.patient_menu.set(
                        display_value
                    )

                    break

            # Doctor
            for display_value, doctor_id in self.doctor_map.items():

                if doctor_id == appointment["doctor_id"]:

                    self.doctor_menu.set(
                        display_value
                    )

                    break

            self.date_entry.delete(
                0,
                "end"
            )

            self.date_entry.insert(
                0,
                appointment["appointment_date"]
            )

            self.time_entry.delete(
                0,
                "end"
            )

            self.time_entry.insert(
                0,
                appointment["appointment_time"]
            )

            self.status_menu.set(
                appointment["status"]
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    def update_appointment(self):

        if not self.selected_appointment_id:

            messagebox.showwarning(
                "Select Appointment",
                "Double-click an appointment first."
            )

            return

        try:

            patient_display = self.patient_menu.get()
            doctor_display = self.doctor_menu.get()

            patient_id = self.patient_map.get(
                patient_display
            )

            doctor_id = self.doctor_map.get(
                doctor_display
            )

            date = self.date_entry.get().strip()
            time = self.time_entry.get().strip()
            status = self.status_menu.get()

            self.appointment_service.update_appointment(
                self.selected_appointment_id,
                patient_id,
                doctor_id,
                date,
                time,
                status
            )

            messagebox.showinfo(
                "Success",
                "Appointment updated successfully."
            )

            self.clear_form()
            self.load_appointments()

        except ValueError as error:

            messagebox.showerror(
                "Validation Error",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not update appointment.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Cancel
    # ---------------------------------------------------------

    def cancel_appointment(self):

        if not self.selected_appointment_id:

            messagebox.showwarning(
                "Select Appointment",
                "Double-click an appointment first."
            )

            return

        confirm = messagebox.askyesno(
            "Cancel Appointment",
            "Are you sure you want to cancel this appointment?"
        )

        if not confirm:
            return

        try:

            appointment = (
                self.appointment_service.get_appointment(
                    self.selected_appointment_id
                )
            )

            self.appointment_service.update_appointment(
                self.selected_appointment_id,
                appointment["patient_id"],
                appointment["doctor_id"],
                appointment["appointment_date"],
                appointment["appointment_time"],
                "Cancelled"
            )

            messagebox.showinfo(
                "Success",
                "Appointment cancelled successfully."
            )

            self.clear_form()
            self.load_appointments()

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not cancel appointment.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Check in
    # ---------------------------------------------------------

    def check_in(self):

        if not self.selected_appointment_id:

            messagebox.showwarning(
                "Select Appointment",
                "Double-click an appointment first."
            )

            return

        try:

            appointment = (
                self.appointment_service.get_appointment(
                    self.selected_appointment_id
                )
            )

            self.appointment_service.check_in_patient(
                self.selected_appointment_id
            )

            self.appointment_service.update_appointment(
                self.selected_appointment_id,
                appointment["patient_id"],
                appointment["doctor_id"],
                appointment["appointment_date"],
                appointment["appointment_time"],
                "Checked In"
            )

            messagebox.showinfo(
                "Check In",
                "Patient check-in time recorded."
            )

            self.clear_form()
            self.load_appointments()

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not check in patient.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Start consultation
    # ---------------------------------------------------------

    def start_consultation(self):

        if not self.selected_appointment_id:

            messagebox.showwarning(
                "Select Appointment",
                "Double-click an appointment first."
            )

            return

        try:

            appointment = (
                self.appointment_service.get_appointment(
                    self.selected_appointment_id
                )
            )

            if not appointment["check_in_time"]:

                messagebox.showwarning(
                    "Patient Not Checked In",
                    "The patient must be checked in first."
                )

                return

            self.appointment_service.start_consultation(
                self.selected_appointment_id
            )

            self.appointment_service.update_appointment(
                self.selected_appointment_id,
                appointment["patient_id"],
                appointment["doctor_id"],
                appointment["appointment_date"],
                appointment["appointment_time"],
                "In Consultation"
            )

            messagebox.showinfo(
                "Consultation",
                "Consultation start time recorded."
            )

            self.clear_form()
            self.load_appointments()

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not start consultation.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Waiting time
    # ---------------------------------------------------------

    def get_waiting_time_text(self, appointment):

        waiting_seconds = (
            self.appointment_service.calculate_waiting_time(
                appointment["check_in_time"],
                appointment["consultation_start_time"]
            )
        )

        if waiting_seconds is None:
            return "-"

        minutes = waiting_seconds // 60
        seconds = waiting_seconds % 60

        if minutes > 0:

            return f"{minutes} min {seconds} sec"

        return f"{seconds} sec"

    # ---------------------------------------------------------
    # Refresh
    # ---------------------------------------------------------

    def refresh_appointments(self):

        self.search_entry.unbind(
            "<KeyRelease>"
        )

        self.search_entry.delete(
            0,
            "end"
        )

        self.load_patients()
        self.load_doctors()
        self.load_appointments()

        self.clear_form()

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_appointments
        )

    # ---------------------------------------------------------
    # Clear
    # ---------------------------------------------------------

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

        self.status_menu.set(
            "Scheduled"
        )

        if self.patient_map:

            first_patient = next(
                iter(self.patient_map)
            )

            self.patient_menu.set(
                first_patient
            )

        if self.doctor_map:

            first_doctor = next(
                iter(self.doctor_map)
            )

            self.doctor_menu.set(
                first_doctor
            )


# -------------------------------------------------------------
# Standalone testing
# -------------------------------------------------------------

if __name__ == "__main__":

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    root.title(
        "Hospital Management System - Appointments"
    )

    root.geometry(
        "1250x750"
    )

    appointment_gui = AppointmentGUI(root)
    appointment_gui.pack(
        fill="both",
        expand=True
    )

    root.mainloop()