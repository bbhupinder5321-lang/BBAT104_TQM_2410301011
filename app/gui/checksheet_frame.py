import customtkinter as ctk
from tkinter import ttk, messagebox

from app.services.checksheet_service import ChecksheetService


class ChecksheetFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.service = ChecksheetService()

        self.configure(fg_color="transparent")

        self.create_layout()
        self.refresh_data()

    def create_layout(self):
        # -------------------------------------------------
        # Header
        # -------------------------------------------------
        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=20,
            pady=(15, 8)
        )

        title = ctk.CTkLabel(
            header,
            text="Checksheet Analysis",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Track and measure the frequency of performance defects",
            font=ctk.CTkFont(size=12)
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # -------------------------------------------------
        # Summary Cards
        # -------------------------------------------------
        summary_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        summary_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        summary_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.total_card = self.create_summary_card(
            summary_frame,
            "Total Defects",
            "0"
        )
        self.total_card.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        self.types_card = self.create_summary_card(
            summary_frame,
            "Defect Types",
            "0"
        )
        self.types_card.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5
        )

        self.frequent_card = self.create_summary_card(
            summary_frame,
            "Most Frequent",
            "-"
        )
        self.frequent_card.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=(5, 0)
        )

        # -------------------------------------------------
        # Add Defect Section
        # -------------------------------------------------
        input_frame = ctk.CTkFrame(
            self,
            corner_radius=10
        )
        input_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        input_frame.grid_columnconfigure(1, weight=1)

        label = ctk.CTkLabel(
            input_frame,
            text="Add / Record Defect",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        label.grid(
            row=0,
            column=0,
            padx=(12, 10),
            pady=10
        )

        self.defect_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Performance defect name"
        )
        self.defect_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
            pady=10
        )

        self.count_entry = ctk.CTkEntry(
            input_frame,
            width=90,
            placeholder_text="Count"
        )
        self.count_entry.grid(
            row=0,
            column=2,
            padx=5,
            pady=10
        )

        add_button = ctk.CTkButton(
            input_frame,
            text="Add Defect",
            width=110,
            command=self.add_defect
        )
        add_button.grid(
            row=0,
            column=3,
            padx=(5, 12),
            pady=10
        )

        # -------------------------------------------------
        # Table Section
        # -------------------------------------------------
        table_frame = ctk.CTkFrame(
            self,
            corner_radius=10
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        # Table heading
        table_header = ctk.CTkFrame(
            table_frame,
            fg_color="transparent"
        )
        table_header.pack(
            fill="x",
            padx=12,
            pady=(8, 4)
        )

        table_title = ctk.CTkLabel(
            table_header,
            text="Defect Frequency",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        table_title.pack(side="left")

        table_hint = ctk.CTkLabel(
            table_header,
            text="Double-click a row to record +1 occurrence",
            font=ctk.CTkFont(size=10)
        )
        table_hint.pack(side="right")

        # -------------------------------------------------
        # Treeview
        # -------------------------------------------------
        tree_container = ctk.CTkFrame(
            table_frame,
            fg_color="transparent"
        )
        tree_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 8)
        )

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        columns = (
            "number",
            "defect",
            "occurrences",
            "percentage"
        )

        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "number",
            text="#"
        )

        self.tree.heading(
            "defect",
            text="Performance Defect"
        )

        self.tree.heading(
            "occurrences",
            text="Occurrences"
        )

        self.tree.heading(
            "percentage",
            text="Percentage"
        )

        self.tree.column(
            "number",
            width=55,
            anchor="center",
            stretch=False
        )

        self.tree.column(
            "defect",
            width=400,
            anchor="w"
        )

        self.tree.column(
            "occurrences",
            width=130,
            anchor="center",
            stretch=False
        )

        self.tree.column(
            "percentage",
            width=120,
            anchor="center",
            stretch=False
        )

        scrollbar = ttk.Scrollbar(
            tree_container,
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
            self.record_selected_occurrence
        )

        # -------------------------------------------------
        # Bottom Controls
        # -------------------------------------------------
        controls = ctk.CTkFrame(
            table_frame,
            fg_color="transparent"
        )
        controls.pack(
            fill="x",
            padx=10,
            pady=(0, 8)
        )

        plus_button = ctk.CTkButton(
            controls,
            text="+1 Occurrence",
            width=130,
            command=self.record_selected_occurrence
        )
        plus_button.pack(
            side="left",
            padx=(0, 6)
        )

        remove_button = ctk.CTkButton(
            controls,
            text="Remove",
            width=100,
            command=self.remove_selected_defect
        )
        remove_button.pack(
            side="left",
            padx=6
        )

        refresh_button = ctk.CTkButton(
            controls,
            text="Refresh",
            width=100,
            command=self.refresh_data
        )
        refresh_button.pack(
            side="right"
        )

    # -----------------------------------------------------
    # Summary Card
    # -----------------------------------------------------
    def create_summary_card(self, parent, title, value):
        card = ctk.CTkFrame(
            parent,
            corner_radius=10
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=10)
        )
        title_label.pack(
            anchor="w",
            padx=12,
            pady=(7, 0)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        value_label.pack(
            anchor="w",
            padx=12,
            pady=(0, 7)
        )

        card.value_label = value_label

        return card

    # -----------------------------------------------------
    # Refresh
    # -----------------------------------------------------
    def refresh_data(self):
        records = self.service.get_records()

        total = self.service.get_total_defects()

        summary = self.service.get_summary()

        self.total_card.value_label.configure(
            text=str(total)
        )

        self.types_card.value_label.configure(
            text=str(summary["defect_types"])
        )

        most_frequent = summary["most_frequent"]

        if most_frequent:
            self.frequent_card.value_label.configure(
                text=most_frequent
            )
        else:
            self.frequent_card.value_label.configure(
                text="-"
            )

        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        if total == 0:
            return

        sorted_records = sorted(
            records.items(),
            key=lambda item: item[1],
            reverse=True
        )

        for index, (defect, count) in enumerate(
            sorted_records,
            start=1
        ):
            percentage = (
                count / total
            ) * 100

            self.tree.insert(
                "",
                "end",
                values=(
                    index,
                    defect,
                    count,
                    f"{percentage:.1f}%"
                )
            )

    # -----------------------------------------------------
    # Add Defect
    # -----------------------------------------------------
    def add_defect(self):
        defect = self.defect_entry.get().strip()
        count_text = self.count_entry.get().strip()

        if not defect:
            messagebox.showerror(
                "Invalid Input",
                "Defect name is required."
            )
            return

        if count_text:
            try:
                count = int(count_text)
            except ValueError:
                messagebox.showerror(
                    "Invalid Count",
                    "Count must be a whole number."
                )
                return
        else:
            count = 1

        try:
            self.service.add_defect(
                defect,
                count
            )

            self.defect_entry.delete(
                0,
                "end"
            )

            self.count_entry.delete(
                0,
                "end"
            )

            self.refresh_data()

        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error)
            )

    # -----------------------------------------------------
    # Get Selected Defect
    # -----------------------------------------------------
    def get_selected_defect(self):
        selected = self.tree.selection()

        if not selected:
            return None

        values = self.tree.item(
            selected[0],
            "values"
        )

        if not values:
            return None

        return values[1]

    # -----------------------------------------------------
    # Record Occurrence
    # -----------------------------------------------------
    def record_selected_occurrence(self, event=None):
        defect = self.get_selected_defect()

        if defect is None:
            if event is None:
                messagebox.showwarning(
                    "Select Defect",
                    "Please select a defect first."
                )
            return

        try:
            self.service.record_occurrence(
                defect
            )

            self.refresh_data()

        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error)
            )

    # -----------------------------------------------------
    # Remove Defect
    # -----------------------------------------------------
    def remove_selected_defect(self):
        defect = self.get_selected_defect()

        if defect is None:
            messagebox.showwarning(
                "Select Defect",
                "Please select a defect to remove."
            )
            return

        answer = messagebox.askyesno(
            "Remove Defect",
            f"Remove '{defect}' from the checksheet?"
        )

        if not answer:
            return

        try:
            self.service.remove_defect(
                defect
            )

            self.refresh_data()

        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error)
            )


def main():
    root = ctk.CTk()
    root.title("Checksheet Analysis")
    root.geometry("1100x700")
    root.minsize(900, 600)

    frame = ChecksheetFrame(root)
    frame.pack(
        fill="both",
        expand=True
    )

    root.mainloop()


if __name__ == "__main__":
    main()