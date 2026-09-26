import tkinter as tk
from tkinter import ttk, messagebox

import customtkinter as ctk

from app.services.doctor_service import DoctorService


class DoctorFrame(ctk.CTkFrame):

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

        self.service = DoctorService()
        self.selected_doctor_id = None

        self.create_ui()
        self.load_doctors()

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
            text="Doctor Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.TEXT_DARK
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Manage doctors, specializations and availability",
            font=ctk.CTkFont(size=11),
            text_color=self.SECONDARY
        )
        subtitle.pack(
            anchor="w",
            pady=(2, 0)
        )

        # -----------------------------------------------------
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
            text="Doctor Details",
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

        # Doctor name
        self.create_label(
            form_card,
            "Full Name",
            1,
            0
        )

        self.name_entry = ctk.CTkEntry(
            form_card,
            height=36,
            placeholder_text="Enter doctor name"
        )

        self.name_entry.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 12)
        )

        # Specialization
        self.create_label(
            form_card,
            "Specialization",
            1,
            1
        )

        self.specialization_entry = ctk.CTkEntry(
            form_card,
            height=36,
            placeholder_text="e.g. Cardiologist"
        )

        self.specialization_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=(0, 12)
        )

        # Phone
        self.create_label(
            form_card,
            "Phone Number",
            1,
            2
        )

        self.phone_entry = ctk.CTkEntry(
            form_card,
            height=36,
            placeholder_text="10 digit phone number"
        )

        self.phone_entry.grid(
            row=2,
            column=2,
            sticky="ew",
            padx=(10, 20),
            pady=(0, 12)
        )

        # Status
        self.create_label(
            form_card,
            "Status",
            3,
            0
        )

        self.status_combo = ctk.CTkComboBox(
            form_card,
            height=36,
            values=[
                "Active",
                "Inactive"
            ]
        )

        self.status_combo.set("Active")

        self.status_combo.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=(20, 10),
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

        add_button = ctk.CTkButton(
            button_frame,
            text="Add Doctor",
            width=115,
            height=36,
            command=self.add_doctor
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
            command=self.update_doctor
        )

        update_button.pack(
            side="left",
            padx=8
        )

        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete",
            width=100,
            height=36,
            fg_color="#B42318",
            hover_color="#912018",
            command=self.delete_doctor
        )

        delete_button.pack(
            side="left",
            padx=8
        )

        clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            width=100,
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

        # Search
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
            text="Doctor Records",
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
            placeholder_text="Search name, specialization or phone..."
        )

        self.search_entry.pack(
            side="right",
            padx=(10, 0)
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_doctors
        )

        refresh_button = ctk.CTkButton(
            search_frame,
            text="↻ Refresh",
            width=90,
            height=36,
            command=self.refresh_doctors
        )

        refresh_button.pack(
            side="right"
        )

        # Tree
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
            "specialization",
            "phone",
            "status"
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
            "name",
            text="Doctor Name"
        )

        self.tree.heading(
            "specialization",
            text="Specialization"
        )

        self.tree.heading(
            "phone",
            text="Phone"
        )

        self.tree.heading(
            "status",
            text="Status"
        )

        self.tree.column(
            "id",
            width=70,
            anchor="center"
        )

        self.tree.column(
            "name",
            width=220
        )

        self.tree.column(
            "specialization",
            width=220
        )

        self.tree.column(
            "phone",
            width=160,
            anchor="center"
        )

        self.tree.column(
            "status",
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
            self.select_doctor
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

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    def add_doctor(self):
        try:
            doctor_id = self.service.add_doctor(
                self.name_entry.get(),
                self.specialization_entry.get(),
                self.phone_entry.get(),
                self.status_combo.get()
            )

            messagebox.showinfo(
                "Success",
                f"Doctor added successfully.\nDoctor ID: {doctor_id}"
            )

            self.clear_form()
            self.load_doctors()

        except Exception as error:
            messagebox.showerror(
                "Unable to Add Doctor",
                str(error)
            )

    def update_doctor(self):
        if not self.selected_doctor_id:
            messagebox.showwarning(
                "Select Doctor",
                "Double-click a doctor record first."
            )
            return

        try:
            self.service.update_doctor(
                self.selected_doctor_id,
                self.name_entry.get(),
                self.specialization_entry.get(),
                self.phone_entry.get(),
                self.status_combo.get()
            )

            messagebox.showinfo(
                "Success",
                "Doctor updated successfully."
            )

            self.clear_form()
            self.load_doctors()

        except Exception as error:
            messagebox.showerror(
                "Unable to Update Doctor",
                str(error)
            )

    def delete_doctor(self):
        if not self.selected_doctor_id:
            messagebox.showwarning(
                "Select Doctor",
                "Double-click a doctor record first."
            )
            return

        answer = messagebox.askyesno(
            "Delete Doctor",
            "Are you sure you want to delete this doctor?"
        )

        if not answer:
            return

        try:
            self.service.delete_doctor(
                self.selected_doctor_id
            )

            messagebox.showinfo(
                "Success",
                "Doctor deleted successfully."
            )

            self.clear_form()
            self.load_doctors()

        except Exception as error:
            messagebox.showerror(
                "Unable to Delete Doctor",
                str(error)
            )

    # ---------------------------------------------------------
    # Loading / Search
    # ---------------------------------------------------------

    def load_doctors(self):
        try:
            doctors = self.service.get_all_doctors()
            self.display_doctors(doctors)

        except Exception as error:
            messagebox.showerror(
                "Loading Error",
                str(error)
            )

    def search_doctors(self, event=None):
        search_text = self.search_entry.get().strip()

        try:
            if search_text:
                doctors = self.service.search_doctors(
                    search_text
                )
            else:
                doctors = self.service.get_all_doctors()

            self.display_doctors(doctors)

        except Exception as error:
            messagebox.showerror(
                "Search Error",
                str(error)
            )

    def display_doctors(self, doctors):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for doctor in doctors:
            self.tree.insert(
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
        self.search_entry.unbind(
            "<KeyRelease>"
        )

        self.search_entry.delete(
            0,
            "end"
        )

        self.clear_form()
        self.load_doctors()

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_doctors
        )

    # ---------------------------------------------------------
    # Selection / Form
    # ---------------------------------------------------------

    def select_doctor(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        self.selected_doctor_id = int(
            values[0]
        )

        self.name_entry.delete(
            0,
            "end"
        )

        self.name_entry.insert(
            0,
            values[1]
        )

        self.specialization_entry.delete(
            0,
            "end"
        )

        self.specialization_entry.insert(
            0,
            values[2]
        )

        self.phone_entry.delete(
            0,
            "end"
        )

        self.phone_entry.insert(
            0,
            values[3]
        )

        self.status_combo.set(
            values[4]
        )

    def clear_form(self):
        self.selected_doctor_id = None

        self.name_entry.delete(
            0,
            "end"
        )

        self.specialization_entry.delete(
            0,
            "end"
        )

        self.phone_entry.delete(
            0,
            "end"
        )

        self.status_combo.set(
            "Active"
        )

        for item in self.tree.selection():
            self.tree.selection_remove(item)


# -------------------------------------------------------------
# Standalone Test
# -------------------------------------------------------------

if __name__ == "__main__":
    root = ctk.CTk()

    root.title(
        "Doctor Management"
    )

    root.geometry(
        "1280x760"
    )

    frame = DoctorFrame(root)

    frame.pack(
        fill="both",
        expand=True
    )

    root.mainloop()