import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date

from app.services.patient_service import PatientService


class PatientFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="#F4F7FB"
        )

        self.service = PatientService()
        self.selected_patient_id = None

        self.create_ui()
        self.load_patients()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def create_ui(self):
        # Header
        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        title = ctk.CTkLabel(
            header,
            text="Patient Management",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#172033"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Register, search and manage patient records",
            font=ctk.CTkFont(size=13),
            text_color="#6B7280"
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Form card
        form_card = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color="white"
        )
        form_card.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        form_card.grid_columnconfigure(0, weight=1)
        form_card.grid_columnconfigure(1, weight=1)
        form_card.grid_columnconfigure(2, weight=1)

        form_title = ctk.CTkLabel(
            form_card,
            text="Patient Details",
            font=ctk.CTkFont(size=17, weight="bold"),
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

        # Full name
        self.create_label(form_card, "Full Name", 1, 0)

        self.name_entry = ctk.CTkEntry(
            form_card,
            height=36,
            placeholder_text="Enter patient name"
        )
        self.name_entry.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 12)
        )

        # DOB
        self.create_label(form_card, "Date of Birth", 1, 1)

        self.dob_entry = ctk.CTkEntry(
            form_card,
            height=36,
            placeholder_text="YYYY-MM-DD"
        )
        self.dob_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=(0, 12)
        )

        # Gender
        self.create_label(form_card, "Gender", 1, 2)

        self.gender_combo = ctk.CTkComboBox(
            form_card,
            height=36,
            values=["Male", "Female", "Other"]
        )
        self.gender_combo.set("Male")
        self.gender_combo.grid(
            row=2,
            column=2,
            sticky="ew",
            padx=(10, 20),
            pady=(0, 12)
        )

        # Phone
        self.create_label(form_card, "Phone Number", 3, 0)

        self.phone_entry = ctk.CTkEntry(
            form_card,
            height=36,
            placeholder_text="10 digit phone number"
        )
        self.phone_entry.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 12)
        )

        # Blood group
        self.create_label(form_card, "Blood Group", 3, 1)

        self.blood_combo = ctk.CTkComboBox(
            form_card,
            height=36,
            values=[
                "A+",
                "A-",
                "B+",
                "B-",
                "AB+",
                "AB-",
                "O+",
                "O-"
            ]
        )
        self.blood_combo.set("A+")
        self.blood_combo.grid(
            row=4,
            column=1,
            sticky="ew",
            padx=10,
            pady=(0, 12)
        )

        # Address
        self.create_label(form_card, "Address", 3, 2)

        self.address_entry = ctk.CTkEntry(
            form_card,
            height=36,
            placeholder_text="Enter address"
        )
        self.address_entry.grid(
            row=4,
            column=2,
            sticky="ew",
            padx=(10, 20),
            pady=(0, 12)
        )

        # Buttons
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

        self.add_button = ctk.CTkButton(
            button_frame,
            text="Add Patient",
            width=115,
            height=36,
            command=self.add_patient
        )
        self.add_button.pack(side="left", padx=(0, 8))

        self.update_button = ctk.CTkButton(
            button_frame,
            text="Update",
            width=100,
            height=36,
            fg_color="#37445D",
            hover_color="#4A5872",
            command=self.update_patient
        )
        self.update_button.pack(side="left", padx=8)

        self.delete_button = ctk.CTkButton(
            button_frame,
            text="Delete",
            width=100,
            height=36,
            fg_color="#B42318",
            hover_color="#912018",
            command=self.delete_patient
        )
        self.delete_button.pack(side="left", padx=8)

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            width=100,
            height=36,
            fg_color="#E5E7EB",
            hover_color="#D1D5DB",
            text_color="#172033",
            command=self.clear_form
        )
        self.clear_button.pack(side="left", padx=8)

        # Table card
        table_card = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color="white"
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

        search_title = ctk.CTkLabel(
            search_frame,
            text="Patient Records",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#172033"
        )
        search_title.pack(side="left")

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            height=36,
            placeholder_text="Search by name, phone or ID..."
        )
        self.search_entry.pack(side="right", padx=(10, 0))

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_patients
        )

        refresh_button = ctk.CTkButton(
            search_frame,
            text="↻ Refresh",
            width=90,
            height=36,
            command=self.refresh_patients
        )
        refresh_button.pack(side="right")

        # Treeview
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
            "name",
            "dob",
            "gender",
            "phone",
            "address",
            "blood",
            "registration"
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("dob", text="DOB")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("address", text="Address")
        self.tree.heading("blood", text="Blood Group")
        self.tree.heading("registration", text="Registered")

        self.tree.column("id", width=55, anchor="center")
        self.tree.column("name", width=160)
        self.tree.column("dob", width=100, anchor="center")
        self.tree.column("gender", width=80, anchor="center")
        self.tree.column("phone", width=120, anchor="center")
        self.tree.column("address", width=180)
        self.tree.column("blood", width=90, anchor="center")
        self.tree.column("registration", width=110, anchor="center")

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
            self.select_patient
        )

        # Treeview styling
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

    def create_label(self, parent, text, row, column):
        label = ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#4B5563"
        )
        label.grid(
            row=row,
            column=column,
            sticky="w",
            padx=20 if column == 0 else 10,
            pady=(0, 5)
        )

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    def add_patient(self):
        try:
            patient_id = self.service.add_patient(
                self.name_entry.get(),
                self.dob_entry.get(),
                self.gender_combo.get(),
                self.phone_entry.get(),
                self.address_entry.get(),
                self.blood_combo.get(),
                date.today().isoformat()
            )

            messagebox.showinfo(
                "Success",
                f"Patient added successfully.\nPatient ID: {patient_id}"
            )

            self.clear_form()
            self.load_patients()

        except Exception as error:
            messagebox.showerror(
                "Unable to Add Patient",
                str(error)
            )

    def update_patient(self):
        if not self.selected_patient_id:
            messagebox.showwarning(
                "Select Patient",
                "Double-click a patient record first."
            )
            return

        try:
            self.service.update_patient(
                self.selected_patient_id,
                self.name_entry.get(),
                self.dob_entry.get(),
                self.gender_combo.get(),
                self.phone_entry.get(),
                self.address_entry.get(),
                self.blood_combo.get()
            )

            messagebox.showinfo(
                "Success",
                "Patient updated successfully."
            )

            self.clear_form()
            self.load_patients()

        except Exception as error:
            messagebox.showerror(
                "Unable to Update Patient",
                str(error)
            )

    def delete_patient(self):
        if not self.selected_patient_id:
            messagebox.showwarning(
                "Select Patient",
                "Double-click a patient record first."
            )
            return

        answer = messagebox.askyesno(
            "Delete Patient",
            "Are you sure you want to delete this patient?"
        )

        if not answer:
            return

        try:
            self.service.delete_patient(
                self.selected_patient_id
            )

            messagebox.showinfo(
                "Success",
                "Patient deleted successfully."
            )

            self.clear_form()
            self.load_patients()

        except Exception as error:
            messagebox.showerror(
                "Unable to Delete Patient",
                str(error)
            )

    # ---------------------------------------------------------
    # Loading / Search
    # ---------------------------------------------------------

    def load_patients(self):
        try:
            patients = self.service.get_all_patients()
            self.display_patients(patients)

        except Exception as error:
            messagebox.showerror(
                "Loading Error",
                str(error)
            )

    def search_patients(self, event=None):
        search_text = self.search_entry.get().strip()

        try:
            if search_text:
                patients = self.service.search_patients(search_text)
            else:
                patients = self.service.get_all_patients()

            self.display_patients(patients)

        except Exception as error:
            messagebox.showerror(
                "Search Error",
                str(error)
            )

    def display_patients(self, patients):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for patient in patients:
            self.tree.insert(
                "",
                "end",
                values=(
                    patient["patient_id"],
                    patient["full_name"],
                    patient["dob"],
                    patient["gender"],
                    patient["phone"],
                    patient["address"] or "",
                    patient["blood_group"] or "",
                    patient["registration_date"]
                )
            )

    def refresh_patients(self):
        self.search_entry.unbind("<KeyRelease>")

        self.search_entry.delete(
            0,
            "end"
        )

        self.clear_form()
        self.load_patients()

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_patients
        )

    # ---------------------------------------------------------
    # Selection / Form
    # ---------------------------------------------------------

    def select_patient(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        self.selected_patient_id = int(values[0])

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, values[1])

        self.dob_entry.delete(0, "end")
        self.dob_entry.insert(0, values[2])

        self.gender_combo.set(values[3])

        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, values[4])

        self.address_entry.delete(0, "end")
        self.address_entry.insert(0, values[5])

        if values[6]:
            self.blood_combo.set(values[6])
        else:
            self.blood_combo.set("A+")

    def clear_form(self):
        self.selected_patient_id = None

        self.name_entry.delete(0, "end")
        self.dob_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.address_entry.delete(0, "end")

        self.gender_combo.set("Male")
        self.blood_combo.set("A+")

        for item in self.tree.selection():
            self.tree.selection_remove(item)


if __name__ == "__main__":
    import tkinter as tk

    root = ctk.CTk()
    root.title("Patient Management")
    root.geometry("1280x760")

    frame = PatientFrame(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()