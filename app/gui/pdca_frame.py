import customtkinter as ctk
from tkinter import ttk, messagebox

from app.services.pdca_service import PDCAService


class PDCAFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.service = PDCAService()

        self.configure(
            fg_color="transparent"
        )

        self.create_layout()
        self.refresh_data()

    # -----------------------------------------------------
    # Main Layout
    # -----------------------------------------------------
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
            text="PDCA Cycle Log",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )
        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Plan → Do → Check → Act for continuous quality improvement",
            font=ctk.CTkFont(
                size=12
            )
        )
        subtitle.pack(
            anchor="w",
            pady=(2, 0)
        )

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
            (0, 1, 2, 3),
            weight=1
        )

        self.total_card = self.create_summary_card(
            summary_frame,
            "Total Activities",
            "0"
        )
        self.total_card.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 4)
        )

        self.plan_card = self.create_summary_card(
            summary_frame,
            "Plan",
            "0"
        )
        self.plan_card.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=4
        )

        self.do_card = self.create_summary_card(
            summary_frame,
            "Do",
            "0"
        )
        self.do_card.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=4
        )

        self.check_card = self.create_summary_card(
            summary_frame,
            "Check",
            "0"
        )
        self.check_card.grid(
            row=0,
            column=3,
            sticky="ew",
            padx=4
        )

        # -------------------------------------------------
        # Add Activity Section
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

        input_frame.grid_columnconfigure(
            1,
            weight=1
        )

        input_title = ctk.CTkLabel(
            input_frame,
            text="Add PDCA Activity",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )
        input_title.grid(
            row=0,
            column=0,
            padx=(12, 8),
            pady=10
        )

        self.phase_combo = ctk.CTkComboBox(
            input_frame,
            values=[
                "Plan",
                "Do",
                "Check",
                "Act"
            ],
            width=100
        )
        self.phase_combo.set("Plan")
        self.phase_combo.grid(
            row=0,
            column=1,
            sticky="w",
            padx=5,
            pady=10
        )

        self.activity_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Activity description"
        )
        self.activity_entry.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=5,
            pady=10
        )

        self.result_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Result / outcome"
        )
        self.result_entry.grid(
            row=0,
            column=3,
            sticky="ew",
            padx=5,
            pady=10
        )

        input_frame.grid_columnconfigure(
            2,
            weight=1
        )

        input_frame.grid_columnconfigure(
            3,
            weight=1
        )

        add_button = ctk.CTkButton(
            input_frame,
            text="Add Activity",
            width=110,
            command=self.add_cycle
        )
        add_button.grid(
            row=0,
            column=4,
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
            text="PDCA Improvement Log",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )
        table_title.pack(
            side="left"
        )

        table_hint = ctk.CTkLabel(
            table_header,
            text="Select a row to edit or remove",
            font=ctk.CTkFont(
                size=10
            )
        )
        table_hint.pack(
            side="right"
        )

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
            rowheight=34,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        columns = (
            "id",
            "phase",
            "activity",
            "result"
        )

        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "id",
            text="ID"
        )

        self.tree.heading(
            "phase",
            text="Phase"
        )

        self.tree.heading(
            "activity",
            text="Activity"
        )

        self.tree.heading(
            "result",
            text="Result / Outcome"
        )

        self.tree.column(
            "id",
            width=60,
            anchor="center",
            stretch=False
        )

        self.tree.column(
            "phase",
            width=100,
            anchor="center",
            stretch=False
        )

        self.tree.column(
            "activity",
            width=420,
            anchor="w"
        )

        self.tree.column(
            "result",
            width=420,
            anchor="w"
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
            self.load_selected_cycle
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

        edit_button = ctk.CTkButton(
            controls,
            text="Load Selected",
            width=120,
            command=self.load_selected_cycle
        )
        edit_button.pack(
            side="left",
            padx=(0, 6)
        )

        update_button = ctk.CTkButton(
            controls,
            text="Update",
            width=100,
            command=self.update_cycle
        )
        update_button.pack(
            side="left",
            padx=6
        )

        remove_button = ctk.CTkButton(
            controls,
            text="Remove",
            width=100,
            command=self.remove_selected_cycle
        )
        remove_button.pack(
            side="left",
            padx=6
        )

        clear_button = ctk.CTkButton(
            controls,
            text="Clear",
            width=100,
            command=self.clear_inputs
        )
        clear_button.pack(
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
    def create_summary_card(
        self,
        parent,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=10
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=10
            )
        )
        title_label.pack(
            anchor="w",
            padx=12,
            pady=(7, 0)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )
        value_label.pack(
            anchor="w",
            padx=12,
            pady=(0, 7)
        )

        card.value_label = value_label

        return card

    # -----------------------------------------------------
    # Refresh Data
    # -----------------------------------------------------
    def refresh_data(self):

        cycles = self.service.get_cycles()
        summary = self.service.get_summary()

        self.total_card.value_label.configure(
            text=str(summary["total_cycles"])
        )

        self.plan_card.value_label.configure(
            text=str(summary["plan"])
        )

        self.do_card.value_label.configure(
            text=str(summary["do"])
        )

        self.check_card.value_label.configure(
            text=str(summary["check"])
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        for cycle in cycles:
            self.tree.insert(
                "",
                "end",
                values=(
                    cycle["id"],
                    cycle["phase"],
                    cycle["activity"],
                    cycle["result"]
                )
            )

    # -----------------------------------------------------
    # Add Cycle
    # -----------------------------------------------------
    def add_cycle(self):

        phase = self.phase_combo.get().strip()
        activity = self.activity_entry.get().strip()
        result = self.result_entry.get().strip()

        try:
            self.service.add_cycle(
                phase,
                activity,
                result
            )

            self.clear_inputs()
            self.refresh_data()

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                str(error)
            )

    # -----------------------------------------------------
    # Get Selected Cycle ID
    # -----------------------------------------------------
    def get_selected_cycle_id(self):

        selected = self.tree.selection()

        if not selected:
            return None

        values = self.tree.item(
            selected[0],
            "values"
        )

        if not values:
            return None

        return int(values[0])

    # -----------------------------------------------------
    # Load Selected Cycle
    # -----------------------------------------------------
    def load_selected_cycle(self, event=None):

        cycle_id = self.get_selected_cycle_id()

        if cycle_id is None:
            if event is None:
                messagebox.showwarning(
                    "Select Cycle",
                    "Please select a PDCA cycle first."
                )
            return

        try:
            cycle = self.service.get_cycle(
                cycle_id
            )

            self.phase_combo.set(
                cycle["phase"]
            )

            self.activity_entry.delete(
                0,
                "end"
            )

            self.activity_entry.insert(
                0,
                cycle["activity"]
            )

            self.result_entry.delete(
                0,
                "end"
            )

            self.result_entry.insert(
                0,
                cycle["result"]
            )

        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error)
            )

    # -----------------------------------------------------
    # Update Cycle
    # -----------------------------------------------------
    def update_cycle(self):

        cycle_id = self.get_selected_cycle_id()

        if cycle_id is None:
            messagebox.showwarning(
                "Select Cycle",
                "Please select a PDCA cycle to update."
            )
            return

        phase = self.phase_combo.get().strip()
        activity = self.activity_entry.get().strip()
        result = self.result_entry.get().strip()

        try:
            self.service.update_cycle(
                cycle_id,
                phase,
                activity,
                result
            )

            self.clear_inputs()
            self.refresh_data()

        except ValueError as error:
            messagebox.showerror(
                "Update Error",
                str(error)
            )

    # -----------------------------------------------------
    # Remove Selected Cycle
    # -----------------------------------------------------
    def remove_selected_cycle(self):

        cycle_id = self.get_selected_cycle_id()

        if cycle_id is None:
            messagebox.showwarning(
                "Select Cycle",
                "Please select a PDCA cycle to remove."
            )
            return

        answer = messagebox.askyesno(
            "Remove Cycle",
            f"Remove PDCA activity #{cycle_id}?"
        )

        if not answer:
            return

        try:
            self.service.remove_cycle(
                cycle_id
            )

            self.clear_inputs()
            self.refresh_data()

        except ValueError as error:
            messagebox.showerror(
                "Remove Error",
                str(error)
            )

    # -----------------------------------------------------
    # Clear Inputs
    # -----------------------------------------------------
    def clear_inputs(self):

        self.phase_combo.set(
            "Plan"
        )

        self.activity_entry.delete(
            0,
            "end"
        )

        self.result_entry.delete(
            0,
            "end"
        )


def main():

    root = ctk.CTk()

    root.title(
        "PDCA Cycle Log"
    )

    root.geometry(
        "1200x700"
    )

    root.minsize(
        950,
        600
    )

    frame = PDCAFrame(root)

    frame.pack(
        fill="both",
        expand=True
    )

    root.mainloop()


if __name__ == "__main__":
    main()