"""
Global QSS Stylesheet and Palette for MedCare PySide6 Application.
Pixel-perfect recreation of Drittech Queue / City Care Hospital SaaS aesthetic.

BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Quality Goal: Q02 - Improve Performance
"""

PALETTE = {
    # Dark Sidebar Palette (Matching Drittech Queue Photo)
    "sidebar_bg": "#0A1128",
    "sidebar_active": "#1E293B",
    "sidebar_hover": "#162035",
    "sidebar_text": "#94A3B8",
    "sidebar_text_active": "#FFFFFF",
    "sidebar_cyan": "#00E5FF",
    "sidebar_border": "#1E293B",

    # Main Application Palette
    "main_bg": "#F4F7FB",
    "card_bg": "#FFFFFF",
    "card_border": "#E2E8F0",
    "hero_navy": "#0A192F",
    "hero_border": "#1E2D48",

    # Text Colors
    "text_primary": "#0F172A",
    "text_secondary": "#64748B",
    "text_muted": "#94A3B8",

    # Accent Colors
    "primary": "#0284C7",
    "cyan": "#00BCD4",
    "cyan_light": "#E0F7FA",
    "cyan_badge_bg": "#E0F2FE",
    "cyan_badge_fg": "#0284C7",
    "success": "#16A34A",
    "success_bg": "#DCFCE7",
    "warning": "#D97706",
    "warning_bg": "#FEF3C7",
    "danger": "#EF4444",
    "danger_bg": "#FEE2E2",
    "purple": "#8B5CF6",
    "purple_bg": "#EDE9FE",
}

MAIN_QSS = """
/* Global Application Reset */
QWidget {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', Roboto, sans-serif;
    font-size: 13px;
    color: #0F172A;
}

QMainWindow, QDialog {
    background-color: #F4F7FB;
}

/* Scroll Area & Bars */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background: #F1F5F9;
    width: 8px;
    border-radius: 4px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #CBD5E1;
    min-height: 25px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #94A3B8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
    border: none;
}

/* Card Containers */
QFrame#Card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

QFrame#HeroCard {
    background-color: #0A192F;
    border: 1px solid #1E2D48;
    border-radius: 14px;
}

/* Tables (QTableWidget) */
QTableWidget {
    background-color: #FFFFFF;
    border: none;
    gridline-color: transparent;
    selection-background-color: #F0F9FF;
    selection-color: #0284C7;
    font-size: 13px;
}

QTableWidget::item {
    padding: 8px 12px;
    border-bottom: 1px solid #F1F5F9;
}

QTableWidget::item:selected {
    background-color: #F0F9FF;
    color: #0284C7;
}

QHeaderView::section {
    background-color: #FFFFFF;
    color: #64748B;
    font-size: 12px;
    font-weight: bold;
    padding: 10px 12px;
    border: none;
    border-bottom: 1px solid #E2E8F0;
}

/* Input Fields */
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    color: #0F172A;
}

QLineEdit:focus {
    border: 1.5px solid #0284C7;
    background-color: #FAFCFF;
}

/* ComboBox */
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 13px;
    color: #0F172A;
    min-width: 100px;
}

QComboBox:focus {
    border: 1.5px solid #0284C7;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
    border-left: none;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    selection-background-color: #E0F2FE;
    selection-color: #0284C7;
    padding: 4px;
}

/* Buttons */
QPushButton#PrimaryButton {
    background-color: #0284C7;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton#PrimaryButton:hover {
    background-color: #0369A1;
}

QPushButton#PrimaryButton:pressed {
    background-color: #075985;
}

QPushButton#SuccessButton {
    background-color: #16A34A;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton#SuccessButton:hover {
    background-color: #15803D;
}

QPushButton#SecondaryButton {
    background-color: #F1F5F9;
    color: #475569;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton#SecondaryButton:hover {
    background-color: #E2E8F0;
    color: #0F172A;
}

QPushButton#DangerButton {
    background-color: #FEE2E2;
    color: #DC2626;
    border: 1px solid #FECACA;
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton#DangerButton:hover {
    background-color: #FCA5A5;
    color: #991B1B;
}
"""
