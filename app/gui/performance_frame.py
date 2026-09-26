import customtkinter as ctk

from app.gui.ui_kit import HospitalFrame
from tkinter import messagebox

from app.services.performance_service import PerformanceService


class PerformanceFrame(HospitalFrame):

    BACKGROUND = "#F6F8FC"
    CARD = "#FFFFFF"
    BORDER = "#E6EAF0"
    TEXT_DARK = "#0F172A"
    SECONDARY = "#64748B"
    PRIMARY = "#2563EB"

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=self.BACKGROUND
        )

        self.service = PerformanceService()

        self.metric_cards = {}

        self.create_widgets()

        self.run_performance_test()

    def create_widgets(self):

        # Title
        title = ctk.CTkLabel(
            self,
            text="⌁  Q02 Performance Analysis",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )
        title.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text=(
                "Measure system response time and verify "
                "performance improvement targets."
            ),
            font=ctk.CTkFont(size=14)
        )
        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # Target information
        target_frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )
        target_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        target_title = ctk.CTkLabel(
            target_frame,
            text="Q02 Performance Target",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )
        target_title.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        target_text = ctk.CTkLabel(
            target_frame,
            text=(
                "Dashboard loading time should remain "
                "below 1 second (1000 ms) under normal "
                "local operating conditions."
            ),
            font=ctk.CTkFont(size=13),
            justify="left"
        )
        target_text.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # Metrics container
        metrics_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        metrics_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        metrics = [
            ("database_query", "Database Query"),
            ("patient_search", "Patient Search"),
            ("dashboard_load", "Dashboard Load"),
            ("report_generation", "Report Generation")
        ]

        for column, (key, label) in enumerate(metrics):

            card = ctk.CTkFrame(
                metrics_frame,
                corner_radius=12
            )

            card.grid(
                row=0,
                column=column,
                padx=6,
                pady=6,
                sticky="nsew"
            )

            metrics_frame.grid_columnconfigure(
                column,
                weight=1
            )

            title_label = ctk.CTkLabel(
                card,
                text=label,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                )
            )
            title_label.pack(
                pady=(18, 5)
            )

            value_label = ctk.CTkLabel(
                card,
                text="-- ms",
                font=ctk.CTkFont(
                    size=24,
                    weight="bold"
                )
            )
            value_label.pack(
                pady=(0, 18)
            )

            self.metric_cards[key] = value_label

        # Status section
        status_frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )
        status_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        status_title = ctk.CTkLabel(
            status_frame,
            text="Performance Status",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )
        status_title.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Not measured",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )
        self.status_label.pack(
            anchor="w",
            padx=20,
            pady=5
        )

        self.details_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=13),
            justify="left"
        )
        self.details_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # Buttons
        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        run_button = ctk.CTkButton(
            button_frame,
            text="Run Performance Test",
            height=40,
            command=self.run_performance_test
        )
        run_button.pack(
            side="left",
            padx=(0, 10)
        )

        explanation_button = ctk.CTkButton(
            button_frame,
            text="Q02 Explanation",
            height=40,
            command=self.show_explanation
        )
        explanation_button.pack(
            side="left"
        )

    def run_performance_test(self):

        try:
            results = self.service.measure_all()

            for key, value in results.items():

                if key in self.metric_cards:
                    self.metric_cards[key].configure(
                        text=f"{value} ms"
                    )

            dashboard_time = results["dashboard_load"]

            status = self.service.get_performance_status(
                dashboard_time
            )

            self.status_label.configure(
                text=status
            )

            self.details_label.configure(
                text=(
                    f"Dashboard load time: "
                    f"{dashboard_time} ms\n"
                    f"Target: Less than 1000 ms"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Performance Error",
                f"Could not measure performance:\n{error}"
            )

    def show_explanation(self):

        messagebox.showinfo(
            "Q02 Performance Improvement",
            "Q02: Improve Performance\n\n"
            "The system improves performance using:\n\n"
            "• Indexed database fields\n"
            "• Filtered SQL queries\n"
            "• Parameterized queries\n"
            "• Aggregated dashboard queries\n"
            "• Optimized report queries\n"
            "• Pandas-based bulk CSV processing\n\n"
            "Performance is measured using execution time "
            "in milliseconds.\n\n"
            "Dashboard target: below 1000 ms."
        )