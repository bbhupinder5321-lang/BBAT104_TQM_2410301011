import tkinter as tk
from tkinter import ttk, messagebox

import customtkinter as ctk

from app.services.bill_service import BillService
from app.services.patient_service import PatientService


class BillGUI(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.bill_service = BillService()
        self.patient_service = PatientService()

        self.selected_bill_id = None
        self.patient_map = {}

        self.create_widgets()
        self.load_patients()
        self.load_bills()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Billing Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Generate and manage patient bills",
            font=ctk.CTkFont(size=13)
        )
        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        # Patient
        ctk.CTkLabel(
            form_frame,
            text="Patient"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.patient_menu = ctk.CTkOptionMenu(
            form_frame,
            width=260,
            values=["No patients available"]
        )
        self.patient_menu.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15)
        )

        # Bill date
        ctk.CTkLabel(
            form_frame,
            text="Bill Date (YYYY-MM-DD)"
        ).grid(
            row=0,
            column=1,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.date_entry = ctk.CTkEntry(
            form_frame,
            width=180,
            placeholder_text="2026-09-26"
        )
        self.date_entry.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 15)
        )

        # Description
        ctk.CTkLabel(
            form_frame,
            text="Description"
        ).grid(
            row=0,
            column=2,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.description_entry = ctk.CTkEntry(
            form_frame,
            width=280,
            placeholder_text="Consultation Fee"
        )
        self.description_entry.grid(
            row=1,
            column=2,
            padx=15,
            pady=(0, 15)
        )

        # Amount
        ctk.CTkLabel(
            form_frame,
            text="Amount (₹)"
        ).grid(
            row=0,
            column=3,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.amount_entry = ctk.CTkEntry(
            form_frame,
            width=160,
            placeholder_text="500.00"
        )
        self.amount_entry.grid(
            row=1,
            column=3,
            padx=15,
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        ctk.CTkButton(
            button_frame,
            text="Generate Bill",
            command=self.add_bill
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ctk.CTkButton(
            button_frame,
            text="Update",
            command=self.update_bill
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            button_frame,
            text="Delete",
            command=self.delete_bill
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_form
        ).pack(
            side="left",
            padx=8
        )

        # -----------------------------------------------------
        # Search
        # -----------------------------------------------------

        search_frame = ctk.CTkFrame(self)
        search_frame.pack(
            fill="x",
            padx=25,
            pady=(10, 5)
        )

        ctk.CTkLabel(
            search_frame,
            text="Search"
        ).pack(
            side="left",
            padx=(15, 8)
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=350,
            placeholder_text="Patient, description, date or bill ID"
        )
        self.search_entry.pack(
            side="left",
            padx=5,
            pady=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_bills
        )

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            command=self.refresh_bills
        ).pack(
            side="left",
            padx=10
        )

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
            "bill_id",
            "patient",
            "date",
            "description",
            "amount"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "bill_id",
            text="Bill ID"
        )

        self.tree.heading(
            "patient",
            text="Patient"
        )

        self.tree.heading(
            "date",
            text="Date"
        )

        self.tree.heading(
            "description",
            text="Description"
        )

        self.tree.heading(
            "amount",
            text="Amount"
        )

        self.tree.column(
            "bill_id",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "patient",
            width=200
        )

        self.tree.column(
            "date",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "description",
            width=300
        )

        self.tree.column(
            "amount",
            width=120,
            anchor="e"
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
            self.select_bill
        )

    # ---------------------------------------------------------
    # Patient dropdown
    # ---------------------------------------------------------

    def load_patients(self):

        patients = self.patient_service.get_all_patients()

        self.patient_map.clear()

        values = []

        for patient in patients:

            patient_id = patient["patient_id"]
            patient_name = patient["full_name"]

            display_value = (
                f"{patient_id} - {patient_name}"
            )

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

    # ---------------------------------------------------------
    # Add bill
    # ---------------------------------------------------------

    def add_bill(self):

        try:

            patient_display = self.patient_menu.get()

            patient_id = self.patient_map.get(
                patient_display
            )

            bill_date = (
                self.date_entry.get().strip()
            )

            description = (
                self.description_entry.get().strip()
            )

            amount = (
                self.amount_entry.get().strip()
            )

            bill_id = self.bill_service.add_bill(
                patient_id,
                bill_date,
                description,
                amount
            )

            messagebox.showinfo(
                "Success",
                f"Bill generated successfully.\n\n"
                f"Bill ID: {bill_id}"
            )

            self.clear_form()
            self.load_bills()

        except ValueError as error:

            messagebox.showerror(
                "Validation Error",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not generate bill.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Load bills
    # ---------------------------------------------------------

    def load_bills(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        bills = self.bill_service.get_all_bills()

        for bill in bills:

            self.tree.insert(
                "",
                "end",
                values=(
                    bill["bill_id"],
                    bill["patient_name"],
                    bill["bill_date"],
                    bill["description"],
                    f"₹ {bill['amount']:.2f}"
                )
            )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search_bills(self, event=None):

        search_text = (
            self.search_entry.get().strip()
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not search_text:

            self.load_bills()
            return

        bills = self.bill_service.search_bills(
            search_text
        )

        for bill in bills:

            self.tree.insert(
                "",
                "end",
                values=(
                    bill["bill_id"],
                    bill["patient_name"],
                    bill["bill_date"],
                    bill["description"],
                    f"₹ {bill['amount']:.2f}"
                )
            )

    # ---------------------------------------------------------
    # Select bill
    # ---------------------------------------------------------

    def select_bill(self, event=None):

        selected_item = self.tree.focus()

        if not selected_item:
            return

        values = self.tree.item(
            selected_item,
            "values"
        )

        if not values:
            return

        bill_id = values[0]

        try:

            bill = self.bill_service.get_bill(
                bill_id
            )

            if bill is None:
                return

            self.selected_bill_id = bill_id

            # Patient
            for display_value, patient_id in self.patient_map.items():

                if patient_id == bill["patient_id"]:

                    self.patient_menu.set(
                        display_value
                    )

                    break

            # Date
            self.date_entry.delete(
                0,
                "end"
            )

            self.date_entry.insert(
                0,
                bill["bill_date"]
            )

            # Description
            self.description_entry.delete(
                0,
                "end"
            )

            self.description_entry.insert(
                0,
                bill["description"]
            )

            # Amount
            self.amount_entry.delete(
                0,
                "end"
            )

            self.amount_entry.insert(
                0,
                str(bill["amount"])
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    def update_bill(self):

        if not self.selected_bill_id:

            messagebox.showwarning(
                "Select Bill",
                "Double-click a bill first."
            )

            return

        try:

            patient_display = self.patient_menu.get()

            patient_id = self.patient_map.get(
                patient_display
            )

            bill_date = (
                self.date_entry.get().strip()
            )

            description = (
                self.description_entry.get().strip()
            )

            amount = (
                self.amount_entry.get().strip()
            )

            self.bill_service.update_bill(
                self.selected_bill_id,
                patient_id,
                bill_date,
                description,
                amount
            )

            messagebox.showinfo(
                "Success",
                "Bill updated successfully."
            )

            self.clear_form()
            self.load_bills()

        except ValueError as error:

            messagebox.showerror(
                "Validation Error",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not update bill.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete_bill(self):

        if not self.selected_bill_id:

            messagebox.showwarning(
                "Select Bill",
                "Double-click a bill first."
            )

            return

        confirm = messagebox.askyesno(
            "Delete Bill",
            "Are you sure you want to delete this bill?"
        )

        if not confirm:
            return

        try:

            self.bill_service.delete_bill(
                self.selected_bill_id
            )

            messagebox.showinfo(
                "Success",
                "Bill deleted successfully."
            )

            self.clear_form()
            self.load_bills()

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not delete bill.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Refresh
    # ---------------------------------------------------------

    def refresh_bills(self):

        self.search_entry.unbind(
            "<KeyRelease>"
        )

        self.search_entry.delete(
            0,
            "end"
        )

        self.load_patients()
        self.load_bills()

        self.clear_form()

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_bills
        )

    # ---------------------------------------------------------
    # Clear form
    # ---------------------------------------------------------

    def clear_form(self):

        self.selected_bill_id = None

        self.date_entry.delete(
            0,
            "end"
        )

        self.description_entry.delete(
            0,
            "end"
        )

        self.amount_entry.delete(
            0,
            "end"
        )

        if self.patient_map:

            first_patient = next(
                iter(self.patient_map)
            )

            self.patient_menu.set(
                first_patient
            )


# -------------------------------------------------------------
# Standalone testing
# -------------------------------------------------------------

if __name__ == "__main__":

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    root.title(
        "Hospital Management System - Billing"
    )

    root.geometry(
        "1150x700"
    )

    bill_gui = BillGUI(root)

    bill_gui.pack(
        fill="both",
        expand=True
    )

    root.mainloop()