"""
Doctor Management and Status Roster Module - Modern Behance / Dribbble Healthcare UI.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from src.config import THEME
from src.widgets.ui_kit import HeroMetricCard, PillButton, RoundedCard
from src.models.doctor import (
    get_all_doctors, create_doctor, update_doctor, 
    toggle_doctor_status, delete_doctor, get_doctor_by_id
)


class DoctorView(tk.Frame):
    """Physician Roster, Specialization and Real-time Availability Management."""

    def __init__(self, parent):
        super().__init__(parent, bg=THEME["background"])
        self.selected_doctor_id = None
        self._build_ui()
        self.load_doctors()

    def _build_ui(self):
        container = tk.Frame(self, bg=THEME["background"], padx=4, pady=2)
        container.pack(fill=tk.BOTH, expand=True)

        # 0. Doctor Operations Dashboard KPI Strip
        kpi_strip = tk.Frame(container, bg=THEME["background"])
        kpi_strip.pack(fill=tk.X, pady=(0, 10))

        self.kpi_doctor_cards = {}
        self.kpi_doctor_cards["total"] = HeroMetricCard(
            kpi_strip, title="Medical Faculty", value="0 Doctors",
            sub="Certified Clinical Specialists", icon="👨‍⚕️", bg_color="#2563EB"
        )
        self.kpi_doctor_cards["total"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.kpi_doctor_cards["avail"] = HeroMetricCard(
            kpi_strip, title="Active On Duty", value="0 On Duty",
            sub="Ready for Patient Consultations", icon="🟢", bg_color="#059669"
        )
        self.kpi_doctor_cards["avail"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.kpi_doctor_cards["surgery"] = HeroMetricCard(
            kpi_strip, title="In Procedure / OT", value="0 Active",
            sub="Operating Theaters Active", icon="🏥", bg_color="#7C3AED"
        )
        self.kpi_doctor_cards["surgery"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.kpi_doctor_cards["fee"] = HeroMetricCard(
            kpi_strip, title="Avg Consultation Fee", value="₹0.00",
            sub="Standard OPD Tariff", icon="💰", bg_color="#E11D48"
        )
        self.kpi_doctor_cards["fee"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # 1. Main Table Floating Rounded Card
        main_card = RoundedCard(
            container, bg_color="#FFFFFF", border_color="#E2E8F0",
            radius=16, pad_shadow=6, padx=16, pady=14
        )
        main_card.pack(fill=tk.BOTH, expand=True)
        card = main_card.inner

        # 1a. Header filter row
        top_strip = tk.Frame(card, bg="white")
        top_strip.pack(fill=tk.X, pady=(0, 14))

        tk.Label(top_strip, text="Filter by Status:", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(side=tk.LEFT, padx=(0, 8))

        self.cmb_filter = ttk.Combobox(top_strip, values=["All", "Available", "On Leave", "In Surgery", "Inactive"], state="readonly", width=15)
        self.cmb_filter.set("All")
        self.cmb_filter.pack(side=tk.LEFT, padx=(0, 10))
        self.cmb_filter.bind("<<ComboboxSelected>>", lambda e: self.load_doctors())

        btn_refresh = PillButton(
            top_strip, text="🔄 Refresh Roster", font_size=8,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=10, pady=4, command=self.load_doctors
        )
        btn_refresh.pack(side=tk.LEFT)

        btn_add = PillButton(
            top_strip, text="➕ Onboard New Doctor", font_size=9,
            bg_color=THEME["primary"], fg_color="white", hover_color=THEME["primary_dark"],
            padx=14, pady=6, command=self.open_add_doctor_modal
        )
        btn_add.pack(side=tk.RIGHT)

        # Main Doctor Grid
        table_frame = tk.Frame(card, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "code", "name", "specialization", "phone", "room", "fee", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("code", text="Doctor Code")
        self.tree.heading("name", text="Doctor Name")
        self.tree.heading("specialization", text="Specialization")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("room", text="Room / OPD")
        self.tree.heading("fee", text="Fee (₹)")
        self.tree.heading("status", text="Availability Status")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("code", width=95, anchor=tk.CENTER)
        self.tree.column("name", width=170, anchor=tk.W)
        self.tree.column("specialization", width=140, anchor=tk.W)
        self.tree.column("phone", width=110, anchor=tk.CENTER)
        self.tree.column("room", width=95, anchor=tk.CENTER)
        self.tree.column("fee", width=85, anchor=tk.E)
        self.tree.column("status", width=110, anchor=tk.CENTER)

        self.tree.tag_configure("Available", background="#ECFDF5", foreground="#047857")
        self.tree.tag_configure("On Leave", background="#FEF3C7", foreground="#B45309")
        self.tree.tag_configure("In Surgery", background="#FEF2F2", foreground="#B91C1C")
        self.tree.tag_configure("Inactive", background="#F1F5F9", foreground="#64748B")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_doctor_selected)

        # Action Toolbar with color status pills
        action_bar = tk.Frame(card, bg="white", pady=12)
        action_bar.pack(fill=tk.X)

        self.btn_edit = PillButton(
            action_bar, text="✏️ Edit Doctor", font_size=8,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=12, pady=5, state=tk.DISABLED, command=self.open_edit_doctor_modal
        )
        self.btn_edit.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_avail = PillButton(
            action_bar, text="🟢 Set Available", font_size=8,
            bg_color="#ECFDF5", fg_color="#047857", hover_color="#D1FAE5",
            padx=10, pady=5, state=tk.DISABLED, command=lambda: self._set_status("Available")
        )
        self.btn_avail.pack(side=tk.LEFT, padx=4)

        self.btn_leave = PillButton(
            action_bar, text="🟠 Set On Leave", font_size=8,
            bg_color="#FEF3C7", fg_color="#B45309", hover_color="#FDE68A",
            padx=10, pady=5, state=tk.DISABLED, command=lambda: self._set_status("On Leave")
        )
        self.btn_leave.pack(side=tk.LEFT, padx=4)

        self.btn_surgery = PillButton(
            action_bar, text="🔴 Set In Surgery", font_size=8,
            bg_color="#FEF2F2", fg_color=THEME["danger"], hover_color="#FEE2E2",
            padx=10, pady=5, state=tk.DISABLED, command=lambda: self._set_status("In Surgery")
        )
        self.btn_surgery.pack(side=tk.LEFT, padx=4)

        self.btn_delete = PillButton(
            action_bar, text="🗑️ Delete", font_size=8,
            bg_color="#FEF2F2", fg_color=THEME["danger"], hover_color="#FEE2E2",
            padx=12, pady=5, state=tk.DISABLED, command=self.delete_selected_doctor
        )
        self.btn_delete.pack(side=tk.RIGHT)

    def load_doctors(self):
        status_filter = self.cmb_filter.get()
        doctors = get_all_doctors(status_filter=status_filter)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for d in doctors:
            self.tree.insert("", tk.END, values=(
                d["id"], d["doctor_code"], d["full_name"], d["specialization"],
                d["phone"], d["room_no"], f"₹{d['consultation_fee']:.2f}", d["status"]
            ), tags=(d["status"],))

        if hasattr(self, "kpi_doctor_cards"):
            all_docs = get_all_doctors()
            total_cnt = len(all_docs)
            avail_cnt = sum(1 for doc in all_docs if doc["status"] == "Available")
            surg_cnt = sum(1 for doc in all_docs if doc["status"] == "In Surgery")
            avg_fee = sum(doc["consultation_fee"] for doc in all_docs) / total_cnt if total_cnt > 0 else 0.0

            self.kpi_doctor_cards["total"].config(text=f"{total_cnt} Doctors")
            self.kpi_doctor_cards["avail"].config(text=f"{avail_cnt} On Duty")
            self.kpi_doctor_cards["surgery"].config(text=f"{surg_cnt} In Surgery")
            self.kpi_doctor_cards["fee"].config(text=f"₹{avg_fee:.0f}")

        self._on_doctor_selected()

    def _on_doctor_selected(self, event=None):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.selected_doctor_id = item["values"][0]
            self.btn_edit.config(state=tk.NORMAL)
            self.btn_avail.config(state=tk.NORMAL)
            self.btn_leave.config(state=tk.NORMAL)
            self.btn_surgery.config(state=tk.NORMAL)
            self.btn_delete.config(state=tk.NORMAL)
        else:
            self.selected_doctor_id = None
            self.btn_edit.config(state=tk.DISABLED)
            self.btn_avail.config(state=tk.DISABLED)
            self.btn_leave.config(state=tk.DISABLED)
            self.btn_surgery.config(state=tk.DISABLED)
            self.btn_delete.config(state=tk.DISABLED)

    def _set_status(self, new_status: str):
        if self.selected_doctor_id:
            toggle_doctor_status(self.selected_doctor_id, new_status)
            self.load_doctors()

    def open_add_doctor_modal(self):
        DoctorFormModal(self, title="Onboard New Doctor", on_saved=self.load_doctors)

    def open_edit_doctor_modal(self):
        if not self.selected_doctor_id:
            return
        doc = get_doctor_by_id(self.selected_doctor_id)
        if doc:
            DoctorFormModal(self, title="Edit Doctor Profile", doctor_data=doc, on_saved=self.load_doctors)

    def delete_selected_doctor(self):
        if not self.selected_doctor_id:
            return
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this doctor?")
        if confirm:
            try:
                delete_doctor(self.selected_doctor_id)
                self.load_doctors()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete doctor: {e}")


class DoctorFormModal(tk.Toplevel):
    """Modal Form for Doctor Creation and Profile Editing."""

    def __init__(self, parent, title: str, doctor_data: Optional[dict] = None, on_saved: Optional[Callable] = None):
        super().__init__(parent)
        self.title(title)
        self.geometry("450x520")
        self.resizable(False, False)
        self.configure(bg="white")
        self.grab_set()
        self.doctor_data = doctor_data
        self.on_saved = on_saved

        self._build_form()

    def _build_form(self):
        form_frame = tk.Frame(self, bg="white", padx=25, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="Doctor Profile Information", font=("Segoe UI", 12, "bold"), fg=THEME["primary"], bg="white").pack(anchor=tk.W, pady=(0, 15))

        tk.Label(form_frame, text="Doctor Code (e.g. DOC-106) *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_code = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_code.pack(fill=tk.X, pady=(2, 8), ipady=3)

        tk.Label(form_frame, text="Full Name *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_name = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_name.pack(fill=tk.X, pady=(2, 8), ipady=3)

        tk.Label(form_frame, text="Specialization *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.cmb_spec = ttk.Combobox(form_frame, values=[
            "Cardiology", "Pediatrics", "Orthopedics", "General Medicine", 
            "Neurology", "Dermatology", "ENT", "Gynecology", "Ophthalmology"
        ])
        self.cmb_spec.set("General Medicine")
        self.cmb_spec.pack(fill=tk.X, pady=(2, 8))

        tk.Label(form_frame, text="Phone Number *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_phone = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_phone.pack(fill=tk.X, pady=(2, 8), ipady=3)

        tk.Label(form_frame, text="Email Address", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_email = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_email.pack(fill=tk.X, pady=(2, 8), ipady=3)

        # Room & Fee Row
        row1 = tk.Frame(form_frame, bg="white")
        row1.pack(fill=tk.X, pady=(2, 8))

        col_room = tk.Frame(row1, bg="white")
        col_room.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(col_room, text="Room / OPD No *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_room = tk.Entry(col_room, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_room.pack(fill=tk.X, pady=2, ipady=3)

        col_fee = tk.Frame(row1, bg="white")
        col_fee.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(col_fee, text="Fee (₹) *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_fee = tk.Entry(col_fee, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_fee.insert(0, "500.0")
        self.txt_fee.pack(fill=tk.X, pady=2, ipady=3)

        tk.Label(form_frame, text="Initial Status", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.cmb_status = ttk.Combobox(form_frame, values=["Available", "On Leave", "In Surgery", "Inactive"], state="readonly")
        self.cmb_status.set("Available")
        self.cmb_status.pack(fill=tk.X, pady=(2, 15))

        if self.doctor_data:
            self.txt_code.insert(0, self.doctor_data.get("doctor_code", ""))
            self.txt_code.config(state="disabled")
            self.txt_name.insert(0, self.doctor_data.get("full_name", ""))
            self.cmb_spec.set(self.doctor_data.get("specialization", "General Medicine"))
            self.txt_phone.insert(0, self.doctor_data.get("phone", ""))
            self.txt_email.insert(0, self.doctor_data.get("email", ""))
            self.txt_room.insert(0, self.doctor_data.get("room_no", ""))
            self.txt_fee.delete(0, tk.END)
            self.txt_fee.insert(0, str(self.doctor_data.get("consultation_fee", 500.0)))
            self.cmb_status.set(self.doctor_data.get("status", "Available"))

        btn_frame = tk.Frame(form_frame, bg="white", pady=10)
        btn_frame.pack(fill=tk.X)

        btn_save = PillButton(
            btn_frame, text="💾 Save Doctor", font_size=9,
            bg_color=THEME["primary"], fg_color="white", hover_color=THEME["primary_dark"],
            padx=16, pady=7, command=self.save_doctor
        )
        btn_save.pack(side=tk.RIGHT, padx=5)

        btn_cancel = PillButton(
            btn_frame, text="Cancel", font_size=9,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=12, pady=7, command=self.destroy
        )
        btn_cancel.pack(side=tk.RIGHT, padx=5)

    def save_doctor(self):
        code = self.txt_code.get().strip()
        name = self.txt_name.get().strip()
        spec = self.cmb_spec.get().strip()
        phone = self.txt_phone.get().strip()
        email = self.txt_email.get().strip()
        room = self.txt_room.get().strip()
        status = self.cmb_status.get()

        try:
            fee = float(self.txt_fee.get().strip())
        except ValueError:
            messagebox.showerror("Validation Error", "Fee must be a valid number.")
            return

        try:
            if self.doctor_data:
                update_doctor(self.doctor_data["id"], name, spec, phone, email, room, fee, status)
                messagebox.showinfo("Success", f"Doctor {name} updated.")
            else:
                create_doctor(code, name, spec, phone, email, room, fee, status)
                messagebox.showinfo("Success", f"Doctor {name} added to roster.")

            if self.on_saved:
                self.on_saved()
            self.destroy()

        except Exception as ex:
            messagebox.showerror("Error", f"Failed to save doctor: {ex}")
