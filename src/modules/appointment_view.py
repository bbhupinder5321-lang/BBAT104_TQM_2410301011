"""
Appointment Scheduling, OPD Queue Sequencing, and Wait-Time Telemetry View.
Modern Behance / Dribbble Healthcare UI.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from datetime import date, datetime
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from src.config import THEME
from src.widgets.ui_kit import HeroMetricCard, PillButton, RoundedCard
from src.models.appointment import (
    get_appointments_list, book_appointment, check_in_patient, 
    start_consultation, complete_consultation, cancel_appointment, get_waiting_time_kpi
)
from src.models.doctor import get_all_doctors
from src.models.patient import fast_search_patients


class AppointmentView(tk.Frame):
    """
    OPD Queue Sequencing & Wait-Time Telemetry Interface.
    Directly addresses Core TQM Goal: Reduce Patient Waiting Time.
    """

    def __init__(self, parent, on_open_billing: Optional[Callable] = None):
        super().__init__(parent, bg=THEME["background"])
        self.on_open_billing = on_open_billing
        self.selected_appointment_id = None

        self._build_ui()
        self.load_appointments()

    def _build_ui(self):
        container = tk.Frame(self, bg=THEME["background"], padx=4, pady=2)
        container.pack(fill=tk.BOTH, expand=True)

        # 0. OPD Queue Dashboard KPI Metric Strip
        kpi_strip = tk.Frame(container, bg=THEME["background"])
        kpi_strip.pack(fill=tk.X, pady=(0, 10))

        self.kpi_appt_cards = {}
        self.kpi_appt_cards["total"] = HeroMetricCard(
            kpi_strip, title="Today's Bookings", value="0 Tokens",
            sub="Active Clinical Roster", icon="📅", bg_color="#0EA5E9"
        )
        self.kpi_appt_cards["total"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))

        self.kpi_appt_cards["waiting"] = HeroMetricCard(
            kpi_strip, title="Waiting Lounge", value="0 Patients",
            sub="Queue In-Service", icon="⏳", bg_color="#F97316"
        )
        self.kpi_appt_cards["waiting"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        self.kpi_appt_cards["consult"] = HeroMetricCard(
            kpi_strip, title="In-Consultation", value="0 Active",
            sub="Attending Physicians", icon="🩺", bg_color="#84CC16"
        )
        self.kpi_appt_cards["consult"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        self.kpi_appt_cards["wait_avg"] = HeroMetricCard(
            kpi_strip, title="Average Wait Time", value="0.0 min",
            sub="TQM Target < 15.0m (Q02)", icon="⏱️", bg_color="#EF4444"
        )
        self.kpi_appt_cards["wait_avg"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 0))

        # 1. Main Table Container Card
        card = tk.Frame(
            container, bg="#FFFFFF", highlightthickness=1, highlightbackground="#E2E8F0",
            padx=18, pady=16
        )
        card.pack(fill=tk.BOTH, expand=True)

        # 1a. Header Filter Bar & Wait-Time KPI Summary
        top_strip = tk.Frame(card, bg="white")
        top_strip.pack(fill=tk.X, pady=(0, 14))

        tk.Label(top_strip, text="Filter Date:", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(side=tk.LEFT, padx=(0, 6))

        self.txt_date_filter = tk.Entry(top_strip, font=("Segoe UI", 9), bg="#F8FAFC", relief="solid", bd=1, width=12)
        self.txt_date_filter.insert(0, date.today().isoformat())
        self.txt_date_filter.pack(side=tk.LEFT, padx=(0, 6), ipady=2)

        btn_today = PillButton(
            top_strip, text="Today", font_size=8,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=10, pady=4, command=self._set_today
        )
        btn_today.pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(top_strip, text="Status:", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(side=tk.LEFT, padx=(0, 6))

        self.cmb_status_filter = ttk.Combobox(
            top_strip, 
            values=["All", "Scheduled", "Waiting", "In-Consultation", "Completed", "Cancelled"], 
            state="readonly", width=14
        )
        self.cmb_status_filter.set("All")
        self.cmb_status_filter.pack(side=tk.LEFT, padx=(0, 10))

        btn_filter = PillButton(
            top_strip, text="🔍 Filter", font_size=8,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=10, pady=4, command=self.load_appointments
        )
        btn_filter.pack(side=tk.LEFT)

        # Live Wait-Time Metric Display
        self.lbl_wait_kpi = tk.Label(
            top_strip, 
            text="⏱️ Avg Wait: -- min | Completed: 0", 
            font=("Segoe UI", 9, "bold"),
            bg="#DDF2FD", fg="#0284C7",
            padx=12, pady=5, relief="flat"
        )
        self.lbl_wait_kpi.pack(side=tk.LEFT, padx=15)

        btn_book = PillButton(
            top_strip, text="🎟️ Book Token / Slot", font_size=9,
            bg_color="#003E5C", fg_color="white", hover_color="#002D42",
            padx=14, pady=6, command=self.open_booking_modal
        )
        btn_book.pack(side=tk.RIGHT)

        # 2. Appointments TreeView Table
        table_frame = tk.Frame(card, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "appt_num", "token", "patient", "doctor", "date", "time", "status", "wait_min")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("appt_num", text="Appt #")
        self.tree.heading("token", text="Token #")
        self.tree.heading("patient", text="Patient (UHID)")
        self.tree.heading("doctor", text="Doctor (Room)")
        self.tree.heading("date", text="Date")
        self.tree.heading("time", text="Time")
        self.tree.heading("status", text="Queue Status")
        self.tree.heading("wait_min", text="Wait Time (min)")

        self.tree.column("id", width=35, anchor=tk.CENTER)
        self.tree.column("appt_num", width=120, anchor=tk.CENTER)
        self.tree.column("token", width=70, anchor=tk.CENTER)
        self.tree.column("patient", width=190, anchor=tk.W)
        self.tree.column("doctor", width=165, anchor=tk.W)
        self.tree.column("date", width=85, anchor=tk.CENTER)
        self.tree.column("time", width=75, anchor=tk.CENTER)
        self.tree.column("status", width=110, anchor=tk.CENTER)
        self.tree.column("wait_min", width=95, anchor=tk.CENTER)

        self.tree.tag_configure("Waiting", background="#FFFBEB", foreground="#B45309")
        self.tree.tag_configure("Scheduled", background="#EFF6FF", foreground="#1D4ED8")
        self.tree.tag_configure("In-Consultation", background="#F5F3FF", foreground="#7C3AED")
        self.tree.tag_configure("Completed", background="#ECFDF5", foreground="#047857")
        self.tree.tag_configure("Cancelled", background="#FEF2F2", foreground="#B91C1C")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_appt_selected)

        # 3. Queue Lifecycle Toolbar
        action_bar = tk.Frame(card, bg="white", pady=12)
        action_bar.pack(fill=tk.X)

        self.btn_checkin = PillButton(
            action_bar, text="📥 1. Patient Check-In", font_size=9,
            bg_color="#EFF6FF", fg_color="#1D4ED8", hover_color="#DBEAFE",
            padx=12, pady=6, state=tk.DISABLED, command=self._action_checkin
        )
        self.btn_checkin.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_call = PillButton(
            action_bar, text="🩺 2. Call into Consultation", font_size=9,
            bg_color="#FEF3C7", fg_color="#B45309", hover_color="#FDE68A",
            padx=12, pady=6, state=tk.DISABLED, command=self._action_call
        )
        self.btn_call.pack(side=tk.LEFT, padx=6)

        self.btn_complete = PillButton(
            action_bar, text="✅ 3. Complete & Bill", font_size=9,
            bg_color="#ECFDF5", fg_color="#047857", hover_color="#A7F3D0",
            padx=12, pady=6, state=tk.DISABLED, command=self._action_complete
        )
        self.btn_complete.pack(side=tk.LEFT, padx=6)

        self.btn_cancel = PillButton(
            action_bar, text="❌ Cancel Slot", font_size=9,
            bg_color="#FEF2F2", fg_color=THEME["danger"], hover_color="#FEE2E2",
            padx=12, pady=6, state=tk.DISABLED, command=self._action_cancel
        )
        self.btn_cancel.pack(side=tk.RIGHT)

    def _set_today(self):
        self.txt_date_filter.delete(0, tk.END)
        self.txt_date_filter.insert(0, date.today().isoformat())
        self.load_appointments()

    def load_appointments(self):
        target_date = self.txt_date_filter.get().strip() or None
        status = self.cmb_status_filter.get()
        appts = get_appointments_list(target_date=target_date, status=status)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for a in appts:
            patient_desc = f"{a['patient_name']} ({a['uhid']})"
            doc_desc = f"{a['doctor_name']} ({a['room_no']})"
            wait_str = f"{a['wait_time_minutes']:.1f} m" if a['wait_time_minutes'] > 0 else "-"

            self.tree.insert("", tk.END, values=(
                a["id"], a["appointment_number"], f"Token #{a['token_number']}",
                patient_desc, doc_desc, a["appointment_date"], a["appointment_time"],
                a["status"], wait_str
            ), tags=(a["status"],))

        kpi = get_waiting_time_kpi(target_date)
        self.lbl_wait_kpi.config(
            text=f"⏱️ Avg Wait: {kpi['avg_wait_min']} min | Max: {kpi['max_wait_min']} min | Completed: {kpi['total_completed']}"
        )

        if hasattr(self, "kpi_appt_cards"):
            waiting_cnt = sum(1 for a in appts if a["status"] == "Waiting")
            consult_cnt = sum(1 for a in appts if a["status"] == "In-Consultation")
            self.kpi_appt_cards["total"].config(text=f"{len(appts)} Bookings")
            self.kpi_appt_cards["waiting"].config(text=f"{waiting_cnt} Waiting")
            self.kpi_appt_cards["consult"].config(text=f"{consult_cnt} In-Consult")
            self.kpi_appt_cards["wait_avg"].config(text=f"{kpi['avg_wait_min']} min")

        self._on_appt_selected()

    def _on_appt_selected(self, event=None):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.selected_appointment_id = item["values"][0]
            status = item["values"][7]

            self.btn_checkin.config(state=tk.NORMAL if status == "Scheduled" else tk.DISABLED)
            self.btn_call.config(state=tk.NORMAL if status == "Waiting" else tk.DISABLED)
            self.btn_complete.config(state=tk.NORMAL if status == "In-Consultation" else tk.DISABLED)
            self.btn_cancel.config(state=tk.NORMAL if status in ("Scheduled", "Waiting") else tk.DISABLED)
        else:
            self.selected_appointment_id = None
            self.btn_checkin.config(state=tk.DISABLED)
            self.btn_call.config(state=tk.DISABLED)
            self.btn_complete.config(state=tk.DISABLED)
            self.btn_cancel.config(state=tk.DISABLED)

    def _action_checkin(self):
        if self.selected_appointment_id:
            check_in_patient(self.selected_appointment_id)
            self.load_appointments()

    def _action_call(self):
        if self.selected_appointment_id:
            start_consultation(self.selected_appointment_id)
            self.load_appointments()

    def _action_complete(self):
        if self.selected_appointment_id:
            complete_consultation(self.selected_appointment_id)
            self.load_appointments()
            if self.on_open_billing:
                confirm = messagebox.askyesno(
                    "Consultation Completed", 
                    "Consultation marked as completed!\nWould you like to open the Billing Desk for this patient now?"
                )
                if confirm:
                    self.on_open_billing(self.selected_appointment_id)

    def _action_cancel(self):
        if self.selected_appointment_id:
            confirm = messagebox.askyesno("Cancel Appointment", "Cancel this appointment slot?")
            if confirm:
                cancel_appointment(self.selected_appointment_id)
                self.load_appointments()

    def open_booking_modal(self, preselected_patient_id: Optional[int] = None):
        AppointmentBookingModal(self, preselected_patient_id=preselected_patient_id, on_saved=self.load_appointments)


class AppointmentBookingModal(tk.Toplevel):
    """Modal for Scheduling an Outpatient Appointment and Issuing Token."""

    def __init__(self, parent, preselected_patient_id: Optional[int] = None, on_saved: Optional[Callable] = None):
        super().__init__(parent)
        self.title("Book Outpatient Appointment / Issue Token")
        self.geometry("500x520")
        self.resizable(False, False)
        self.configure(bg="white")
        self.grab_set()
        self.preselected_patient_id = preselected_patient_id
        self.on_saved = on_saved
        self.patient_map = {}
        self.doctor_map = {}

        self._build_form()

    def _build_form(self):
        # 0. Modern Clinical Topbar
        topbar = tk.Frame(self, bg="#003E5C", padx=20, pady=12)
        topbar.pack(fill=tk.X)

        tk.Label(
            topbar, text="✚  OPD Appointment Booking & Token", font=("Segoe UI", 12, "bold"),
            fg="#FFFFFF", bg="#003E5C"
        ).pack(side=tk.LEFT)

        tk.Label(
            topbar, text="TQM OPD Queue Sequencing", font=("Segoe UI", 8, "bold"),
            fg="#38BDF8", bg="#003E5C"
        ).pack(side=tk.RIGHT)

        form_frame = tk.Frame(self, bg="white", padx=25, pady=16)
        form_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="Select Patient (Name / UHID) *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.cmb_patient = ttk.Combobox(form_frame, state="readonly", width=50)
        self._populate_patients()
        self.cmb_patient.pack(fill=tk.X, pady=(2, 10))

        tk.Label(form_frame, text="Select Attending Doctor *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.cmb_doctor = ttk.Combobox(form_frame, state="readonly", width=50)
        self._populate_doctors()
        self.cmb_doctor.pack(fill=tk.X, pady=(2, 10))

        # Date & Time Row
        row1 = tk.Frame(form_frame, bg="white")
        row1.pack(fill=tk.X, pady=(2, 10))

        col_date = tk.Frame(row1, bg="white")
        col_date.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(col_date, text="Appointment Date (YYYY-MM-DD) *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_date = tk.Entry(col_date, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_date.insert(0, date.today().isoformat())
        self.txt_date.pack(fill=tk.X, pady=2, ipady=3)

        col_time = tk.Frame(row1, bg="white")
        col_time.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(col_time, text="Time Slot *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.cmb_time = ttk.Combobox(col_time, values=[
            "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM",
            "12:00 PM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM", "04:00 PM"
        ], state="readonly")
        self.cmb_time.set("09:30 AM")
        self.cmb_time.pack(fill=tk.X, pady=2)

        tk.Label(form_frame, text="Symptoms / Clinical Notes", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_notes = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_notes.insert(0, "Routine OPD Consultation")
        self.txt_notes.pack(fill=tk.X, pady=(2, 12), ipady=3)

        self.lbl_token_preview = tk.Label(
            form_frame, text="ℹ️ Sequential OPD daily token will be automatically assigned.", 
            font=("Segoe UI", 8), fg="#64748B", bg="white"
        )
        self.lbl_token_preview.pack(anchor=tk.W, pady=(0, 15))

        btn_frame = tk.Frame(form_frame, bg="white", pady=10)
        btn_frame.pack(fill=tk.X)

        btn_confirm = PillButton(
            btn_frame, text="🎟️ Confirm Booking & Issue Token", font_size=9,
            bg_color="#003E5C", fg_color="white", hover_color="#002D42",
            padx=16, pady=7, command=self.save_booking
        )
        btn_confirm.pack(side=tk.RIGHT, padx=5)

        btn_cancel = PillButton(
            btn_frame, text="Cancel", font_size=9,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=12, pady=7, command=self.destroy
        )
        btn_cancel.pack(side=tk.RIGHT, padx=5)

    def _populate_patients(self):
        patients, _ = fast_search_patients("", limit=200)
        options = []
        selected_idx = 0
        for idx, p in enumerate(patients):
            label = f"{p['full_name']} | {p['uhid']} | {p['phone']}"
            self.patient_map[label] = p["id"]
            options.append(label)
            if self.preselected_patient_id == p["id"]:
                selected_idx = idx

        self.cmb_patient["values"] = options
        if options:
            self.cmb_patient.current(selected_idx)

    def _populate_doctors(self):
        doctors = get_all_doctors(status_filter="Available")
        options = []
        for d in doctors:
            label = f"{d['full_name']} ({d['specialization']} - {d['room_no']} - ₹{d['consultation_fee']})"
            self.doctor_map[label] = d["id"]
            options.append(label)

        self.cmb_doctor["values"] = options
        if options:
            self.cmb_doctor.current(0)

    def save_booking(self):
        patient_str = self.cmb_patient.get()
        doc_str = self.cmb_doctor.get()
        appt_date = self.txt_date.get().strip()
        appt_time = self.cmb_time.get()
        notes = self.txt_notes.get().strip()

        if not patient_str or not doc_str or not appt_date:
            messagebox.showerror("Error", "Please fill all required appointment fields.")
            return

        patient_id = self.patient_map.get(patient_str)
        doctor_id = self.doctor_map.get(doc_str)

        try:
            appt_id, appt_num, token_num = book_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=appt_date,
                appointment_time=appt_time,
                notes=notes
            )
            messagebox.showinfo(
                "Appointment Confirmed!", 
                f"Appointment Successfully Scheduled!\n\n"
                f"• Appointment Number: {appt_num}\n"
                f"• Assigned Token: Token #{token_num}\n"
                f"• Date: {appt_date} at {appt_time}"
            )
            if self.on_saved:
                self.on_saved()
            self.destroy()

        except Exception as ex:
            messagebox.showerror("Error", f"Failed to book appointment: {ex}")
