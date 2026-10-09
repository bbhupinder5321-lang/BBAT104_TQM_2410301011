"""Launch the PySide6 MediCare interface.

Run from the repository root:
    python -m app.gui.qt_main
"""
import sys

from PySide6.QtWidgets import QApplication

from app.database.database import initialize_database
from app.gui.qt_app import APP_STYLE, LoginWindow


def main():
    initialize_database()
    application = QApplication(sys.argv)
    application.setApplicationName("MediCare Hospital Management System")
    application.setOrganizationName("BBAT104 TQM Project")
    application.setStyle("Fusion")
    application.setStyleSheet(APP_STYLE)
    application.setFont(application.font())
    window = LoginWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
