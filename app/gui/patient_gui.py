import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date

from app.services.patient_service import PatientService


class PatientGUI(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.service = PatientService()

        self.create_screen()
        self.load_patients()

    def create_screen(self):

        title = ctk.CTkLabel(
            self,
            text="Patient Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Register, search, edit and delete patient records"
        )
        subtitle.pack(pady=(0, 15))

        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search patient by ID, name or phone..."
        )
        self.search_entry.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_patients
        )

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        add_button = ctk.CTkButton(
            button_frame,
            text="+ Add Patient",
            command=self.open_add_patient_form
        )
        add_button.grid(row=0, column=0, padx=5)

        edit_button = ctk.CTkButton(
            button_frame,
            text="✏ Edit Patient",
            command=self.open_edit_patient_form
        )
        edit_button.grid(row=0, column=1, padx=5)

        delete_button = ctk.CTkButton(
            button_frame,
            text="🗑 Delete Patient",
            command=self.delete_patient
        )
        delete_button.grid(row=0, column=2, padx=5)

        refresh_button = ctk.CTkButton(
            button_frame,
            text="↻ Refresh",
            command=self.refresh_patients
        )
        refresh_button.grid(row=0, column=3, padx=5)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(
            padx=30,
            pady=15,
            fill="both",
            expand=True
        )

        columns = (
            "ID",
            "Name",
            "DOB",
            "Gender",
            "Phone",
            "Blood Group"
        )

        self.patient_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.patient_table.heading(
                column,
                text=column
            )

            self.patient_table.column(
                column,
                width=140
            )

        self.patient_table.pack(
            fill="both",
            expand=True
        )

        self.patient_table.bind(
            "<Double-1>",
            lambda event: self.open_edit_patient_form()
        )

    def load_patients(self):

        for row in self.patient_table.get_children():
            self.patient_table.delete(row)

        patients = self.service.get_all_patients()

        for patient in patients:
            self.patient_table.insert(
                "",
                "end",
                values=(
                    patient["patient_id"],
                    patient["full_name"],
                    patient["dob"],
                    patient["gender"],
                    patient["phone"],
                    patient["blood_group"]
                )
            )

    def refresh_patients(self):

        self.search_entry.unbind("<KeyRelease>")

        self.search_entry.delete(0, "end")

        self.load_patients()

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_patients
        )

        messagebox.showinfo(
            "Refresh",
            "Patient records refreshed successfully."
        )

    def search_patients(self, event=None):

        search_text = self.search_entry.get().strip()

        if not search_text:
            self.load_patients()
            return

        patients = self.service.search_patients(
            search_text
        )

        for row in self.patient_table.get_children():
            self.patient_table.delete(row)

        for patient in patients:
            self.patient_table.insert(
                "",
                "end",
                values=(
                    patient["patient_id"],
                    patient["full_name"],
                    patient["dob"],
                    patient["gender"],
                    patient["phone"],
                    patient["blood_group"]
                )
            )

    def get_selected_patient_id(self):

        selected = self.patient_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Patient Selected",
                "Please select a patient first."
            )
            return None

        values = self.patient_table.item(
            selected[0],
            "values"
        )

        return int(values[0])

    def open_add_patient_form(self):

        form = ctk.CTkToplevel(self)
        form.title("Add Patient")
        form.geometry("500x600")

        title = ctk.CTkLabel(
            form,
            text="Register New Patient",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=20)

        name_entry = ctk.CTkEntry(
            form,
            placeholder_text="Full Name"
        )
        name_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )

        dob_entry = ctk.CTkEntry(
            form,
            placeholder_text="Date of Birth (YYYY-MM-DD)"
        )
        dob_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )

        gender_entry = ctk.CTkEntry(
            form,
            placeholder_text="Gender"
        )
        gender_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )

        phone_entry = ctk.CTkEntry(
            form,
            placeholder_text="Phone Number"
        )
        phone_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )

        address_entry = ctk.CTkEntry(
            form,
            placeholder_text="Address"
        )
        address_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )

        blood_group_entry = ctk.CTkEntry(
            form,
            placeholder_text="Blood Group"
        )
        blood_group_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )

        message_label = ctk.CTkLabel(
            form,
            text=""
        )
        message_label.pack(pady=10)

        def save_patient():

            try:

                patient_id = self.service.add_patient(
                    name_entry.get(),
                    dob_entry.get(),
                    gender_entry.get(),
                    phone_entry.get(),
                    address_entry.get(),
                    blood_group_entry.get(),
                    date.today().isoformat()
                )

                message_label.configure(
                    text=f"Patient added successfully! ID: {patient_id}"
                )

                self.load_patients()

            except ValueError as error:

                message_label.configure(
                    text=str(error)
                )

            except Exception as error:

                message_label.configure(
                    text=f"Database error: {error}"
                )

        save_button = ctk.CTkButton(
            form,
            text="Save Patient",
            command=save_patient
        )
        save_button.pack(pady=15)

    def open_edit_patient_form(self):

        patient_id = self.get_selected_patient_id()

        if patient_id is None:
            return

        patient = self.service.get_patient(
            patient_id
        )

        if patient is None:

            messagebox.showerror(
                "Error",
                "Patient record not found."
            )
            return

        form = ctk.CTkToplevel(self)
        form.title("Edit Patient")
        form.geometry("500x600")

        title = ctk.CTkLabel(
            form,
            text="Edit Patient",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=20)

        name_entry = ctk.CTkEntry(form)
        name_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )
        name_entry.insert(
            0,
            patient["full_name"]
        )

        dob_entry = ctk.CTkEntry(form)
        dob_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )
        dob_entry.insert(
            0,
            patient["dob"]
        )

        gender_entry = ctk.CTkEntry(form)
        gender_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )
        gender_entry.insert(
            0,
            patient["gender"]
        )

        phone_entry = ctk.CTkEntry(form)
        phone_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )
        phone_entry.insert(
            0,
            patient["phone"]
        )

        address_entry = ctk.CTkEntry(form)
        address_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )
        address_entry.insert(
            0,
            patient["address"] or ""
        )

        blood_group_entry = ctk.CTkEntry(form)
        blood_group_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )
        blood_group_entry.insert(
            0,
            patient["blood_group"] or ""
        )

        message_label = ctk.CTkLabel(
            form,
            text=""
        )
        message_label.pack(pady=10)

        def update_patient():

            try:

                updated = self.service.update_patient(
                    patient_id,
                    name_entry.get(),
                    dob_entry.get(),
                    gender_entry.get(),
                    phone_entry.get(),
                    address_entry.get(),
                    blood_group_entry.get()
                )

                if updated:

                    message_label.configure(
                        text="Patient updated successfully!"
                    )

                    self.load_patients()

            except ValueError as error:

                message_label.configure(
                    text=str(error)
                )

            except Exception as error:

                message_label.configure(
                    text=f"Database error: {error}"
                )

        update_button = ctk.CTkButton(
            form,
            text="Save Changes",
            command=update_patient
        )
        update_button.pack(pady=15)

    def delete_patient(self):

        patient_id = self.get_selected_patient_id()

        if patient_id is None:
            return

        confirm = messagebox.askyesno(
            "Delete Patient",
            f"Are you sure you want to delete patient ID {patient_id}?"
        )

        if not confirm:
            return

        try:

            if deleted := self.service.delete_patient(
                patient_id
            ):

                messagebox.showinfo(
                    "Success",
                    "Patient deleted successfully."
                )

                self.load_patients()

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )


if __name__ == "__main__":

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Hospital Management System")
    app.geometry("1000x650")

    patient_screen = PatientGUI(app)

    patient_screen.pack(
        fill="both",
        expand=True
    )

    app.mainloop()