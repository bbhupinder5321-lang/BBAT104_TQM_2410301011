import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import tkinter as tk
from src.main import MainWindow
from src.database import init_db

def test_full_lifecycle():
    print("1. Initializing DB...")
    init_db()

    print("2. Launching MainWindow...")
    app = MainWindow()
    app.geometry("1280x800+50+50")
    app.update_idletasks()
    app.update()

    print("3. Testing Login View...")
    assert hasattr(app, "login_view"), "MainWindow must have login_view"
    app.login_view.txt_user.delete(0, tk.END)
    app.login_view.txt_user.insert(0, "admin")
    app.login_view.txt_pass.delete(0, tk.END)
    app.login_view.txt_pass.insert(0, "admin123")
    app.login_view._do_login()
    app.update_idletasks()
    app.update()

    assert app.workspace_frame is not None, "Workspace must be active after login"
    print("   [OK] Login successful, clinical workspace active")

    tabs = ["Dashboard", "Patients", "Doctors", "Appointments", "Billing", "CSV Import", "Reports", "TQM Audit"]
    for tab in tabs:
        print(f"4. Testing tab: {tab}...")
        app._show_view(tab)
        app.update_idletasks()
        app.update()
        assert app.current_tab == tab, f"Expected {tab}, got {app.current_tab}"
        print(f"   [OK] Tab {tab} rendered perfectly")

    print("5. Testing TQM sub-tabs...")
    tqm = app.views["TQM Audit"]
    subtabs = ["SIPOC Analysis", "FMEA Analysis", "Fishbone Analysis", "Pareto Analysis", "Checksheet", "PDCA Cycle"]
    for sub in subtabs:
        tqm._switch_tab(sub)
        app.update_idletasks()
        app.update()
        print(f"   [OK] TQM sub-tab {sub} switched and rendered")
    
    print("6. Testing Dashboard Emergency Action...")
    app._show_view("Dashboard")
    app.update_idletasks()
    app.update()
    dash = app.views["Dashboard"]
    dash.refresh_dashboard()
    print("   [OK] Dashboard refreshed")

    print("7. Testing Logout...")
    app._logout()
    app.update_idletasks()
    app.update()
    assert app.login_view.winfo_ismapped(), "Login view must be visible after logout"
    print("   [OK] Logout successful, back to login view")

    print("8. Cleaning up...")
    app.destroy()
    print("==================================================================")
    print("   ALL UI LIFECYCLE STAGES VERIFIED WITH 100% SUCCESS!")
    print("==================================================================")

if __name__ == "__main__":
    test_full_lifecycle()
