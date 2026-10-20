"""
Hero Display Card: "NOW SERVING", "WAITING TOKENS" & Live Clock.
Exact pixel-perfect replica of the Drittech Queue clinical dashboard.

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from datetime import datetime
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QWidget
)
from PySide6.QtCore import Qt, QTimer


class HeroTokenBanner(QFrame):
    """
    Top Navy Hero Display Card showing the current serving token,
    the live two-column waiting token queue, and real-time digital clock.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HeroCard")
        self.setStyleSheet("""
            QFrame#HeroCard {
                background-color: #0A192F;
                border: 1px solid #1E2D48;
                border-radius: 14px;
            }
        """)
        self._build_ui()
        self._start_clock()

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(20)

        # -------------------------------------------------------------
        # 1. LEFT PANE: NOW SERVING (35% width)
        # -------------------------------------------------------------
        left_pane = QVBoxLayout()
        left_pane.setAlignment(Qt.AlignCenter)
        left_pane.setSpacing(4)

        lbl_now_serving = QLabel("NOW SERVING")
        lbl_now_serving.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: bold; letter-spacing: 1.5px;")
        lbl_now_serving.setAlignment(Qt.AlignCenter)
        left_pane.addWidget(lbl_now_serving)

        self.lbl_big_token = QLabel("A-042")
        self.lbl_big_token.setStyleSheet("color: #FFFFFF; font-size: 44px; font-weight: 800; padding: 2px 0px;")
        self.lbl_big_token.setAlignment(Qt.AlignCenter)
        left_pane.addWidget(self.lbl_big_token)

        lbl_at = QLabel("AT")
        lbl_at.setStyleSheet("color: #94A3B8; font-size: 10px; font-weight: bold;")
        lbl_at.setAlignment(Qt.AlignCenter)
        left_pane.addWidget(lbl_at)

        counter_row = QHBoxLayout()
        counter_row.setAlignment(Qt.AlignCenter)
        counter_row.setSpacing(6)

        lbl_megaphone = QLabel("📢")
        lbl_megaphone.setStyleSheet("font-size: 16px; background: transparent;")
        counter_row.addWidget(lbl_megaphone)

        self.lbl_counter_name = QLabel("COUNTER 3")
        self.lbl_counter_name.setStyleSheet("color: #00E5FF; font-size: 17px; font-weight: 800;")
        counter_row.addWidget(self.lbl_counter_name)
        left_pane.addLayout(counter_row)

        self.lbl_department = QLabel("General OPD")
        self.lbl_department.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 500;")
        self.lbl_department.setAlignment(Qt.AlignCenter)
        left_pane.addWidget(self.lbl_department)

        main_layout.addLayout(left_pane, 35)

        # Vertical Divider 1
        div1 = QFrame()
        div1.setFrameShape(QFrame.VLine)
        div1.setStyleSheet("background-color: #1E2D48; max-width: 1px;")
        main_layout.addWidget(div1)

        # -------------------------------------------------------------
        # 2. MIDDLE PANE: WAITING TOKENS (45% width)
        # -------------------------------------------------------------
        mid_pane = QVBoxLayout()
        mid_pane.setSpacing(10)
        mid_pane.setAlignment(Qt.AlignTop)

        lbl_waiting_title = QLabel("WAITING TOKENS")
        lbl_waiting_title.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: bold; letter-spacing: 1.5px;")
        lbl_waiting_title.setAlignment(Qt.AlignCenter)
        mid_pane.addWidget(lbl_waiting_title)

        # 2-column waiting tokens grid
        self.token_grid = QGridLayout()
        self.token_grid.setContentsMargins(10, 0, 10, 0)
        self.token_grid.setHorizontalSpacing(24)
        self.token_grid.setVerticalSpacing(8)

        # Default sample list matching image
        sample_tokens_col1 = [
            ("A-043", "Counter 2"),
            ("A-044", "Counter 1"),
            ("A-045", "Counter 4"),
            ("A-046", "Counter 2"),
            ("A-047", "Counter 3"),
        ]
        sample_tokens_col2 = [
            ("B-118", "Counter 5"),
            ("B-119", "Counter 5"),
            ("B-120", "Counter 6"),
            ("C-007", "Counter 1"),
            ("C-008", "Counter 2"),
        ]

        for row, ((t1, c1), (t2, c2)) in enumerate(zip(sample_tokens_col1, sample_tokens_col2)):
            # Column 1 Token
            lbl_t1 = QLabel(t1)
            lbl_t1.setStyleSheet("color: #FFFFFF; font-size: 13px; font-weight: bold;")
            self.token_grid.addWidget(lbl_t1, row, 0)

            # Column 1 Counter Pill
            lbl_c1 = QLabel(c1)
            lbl_c1.setStyleSheet("color: #38BDF8; background-color: #0F2D54; border-radius: 4px; padding: 2px 8px; font-size: 11px; font-weight: 600;")
            lbl_c1.setAlignment(Qt.AlignCenter)
            self.token_grid.addWidget(lbl_c1, row, 1)

            # Column 2 Token
            lbl_t2 = QLabel(t2)
            lbl_t2.setStyleSheet("color: #FFFFFF; font-size: 13px; font-weight: bold;")
            self.token_grid.addWidget(lbl_t2, row, 2)

            # Column 2 Counter Pill
            lbl_c2 = QLabel(c2)
            lbl_c2.setStyleSheet("color: #38BDF8; background-color: #0F2D54; border-radius: 4px; padding: 2px 8px; font-size: 11px; font-weight: 600;")
            lbl_c2.setAlignment(Qt.AlignCenter)
            self.token_grid.addWidget(lbl_c2, row, 3)

        mid_pane.addLayout(self.token_grid)
        main_layout.addLayout(mid_pane, 45)

        # Vertical Divider 2
        div2 = QFrame()
        div2.setFrameShape(QFrame.VLine)
        div2.setStyleSheet("background-color: #1E2D48; max-width: 1px;")
        main_layout.addWidget(div2)

        # -------------------------------------------------------------
        # 3. RIGHT PANE: DIGITAL CLOCK & APPRECIATION (20% width)
        # -------------------------------------------------------------
        right_pane = QVBoxLayout()
        right_pane.setAlignment(Qt.AlignCenter)
        right_pane.setSpacing(6)

        lbl_clock_icon = QLabel("🕒")
        lbl_clock_icon.setStyleSheet("font-size: 18px; color: #38BDF8;")
        lbl_clock_icon.setAlignment(Qt.AlignCenter)
        right_pane.addWidget(lbl_clock_icon)

        self.lbl_clock_time = QLabel("10:24 AM")
        self.lbl_clock_time.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: 800;")
        self.lbl_clock_time.setAlignment(Qt.AlignCenter)
        right_pane.addWidget(self.lbl_clock_time)

        self.lbl_clock_date = QLabel("24 May 2025\nSaturday")
        self.lbl_clock_date.setStyleSheet("color: #94A3B8; font-size: 11px; line-height: 1.2;")
        self.lbl_clock_date.setAlignment(Qt.AlignCenter)
        right_pane.addWidget(self.lbl_clock_date)

        right_pane.addSpacing(8)

        lbl_patients_icon = QLabel("👥")
        lbl_patients_icon.setStyleSheet("font-size: 18px; color: #38BDF8;")
        lbl_patients_icon.setAlignment(Qt.AlignCenter)
        right_pane.addWidget(lbl_patients_icon)

        lbl_thanks = QLabel("THANK YOU!")
        lbl_thanks.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;")
        lbl_thanks.setAlignment(Qt.AlignCenter)
        right_pane.addWidget(lbl_thanks)

        lbl_keep_ready = QLabel("Please keep your\ntoken ready")
        lbl_keep_ready.setStyleSheet("color: #94A3B8; font-size: 10px;")
        lbl_keep_ready.setAlignment(Qt.AlignCenter)
        right_pane.addWidget(lbl_keep_ready)

        main_layout.addLayout(right_pane, 20)

    def _start_clock(self):
        """Live ticking digital clock updating date and time every second."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_clock)
        self.timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        now = datetime.now()
        self.lbl_clock_time.setText(now.strftime("%I:%M %p"))
        self.lbl_clock_date.setText(now.strftime("%d %b %Y\n%A"))

    def update_serving_token(self, token_code: str, counter_name: str, department: str = "General OPD"):
        self.lbl_big_token.setText(token_code)
        self.lbl_counter_name.setText(counter_name.upper())
        self.lbl_department.setText(department)
