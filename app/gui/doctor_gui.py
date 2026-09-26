import customtkinter as ctk
from tkinter import ttk, messagebox

from app.services.doctor_service import DoctorService


class DoctorGUI(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.service = DoctorService()

        self.create_screen()
        self.load_doctors()

    def create_screen(self):

        title = ctk.CTkLabel(
            self,
            text="Doctor Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Add, search, edit and delete doctor records"
        )
        subtitle.pack(pady=(0, 15))

        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search doctor by ID, name, specialization or phone..."
        )
        self.search_entry.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_doctors
        )

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        add_button = ctk.CTkButton(
            button_frame,
            text="+ Add Doctor",
            command=self.open_add_doctor_form
        )
        add_button.grid(
            row=0,
            column=0,
            padx=5
        )

        edit_button = ctk.CTkButton(
            button_frame,
            text="✏ Edit Doctor",
            command=self.open_edit_doctor_form
        )
        edit_button.grid(
            row=0,
            column=1,
            padx=5
        )

        delete_button = ctk.CTkButton(
            button_frame,
            text="🗑 Delete Doctor",
            command=self.delete_doctor
        )
        delete_button.grid(
            row=0,
            column=2,
            padx=5
        )

        refresh_button = ctk.CTkButton(
            button_frame,
            text="↻ Refresh",
            command=self.refresh_doctors
        )
        refresh_button.grid(
            row=0,
            column=3,
            padx=5
        )

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
            "Specialization",
            "Phone",
            "Status"
        )

        self.doctor_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        column_widths = {
            "ID": 70,
            "Name": 220,
            "Specialization": 200,
            "Phone": 160,
            "Status": 120
        }

        for column in columns:

            self.doctor_table.heading(
                column,
                text=column
            )

            self.doctor_table.column(
                column,
                width=column_widths[column],
                anchor="center"
            )

        self.doctor_table.pack(
            fill="both",
            expand=True
        )

        self.doctor_table.bind(
            "<Double-1>",
            lambda event: self.open_edit_doctor_form()
        )

    def load_doctors(self):

        for row in self.doctor_table.get_children():
            self.doctor_table.delete(row)

        doctors = self.service.get_all_doctors()

        for doctor in doctors:

            self.doctor_table.insert(
                "",
                "end",
                values=(
                    doctor["doctor_id"],
                    doctor["full_name"],
                    doctor["specialization"],
                    doctor["phone"],
                    doctor["status"]
                )
            )

    def refresh_doctors(self):

        self.search_entry.unbind("<KeyRelease>")

        self.search_entry.delete(
            0,
            "end"
        )

        self.load_doctors()

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_doctors
        )

    def search_doctors(self, event=None):

        search_text = self.search_entry.get().strip()

        if not search_text:

            self.load_doctors()

            return

        doctors = self.service.search_doctors(
            search_text
        )

        for row in self.doctor_table.get_children():
            self.doctor_table.delete(row)

        for doctor in doctors:

            self.doctor_table.insert(
                "",
                "end",
                values=(
                    doctor["doctor_id"],
                    doctor["full_name"],
                    doctor["specialization"],
                    doctor["phone"],
                    doctor["status"]
                )
            )

    def get_selected_doctor_id(self):

        selected = self.doctor_table.selection()

        if not selected:

            messagebox.showwarning(
                "No Doctor Selected",
                "Please select a doctor first."
            )

            return None

        values = self.doctor_table.item(
            selected[0],
            "values"
        )

        return int(values[0])

    def open_add_doctor_form(self):

        form = ctk.CTkToplevel(self)

        form.title("Add Doctor")
        form.geometry("500x520")

        form.transient(self.winfo_toplevel())

        title = ctk.CTkLabel(
            form,
            text="Register New Doctor",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
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

        specialization_entry = ctk.CTkEntry(
            form,
            placeholder_text="Specialization"
        )
        specialization_entry.pack(
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

        status_label = ctk.CTkLabel(
            form,
            text="Status"
        )
        status_label.pack(
            padx=30,
            pady=(8, 2),
            anchor="w"
        )

        status_variable = ctk.StringVar(
            value="Active"
        )

        status_menu = ctk.CTkOptionMenu(
            form,
            variable=status_variable,
            values=[
                "Active",
                "Inactive"
            ]
        )
        status_menu.pack(
            padx=30,
            pady=8,
            fill="x"
        )

        message_label = ctk.CTkLabel(
            form,
            text=""
        )
        message_label.pack(
            pady=10
        )

        def save_doctor():

            try:

                doctor_id = self.service.add_doctor(
                    name_entry.get(),
                    specialization_entry.get(),
                    phone_entry.get(),
                    status_variable.get()
                )

                message_label.configure(
                    text=f"Doctor added successfully! ID: {doctor_id}"
                )

                self.load_doctors()

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
            text="Save Doctor",
            command=save_doctor
        )
        save_button.pack(
            pady=15
        )

    def open_edit_doctor_form(self):

        doctor_id = self.get_selected_doctor_id()

        if doctor_id is None:
            return

        doctor = self.service.get_doctor(
            doctor_id
        )

        if doctor is None:

            messagebox.showerror(
                "Error",
                "Doctor record not found."
            )

            return

        form = ctk.CTkToplevel(self)

        form.title("Edit Doctor")
        form.geometry("500x520")

        form.transient(self.winfo_toplevel())

        title = ctk.CTkLabel(
            form,
            text="Edit Doctor",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
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
            doctor["full_name"]
        )

        specialization_entry = ctk.CTkEntry(form)
        specialization_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )

        specialization_entry.insert(
            0,
            doctor["specialization"]
        )

        phone_entry = ctk.CTkEntry(form)
        phone_entry.pack(
            padx=30,
            pady=8,
            fill="x"
        )

        phone_entry.insert(
            0,
            doctor["phone"]
        )

        status_label = ctk.CTkLabel(
            form,
            text="Status"
        )
        status_label.pack(
            padx=30,
            pady=(8, 2),
            anchor="w"
        )

        status_variable = ctk.StringVar(
            value=doctor["status"]
        )

        status_menu = ctk.CTkOptionMenu(
            form,
            variable=status_variable,
            values=[
                "Active",
                "Inactive"
            ]
        )
        status_menu.pack(
            padx=30,
            pady=8,
            fill="x"
        )

        message_label = ctk.CTkLabel(
            form,
            text=""
        )
        message_label.pack(
            pady=10
        )

        def update_doctor():

            try:

                updated = self.service.update_doctor(
                    doctor_id,
                    name_entry.get(),
                    specialization_entry.get(),
                    phone_entry.get(),
                    status_variable.get()
                )

                if updated:

                    message_label.configure(
                        text="Doctor updated successfully!"
                    )

                    self.load_doctors()

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
            command=update_doctor
        )
        update_button.pack(
            pady=15
        )

    def delete_doctor(self):

        doctor_id = self.get_selected_doctor_id()

        if doctor_id is None:
            return

        confirm = messagebox.askyesno(
            "Delete Doctor",
            f"Are you sure you want to delete doctor ID {doctor_id}?"
        )

        if not confirm:
            return

        try:

            deleted = self.service.delete_doctor(
                doctor_id
            )

            if deleted:

                messagebox.showinfo(
                    "Success",
                    "Doctor deleted successfully."
                )

                self.load_doctors()

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

    app.title(
        "Hospital Management System - Doctors"
    )

    app.geometry(
        "1000x650"
    )

    doctor_screen = DoctorGUI(app)

    doctor_screen.pack(
        fill="both",
        expand=True
    )

    app.mainloop()