import customtkinter as ctk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from app.services.pareto_service import ParetoService


class ParetoFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.service = ParetoService()

        self.create_layout()
        self.load_pareto_data()

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
            text="Pareto Analysis",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text=(
                "Identify the performance defects contributing "
                "most to the overall problem."
            ),
            font=ctk.CTkFont(size=12)
        )

        subtitle.pack(
            anchor="w",
            pady=(4, 0)
        )

        # -----------------------------------------------------
        # SUMMARY CARDS
        # -----------------------------------------------------

        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.total_card = self.create_card(
            cards_frame,
            "Total Defects",
            "0"
        )

        self.top_card = self.create_card(
            cards_frame,
            "Top Defect",
            "-"
        )

        self.major_card = self.create_card(
            cards_frame,
            "80% Range",
            "0"
        )

        # -----------------------------------------------------
        # TABLE
        # -----------------------------------------------------

        table_frame = ctk.CTkFrame(
            self
        )

        table_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 10)
        )

        table_title = ctk.CTkLabel(
            table_frame,
            text="Pareto Data",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        table_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 8)
        )

        columns = (
            "defect",
            "occurrence",
            "percentage",
            "cumulative"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=6
        )

        self.tree.heading(
            "defect",
            text="Defect"
        )

        self.tree.heading(
            "occurrence",
            text="Occurrences"
        )

        self.tree.heading(
            "percentage",
            text="Percentage"
        )

        self.tree.heading(
            "cumulative",
            text="Cumulative %"
        )

        self.tree.column(
            "defect",
            width=300
        )

        self.tree.column(
            "occurrence",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "percentage",
            width=130,
            anchor="center"
        )

        self.tree.column(
            "cumulative",
            width=140,
            anchor="center"
        )

        self.tree.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # CHART
        # -----------------------------------------------------

        chart_frame = ctk.CTkFrame(
            self
        )

        chart_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        chart_title = ctk.CTkLabel(
            chart_frame,
            text="Pareto Chart",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        chart_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        self.figure = Figure(
            figsize=(8, 4),
            dpi=100
        )

        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=chart_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # =========================================================
    # SUMMARY CARD
    # =========================================================

    def create_card(
        self,
        parent,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=11
            )
        )

        title_label.pack(
            anchor="w",
            padx=15,
            pady=(12, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        value_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        return value_label

    # =========================================================
    # LOAD DATA
    # =========================================================

    def load_pareto_data(self):

        results = self.service.calculate_pareto()

        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert data
        for result in results:

            self.tree.insert(
                "",
                "end",
                values=(
                    result["defect"],
                    result["occurrence"],
                    f'{result["percentage"]:.2f}%',
                    f'{result["cumulative_percentage"]:.2f}%'
                )
            )

        # Summary
        total = self.service.get_total_occurrences()

        self.total_card.configure(
            text=str(total)
        )

        if results:
            self.top_card.configure(
                text=results[0]["defect"]
            )

        major_defects = self.service.get_major_defects()

        self.major_card.configure(
            text=str(len(major_defects))
        )

        # Draw chart
        self.draw_chart(results)

    # =========================================================
    # DRAW PARETO CHART
    # =========================================================

    def draw_chart(self, results):

        self.ax.clear()

        if not results:
            self.canvas.draw()
            return

        defects = [
            result["defect"]
            for result in results
        ]

        occurrences = [
            result["occurrence"]
            for result in results
        ]

        cumulative = [
            result["cumulative_percentage"]
            for result in results
        ]

        x_positions = range(len(defects))

        self.ax.bar(
            x_positions,
            occurrences
        )

        self.ax.set_xlabel(
            "Performance Defects"
        )

        self.ax.set_ylabel(
            "Occurrences"
        )

        self.ax.set_title(
            "Performance Defect Pareto Analysis"
        )

        self.ax.set_xticks(
            list(x_positions)
        )

        self.ax.set_xticklabels(
            defects,
            rotation=25,
            ha="right"
        )

        self.ax.grid(
            axis="y",
            alpha=0.25
        )

        # Secondary axis for cumulative percentage
        cumulative_axis = self.ax.twinx()

        cumulative_axis.plot(
            list(x_positions),
            cumulative,
            marker="o"
        )

        cumulative_axis.set_ylabel(
            "Cumulative Percentage"
        )

        cumulative_axis.set_ylim(
            0,
            110
        )

        cumulative_axis.axhline(
            80,
            linestyle="--",
            alpha=0.7
        )

        cumulative_axis.text(
            len(results) - 1,
            81,
            "80% reference",
            va="bottom",
            ha="right"
        )

        self.figure.tight_layout()

        self.canvas.draw()


# =============================================================
# STANDALONE TEST WINDOW
# =============================================================

def main():

    app = ctk.CTk()

    app.title("Pareto Analysis")
    app.geometry("1150x750")

    frame = ParetoFrame(app)

    frame.pack(
        fill="both",
        expand=True
    )

    app.mainloop()


if __name__ == "__main__":
    main()