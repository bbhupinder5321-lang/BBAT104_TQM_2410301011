"""
Custom Pill Badge and Circle Icon Widgets for PySide6.
BBAT104: Fundamentals of Total Quality Management
"""

from PySide6.QtWidgets import QLabel, QFrame, QHBoxLayout
from PySide6.QtCore import Qt


class Badge(QFrame):
    """Modern Pill Badge Widget (e.g. Counter 1, Serving, Idle, Priority)."""

    TYPE_PALETTE = {
        "green": ("#DCFCE7", "#16A34A", "#BBF7D0"),
        "amber": ("#FEF3C7", "#D97706", "#FDE68A"),
        "cyan": ("#E0F2FE", "#0284C7", "#BAE6FD"),
        "red": ("#FEE2E2", "#DC2626", "#FECACA"),
        "danger": ("#FEE2E2", "#DC2626", "#FECACA"),
        "purple": ("#EDE9FE", "#8B5CF6", "#DDD6FE"),
        "gray": ("#F1F5F9", "#475569", "#E2E8F0"),
    }

    def __init__(self, text: str, bg_color: str = "#E0F2FE", fg_color: str = "#0284C7",
                 border_color: str = "transparent", font_size: int = 11, bold: bool = True,
                 badge_type: str = None, parent=None):
        super().__init__(parent)
        if badge_type and badge_type.lower() in self.TYPE_PALETTE:
            bg_color, fg_color, border_color = self.TYPE_PALETTE[badge_type.lower()]

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 6px;
                padding: 2px 8px;
            }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(0)

        self.label = QLabel(text)
        weight = "bold" if bold else "normal"
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {fg_color};
                font-size: {font_size}px;
                font-weight: {weight};
                background: transparent;
                border: none;
            }}
        """)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

    def setText(self, text: str):
        self.label.setText(text)


class CircleIconBadge(QLabel):
    """Circular Icon Badge (for Live Overview stats and top bar)."""

    def __init__(self, icon: str, bg_color: str = "#E0F2FE", fg_color: str = "#0284C7",
                 size: int = 38, font_size: int = 16, parent=None):
        super().__init__(icon, parent)
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {fg_color};
                font-size: {font_size}px;
                border-radius: {size // 2}px;
                border: none;
            }}
        """)
