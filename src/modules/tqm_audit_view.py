"""
TQM Quality Audit, FMEA, SIPOC & Continuous Improvement (PDCA) Module.
Directly implements Review 3, Review 4 & Evaluation Rubrics of BBAT104:
- Top Metric Cards with Left Color Accent Lines (Failure Modes, High Risk, Medium Risk, Highest RPN)
- Horizontal Pill Navigation (SIPOC Analysis, FMEA Analysis, Fishbone Analysis, Pareto Analysis, Checksheet, PDCA Cycle)
- Checksheet Analysis with dynamic incident recording and frequency table
- Deming PDCA Cycle Log with interactive CRUD activity management
- FMEA Matrix with Pre/Post RPN calculations
- SIPOC Process Map with CTQ indicators
- Direct Matplotlib SQC Visualizers (Pareto 80/20 and Ishikawa Fishbone)

BBAT104: Fundamentals of Total Quality Management
Academic Session: 2026–27 | Max Assessment: 70 Raw Marks (CO1, CO2, CO3)
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
Assigned Quality Goal: Q02 - Improve Performance
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from src.config import THEME, STUDENT_NAME, STUDENT_ROLL, COURSE_CODE, QUALITY_GOAL
from src.widgets.ui_kit import RoundedCard, AccentLineStatCard, PillButton, CircleBadge
from src.utils.sqc_visualizer import generate_pareto_chart, generate_fishbone_diagram


class TQMAuditView(tk.Frame):
    """
    Dedicated TQM Quality Audit & Accreditation View for BBAT104.
    Refined modern SaaS aesthetic matching Reference Screenshots.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=THEME["background"])
        self.selected_pdca_id = None
        self._build_ui()

    def _build_ui(self):
        container = tk.Frame(self, bg=THEME["background"], padx=6, pady=4)
        container.pack(fill=tk.BOTH, expand=True)

        # 0. Top Header Bar
        head_bar = tk.Frame(container, bg=THEME["background"])
        head_bar.pack(fill=tk.X, pady=(0, 10))

        head_left = tk.Frame(head_bar, bg=THEME["background"])
        head_left.pack(side=tk.LEFT)

        tk.Label(
            head_left, text="✓  TQM Analysis",
            font=("Segoe UI", 16, "bold"), fg="#0F172A", bg=THEME["background"]
        ).pack(anchor=tk.W)

        tk.Label(
            head_left, text="Quality analysis for Q02 - Improve Performance",
            font=("Segoe UI", 9), fg="#64748B", bg=THEME["background"]
        ).pack(anchor=tk.W, pady=(1, 0))

        # 1. 4 Metric Cards Strip with Left Color Accent Lines
        kpi_row = tk.Frame(container, bg=THEME["background"])
        kpi_row.pack(fill=tk.X, pady=(0, 12))

        self.kpi_modes = AccentLineStatCard(
            kpi_row, value="6", title="Failure Modes",
            sub_text="Performance risks identified", accent_color="#2563EB"
        )
        self.kpi_modes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.kpi_high = AccentLineStatCard(
            kpi_row, value="0", title="High Risk",
            sub_text="Requires attention", accent_color="#EF4444"
        )
        self.kpi_high.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.kpi_med = AccentLineStatCard(
            kpi_row, value="6", title="Medium Risk",
            sub_text="Needs monitoring", accent_color="#F59E0B"
        )
        self.kpi_med.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.kpi_rpn = AccentLineStatCard(
            kpi_row, value="192", title="Highest RPN",
            sub_text="Risk priority number", accent_color="#8B5CF6"
        )
        self.kpi_rpn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # 2. Main Content Card
        main_card = RoundedCard(
            container, bg_color="#FFFFFF", border_color="#E2E8F0",
            radius=16, pad_shadow=6, padx=16, pady=14
        )
        main_card.pack(fill=tk.BOTH, expand=True)

        # Sub-Navigation Tabs Bar (Pills matching Reference Screenshots)
        tab_bar = tk.Frame(main_card.inner, bg="#FFFFFF", pady=2)
        tab_bar.pack(anchor=tk.CENTER, pady=(0, 14))

        self.tab_buttons = {}
        self.tab_frames = {}

        tabs_meta = [
            ("sipoc", "SIPOC Analysis"),
            ("fmea", "FMEA Analysis"),
            ("fishbone", "Fishbone Analysis"),
            ("pareto", "Pareto Analysis"),
            ("checksheet", "Checksheet"),
            ("pdca", "PDCA Cycle"),
        ]

        for tab_id, label in tabs_meta:
            btn = tk.Button(
                tab_bar, text=label, font=("Segoe UI", 9, "bold"),
                relief="flat", cursor="hand2", padx=14, pady=5, bd=0,
                command=lambda tid=tab_id: self._switch_tab(tid)
            )
            btn.pack(side=tk.LEFT, padx=3)
            self.tab_buttons[tab_id] = btn

            frame = tk.Frame(main_card.inner, bg="#FFFFFF")
            self.tab_frames[tab_id] = frame

        # Build each tab's contents
        self._build_sipoc_tab()
        self._build_fmea_tab()
        self._build_fishbone_tab()
        self._build_pareto_tab()
        self._build_checksheet_tab()
        self._build_pdca_tab()

        # Default to Checksheet or PDCA as shown in screenshots
        self._switch_tab("checksheet")

    def _switch_tab(self, active_id: str):
        for tid, btn in self.tab_buttons.items():
            if tid == active_id:
                btn.config(bg="#2563EB", fg="#FFFFFF", relief="flat")
            else:
                btn.config(bg="#F1F5F9", fg="#64748B", relief="flat")

        for tid, frame in self.tab_frames.items():
            frame.pack_forget()

        if active_id in self.tab_frames:
            self.tab_frames[active_id].pack(fill=tk.BOTH, expand=True)

    # ---------------- TAB 1: SIPOC PROCESS MAP ----------------
    def _build_sipoc_tab(self):
        f = self.tab_frames["sipoc"]

        head = tk.Frame(f, bg="#FFFFFF")
        head.pack(fill=tk.X, pady=(0, 6))

        tk.Label(head, text="SIPOC Process Mapping", font=("Segoe UI", 12, "bold"), fg="#0F172A", bg="#FFFFFF").pack(anchor=tk.W)
        tk.Label(head, text="Suppliers → Inputs → Process → Outputs → Customers with CTQ indicators", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(anchor=tk.W)

        cols = ("stage", "supplier", "input", "process", "output", "customer", "ctq")
        tree = ttk.Treeview(f, columns=cols, show="headings", height=8)

        tree.heading("stage", text="Stage")
        tree.heading("supplier", text="Suppliers (S)")
        tree.heading("input", text="Inputs (I)")
        tree.heading("process", text="Process Workflow (P)")
        tree.heading("output", text="Outputs (O)")
        tree.heading("customer", text="Customers (C)")
        tree.heading("ctq", text="Critical To Quality (CTQ)")

        tree.column("stage", width=55, anchor=tk.CENTER)
        tree.column("supplier", width=120, anchor=tk.W)
        tree.column("input", width=130, anchor=tk.W)
        tree.column("process", width=160, anchor=tk.W)
        tree.column("output", width=130, anchor=tk.W)
        tree.column("customer", width=120, anchor=tk.W)
        tree.column("ctq", width=140, anchor=tk.W)

        tree.pack(fill=tk.BOTH, expand=True, pady=(6, 8))

        sipoc_data = [
            ("1", "Ambulatory Patients", "Name, Phone, Age, Gender", "Fast Search & Verification", "Verified Profile / Match", "Front Desk Staff", "Search Latency < 100ms"),
            ("2", "Referring Clinics / CSV", "CSV Patient Dataset", "Poka-Yoke Registration", "UHID + Zero Duplicates", "Registry / Admin", "Zero Phone Collisions"),
            ("3", "Front Desk Reception", "Doctor & Slot Preference", "Slot Booking & Token Issue", "Sequential Token Slip", "Patient & Doctor", "FIFO Sequential Tokens"),
            ("4", "Waiting Lounge Patients", "Token Number & Arrival", "Reception Check-In Timestamp", "Active Waiting Queue", "Attending Doctor", "Queue Wait < 15.0 min"),
            ("5", "Attending Physicians", "Vitals, Symptoms & Diagnosis", "Clinical Consultation", "Diagnosis & Prescriptions", "Patient & Pharmacist", "Clinical Consultation Done"),
            ("6", "Billing Cashier Desk", "Doctor Fee, Meds, Labs", "Itemized Invoicing & 5% GST", "Settled Tax Invoice", "Patient & Management", "Zero Billing Discrepancies"),
        ]

        for r in sipoc_data:
            tree.insert("", tk.END, values=r)

    # ---------------- TAB 2: FMEA MATRIX ----------------
    def _build_fmea_tab(self):
        f = self.tab_frames["fmea"]

        head = tk.Frame(f, bg="#FFFFFF")
        head.pack(fill=tk.X, pady=(0, 6))

        tk.Label(head, text="Failure Mode and Effects Analysis (FMEA) Matrix", font=("Segoe UI", 12, "bold"), fg="#0F172A", bg="#FFFFFF").pack(anchor=tk.W)
        tk.Label(head, text="Formula: RPN = Severity (S) × Occurrence (O) × Detection (D)", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(anchor=tk.W)

        cols = ("code", "failure_mode", "effect", "s", "o", "d", "pre_rpn", "countermeasure", "post_rpn")
        tree = ttk.Treeview(f, columns=cols, show="headings", height=8)

        tree.heading("code", text="Defect #")
        tree.heading("failure_mode", text="Potential Failure Mode")
        tree.heading("effect", text="Impact / Potential Effect")
        tree.heading("s", text="S")
        tree.heading("o", text="O")
        tree.heading("d", text="D")
        tree.heading("pre_rpn", text="Pre RPN")
        tree.heading("countermeasure", text="TQM Q02 Mitigation Countermeasure")
        tree.heading("post_rpn", text="Post RPN")

        tree.column("code", width=65, anchor=tk.CENTER)
        tree.column("failure_mode", width=175, anchor=tk.W)
        tree.column("effect", width=160, anchor=tk.W)
        tree.column("s", width=35, anchor=tk.CENTER)
        tree.column("o", width=35, anchor=tk.CENTER)
        tree.column("d", width=35, anchor=tk.CENTER)
        tree.column("pre_rpn", width=70, anchor=tk.CENTER)
        tree.column("countermeasure", width=220, anchor=tk.W)
        tree.column("post_rpn", width=70, anchor=tk.CENTER)

        tree.pack(fill=tk.BOTH, expand=True, pady=(6, 8))

        fmea_data = [
            ("FM-01", "Slow Patient Record Search", "Queue congestion, triage delays", "7", "8", "7", "392", "B-Tree Composite Indexes + Fast Search (<100ms)", "14 (↓ 96%)"),
            ("FM-02", "Excessive Queue Waiting", "Patient frustration, room idling", "8", "7", "6", "336", "FIFO Token Sequencer + Real-Time Telemetry", "32 (↓ 90%)"),
            ("FM-03", "Duplicate Patient Profiles", "Fractured medical histories, billing conflict", "8", "6", "6", "288", "Poka-Yoke Pre-Add Phone & UHID Unique Guard", "12 (↓ 96%)"),
            ("FM-04", "Report Generation Freeze", "Administrative reporting lag, thread lock", "6", "6", "6", "216", "Vectorized Pandas Aggregations in < 15ms", "16 (↓ 93%)"),
            ("FM-05", "Doctor Room Conflict", "Doctor overlapping, room contention", "6", "4", "5", "120", "Relational Room Allocation Constraint Model", "18 (↓ 85%)"),
            ("FM-06", "Billing Tax Math Errors", "Financial reconciliation failure, audit fault", "7", "3", "4", "84", "Automated 5% GST Formula + Transaction Lock", "14 (↓ 83%)"),
        ]

        tree.tag_configure("high_rpn", background="#FFF1F2", foreground="#9F1239")
        tree.tag_configure("med_rpn", background="#FFFDF0", foreground="#B45309")

        for row in fmea_data:
            tag = "high_rpn" if int(row[6]) >= 250 else "med_rpn"
            tree.insert("", tk.END, values=row, tags=(tag,))

    # ---------------- TAB 3: FISHBONE ANALYSIS ----------------
    def _build_fishbone_tab(self):
        f = self.tab_frames["fishbone"]

        head = tk.Frame(f, bg="#FFFFFF")
        head.pack(fill=tk.X, pady=(0, 6))

        tk.Label(head, text="Ishikawa (Fishbone) Cause-and-Effect Analysis", font=("Segoe UI", 12, "bold"), fg="#0F172A", bg="#FFFFFF").pack(anchor=tk.W)
        tk.Label(head, text="Root cause breakdown across People, Process, Software Code, and Infrastructure", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(anchor=tk.W)

        branches = [
            ("👨‍⚕️ PEOPLE", "#EFF6FF", "#1E40AF", "• Staff manual data typing mistakes\n• Unregistered walk-ins unnotified\n• Lack of keyboard shortcuts"),
            ("🔄 PROCESS", "#F0FDF4", "#15803D", "• Unordered queue management\n• Duplicate check-ins without verification\n• Missing triage classification"),
            ("💻 SOFTWARE", "#FEFCE8", "#B45309", "• Missing B-Tree database indexes\n• Non-vectorized report loops\n• Synchronous UI thread lock on queries"),
            ("🏗️ INFRASTRUCTURE", "#FAF5FF", "#6B21A8", "• SQLite disk I/O lock (solved via WAL)\n• Network latency on client terminals\n• Unindexed foreign keys")
        ]

        b_frame = tk.Frame(f, bg="#FFFFFF")
        b_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        for i, (title, bg_c, fg_c, text) in enumerate(branches):
            col = tk.Frame(b_frame, bg=bg_c, highlightthickness=1, highlightbackground="#E2E8F0", padx=12, pady=10)
            col.grid(row=i // 2, column=i % 2, sticky="nsew", padx=6, pady=6)
            b_frame.grid_columnconfigure(i % 2, weight=1)
            b_frame.grid_rowconfigure(i // 2, weight=1)

            tk.Label(col, text=title, font=("Segoe UI", 10, "bold"), fg=fg_c, bg=bg_c).pack(anchor=tk.W)
            tk.Label(col, text=text, font=("Segoe UI", 8), fg="#1E293B", bg=bg_c, justify=tk.LEFT).pack(anchor=tk.W, pady=(4, 0))

        btn = PillButton(
            f, text="🐟 Launch Matplotlib Ishikawa Diagram", font_size=9,
            bg_color="#15803D", fg_color="white", hover_color="#14532D",
            padx=14, pady=6, command=generate_fishbone_diagram
        )
        btn.pack(anchor=tk.W, pady=(4, 0))

    # ---------------- TAB 4: PARETO ANALYSIS ----------------
    def _build_pareto_tab(self):
        f = self.tab_frames["pareto"]

        head = tk.Frame(f, bg="#FFFFFF")
        head.pack(fill=tk.X, pady=(0, 6))

        tk.Label(head, text="Pareto 80/20 Defect Analysis", font=("Segoe UI", 12, "bold"), fg="#0F172A", bg="#FFFFFF").pack(anchor=tk.W)
        tk.Label(head, text="Isolating the vital 20% causes driving 80% of operational throughput delays", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(anchor=tk.W)

        summary_box = tk.Frame(f, bg="#F8FAFC", highlightthickness=1, highlightbackground="#E2E8F0", padx=14, pady=10)
        summary_box.pack(fill=tk.X, pady=8)

        tk.Label(summary_box, text="⚡ Vital Few Root Causes Identified:", font=("Segoe UI", 9, "bold"), fg="#0F172A", bg="#F8FAFC").pack(anchor=tk.W)
        tk.Label(
            summary_box,
            text="1. Slow Patient Search (37.0% of defects) → Solved via B-Tree Composite Indexing (< 1ms)\n"
                 "2. Queue Waiting Delays (30.7% of defects) → Solved via FIFO Token Dispenser & Live Telemetry\n"
                 "3. Duplicate Patient Profiles (16.7% of defects) → Solved via Poka-Yoke Uniqueness Validation\n"
                 "➜ Together, these top 3 causes accounted for 84.4% of all operational performance incidents.",
            font=("Segoe UI", 8), fg="#475569", bg="#F8FAFC", justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(4, 0))

        btn = PillButton(
            f, text="📈 Launch Matplotlib Pareto 80/20 Chart", font_size=9,
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
            padx=14, pady=6, command=generate_pareto_chart
        )
        btn.pack(anchor=tk.W, pady=(6, 0))

    # ---------------- TAB 5: CHECKSHEET ANALYSIS (IMAGE 5) ----------------
    def _build_checksheet_tab(self):
        f = self.tab_frames["checksheet"]

        head = tk.Frame(f, bg="#FFFFFF")
        head.pack(fill=tk.X, pady=(0, 4))

        tk.Label(head, text="Checksheet Analysis", font=("Segoe UI", 13, "bold"), fg="#0F172A", bg="#FFFFFF").pack(anchor=tk.W)
        tk.Label(head, text="Track and measure the frequency of performance defects", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(anchor=tk.W, pady=(1, 6))

        # Mini summary boxes
        stat_bar = tk.Frame(f, bg="#FFFFFF")
        stat_bar.pack(fill=tk.X, pady=(0, 8))

        boxes = [
            ("Total Defects", "68", 140),
            ("Defect Types", "6", 140),
            ("Most Frequent", "Slow patient search", 220),
        ]
        self.check_stat_labels = {}
        for title, val, w in boxes:
            b = tk.Frame(stat_bar, bg="#F1F5F9", padx=12, pady=6, width=w)
            b.pack(side=tk.LEFT, padx=(0, 8))
            b.pack_propagate(False)

            tk.Label(b, text=title, font=("Segoe UI", 7), fg="#64748B", bg="#F1F5F9").pack(anchor=tk.W)
            lbl_v = tk.Label(b, text=val, font=("Segoe UI", 10, "bold"), fg="#0F172A", bg="#F1F5F9")
            lbl_v.pack(anchor=tk.W)
            self.check_stat_labels[title] = lbl_v

        # Add / Record Defect Row
        form_row = tk.Frame(f, bg="#FFFFFF")
        form_row.pack(fill=tk.X, pady=(0, 8))

        tk.Label(form_row, text="Add / Record Defect", font=("Segoe UI", 8, "bold"), fg="#0F172A", bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 8))

        self.txt_defect_name = tk.Entry(form_row, font=("Segoe UI", 9), bg="#FFFFFF", relief="solid", bd=1, width=40)
        self.txt_defect_name.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), ipady=3)
        self.txt_defect_name.insert(0, "Performance defect name")
        self.txt_defect_name.bind("<FocusIn>", lambda e: self.txt_defect_name.delete(0, tk.END) if self.txt_defect_name.get() == "Performance defect name" else None)

        self.txt_defect_count = tk.Entry(form_row, font=("Segoe UI", 9), bg="#FFFFFF", relief="solid", bd=1, width=8)
        self.txt_defect_count.pack(side=tk.LEFT, padx=(0, 8), ipady=3)
        self.txt_defect_count.insert(0, "1")

        btn_add = PillButton(
            form_row, text="Add Defect", font_size=8,
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
            padx=12, pady=4, command=self._add_defect
        )
        btn_add.pack(side=tk.LEFT)

        # Defect Frequency Table
        table_head = tk.Frame(f, bg="#FFFFFF")
        table_head.pack(fill=tk.X)
        tk.Label(table_head, text="Defect Frequency", font=("Segoe UI", 9, "bold"), fg="#0F172A", bg="#FFFFFF").pack(side=tk.LEFT)
        tk.Label(table_head, text="Double-click a row to record +1 occurrence", font=("Segoe UI", 7), fg="#64748B", bg="#FFFFFF").pack(side=tk.RIGHT)

        cols = ("num", "defect", "occurrences", "percentage")
        self.check_tree = ttk.Treeview(f, columns=cols, show="headings", height=7)

        self.check_tree.heading("num", text="#")
        self.check_tree.heading("defect", text="Performance Defect")
        self.check_tree.heading("occurrences", text="Occurrences")
        self.check_tree.heading("percentage", text="Percentage")

        self.check_tree.column("num", width=45, anchor=tk.CENTER)
        self.check_tree.column("defect", width=340, anchor=tk.W)
        self.check_tree.column("occurrences", width=100, anchor=tk.CENTER)
        self.check_tree.column("percentage", width=100, anchor=tk.CENTER)

        self.check_tree.pack(fill=tk.BOTH, expand=True, pady=(4, 8))
        self.check_tree.bind("<Double-1>", lambda e: self._increment_selected_defect())

        # Checksheet Default Data
        self.defects_data = [
            {"name": "Slow patient search", "count": 18},
            {"name": "Duplicate patient record", "count": 15},
            {"name": "Slow reports", "count": 12},
            {"name": "Dashboard loading slowly", "count": 10},
            {"name": "Database query timeout", "count": 8},
            {"name": "Slow CSV import", "count": 5},
        ]
        self._refresh_checksheet_table()

        # Action Buttons Bottom
        act_row = tk.Frame(f, bg="#FFFFFF")
        act_row.pack(fill=tk.X)

        btn_inc = PillButton(
            act_row, text="+1 Occurrence", font_size=8,
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
            padx=10, pady=4, command=self._increment_selected_defect
        )
        btn_inc.pack(side=tk.LEFT, padx=(0, 6))

        btn_rem = PillButton(
            act_row, text="Remove", font_size=8,
            bg_color="#EF4444", fg_color="white", hover_color="#DC2626",
            padx=10, pady=4, command=self._remove_selected_defect
        )
        btn_rem.pack(side=tk.LEFT)

        btn_ref = PillButton(
            act_row, text="Refresh", font_size=8,
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
            padx=12, pady=4, command=self._refresh_checksheet_table
        )
        btn_ref.pack(side=tk.RIGHT)

    def _refresh_checksheet_table(self):
        for item in self.check_tree.get_children():
            self.check_tree.delete(item)

        total = sum(d["count"] for d in self.defects_data) or 1
        for idx, d in enumerate(self.defects_data, 1):
            pct = (d["count"] / total) * 100
            self.check_tree.insert("", tk.END, iid=str(idx - 1), values=(
                idx, d["name"], d["count"], f"{pct:.1f}%"
            ))

        self.check_stat_labels["Total Defects"].config(text=str(total))
        self.check_stat_labels["Defect Types"].config(text=str(len(self.defects_data)))
        top_name = max(self.defects_data, key=lambda x: x["count"])["name"] if self.defects_data else "None"
        self.check_stat_labels["Most Frequent"].config(text=top_name[:20])

    def _add_defect(self):
        name = self.txt_defect_name.get().strip()
        count_str = self.txt_defect_count.get().strip()
        if not name or name == "Performance defect name":
            return
        try:
            count = max(1, int(count_str))
        except ValueError:
            count = 1

        for d in self.defects_data:
            if d["name"].lower() == name.lower():
                d["count"] += count
                self._refresh_checksheet_table()
                return

        self.defects_data.append({"name": name, "count": count})
        self._refresh_checksheet_table()
        self.txt_defect_name.delete(0, tk.END)

    def _increment_selected_defect(self):
        sel = self.check_tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        if 0 <= idx < len(self.defects_data):
            self.defects_data[idx]["count"] += 1
            self._refresh_checksheet_table()

    def _remove_selected_defect(self):
        sel = self.check_tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        if 0 <= idx < len(self.defects_data):
            self.defects_data.pop(idx)
            self._refresh_checksheet_table()

    # ---------------- TAB 6: PDCA CYCLE LOG (IMAGE 4) ----------------
    def _build_pdca_tab(self):
        f = self.tab_frames["pdca"]

        head = tk.Frame(f, bg="#FFFFFF")
        head.pack(fill=tk.X, pady=(0, 4))

        tk.Label(head, text="PDCA Cycle Log", font=("Segoe UI", 13, "bold"), fg="#0F172A", bg="#FFFFFF").pack(anchor=tk.W)
        tk.Label(head, text="Plan → Do → Check → Act for continuous quality improvement", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF").pack(anchor=tk.W, pady=(1, 6))

        # Mini summary boxes
        stat_bar = tk.Frame(f, bg="#FFFFFF")
        stat_bar.pack(fill=tk.X, pady=(0, 8))

        boxes = [
            ("Total Activities", "4", 130),
            ("Plan", "1", 100),
            ("Do", "1", 100),
            ("Check", "1", 100),
        ]
        self.pdca_stat_labels = {}
        for title, val, w in boxes:
            b = tk.Frame(stat_bar, bg="#F1F5F9", padx=12, pady=6, width=w)
            b.pack(side=tk.LEFT, padx=(0, 8))
            b.pack_propagate(False)

            tk.Label(b, text=title, font=("Segoe UI", 7), fg="#64748B", bg="#F1F5F9").pack(anchor=tk.W)
            lbl_v = tk.Label(b, text=val, font=("Segoe UI", 10, "bold"), fg="#0F172A", bg="#F1F5F9")
            lbl_v.pack(anchor=tk.W)
            self.pdca_stat_labels[title] = lbl_v

        # Add PDCA Activity Row
        form_row = tk.Frame(f, bg="#FFFFFF")
        form_row.pack(fill=tk.X, pady=(0, 8))

        tk.Label(form_row, text="Add PDCA Activity", font=("Segoe UI", 8, "bold"), fg="#0F172A", bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 8))

        self.cmb_phase = ttk.Combobox(form_row, values=["Plan", "Do", "Check", "Act"], width=8, state="readonly")
        self.cmb_phase.set("Plan")
        self.cmb_phase.pack(side=tk.LEFT, padx=(0, 6))

        self.txt_activity = tk.Entry(form_row, font=("Segoe UI", 9), bg="#FFFFFF", relief="solid", bd=1, width=28)
        self.txt_activity.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), ipady=3)
        self.txt_activity.insert(0, "Activity description")
        self.txt_activity.bind("<FocusIn>", lambda e: self.txt_activity.delete(0, tk.END) if self.txt_activity.get() == "Activity description" else None)

        self.txt_outcome = tk.Entry(form_row, font=("Segoe UI", 9), bg="#FFFFFF", relief="solid", bd=1, width=28)
        self.txt_outcome.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=3)
        self.txt_outcome.insert(0, "Result / outcome")
        self.txt_outcome.bind("<FocusIn>", lambda e: self.txt_outcome.delete(0, tk.END) if self.txt_outcome.get() == "Result / outcome" else None)

        btn_add = PillButton(
            form_row, text="Add Activity", font_size=8,
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
            padx=12, pady=4, command=self._add_pdca_activity
        )
        btn_add.pack(side=tk.LEFT)

        # Table: PDCA Improvement Log
        table_head = tk.Frame(f, bg="#FFFFFF")
        table_head.pack(fill=tk.X)
        tk.Label(table_head, text="PDCA Improvement Log", font=("Segoe UI", 9, "bold"), fg="#0F172A", bg="#FFFFFF").pack(side=tk.LEFT)
        tk.Label(table_head, text="Select a row to edit or remove", font=("Segoe UI", 7), fg="#64748B", bg="#FFFFFF").pack(side=tk.RIGHT)

        cols = ("id", "phase", "activity", "outcome")
        self.pdca_tree = ttk.Treeview(f, columns=cols, show="headings", height=7)

        self.pdca_tree.heading("id", text="ID")
        self.pdca_tree.heading("phase", text="Phase")
        self.pdca_tree.heading("activity", text="Activity")
        self.pdca_tree.heading("outcome", text="Result / Outcome")

        self.pdca_tree.column("id", width=45, anchor=tk.CENTER)
        self.pdca_tree.column("phase", width=75, anchor=tk.CENTER)
        self.pdca_tree.column("activity", width=280, anchor=tk.W)
        self.pdca_tree.column("outcome", width=280, anchor=tk.W)

        self.pdca_tree.pack(fill=tk.BOTH, expand=True, pady=(4, 8))

        # Default PDCA Data (Matching Image 4)
        self.pdca_data = [
            {"id": 1, "phase": "Plan", "activity": "Identify slow patient search and define performance target.", "outcome": "Search response target set below 1 second."},
            {"id": 2, "phase": "Do", "activity": "Implement database indexes and filtered SQL queries.", "outcome": "Patient search and database operations optimized."},
            {"id": 3, "phase": "Check", "activity": "Measure search, dashboard, report and database response times.", "outcome": "Performance measured against the 1 second target."},
            {"id": 4, "phase": "Act", "activity": "Standardize successful optimizations and identify further improvements.", "outcome": "Performance improvements documented for continuous improvement."},
        ]
        self._refresh_pdca_table()

        # Action Buttons Bottom
        act_row = tk.Frame(f, bg="#FFFFFF")
        act_row.pack(fill=tk.X)

        btn_load = PillButton(
            act_row, text="Load Selected", font_size=8,
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
            padx=10, pady=4, command=self._load_selected_pdca
        )
        btn_load.pack(side=tk.LEFT, padx=(0, 6))

        btn_upd = PillButton(
            act_row, text="Update", font_size=8,
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
            padx=10, pady=4, command=self._update_pdca_activity
        )
        btn_upd.pack(side=tk.LEFT, padx=(0, 6))

        btn_rem = PillButton(
            act_row, text="Remove", font_size=8,
            bg_color="#EF4444", fg_color="white", hover_color="#DC2626",
            padx=10, pady=4, command=self._remove_pdca_activity
        )
        btn_rem.pack(side=tk.LEFT, padx=(0, 6))

        btn_clr = PillButton(
            act_row, text="Clear", font_size=8,
            bg_color="#64748B", fg_color="white", hover_color="#475569",
            padx=10, pady=4, command=self._clear_pdca_inputs
        )
        btn_clr.pack(side=tk.LEFT)

        btn_ref = PillButton(
            act_row, text="Refresh", font_size=8,
            bg_color="#2563EB", fg_color="white", hover_color="#1D4ED8",
            padx=12, pady=4, command=self._refresh_pdca_table
        )
        btn_ref.pack(side=tk.RIGHT)

    def _refresh_pdca_table(self):
        for item in self.pdca_tree.get_children():
            self.pdca_tree.delete(item)

        for d in self.pdca_data:
            self.pdca_tree.insert("", tk.END, iid=str(d["id"]), values=(
                d["id"], d["phase"], d["activity"], d["outcome"]
            ))

        self.pdca_stat_labels["Total Activities"].config(text=str(len(self.pdca_data)))
        p_cnt = sum(1 for d in self.pdca_data if d["phase"] == "Plan")
        d_cnt = sum(1 for d in self.pdca_data if d["phase"] == "Do")
        c_cnt = sum(1 for d in self.pdca_data if d["phase"] == "Check")
        self.pdca_stat_labels["Plan"].config(text=str(p_cnt))
        self.pdca_stat_labels["Do"].config(text=str(d_cnt))
        self.pdca_stat_labels["Check"].config(text=str(c_cnt))

    def _add_pdca_activity(self):
        phase = self.cmb_phase.get()
        activity = self.txt_activity.get().strip()
        outcome = self.txt_outcome.get().strip()
        if not activity or activity == "Activity description":
            return

        new_id = max([d["id"] for d in self.pdca_data], default=0) + 1
        self.pdca_data.append({"id": new_id, "phase": phase, "activity": activity, "outcome": outcome})
        self._refresh_pdca_table()
        self._clear_pdca_inputs()

    def _load_selected_pdca(self):
        sel = self.pdca_tree.selection()
        if not sel:
            return
        item_id = int(sel[0])
        for d in self.pdca_data:
            if d["id"] == item_id:
                self.selected_pdca_id = item_id
                self.cmb_phase.set(d["phase"])
                self.txt_activity.delete(0, tk.END)
                self.txt_activity.insert(0, d["activity"])
                self.txt_outcome.delete(0, tk.END)
                self.txt_outcome.insert(0, d["outcome"])
                break

    def _update_pdca_activity(self):
        if self.selected_pdca_id is None:
            self._load_selected_pdca()
        if self.selected_pdca_id is None:
            return

        for d in self.pdca_data:
            if d["id"] == self.selected_pdca_id:
                d["phase"] = self.cmb_phase.get()
                d["activity"] = self.txt_activity.get().strip()
                d["outcome"] = self.txt_outcome.get().strip()
                break
        self._refresh_pdca_table()
        self._clear_pdca_inputs()

    def _remove_pdca_activity(self):
        sel = self.pdca_tree.selection()
        if not sel:
            return
        item_id = int(sel[0])
        self.pdca_data = [d for d in self.pdca_data if d["id"] != item_id]
        self._refresh_pdca_table()
        self._clear_pdca_inputs()

    def _clear_pdca_inputs(self):
        self.selected_pdca_id = None
        self.cmb_phase.set("Plan")
        self.txt_activity.delete(0, tk.END)
        self.txt_activity.insert(0, "Activity description")
        self.txt_outcome.delete(0, tk.END)
        self.txt_outcome.insert(0, "Result / outcome")
