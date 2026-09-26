import customtkinter as ctk
from tkinter import ttk

from app.services.tqm_service import TQMService
from app.gui.fishbone_frame import FishboneFrame
from app.gui.pareto_frame import ParetoFrame
from app.gui.checksheet_frame import ChecksheetFrame
from app.gui.pdca_frame import PDCAFrame


class TQMFrame(ctk.CTkFrame):

    # =========================================================
    # COLORS
    # =========================================================

    BACKGROUND = "#F4F7FB"
    CARD = "#FFFFFF"

    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"

    TEXT = "#111827"
    SECONDARY_TEXT = "#6B7280"
    BORDER = "#E5E7EB"

    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=self.BACKGROUND
        )

        self.service = TQMService()

        self.create_widgets()

    # =========================================================
    # MAIN UI
    # =========================================================

    def create_widgets(self):

        self.main = ctk.CTkScrollableFrame(
            self,
            fg_color=self.BACKGROUND,
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        self.create_header()
        self.create_summary_cards()
        self.create_tabs()

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        title = ctk.CTkLabel(
            header,
            text="TQM Analysis",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Quality analysis for Q02 - Improve Performance",
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(size=14)
        )

        subtitle.pack(
            anchor="w",
            pady=(4, 0)
        )

    # =========================================================
    # SUMMARY CARDS
    # =========================================================

    def create_summary_cards(self):

        fmea_data = self.service.get_fmea_data()

        total_failures = len(fmea_data)

        high_risk = sum(
            1
            for row in fmea_data
            if self.service.get_risk_level(row["rpn"]) == "High"
        )

        medium_risk = sum(
            1
            for row in fmea_data
            if self.service.get_risk_level(row["rpn"]) == "Medium"
        )

        highest_rpn = max(
            row["rpn"]
            for row in fmea_data
        )

        container = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        container.pack(
            fill="x",
            padx=30,
            pady=5
        )

        for column in range(4):

            container.grid_columnconfigure(
                column,
                weight=1
            )

        cards = [
            (
                "Failure Modes",
                total_failures,
                "Performance risks identified",
                self.PRIMARY
            ),
            (
                "High Risk",
                high_risk,
                "Requires attention",
                self.DANGER
            ),
            (
                "Medium Risk",
                medium_risk,
                "Needs monitoring",
                self.WARNING
            ),
            (
                "Highest RPN",
                highest_rpn,
                "Risk priority number",
                "#7C3AED"
            )
        ]

        for column, data in enumerate(cards):

            self.create_summary_card(
                container,
                data,
                column
            )

    def create_summary_card(
        self,
        parent,
        data,
        column
    ):

        title, value, description, accent = data

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=column,
            padx=6,
            pady=6,
            sticky="nsew"
        )

        accent_bar = ctk.CTkFrame(
            card,
            width=5,
            height=70,
            corner_radius=3,
            fg_color=accent
        )

        accent_bar.pack(
            side="left",
            padx=(12, 10),
            pady=15
        )

        content = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        content.pack(
            side="left",
            fill="both",
            expand=True,
            pady=13
        )

        value_label = ctk.CTkLabel(
            content,
            text=str(value),
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            )
        )

        value_label.pack(
            anchor="w"
        )

        title_label = ctk.CTkLabel(
            content,
            text=title,
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        title_label.pack(
            anchor="w"
        )

        description_label = ctk.CTkLabel(
            content,
            text=description,
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(size=9)
        )

        description_label.pack(
            anchor="w"
        )

    # =========================================================
    # TABS
    # =========================================================

    def create_tabs(self):

        tab_card = ctk.CTkFrame(
            self.main,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )

        tab_card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(18, 30)
        )

        self.tabs = ctk.CTkTabview(
            tab_card,
            fg_color=self.CARD,
            segmented_button_fg_color="#EEF2F7",
            segmented_button_selected_color=self.PRIMARY,
            segmented_button_selected_hover_color=self.PRIMARY_HOVER,
            segmented_button_unselected_color="#EEF2F7",
            segmented_button_unselected_hover_color="#E2E8F0"
        )

        self.tabs.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # =====================================================
        # TQM TOOLS
        # =====================================================

        self.tabs.add("SIPOC Analysis")
        self.tabs.add("FMEA Analysis")
        self.tabs.add("Fishbone Analysis")
        self.tabs.add("Pareto Analysis")
        self.tabs.add("Checksheet")
        self.tabs.add("PDCA Cycle")

        # =====================================================
        # CREATE TAB CONTENT
        # =====================================================

        self.create_sipoc_tab(
            self.tabs.tab("SIPOC Analysis")
        )

        self.create_fmea_tab(
            self.tabs.tab("FMEA Analysis")
        )

        self.create_fishbone_tab(
            self.tabs.tab("Fishbone Analysis")
        )

        self.create_pareto_tab(
            self.tabs.tab("Pareto Analysis")
        )

        self.create_checksheet_tab(
            self.tabs.tab("Checksheet")
        )

        self.create_pdca_tab(
            self.tabs.tab("PDCA Cycle")
        )

    # =========================================================
    # SIPOC
    # =========================================================

    def create_sipoc_tab(self, parent):

        description = ctk.CTkLabel(
            parent,
            text=(
                "SIPOC maps the major suppliers, inputs, process steps, "
                "outputs and customers of the hospital workflow."
            ),
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(size=12),
            wraplength=900,
            justify="left"
        )

        description.pack(
            anchor="w",
            padx=15,
            pady=(15, 20)
        )

        sipoc = self.service.get_sipoc_data()

        grid = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        grid.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        for column in range(5):

            grid.grid_columnconfigure(
                column,
                weight=1
            )

        categories = [
            (
                "Suppliers",
                sipoc["suppliers"],
                self.PRIMARY
            ),
            (
                "Inputs",
                sipoc["inputs"],
                "#7C3AED"
            ),
            (
                "Process",
                sipoc["process"],
                "#0891B2"
            ),
            (
                "Outputs",
                sipoc["outputs"],
                self.SUCCESS
            ),
            (
                "Customers",
                sipoc["customers"],
                "#F59E0B"
            )
        ]

        for column, data in enumerate(categories):

            title, items, accent = data

            self.create_sipoc_column(
                grid,
                title,
                items,
                accent,
                column
            )

    def create_sipoc_column(
        self,
        parent,
        title,
        items,
        accent,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="#F8FAFC",
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=column,
            padx=5,
            pady=5,
            sticky="nsew"
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            text_color=accent,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title_label.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        separator = ctk.CTkFrame(
            card,
            height=2,
            fg_color=accent
        )

        separator.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        for item in items:

            row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=12,
                pady=4
            )

            bullet = ctk.CTkLabel(
                row,
                text="•",
                text_color=accent,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            )

            bullet.pack(
                side="left",
                anchor="n",
                padx=(0, 6)
            )

            label = ctk.CTkLabel(
                row,
                text=item,
                text_color=self.TEXT,
                font=ctk.CTkFont(size=11),
                wraplength=150,
                justify="left"
            )

            label.pack(
                side="left",
                anchor="w"
            )

    # =========================================================
    # FMEA
    # =========================================================

    def create_fmea_tab(self, parent):

        description = ctk.CTkLabel(
            parent,
            text=(
                "FMEA identifies possible performance failures and "
                "calculates RPN using Severity × Occurrence × Detection."
            ),
            text_color=self.SECONDARY_TEXT,
            font=ctk.CTkFont(size=12),
            wraplength=900,
            justify="left"
        )

        description.pack(
            anchor="w",
            padx=15,
            pady=(15, 15)
        )

        table_container = ctk.CTkFrame(
            parent,
            fg_color=self.CARD
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        columns = (
            "failure_mode",
            "effect",
            "cause",
            "severity",
            "occurrence",
            "detection",
            "rpn",
            "risk",
            "improvement"
        )

        self.fmea_tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            height=12
        )

        headings = {
            "failure_mode": "Failure Mode",
            "effect": "Effect",
            "cause": "Cause",
            "severity": "S",
            "occurrence": "O",
            "detection": "D",
            "rpn": "RPN",
            "risk": "Risk",
            "improvement": "Improvement"
        }

        widths = {
            "failure_mode": 180,
            "effect": 210,
            "cause": 210,
            "severity": 45,
            "occurrence": 45,
            "detection": 45,
            "rpn": 60,
            "risk": 80,
            "improvement": 230
        }

        for column in columns:

            self.fmea_tree.heading(
                column,
                text=headings[column]
            )

            self.fmea_tree.column(
                column,
                width=widths[column],
                minwidth=widths[column],
                anchor="center"
            )

        self.fmea_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.fmea_tree.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.fmea_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.insert_fmea_data()

    # =========================================================
    # FMEA DATA
    # =========================================================

    def insert_fmea_data(self):

        for item in self.fmea_tree.get_children():

            self.fmea_tree.delete(item)

        rows = self.service.get_fmea_data()

        for row in rows:

            risk = self.service.get_risk_level(
                row["rpn"]
            )

            tag = risk.lower()

            self.fmea_tree.insert(
                "",
                "end",
                values=(
                    row["failure_mode"],
                    row["effect"],
                    row["cause"],
                    row["severity"],
                    row["occurrence"],
                    row["detection"],
                    row["rpn"],
                    risk,
                    row["improvement"]
                ),
                tags=(tag,)
            )

        self.fmea_tree.tag_configure(
            "high",
            background="#FEE2E2",
            foreground="#991B1B"
        )

        self.fmea_tree.tag_configure(
            "medium",
            background="#FEF3C7",
            foreground="#92400E"
        )

        self.fmea_tree.tag_configure(
            "low",
            background="#DCFCE7",
            foreground="#166534"
        )

    # =========================================================
    # FISHBONE
    # =========================================================

    def create_fishbone_tab(self, parent):

        fishbone_frame = FishboneFrame(
            parent
        )

        fishbone_frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # PARETO
    # =========================================================

    def create_pareto_tab(self, parent):

        pareto_frame = ParetoFrame(
            parent
        )

        pareto_frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # CHECKSHEET
    # =========================================================

    def create_checksheet_tab(self, parent):

        checksheet_frame = ChecksheetFrame(
            parent
        )

        checksheet_frame.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # PDCA
    # =========================================================

    def create_pdca_tab(self, parent):

        pdca_frame = PDCAFrame(
            parent
        )

        pdca_frame.pack(
            fill="both",
            expand=True
        )


# =============================================================
# STANDALONE TEST
# =============================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    root.title(
        "TQM Analysis"
    )

    root.geometry(
        "1400x850"
    )

    frame = TQMFrame(
        root
    )

    frame.pack(
        fill="both",
        expand=True
    )

    root.mainloop()