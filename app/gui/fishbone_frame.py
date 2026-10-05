import customtkinter as ctk
from tkinter import messagebox, Canvas

from app.services.fishbone_service import FishboneService


class FishboneFrame(ctk.CTkFrame):

    # =========================================================
    # COLORS
    # =========================================================

    BACKGROUND = "#F6F8FC"
    CARD = "#FFFFFF"
    TEXT = "#111827"
    SECONDARY_TEXT = "#64748B"
    BORDER = "#E6EAF0"
    PRIMARY = "#2563EB"
    PRIMARY_SOFT = "#EFF6FF"
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    PURPLE = "#7C3AED"
    CYAN = "#0891B2"

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=self.BACKGROUND
        )

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
            text_color=self.TEXT,
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
            text_color=self.SECONDARY_TEXT,
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
            fg_color=self.CARD,
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER
        )

        problem_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        problem_label = ctk.CTkLabel(
            problem_frame,
            text="PROBLEM",
            text_color=self.PRIMARY,
            font=ctk.CTkFont(
                size=11,
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
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        problem_text.pack(
            side="left",
            pady=12
        )

        # -----------------------------------------------------
        # FISHBONE DIAGRAM
        # -----------------------------------------------------

        diagram_card = ctk.CTkFrame(
            self,
            fg_color=self.CARD,
            corner_radius=14,
            border_width=1,
            border_color=self.BORDER
        )

        diagram_card.pack(
            fill="x",
            padx=25,
            pady=(5, 15)
        )

        diagram_header = ctk.CTkFrame(
            diagram_card,
            fg_color="transparent"
        )

        diagram_header.pack(
            fill="x",
            padx=18,
            pady=(12, 0)
        )

        diagram_title = ctk.CTkLabel(
            diagram_header,
            text="Root Cause Fishbone Diagram",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        diagram_title.pack(
            side="left"
        )

        diagram_hint = ctk.CTkLabel(
            diagram_header,
            text="Ishikawa • Cause & Effect",
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(size=10)
        )

        diagram_hint.pack(
            side="right"
        )

        self.diagram_canvas = Canvas(
            diagram_card,
            height=455,
            bg=self.CARD,
            highlightthickness=0,
            bd=0
        )

        self.diagram_canvas.pack(
            fill="x",
            padx=12,
            pady=(4, 15)
        )

        self.diagram_canvas.bind(
            "<Configure>",
            self._on_diagram_resize
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
            text="Category:",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
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
            text="Total Causes: 0",
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        self.total_label.pack(
            side="right"
        )

        # -----------------------------------------------------
        # CAUSES
        # -----------------------------------------------------

        causes_frame = ctk.CTkFrame(
            self,
            fg_color=self.CARD,
            corner_radius=14,
            border_width=1,
            border_color=self.BORDER
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
            text_color=self.TEXT,
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
            height=300,
            fg_color="#F8FAFC",
            border_width=1,
            border_color=self.BORDER
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
            fg_color=self.PRIMARY,
            hover_color="#1D4ED8",
            command=self.add_cause
        )

        add_button.pack(
            side="right"
        )

    # =========================================================
    # FISHBONE DIAGRAM
    # =========================================================

    def draw_fishbone(self):

        canvas = self.diagram_canvas

        width = max(
            canvas.winfo_width(),
            900
        )

        height = max(
            canvas.winfo_height(),
            455
        )

        canvas.delete("all")

        categories = list(
            self.service.get_categories().items()
        )

        # Main fishbone geometry
        spine_start_x = 75
        spine_end_x = width - 205
        spine_y = height / 2

        # Main horizontal spine
        canvas.create_line(
            spine_start_x,
            spine_y,
            spine_end_x,
            spine_y,
            fill=self.PRIMARY,
            width=5
        )

        # Direction arrow into the problem
        canvas.create_polygon(
            spine_end_x,
            spine_y,
            spine_end_x - 18,
            spine_y - 11,
            spine_end_x - 18,
            spine_y + 11,
            fill=self.PRIMARY,
            outline=self.PRIMARY
        )

        # Effect / problem box
        effect_x = width - 160
        effect_width = 145
        effect_height = 92

        canvas.create_rectangle(
            effect_x - effect_width / 2,
            spine_y - effect_height / 2,
            effect_x + effect_width / 2,
            spine_y + effect_height / 2,
            fill=self.PRIMARY_SOFT,
            outline=self.PRIMARY,
            width=2
        )

        canvas.create_text(
            effect_x,
            spine_y - 27,
            text="EFFECT",
            fill=self.PRIMARY,
            font=("Segoe UI", 9, "bold")
        )

        canvas.create_text(
            effect_x,
            spine_y + 5,
            text="Slow System\nPerformance",
            fill=self.TEXT,
            font=("Segoe UI", 10, "bold"),
            width=115,
            justify="center"
        )

        # Category branch colors
        branch_colors = [
            self.PRIMARY,
            self.PURPLE,
            self.CYAN,
            self.SUCCESS,
            self.WARNING,
            self.DANGER
        ]

        # Six categories: three above and three below.
        positions = [
            ("top", 0.10),
            ("top", 0.29),
            ("top", 0.48),
            ("bottom", 0.10),
            ("bottom", 0.29),
            ("bottom", 0.48)
        ]

        for index, ((category, causes), (side, ratio)) in enumerate(
            zip(categories, positions)
        ):

            color = branch_colors[
                index % len(branch_colors)
            ]

            branch_x = (
                spine_start_x
                + (spine_end_x - spine_start_x) * ratio
            )

            branch_y = (
                spine_y - 135
                if side == "top"
                else spine_y + 135
            )

            # Diagonal branch
            canvas.create_line(
                branch_x,
                spine_y,
                branch_x - 62,
                branch_y,
                fill=color,
                width=3
            )

            # Small category node
            node_x = branch_x - 62
            node_y = branch_y

            canvas.create_oval(
                node_x - 5,
                node_y - 5,
                node_x + 5,
                node_y + 5,
                fill=color,
                outline=color
            )

            # Category title
            title_y = (
                node_y - 20
                if side == "top"
                else node_y + 20
            )

            canvas.create_text(
                node_x,
                title_y,
                text=category,
                fill=color,
                font=("Segoe UI", 10, "bold"),
                anchor="s" if side == "top" else "n"
            )

            # Display the first three causes on the branch.
            display_causes = causes[:3]

            for cause_index, cause in enumerate(display_causes):

                cause_x = (
                    node_x
                    - 8
                    - (cause_index * 3)
                )

                cause_y = (
                    node_y
                    - 43
                    - (cause_index * 30)
                    if side == "top"
                    else node_y
                    + 43
                    + (cause_index * 30)
                )

                canvas.create_text(
                    cause_x,
                    cause_y,
                    text=f"• {cause}",
                    fill=self.TEXT,
                    font=("Segoe UI", 8),
                    anchor="e" if side == "top" else "e",
                    width=205
                )

            # Indicate additional causes if the category has more.
            if len(causes) > 3:

                extra_y = (
                    node_y - 132
                    if side == "top"
                    else node_y + 132
                )

                canvas.create_text(
                    node_x,
                    extra_y,
                    text=f"+ {len(causes) - 3} more causes",
                    fill=self.SECONDARY_TEXT,
                    font=("Segoe UI", 7, "italic"),
                    anchor="e"
                )

        # Left tail / root-cause starting point
        canvas.create_line(
            40,
            spine_y,
            spine_start_x,
            spine_y,
            fill="#94A3B8",
            width=3
        )

        canvas.create_text(
            45,
            spine_y - 22,
            text="ROOT\nCAUSES",
            fill=self.SECONDARY_TEXT,
            font=("Segoe UI", 8, "bold"),
            anchor="w"
        )

        # Footer legend
        canvas.create_text(
            20,
            height - 13,
            text="People • Process • Technology • Database • Environment • Measurement",
            fill=self.SECONDARY_TEXT,
            font=("Segoe UI", 8),
            anchor="w"
        )

    def _on_diagram_resize(self, event=None):

        if hasattr(self, "diagram_canvas"):

            self.after(
                50,
                self.draw_fishbone
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

        self.after(
            100,
            self.draw_fishbone
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
        self.draw_fishbone()

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
    app.geometry("1200x900")

    frame = FishboneFrame(app)

    frame.pack(
        fill="both",
        expand=True
    )

    app.mainloop()


if __name__ == "__main__":
    main()
