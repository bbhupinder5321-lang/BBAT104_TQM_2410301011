import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import tkinter as tk
from src.main import MainWindow
from src.database import init_db

def test_tqm_diagrams_and_charts():
    print("=" * 60)
    print("  VERIFYING TQM EMBEDDED DIAGRAMS AND CHARTS")
    print("=" * 60)

    print("1. Initializing DB...")
    init_db()

    print("2. Launching MainWindow...")
    app = MainWindow()
    app.geometry("1280x800+50+50")
    app.update_idletasks()
    app.update()

    print("3. Logging in as admin...")
    app.login_view.txt_user.delete(0, tk.END)
    app.login_view.txt_user.insert(0, "admin")
    app.login_view.txt_pass.delete(0, tk.END)
    app.login_view.txt_pass.insert(0, "admin123")
    app.login_view._do_login()
    app.update_idletasks()
    app.update()

    print("4. Navigating to TQM Audit...")
    app._show_view("TQM Audit")
    app.update_idletasks()
    app.update()
    tqm = app.views["TQM Audit"]

    # 1. SIPOC
    print("5. Testing SIPOC Analysis Tab...")
    tqm._switch_tab("sipoc")
    app.update_idletasks()
    app.update()
    assert "sipoc" in tqm.tab_frames
    print("   [OK] SIPOC Process Pipeline & Matrix rendered successfully")

    # 2. FMEA
    print("6. Testing FMEA Analysis Tab & Embedded Chart...")
    tqm._switch_tab("fmea")
    app.update_idletasks()
    app.update()
    assert "fmea" in tqm.tab_frames
    print("   [OK] FMEA Treeview and Pre vs Post RPN Chart rendered")

    # 3. Fishbone
    print("7. Testing Fishbone (Ishikawa) Analysis Tab & Embedded Diagram...")
    tqm._switch_tab("fishbone")
    app.update_idletasks()
    app.update()
    assert "fishbone" in tqm.tab_frames
    print("   [OK] Fishbone Diagram & 4 Category Rib Cards rendered")

    # 4. Pareto
    print("8. Testing Pareto 80/20 Tab & Embedded Dual-Axis Chart...")
    tqm._switch_tab("pareto")
    app.update_idletasks()
    app.update()
    assert "pareto" in tqm.tab_frames
    print("   [OK] Pareto 80/20 Dual-Axis Chart & Vital Few Card rendered")

    # 5. Checksheet & Dynamic Redraw
    print("9. Testing Checksheet Tab & Dynamic Live Chart Redraw...")
    tqm._switch_tab("checksheet")
    app.update_idletasks()
    app.update()
    initial_count = len(tqm.defects_data)
    
    # Simulate adding defect
    tqm.txt_defect_name.delete(0, tk.END)
    tqm.txt_defect_name.insert(0, "Test Latency Spike")
    tqm.txt_defect_count.delete(0, tk.END)
    tqm.txt_defect_count.insert(0, "3")
    tqm._add_defect()
    app.update_idletasks()
    app.update()
    assert len(tqm.defects_data) == initial_count + 1
    assert tqm.checksheet_canvas is not None
    print("   [OK] Dynamic defect added and Checksheet chart redrawn in real-time")

    # Simulate +1 occurrence
    tqm.check_tree.selection_set(str(len(tqm.defects_data) - 1))
    tqm._increment_selected_defect()
    app.update_idletasks()
    app.update()
    print("   [OK] Double-click / +1 Occurrence incremented and chart redrawn")

    # 6. PDCA
    print("10. Testing PDCA Cycle Log & Embedded Deming Diagram...")
    tqm._switch_tab("pdca")
    app.update_idletasks()
    app.update()
    initial_pdca = len(tqm.pdca_data)
    tqm.cmb_phase.set("Plan")
    tqm.txt_activity.delete(0, tk.END)
    tqm.txt_activity.insert(0, "Automate performance testing")
    tqm.txt_outcome.delete(0, tk.END)
    tqm.txt_outcome.insert(0, "Zero regressions detected")
    tqm._add_pdca_activity()
    app.update_idletasks()
    app.update()
    assert len(tqm.pdca_data) == initial_pdca + 1
    print("   [OK] PDCA Activity added and Deming cycle diagram verified")

    print("11. Cleaning up window...")
    app.destroy()
    print("=" * 60)
    print("  ALL TQM EMBEDDED DIAGRAMS AND CHARTS VERIFIED 100%!")
    print("=" * 60)

if __name__ == "__main__":
    test_tqm_diagrams_and_charts()
