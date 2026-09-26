"""
Patient Management Module with Q02 Fast Search & Poka-Yoke Duplicate Prevention.
Modern Behance / Dribbble Healthcare UI.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from src.config import THEME, SLA_TARGETS
from src.widgets.ui_kit import HeroMetricCard, PillButton, ModernCard
from src.models.patient import (
    fast_search_patients, create_patient, update_patient, 
    delete_patient, check_duplicate_phone, get_patient_by_id
)


class PatientView(tk.Frame):
    """
    Polished Patient Management UI:
    - Q02 Feature 1: Debounced Fast Search-as-you-type (< 100ms) with search icon
    - TQM Poka-Yoke: Live phone collision detection modal and inline warnings
    - Crisp white card presentation
    """

    def __init__(self, parent, on_schedule_appointment: Optional[Callable] = None):
        super().__init__(parent, bg=THEME["background"])
        self.on_schedule_appointment = on_schedule_appointment
        self.debounce_job = None
        self.selected_patient_id = None

        self._build_ui()
        self.load_patients()

    def _build_ui(self):
        # Main Outer White Card
        card = tk.Frame(self, bg="white", highlightthickness=1, highlightbackground=THEME["border"], padx=20, pady=18)
        card.pack(fill=tk.BOTH, expand=True)

        # 0. Dashboard KPI Metric Cards Strip
        kpi_strip = tk.Frame(card, bg="white")
        kpi_strip.pack(fill=tk.X, pady=(0, 16))

        self.kpi_patient_cards = {}
        self.kpi_patient_cards["total"] = HeroMetricCard(
            kpi_strip, title="Registered Patients", value="0 Patients",
            sub="● Active Records", icon="👥", bg_color="#0D9488"
        )
        self.kpi_patient_cards["total"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))

        self.kpi_patient_cards["latency"] = HeroMetricCard(
            kpi_strip, title="Fast Search Speed", value="< 5 ms",
            sub="● SLA: < 100ms (B-Tree)", icon="⚡", bg_color="#0284C7"
        )
        self.kpi_patient_cards["latency"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        self.kpi_patient_cards["pokayoke"] = HeroMetricCard(
            kpi_strip, title="Poka-Yoke Protection", value="100% Protected",
            sub="● Unique Phone & UHID", icon="🛡️", bg_color="#7C3AED"
        )
        self.kpi_patient_cards["pokayoke"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        self.kpi_patient_cards["blood"] = HeroMetricCard(
            kpi_strip, title="Top Blood Group", value="O+ Rh+",
            sub="● Predominant Donor Type", icon="🩸", bg_color="#E11D48"
        )
        self.kpi_patient_cards["blood"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 0))

        # 1. Top Search and Action Strip
        top_strip = tk.Frame(card, bg="white")
        top_strip.pack(fill=tk.X, pady=(0, 15))

        # Search Bar with pill icon
        search_box = tk.Frame(top_strip, bg="#F8FAFC", highlightthickness=1, highlightbackground="#CBD5E1", padx=10, pady=5)
        search_box.pack(side=tk.LEFT)

        tk.Label(search_box, text="🔍", font=("Segoe UI", 10), bg="#F8FAFC", fg="#64748B").pack(side=tk.LEFT, padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_box, textvariable=self.search_var, font=("Segoe UI", 10),
            bg="#F8FAFC", relief="flat", bd=0, width=35
        )
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind("<KeyRelease>", self._on_search_keyrelease)

        btn_clear = tk.Button(
            search_box, text="✕", font=("Segoe UI", 8), bg="#F8FAFC", fg="#94A3B8",
            relief="flat", cursor="hand2", command=self.clear_search
        )
        btn_clear.pack(side=tk.LEFT, padx=(5, 0))

        # Live SLA Latency Badge Pill
        self.lbl_latency = tk.Label(
            top_strip, 
            text="⚡ Search Latency: -- ms | SLA: < 100ms", 
            font=("Segoe UI", 9, "bold"),
            bg=THEME["primary_light"], fg=THEME["primary"],
            padx=12, pady=5, relief="flat"
        )
        self.lbl_latency.pack(side=tk.LEFT, padx=15)

        # Register New Patient Button (Primary Brand Action)
        btn_add = PillButton(
            top_strip, text="➕ Register New Patient", font_size=9,
            bg_color=THEME["primary"], fg_color="white", hover_color=THEME["primary_dark"],
            padx=14, pady=6, command=self.open_add_patient_modal
        )
        btn_add.pack(side=tk.RIGHT)

        # 2. Main Patient Data Table (TreeView)
        table_frame = tk.Frame(card, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "uhid", "name", "gender", "age", "phone", "blood_group", "created_at")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("uhid", text="UHID")
        self.tree.heading("name", text="Patient Full Name")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("age", text="Age")
        self.tree.heading("phone", text="Phone (Unique Poka-Yoke)")
        self.tree.heading("blood_group", text="Blood Group")
        self.tree.heading("created_at", text="Registered Date")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("uhid", width=120, anchor=tk.CENTER)
        self.tree.column("name", width=180, anchor=tk.W)
        self.tree.column("gender", width=70, anchor=tk.CENTER)
        self.tree.column("age", width=50, anchor=tk.CENTER)
        self.tree.column("phone", width=120, anchor=tk.CENTER)
        self.tree.column("blood_group", width=90, anchor=tk.CENTER)
        self.tree.column("created_at", width=140, anchor=tk.CENTER)

        self.tree.tag_configure("evenrow", background="#FFFFFF")
        self.tree.tag_configure("oddrow", background="#F8FAFC")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_patient_selected)

        # 3. Bottom Action Toolbar
        action_bar = tk.Frame(card, bg="white", pady=12)
        action_bar.pack(fill=tk.X)

        self.btn_edit = PillButton(
            action_bar, text="✏️ Edit Profile", font_size=9,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=12, pady=6, state=tk.DISABLED, command=self.open_edit_patient_modal
        )
        self.btn_edit.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_delete = PillButton(
            action_bar, text="🗑️ Delete Patient", font_size=9,
            bg_color="#FEF2F2", fg_color=THEME["danger"], hover_color="#FEE2E2",
            padx=12, pady=6, state=tk.DISABLED, command=self.delete_selected_patient
        )
        self.btn_delete.pack(side=tk.LEFT, padx=6)

        if self.on_schedule_appointment:
            self.btn_book = PillButton(
                action_bar, text="🎟️ Issue Token / Book Appointment →", font_size=9,
                bg_color="#ECFDF5", fg_color="#047857", hover_color="#D1FAE5",
                padx=14, pady=6, state=tk.DISABLED, command=self._book_for_selected
            )
            self.btn_book.pack(side=tk.RIGHT)

    def _on_search_keyrelease(self, event=None):
        if self.debounce_job:
            self.after_cancel(self.debounce_job)
        self.debounce_job = self.after(200, self.load_patients)

    def clear_search(self):
        self.search_var.set("")
        self.load_patients()

    def load_patients(self):
        query_str = self.search_var.get()
        records, latency_ms = fast_search_patients(query_str, limit=100)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, p in enumerate(records):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=(
                p["id"], p["uhid"], p["full_name"], p["gender"], 
                p["age"], p["phone"], p["blood_group"], p["created_at"]
            ), tags=(tag,))

        sla_pass = latency_ms <= SLA_TARGETS["SEARCH_MAX_MS"]
        status_txt = "PASSED" if sla_pass else "BREACHED"
        bg_col = THEME["success_light"] if sla_pass else THEME["danger_light"]
        fg_col = "#047857" if sla_pass else THEME["danger"]

        self.lbl_latency.config(
            text=f"⚡ Fast Search Latency: {latency_ms:.2f} ms ({len(records)} found) | SLA: {status_txt} (< 100ms)",
            bg=bg_col, fg=fg_col
        )

        if hasattr(self, "kpi_patient_cards"):
            self.kpi_patient_cards["total"].config(text=f"{len(records)} Patients")
            self.kpi_patient_cards["latency"].config(text=f"{latency_ms:.1f} ms")
            self.kpi_patient_cards["pokayoke"].config(text="100% Protected")
            b_groups = [p["blood_group"] for p in records if p.get("blood_group")]
            top_bg = max(set(b_groups), key=b_groups.count) if b_groups else "O+"
            self.kpi_patient_cards["blood"].config(text=f"{top_bg}")

        self._on_patient_selected()

    def _on_patient_selected(self, event=None):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.selected_patient_id = item["values"][0]
            self.btn_edit.config(state=tk.NORMAL)
            self.btn_delete.config(state=tk.NORMAL)
            if hasattr(self, "btn_book"):
                self.btn_book.config(state=tk.NORMAL)
        else:
            self.selected_patient_id = None
            self.btn_edit.config(state=tk.DISABLED)
            self.btn_delete.config(state=tk.DISABLED)
            if hasattr(self, "btn_book"):
                self.btn_book.config(state=tk.DISABLED)

    def _book_for_selected(self):
        if self.selected_patient_id and self.on_schedule_appointment:
            self.on_schedule_appointment(self.selected_patient_id)

    def open_add_patient_modal(self):
        PatientFormModal(self, title="Register New Patient (Poka-Yoke Protected)", on_saved=self.load_patients)

    def open_edit_patient_modal(self):
        if not self.selected_patient_id:
            return
        patient = get_patient_by_id(self.selected_patient_id)
        if patient:
            PatientFormModal(self, title="Edit Patient Profile", patient_data=patient, on_saved=self.load_patients)

    def delete_selected_patient(self):
        if not self.selected_patient_id:
            return
        confirm = messagebox.askyesno(
            "Confirm Deletion", 
            "Are you sure you want to delete this patient record?\nThis will cascade delete linked appointments.",
            icon="warning"
        )
        if confirm:
            try:
                delete_patient(self.selected_patient_id)
                self.load_patients()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete patient: {e}")


class PatientFormModal(tk.Toplevel):
    """Modern Modal Form for Patient Registration with real-time Poka-Yoke."""

    def __init__(self, parent, title: str, patient_data: Optional[dict] = None, on_saved: Optional[Callable] = None):
        super().__init__(parent)
        self.title(title)
        self.geometry("480x560")
        self.resizable(False, False)
        self.configure(bg="white")
        self.grab_set()
        self.patient_data = patient_data
        self.on_saved = on_saved

        self._build_form()

    def _build_form(self):
        container = tk.Frame(self, bg="white", padx=25, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(container, text="Patient Registration (TQM Poka-Yoke)", font=("Segoe UI", 13, "bold"), fg=THEME["primary"], bg="white").pack(anchor=tk.W, pady=(0, 15))

        # Full Name
        tk.Label(container, text="Full Name *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_name = tk.Entry(container, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_name.pack(fill=tk.X, pady=(2, 10), ipady=4)

        # Gender & Age Row
        row1 = tk.Frame(container, bg="white")
        row1.pack(fill=tk.X, pady=(2, 10))

        col_gender = tk.Frame(row1, bg="white")
        col_gender.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(col_gender, text="Gender *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.cmb_gender = ttk.Combobox(col_gender, values=["Male", "Female", "Other"], state="readonly")
        self.cmb_gender.set("Male")
        self.cmb_gender.pack(fill=tk.X, pady=2)

        col_age = tk.Frame(row1, bg="white")
        col_age.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(col_age, text="Age (0-125) *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_age = tk.Entry(col_age, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_age.insert(0, "30")
        self.txt_age.pack(fill=tk.X, pady=2, ipady=3)

        # Phone Number (Poka-Yoke duplicate validation)
        tk.Label(container, text="Mobile Phone (Unique Poka-Yoke) *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_phone = tk.Entry(container, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_phone.pack(fill=tk.X, pady=(2, 2), ipady=4)
        self.txt_phone.bind("<KeyRelease>", self._check_duplicate_live)

        self.lbl_poka_yoke = tk.Label(container, text="✓ Phone uniqueness check active", font=("Segoe UI", 8), fg="#64748B", bg="white")
        self.lbl_poka_yoke.pack(anchor=tk.W, pady=(0, 10))

        # Blood Group & Email Row
        row2 = tk.Frame(container, bg="white")
        row2.pack(fill=tk.X, pady=(2, 10))

        col_bg = tk.Frame(row2, bg="white")
        col_bg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(col_bg, text="Blood Group", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.cmb_blood = ttk.Combobox(col_bg, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"], state="readonly")
        self.cmb_blood.set("O+")
        self.cmb_blood.pack(fill=tk.X, pady=2)

        col_email = tk.Frame(row2, bg="white")
        col_email.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(col_email, text="Email Address", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_email = tk.Entry(col_email, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_email.pack(fill=tk.X, pady=2, ipady=3)

        # Address
        tk.Label(container, text="Residential Address", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_address = tk.Entry(container, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_address.pack(fill=tk.X, pady=(2, 15), ipady=4)

        if self.patient_data:
            self.txt_name.insert(0, self.patient_data.get("full_name", ""))
            self.cmb_gender.set(self.patient_data.get("gender", "Male"))
            self.txt_age.delete(0, tk.END)
            self.txt_age.insert(0, str(self.patient_data.get("age", 30)))
            self.txt_phone.insert(0, self.patient_data.get("phone", ""))
            self.txt_email.insert(0, self.patient_data.get("email", ""))
            self.cmb_blood.set(self.patient_data.get("blood_group", "Unknown"))
            self.txt_address.insert(0, self.patient_data.get("address", ""))

        # Buttons
        btn_frame = tk.Frame(container, bg="white", pady=10)
        btn_frame.pack(fill=tk.X)

        btn_save = PillButton(
            btn_frame, text="💾 Save Record", font_size=9,
            bg_color=THEME["primary"], fg_color="white", hover_color=THEME["primary_dark"],
            padx=16, pady=7, command=self.save_patient
        )
        btn_save.pack(side=tk.RIGHT, padx=5)

        btn_cancel = PillButton(
            btn_frame, text="Cancel", font_size=9,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=12, pady=7, command=self.destroy
        )
        btn_cancel.pack(side=tk.RIGHT, padx=5)

    def _check_duplicate_live(self, event=None):
        phone = self.txt_phone.get().strip()
        if len(phone) >= 7:
            exclude_id = self.patient_data["id"] if self.patient_data else None
            existing = check_duplicate_phone(phone, exclude_id=exclude_id)
            if existing:
                self.lbl_poka_yoke.config(
                    text=f"⚠️ DUPLICATE DETECTED! Already assigned to: {existing['full_name']} ({existing['uhid']})",
                    fg=THEME["danger"]
                )
            else:
                self.lbl_poka_yoke.config(
                    text="✓ Phone number is unique and valid",
                    fg=THEME["success"]
                )
        else:
            self.lbl_poka_yoke.config(
                text="ℹ️ Enter at least 7 digits for uniqueness verification",
                fg=THEME["text_muted"]
            )

    def save_patient(self):
        name = self.txt_name.get().strip()
        gender = self.cmb_gender.get()
        phone = self.txt_phone.get().strip()
        email = self.txt_email.get().strip()
        address = self.txt_address.get().strip()
        blood = self.cmb_blood.get()

        try:
            age = int(self.txt_age.get().strip())
        except ValueError:
            messagebox.showerror("Validation Error", "Age must be a valid integer.")
            return

        try:
            if self.patient_data:
                update_patient(self.patient_data["id"], name, gender, age, phone, email, address, blood)
                messagebox.showinfo("Success", f"Patient {name} updated.")
            else:
                p_id, uhid = create_patient(name, gender, age, phone, email, address, blood)
                messagebox.showinfo("Success", f"Patient registered successfully!\nAssigned UHID: {uhid}")

            if self.on_saved:
                self.on_saved()
            self.destroy()

        except ValueError as ve:
            messagebox.showwarning("TQM Poka-Yoke Alert", str(ve))
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to save patient: {ex}")
