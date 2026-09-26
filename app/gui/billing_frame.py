import customtkinter as ctk

from app.gui.ui_kit import HospitalFrame
from tkinter import ttk, messagebox
from datetime import date

from app.services.bill_service import BillService
from app.services.patient_service import PatientService


class BillingFrame(HospitalFrame):

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

        self.bill_service = BillService()
        self.patient_service = PatientService()

        self.selected_bill_id = None
        self.patient_map = {}

        self.create_ui()
        self.load_patients()
        self.load_bills()

    # ---------------------------------------------------------
    # Main UI
    # ---------------------------------------------------------

    def create_ui(self):

        # Header
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
            text="▣  Billing Management",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color="#172033"
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Generate and manage patient bills",
            font=ctk.CTkFont(size=11),
            text_color=self.SECONDARY
        )

        subtitle.pack(anchor="w")

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        form = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER
        )

        form.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        for column in range(4):
            form.grid_columnconfigure(
                column,
                weight=1
            )

        # Patient
        patient_label = ctk.CTkLabel(
            form,
            text="Patient",
            font=ctk.CTkFont(size=12),
            text_color="#4B5563"
        )

        patient_label.grid(
            row=0,
            column=0,
            padx=15,
            pady=(18, 5),
            sticky="w"
        )

        self.patient_combo = ctk.CTkComboBox(
            form,
            height=38,
            values=["No patients available"]
        )

        self.patient_combo.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 18),
            sticky="ew"
        )

        # Bill Date
        date_label = ctk.CTkLabel(
            form,
            text="Bill Date",
            font=ctk.CTkFont(size=12),
            text_color="#4B5563"
        )

        date_label.grid(
            row=0,
            column=1,
            padx=15,
            pady=(18, 5),
            sticky="w"
        )

        self.date_entry = ctk.CTkEntry(
            form,
            height=38,
            placeholder_text="YYYY-MM-DD"
        )

        self.date_entry.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 18),
            sticky="ew"
        )

        self.date_entry.insert(
            0,
            date.today().isoformat()
        )

        # Description
        description_label = ctk.CTkLabel(
            form,
            text="Description",
            font=ctk.CTkFont(size=12),
            text_color="#4B5563"
        )

        description_label.grid(
            row=0,
            column=2,
            padx=15,
            pady=(18, 5),
            sticky="w"
        )

        self.description_entry = ctk.CTkEntry(
            form,
            height=38,
            placeholder_text="e.g. Consultation Fee"
        )

        self.description_entry.grid(
            row=1,
            column=2,
            padx=15,
            pady=(0, 18),
            sticky="ew"
        )

        # Amount
        amount_label = ctk.CTkLabel(
            form,
            text="Amount",
            font=ctk.CTkFont(size=12),
            text_color="#4B5563"
        )

        amount_label.grid(
            row=0,
            column=3,
            padx=15,
            pady=(18, 5),
            sticky="w"
        )

        self.amount_entry = ctk.CTkEntry(
            form,
            height=38,
            placeholder_text="e.g. 500"
        )

        self.amount_entry.grid(
            row=1,
            column=3,
            padx=15,
            pady=(0, 18),
            sticky="ew"
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
            padx=30,
            pady=(0, 15)
        )

        self.generate_button = ctk.CTkButton(
            button_frame,
            text="＋  Generate Bill",
            width=130,
            height=38,
            command=self.add_bill
        )

        self.generate_button.pack(
            side="left",
            padx=(0, 8)
        )

        self.update_button = ctk.CTkButton(
            button_frame,
            text="Update",
            width=100,
            height=38,
            fg_color="#37445D",
            hover_color="#4A5872",
            command=self.update_bill
        )

        self.update_button.pack(
            side="left",
            padx=4
        )

        self.delete_button = ctk.CTkButton(
            button_frame,
            text="Delete",
            width=100,
            height=38,
            fg_color="#B23A48",
            hover_color="#922F3B",
            command=self.delete_bill
        )

        self.delete_button.pack(
            side="left",
            padx=4
        )

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="↺  Clear",
            width=100,
            height=38,
            fg_color="#6B7280",
            hover_color="#555B66",
            command=self.clear_form
        )

        self.clear_button.pack(
            side="left",
            padx=4
        )

        # -----------------------------------------------------
        # Search
        # -----------------------------------------------------

        search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        search_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 10)
        )

        search_label = ctk.CTkLabel(
            search_frame,
            text="Search Bills",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color="#172033"
        )

        search_label.pack(
            side="left",
            padx=(0, 10)
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=36,
            placeholder_text="Search by patient, description or bill ID..."
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_bills
        )

        refresh_button = ctk.CTkButton(
            search_frame,
            text="↻  Refresh",
            width=100,
            height=36,
            command=self.refresh_bills
        )

        refresh_button.pack(
            side="left",
            padx=(10, 0)
        )

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        table_frame = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        columns = (
            "bill_id",
            "patient",
            "bill_date",
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
            "bill_date",
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
            width=220
        )

        self.tree.column(
            "bill_date",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "description",
            width=250
        )

        self.tree.column(
            "amount",
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
            expand=True,
            padx=(15, 0),
            pady=15
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=15
        )

        self.tree.bind(
            "<Double-1>",
            self.select_bill
        )

    # ---------------------------------------------------------
    # Patient Loading
    # ---------------------------------------------------------

    def load_patients(self):

        try:
            patients = self.patient_service.get_all_patients()

        except Exception as error:
            messagebox.showerror(
                "Patient Error",
                str(error)
            )
            return

        self.patient_map.clear()

        patient_values = []

        for patient in patients:

            patient_id = patient["patient_id"]
            patient_name = patient["full_name"]

            display_text = f"{patient_id} - {patient_name}"

            self.patient_map[display_text] = patient_id

            patient_values.append(
                display_text
            )

        if not patient_values:
            patient_values = [
                "No patients available"
            ]

        self.patient_combo.configure(
            values=patient_values
        )

        self.patient_combo.set(
            patient_values[0]
        )

    # ---------------------------------------------------------
    # Load Bills
    # ---------------------------------------------------------

    def update_ux_stats(self):
        try:
            items=self.tree.get_children()
            self.ux_stat_labels["total bills"].configure(text=str(len(items)))
            joined=" ".join(str(v) for i in items for v in self.tree.item(i,"values")).lower()
            self.ux_stat_labels["paid"].configure(text=str(joined.count("paid")))
            self.ux_stat_labels["pending"].configure(text=str(joined.count("pending")))
            self.ux_stat_labels["selected"].configure(text="Ready" if self.selected_bill_id else "None")
        except Exception:
            pass

    def load_bills(self):

        try:
            bills = self.bill_service.get_all_bills()

        except Exception as error:
            messagebox.showerror(
                "Billing Error",
                str(error)
            )
            return

        self.populate_table(
            bills
        )

    # ---------------------------------------------------------
    # Populate Table
    # ---------------------------------------------------------

    def populate_table(self, bills):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for bill in bills:

            amount = bill["amount"]

            self.tree.insert(
                "",
                "end",
                values=(
                    bill["bill_id"],
                    bill["patient_name"],
                    bill["bill_date"],
                    bill["description"],
                    f"₹ {amount:.2f}"
                )
            )

    # ---------------------------------------------------------
    # Add Bill
    # ---------------------------------------------------------

        self.update_ux_stats()

    def add_bill(self):

        patient_display = self.patient_combo.get()

        patient_id = self.patient_map.get(
            patient_display
        )

        if patient_id is None:
            messagebox.showwarning(
                "Invalid Patient",
                "Please select a valid patient."
            )
            return

        bill_date = self.date_entry.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()

        try:

            bill_id = self.bill_service.add_bill(
                patient_id,
                bill_date,
                description,
                amount
            )

            self.show_toast("Operation completed")

            messagebox.showinfo(
                "Success",
                f"Bill generated successfully.\n\nBill ID: {bill_id}"
            )

            self.clear_form()
            self.load_bills()

        except Exception as error:

            messagebox.showerror(
                "Billing Error",
                str(error)
            )

    # ---------------------------------------------------------
    # Update Bill
    # ---------------------------------------------------------

    def update_bill(self):

        if self.selected_bill_id is None:
            messagebox.showwarning(
                "No Selection",
                "Please double-click a bill to edit it."
            )
            return

        patient_display = self.patient_combo.get()

        patient_id = self.patient_map.get(
            patient_display
        )

        if patient_id is None:
            messagebox.showwarning(
                "Invalid Patient",
                "Please select a valid patient."
            )
            return

        bill_date = self.date_entry.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()

        try:

            self.bill_service.update_bill(
                self.selected_bill_id,
                patient_id,
                bill_date,
                description,
                amount
            )

            self.show_toast("Operation completed")

            messagebox.showinfo(
                "Success",
                "Bill updated successfully."
            )

            self.clear_form()
            self.load_bills()

        except Exception as error:

            messagebox.showerror(
                "Billing Error",
                str(error)
            )

    # ---------------------------------------------------------
    # Delete Bill
    # ---------------------------------------------------------

    def delete_bill(self):

        if self.selected_bill_id is None:
            messagebox.showwarning(
                "No Selection",
                "Please double-click a bill to select it."
            )
            return

        answer = messagebox.askyesno(
            "Delete Bill",
            "Are you sure you want to delete this bill?"
        )

        if not answer:
            return

        try:

            self.bill_service.delete_bill(
                self.selected_bill_id
            )

            self.show_toast("Operation completed")

            messagebox.showinfo(
                "Success",
                "Bill deleted successfully."
            )

            self.clear_form()
            self.load_bills()

        except Exception as error:

            messagebox.showerror(
                "Billing Error",
                str(error)
            )

    # ---------------------------------------------------------
    # Select Bill
    # ---------------------------------------------------------

    def select_bill(self, event=None):

        selected_item = self.tree.selection()

        if not selected_item:
            return

        values = self.tree.item(
            selected_item[0],
            "values"
        )

        if not values:
            return

        self.selected_bill_id = int(
            values[0]
        )

        patient_name = values[1]
        bill_date = values[2]
        description = values[3]
        amount = values[4]

        # Find patient in dropdown
        selected_patient = None

        for display_text, patient_id in self.patient_map.items():

            if display_text.endswith(
                f" - {patient_name}"
            ):
                selected_patient = display_text
                break

        if selected_patient:
            self.patient_combo.set(
                selected_patient
            )

        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            bill_date
        )

        self.description_entry.delete(
            0,
            "end"
        )

        self.description_entry.insert(
            0,
            description
        )

        self.amount_entry.delete(
            0,
            "end"
        )

        # Remove ₹ symbol when loading amount
        clean_amount = str(
            amount
        ).replace(
            "₹",
            ""
        ).strip()

        self.amount_entry.insert(
            0,
            clean_amount
        )

    # ---------------------------------------------------------
    # Search Bills
    # ---------------------------------------------------------

    def search_bills(self, event=None):

        search_text = self.search_entry.get()

        try:

            bills = self.bill_service.search_bills(
                search_text
            )

            self.populate_table(
                bills
            )

        except Exception as error:

            messagebox.showerror(
                "Search Error",
                str(error)
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

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_bills
        )

    # ---------------------------------------------------------
    # Clear Form
    # ---------------------------------------------------------

    def clear_form(self):

        self.selected_bill_id = None

        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            date.today().isoformat()
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

            self.patient_combo.set(
                first_patient
            )

        self.tree.selection_remove(
            self.tree.selection()
        )


# -------------------------------------------------------------
# Standalone Test
# -------------------------------------------------------------

if __name__ == "__main__":

    app = ctk.CTk()

    app.title(
        "Billing Management Test"
    )

    app.geometry(
        "1280x760"
    )

    app.minsize(
        1050,
        650
    )

    ctk.set_appearance_mode(
        "light"
    )

    ctk.set_default_color_theme(
        "blue"
    )

    billing_frame = BillingFrame(
        app
    )

    billing_frame.pack(
        fill="both",
        expand=True
    )

    app.mainloop()