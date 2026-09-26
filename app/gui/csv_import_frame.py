import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

import pandas as pd

from app.services.csv_import_service import CSVImportService


class CSVImportFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="#F4F7FB"
        )

        self.csv_service = CSVImportService()
        self.selected_file = None

        self.create_ui()

    # ---------------------------------------------------------
    # Main UI
    # ---------------------------------------------------------

    def create_ui(self):

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
            text="CSV Patient Import",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color="#172033"
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Bulk import patient records using Pandas",
            font=ctk.CTkFont(size=13),
            text_color="#6B7280"
        )

        subtitle.pack(anchor="w")

        # -----------------------------------------------------
        # File Selection
        # -----------------------------------------------------

        file_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color="white"
        )

        file_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        file_frame.grid_columnconfigure(
            1,
            weight=1
        )

        file_label = ctk.CTkLabel(
            file_frame,
            text="CSV File",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color="#172033"
        )

        file_label.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=20
        )

        self.file_entry = ctk.CTkEntry(
            file_frame,
            height=38,
            placeholder_text="Select a CSV file..."
        )

        self.file_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=20,
            sticky="ew"
        )

        self.browse_button = ctk.CTkButton(
            file_frame,
            text="📁  Browse",
            width=110,
            height=38,
            command=self.browse_file
        )

        self.browse_button.grid(
            row=0,
            column=2,
            padx=(10, 20),
            pady=20
        )

        # -----------------------------------------------------
        # Action Buttons
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

        self.preview_button = ctk.CTkButton(
            button_frame,
            text="Preview CSV",
            width=120,
            height=38,
            fg_color="#37445D",
            hover_color="#4A5872",
            command=self.preview_csv
        )

        self.preview_button.pack(
            side="left",
            padx=(0, 8)
        )

        self.import_button = ctk.CTkButton(
            button_frame,
            text="Import Patients",
            width=130,
            height=38,
            command=self.import_csv
        )

        self.import_button.pack(
            side="left",
            padx=4
        )

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            width=100,
            height=38,
            fg_color="#6B7280",
            hover_color="#555B66",
            command=self.clear_all
        )

        self.clear_button.pack(
            side="left",
            padx=4
        )

        # -----------------------------------------------------
        # Summary Cards
        # -----------------------------------------------------

        summary_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        summary_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        for column in range(3):

            summary_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.imported_card = self.create_summary_card(
            summary_frame,
            0,
            "Imported",
            "0"
        )

        self.duplicate_card = self.create_summary_card(
            summary_frame,
            1,
            "Duplicates",
            "0"
        )

        self.rejected_card = self.create_summary_card(
            summary_frame,
            2,
            "Rejected",
            "0"
        )

        # -----------------------------------------------------
        # Preview Section
        # -----------------------------------------------------

        preview_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color="white"
        )

        preview_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        preview_title = ctk.CTkLabel(
            preview_frame,
            text="CSV Preview",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#172033"
        )

        preview_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        preview_subtitle = ctk.CTkLabel(
            preview_frame,
            text=(
                "Required columns: full_name, dob, gender, "
                "phone, address, blood_group"
            ),
            font=ctk.CTkFont(size=11),
            text_color="#6B7280"
        )

        preview_subtitle.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        table_container = ctk.CTkFrame(
            preview_frame,
            fg_color="transparent"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.preview_tree = ttk.Treeview(
            table_container,
            show="headings"
        )

        vertical_scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.preview_tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_container,
            orient="horizontal",
            command=self.preview_tree.xview
        )

        self.preview_tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.preview_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_container.grid_rowconfigure(
            0,
            weight=1
        )

        table_container.grid_columnconfigure(
            0,
            weight=1
        )

    # ---------------------------------------------------------
    # Summary Card
    # ---------------------------------------------------------

    def create_summary_card(
        self,
        parent,
        column,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            height=90,
            corner_radius=12,
            fg_color="white"
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=7
        )

        card.grid_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color="#6B7280"
        )

        title_label.pack(
            anchor="w",
            padx=18,
            pady=(13, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color="#172033"
        )

        value_label.pack(
            anchor="w",
            padx=18
        )

        return value_label

    # ---------------------------------------------------------
    # Get Selected File
    # ---------------------------------------------------------

    def get_selected_file(self):

        file_path = self.file_entry.get().strip()

        if not file_path:

            messagebox.showwarning(
                "No File Selected",
                "Please select a CSV file first."
            )

            return None

        path = Path(file_path)

        if not path.exists():

            messagebox.showerror(
                "File Not Found",
                f"The selected file does not exist:\n\n{path}"
            )

            return None

        if path.suffix.lower() != ".csv":

            messagebox.showerror(
                "Invalid File",
                "Please select a CSV file."
            )

            return None

        self.selected_file = path

        return path

    # ---------------------------------------------------------
    # Browse File
    # ---------------------------------------------------------

    def browse_file(self):

        file_path = filedialog.askopenfilename(
            title="Select Patient CSV File",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        self.selected_file = Path(
            file_path
        )

        self.file_entry.delete(
            0,
            "end"
        )

        self.file_entry.insert(
            0,
            str(self.selected_file)
        )

    # ---------------------------------------------------------
    # Preview CSV
    # ---------------------------------------------------------

    def preview_csv(self):

        path = self.get_selected_file()

        if path is None:
            return

        try:

            dataframe = pd.read_csv(
                path
            )

            if dataframe.empty:

                messagebox.showwarning(
                    "Empty CSV",
                    "The selected CSV file contains no records."
                )

                self.clear_preview_table()

                return

            self.clear_preview_table()

            columns = list(
                dataframe.columns
            )

            self.preview_tree["columns"] = columns

            for column in columns:

                self.preview_tree.heading(
                    column,
                    text=column
                )

                self.preview_tree.column(
                    column,
                    width=150,
                    minwidth=100,
                    anchor="w"
                )

            # Show first 100 rows
            preview_data = dataframe.head(100)

            for _, row in preview_data.iterrows():

                values = []

                for column in columns:

                    value = row[column]

                    if pd.isna(value):
                        value = ""

                    values.append(
                        str(value)
                    )

                self.preview_tree.insert(
                    "",
                    "end",
                    values=values
                )

            messagebox.showinfo(
                "Preview Loaded",
                f"CSV preview loaded successfully.\n\n"
                f"Total rows: {len(dataframe)}\n"
                f"Columns: {len(columns)}"
            )

        except Exception as error:

            messagebox.showerror(
                "Preview Error",
                f"Could not preview the CSV file.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Import CSV
    # ---------------------------------------------------------

    def import_csv(self):

        path = self.get_selected_file()

        if path is None:
            return

        answer = messagebox.askyesno(
            "Import Patients",
            (
                "Are you sure you want to import "
                "patients from this CSV file?"
            )
        )

        if not answer:
            return

        try:

            result = self.csv_service.import_patients(
                path
            )

            self.imported_card.configure(
                text=str(
                    result["imported"]
                )
            )

            self.duplicate_card.configure(
                text=str(
                    result["duplicates"]
                )
            )

            self.rejected_card.configure(
                text=str(
                    result["rejected"]
                )
            )

            message = (
                "CSV import completed.\n\n"
                f"Imported: {result['imported']}\n"
                f"Duplicates: {result['duplicates']}\n"
                f"Rejected: {result['rejected']}"
            )

            if result["rejected_rows"]:

                message += "\n\nRejected rows:\n"

                for rejected in result["rejected_rows"]:

                    message += (
                        f"Row {rejected['row']}: "
                        f"{rejected['reason']}\n"
                    )

            messagebox.showinfo(
                "Import Complete",
                message
            )

        except Exception as error:

            messagebox.showerror(
                "Import Error",
                f"Could not import the CSV file.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Clear Preview
    # ---------------------------------------------------------

    def clear_preview_table(self):

        for item in self.preview_tree.get_children():

            self.preview_tree.delete(
                item
            )

        self.preview_tree["columns"] = ()

    # ---------------------------------------------------------
    # Clear Everything
    # ---------------------------------------------------------

    def clear_all(self):

        self.selected_file = None

        self.file_entry.delete(
            0,
            "end"
        )

        self.clear_preview_table()

        self.imported_card.configure(
            text="0"
        )

        self.duplicate_card.configure(
            text="0"
        )

        self.rejected_card.configure(
            text="0"
        )


# -------------------------------------------------------------
# Standalone Test
# -------------------------------------------------------------

if __name__ == "__main__":

    app = ctk.CTk()

    app.title(
        "CSV Patient Import Test"
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

    csv_frame = CSVImportFrame(
        app
    )

    csv_frame.pack(
        fill="both",
        expand=True
    )

    app.mainloop()