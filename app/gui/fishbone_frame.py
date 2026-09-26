import customtkinter as ctk
from tkinter import messagebox

from app.services.fishbone_service import FishboneService


class FishboneFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.service = FishboneService()

        self.create_layout()
        self.load_categories()

    # =========================================================
    # MAIN LAYOUT
    # =========================================================

    def create_layout(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        title = ctk.CTkLabel(
            header,
            text="Fishbone / Ishikawa Analysis",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text=(
                "Identify possible root causes of "
                "hospital system performance problems."
            ),
            font=ctk.CTkFont(size=12)
        )

        subtitle.pack(
            anchor="w",
            pady=(4, 0)
        )

        # -----------------------------------------------------
        # PROBLEM
        # -----------------------------------------------------

        problem_frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        problem_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        problem_label = ctk.CTkLabel(
            problem_frame,
            text="Problem:",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        problem_label.pack(
            side="left",
            padx=(15, 8),
            pady=12
        )

        problem_text = ctk.CTkLabel(
            problem_frame,
            text="Slow Hospital Management System Performance",
            font=ctk.CTkFont(size=13)
        )

        problem_text.pack(
            side="left",
            pady=12
        )

        # -----------------------------------------------------
        # CATEGORY SELECTION
        # -----------------------------------------------------

        selection_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        selection_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 10)
        )

        category_label = ctk.CTkLabel(
            selection_frame,
            text="Category:"
        )

        category_label.pack(
            side="left",
            padx=(0, 8)
        )

        self.category_menu = ctk.CTkOptionMenu(
            selection_frame,
            values=[],
            command=self.category_selected
        )

        self.category_menu.pack(
            side="left"
        )

        self.total_label = ctk.CTkLabel(
            selection_frame,
            text="Total Causes: 0"
        )

        self.total_label.pack(
            side="right"
        )

        # -----------------------------------------------------
        # CAUSES
        # -----------------------------------------------------

        causes_frame = ctk.CTkFrame(
            self
        )

        causes_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        causes_title = ctk.CTkLabel(
            causes_frame,
            text="Identified Root Causes",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        causes_title.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        self.causes_list = ctk.CTkTextbox(
            causes_frame,
            height=300
        )

        self.causes_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )

        self.causes_list.configure(
            state="disabled"
        )

        # -----------------------------------------------------
        # ADD CAUSE
        # -----------------------------------------------------

        add_frame = ctk.CTkFrame(
            causes_frame,
            fg_color="transparent"
        )

        add_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        self.cause_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="Enter a new root cause..."
        )

        self.cause_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        add_button = ctk.CTkButton(
            add_frame,
            text="Add Cause",
            command=self.add_cause
        )

        add_button.pack(
            side="right"
        )

    # =========================================================
    # LOAD CATEGORIES
    # =========================================================

    def load_categories(self):

        categories = list(
            self.service.get_categories().keys()
        )

        self.category_menu.configure(
            values=categories
        )

        if categories:

            self.category_menu.set(
                categories[0]
            )

            self.category_selected(
                categories[0]
            )

    # =========================================================
    # CATEGORY SELECTED
    # =========================================================

    def category_selected(self, category):

        causes = self.service.get_causes(
            category
        )

        self.causes_list.configure(
            state="normal"
        )

        self.causes_list.delete(
            "1.0",
            "end"
        )

        for index, cause in enumerate(
            causes,
            start=1
        ):

            self.causes_list.insert(
                "end",
                f"{index}. {cause}\n"
            )

        self.causes_list.configure(
            state="disabled"
        )

        self.update_total()

    # =========================================================
    # ADD CAUSE
    # =========================================================

    def add_cause(self):

        category = self.category_menu.get()

        cause = self.cause_entry.get().strip()

        try:

            self.service.add_cause(
                category,
                cause
            )

            self.cause_entry.delete(
                0,
                "end"
            )

            self.category_selected(
                category
            )

        except ValueError as error:

            messagebox.showerror(
                "Invalid Cause",
                str(error)
            )

    # =========================================================
    # UPDATE TOTAL
    # =========================================================

    def update_total(self):

        total = self.service.get_total_causes()

        self.total_label.configure(
            text=f"Total Causes: {total}"
        )


# =============================================================
# STANDALONE TEST WINDOW
# =============================================================

def main():

    app = ctk.CTk()

    app.title("Fishbone Analysis")
    app.geometry("1000x700")

    frame = FishboneFrame(app)

    frame.pack(
        fill="both",
        expand=True
    )

    app.mainloop()


if __name__ == "__main__":
    main()