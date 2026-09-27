import sys
import os
import time
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import tkinter as tk
from PIL import ImageGrab
from src.main import MainWindow
from src.database import init_db

def run_capture():
    init_db()
    
    # Target directory for screenshots
    shot_dir = ROOT_DIR / "screenshots"
    shot_dir.mkdir(parents=True, exist_ok=True)
    
    app = MainWindow()
    # Move window to predictable coordinates on screen
    app.geometry("1280x800+50+50")
    app.update_idletasks()
    app.update()
    time.sleep(0.5)
    
    def capture(name):
        app.update_idletasks()
        app.update()
        time.sleep(0.3)
        x = app.winfo_rootx()
        y = app.winfo_rooty()
        w = app.winfo_width()
        h = app.winfo_height()
        # Grab window rectangle
        bbox = (x, y, x + w, y + h)
        img = ImageGrab.grab(bbox=bbox)
        out_path = shot_dir / f"{name}.png"
        img.save(out_path)
        print(f"Captured: {out_path} ({w}x{h})")
        return out_path

    # 1. Capture Login Screen
    capture("01_login_screen")
    
    # 2. Perform Login
    app.login_view.txt_user.insert(0, "admin")
    app.login_view.txt_pass.insert(0, "admin123")
    app.login_view._do_login()
    app.update_idletasks()
    app.update()
    time.sleep(0.5)
    
    # 3. Capture Dashboard
    capture("02_dashboard")
    
    # 4. Capture Patients
    app._show_view("Patients")
    capture("03_patients")
    
    # 5. Capture Doctors
    app._show_view("Doctors")
    capture("04_doctors")
    
    # 6. Capture Appointments
    app._show_view("Appointments")
    capture("05_appointments")
    
    # 7. Capture Billing
    app._show_view("Billing")
    capture("06_billing")
    
    # 8. Capture CSV Import
    app._show_view("CSV Import")
    capture("07_csv_import")
    
    # 9. Capture Reports
    app._show_view("Reports")
    capture("08_reports")
    
    # 10. Capture TQM Audit
    app._show_view("TQM Audit")
    capture("09_tqm_audit")
    
    # 11. Also capture TQM subtabs
    tqm_view = app.views.get("TQM Audit")
    if tqm_view and hasattr(tqm_view, "_switch_subtab"):
        tqm_view._switch_subtab("FMEA Analysis")
        capture("10_tqm_fmea")
        tqm_view._switch_subtab("Fishbone Analysis")
        capture("11_tqm_fishbone")
        tqm_view._switch_subtab("Pareto Analysis")
        capture("12_tqm_pareto")
        tqm_view._switch_subtab("Checksheet")
        capture("13_tqm_checksheet")
        tqm_view._switch_subtab("PDCA Cycle")
        capture("14_tqm_pdca")
        
    app.destroy()
    print("All captures complete!")

if __name__ == "__main__":
    run_capture()
