"""
Billing and Invoicing Management View - Modern Behance / Dribbble Healthcare UI.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from src.config import THEME, EXPORTS_DIR
from src.widgets.ui_kit import HeroMetricCard, PillButton, RoundedCard
from src.models.billing import get_invoices, create_invoice, update_payment_status
from src.models.patient import fast_search_patients
import pandas as pd


class BillingView(tk.Frame):
    """Hospital Billing, Invoicing, and Payment Settlement Desk."""

    def __init__(self, parent):
        super().__init__(parent, bg=THEME["background"])
        self.selected_bill_id = None
        self._build_ui()
        self.load_invoices()

    def _build_ui(self):
        container = tk.Frame(self, bg=THEME["background"], padx=4, pady=2)
        container.pack(fill=tk.BOTH, expand=True)

        # 0. Financial Accounting Dashboard KPI Strip
        kpi_strip = tk.Frame(container, bg=THEME["background"])
        kpi_strip.pack(fill=tk.X, pady=(0, 10))

        self.kpi_billing_cards = {}
        self.kpi_billing_cards["settled"] = HeroMetricCard(
            kpi_strip, title="Settled Revenue", value="₹0.00",
            sub="Collected Revenue Funds", icon="💰", bg_color="#059669"
        )
        self.kpi_billing_cards["settled"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.kpi_billing_cards["pending"] = HeroMetricCard(
            kpi_strip, title="Pending Invoices", value="₹0.00",
            sub="Awaiting Patient Settlement", icon="⏳", bg_color="#F59E0B"
        )
        self.kpi_billing_cards["pending"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.kpi_billing_cards["invoices"] = HeroMetricCard(
            kpi_strip, title="Invoices Issued", value="0 Invoices",
            sub="Itemized Bills with 5% GST", icon="🧾", bg_color="#2563EB"
        )
        self.kpi_billing_cards["invoices"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.kpi_billing_cards["rate"] = HeroMetricCard(
            kpi_strip, title="Collection Rate", value="0.0%",
            sub="Settlement Clearance Ratio", icon="📈", bg_color="#7C3AED"
        )
        self.kpi_billing_cards["rate"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # 1. Main Table Floating Rounded Card
        main_card = RoundedCard(
            container, bg_color="#FFFFFF", border_color="#E2E8F0",
            radius=16, pad_shadow=6, padx=16, pady=14
        )
        main_card.pack(fill=tk.BOTH, expand=True)
        card = main_card.inner

        # 1a. Header and filter bar
        top_strip = tk.Frame(card, bg="white")
        top_strip.pack(fill=tk.X, pady=(0, 14))

        tk.Label(top_strip, text="Status Filter:", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(side=tk.LEFT, padx=(0, 6))

        self.cmb_filter = ttk.Combobox(top_strip, values=["All", "Paid", "Pending"], state="readonly", width=12)
        self.cmb_filter.set("All")
        self.cmb_filter.pack(side=tk.LEFT, padx=(0, 10))
        self.cmb_filter.bind("<<ComboboxSelected>>", lambda e: self.load_invoices())

        btn_refresh = PillButton(
            top_strip, text="🔄 Refresh", font_size=8,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=10, pady=4, command=self.load_invoices
        )
        btn_refresh.pack(side=tk.LEFT)

        # Revenue Total Badge Pill
        self.lbl_revenue = tk.Label(
            top_strip, 
            text="💰 Total Settled: ₹0.00 | Pending: ₹0.00", 
            font=("Segoe UI", 9, "bold"),
            bg=THEME["success_light"], fg="#047857",
            padx=12, pady=5, relief="flat"
        )
        self.lbl_revenue.pack(side=tk.LEFT, padx=15)

        btn_new_bill = PillButton(
            top_strip, text="🧾 Generate New Patient Bill", font_size=9,
            bg_color=THEME["primary"], fg_color="white", hover_color=THEME["primary_dark"],
            padx=14, pady=6, command=self.open_new_bill_modal
        )
        btn_new_bill.pack(side=tk.RIGHT)

        # Billing TreeView Table
        table_frame = tk.Frame(card, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "inv_num", "date", "patient", "consult", "med", "lab", "tax", "total", "mode", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("inv_num", text="Invoice #")
        self.tree.heading("date", text="Date")
        self.tree.heading("patient", text="Patient (UHID)")
        self.tree.heading("consult", text="Consultation (₹)")
        self.tree.heading("med", text="Medicine (₹)")
        self.tree.heading("lab", text="Lab (₹)")
        self.tree.heading("tax", text="GST 5% (₹)")
        self.tree.heading("total", text="Total (₹)")
        self.tree.heading("mode", text="Payment Mode")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=35, anchor=tk.CENTER)
        self.tree.column("inv_num", width=120, anchor=tk.CENTER)
        self.tree.column("date", width=85, anchor=tk.CENTER)
        self.tree.column("patient", width=180, anchor=tk.W)
        self.tree.column("consult", width=100, anchor=tk.E)
        self.tree.column("med", width=85, anchor=tk.E)
        self.tree.column("lab", width=75, anchor=tk.E)
        self.tree.column("tax", width=75, anchor=tk.E)
        self.tree.column("total", width=95, anchor=tk.E)
        self.tree.column("mode", width=100, anchor=tk.CENTER)
        self.tree.column("status", width=80, anchor=tk.CENTER)

        self.tree.tag_configure("Paid", background="#ECFDF5", foreground="#047857")
        self.tree.tag_configure("Pending", background="#FFFBEB", foreground="#B45309")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_bill_selected)

        # Action Toolbar
        action_bar = tk.Frame(card, bg="white", pady=12)
        action_bar.pack(fill=tk.X)

        self.btn_mark_paid = PillButton(
            action_bar, text="💰 Mark as Settled / Paid", font_size=9,
            bg_color="#ECFDF5", fg_color="#047857", hover_color="#D1FAE5",
            padx=12, pady=5, state=tk.DISABLED, command=self._action_mark_paid
        )
        self.btn_mark_paid.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_view_receipt = PillButton(
            action_bar, text="📄 View Receipt", font_size=9,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=12, pady=5, state=tk.DISABLED, command=self._action_view_receipt
        )
        self.btn_view_receipt.pack(side=tk.LEFT, padx=6)

        btn_export = PillButton(
            action_bar, text="📥 Export Invoices to CSV", font_size=9,
            bg_color="#EFF6FF", fg_color=THEME["primary"], hover_color="#DBEAFE",
            padx=12, pady=5, command=self._export_csv
        )
        btn_export.pack(side=tk.RIGHT)

    def load_invoices(self):
        status = self.cmb_filter.get()
        invoices = get_invoices(status=status)

        for item in self.tree.get_children():
            self.tree.delete(item)

        total_settled = 0.0
        total_pending = 0.0

        for b in invoices:
            p_desc = f"{b['patient_name']} ({b['uhid']})"
            tot = b["total_amount"]
            if b["payment_status"] == "Paid":
                total_settled += tot
            else:
                total_pending += tot

            self.tree.insert("", tk.END, values=(
                b["id"], b["invoice_number"], b["invoice_date"], p_desc,
                f"₹{b['consultation_amount']:.2f}", f"₹{b['medicine_amount']:.2f}",
                f"₹{b['lab_amount']:.2f}", f"₹{b['tax_amount']:.2f}",
                f"₹{b['total_amount']:.2f}", b["payment_mode"], b["payment_status"]
            ), tags=(b["payment_status"],))

        self.lbl_revenue.config(text=f"💰 Total Settled: ₹{total_settled:.2f} | Pending: ₹{total_pending:.2f}")

        if hasattr(self, "kpi_billing_cards"):
            tot_revenue = total_settled + total_pending
            col_rate = (total_settled / tot_revenue * 100.0) if tot_revenue > 0 else 0.0
            self.kpi_billing_cards["settled"].config(text=f"₹{total_settled:.2f}")
            self.kpi_billing_cards["pending"].config(text=f"₹{total_pending:.2f}")
            self.kpi_billing_cards["invoices"].config(text=f"{len(invoices)} Invoices")
            self.kpi_billing_cards["rate"].config(text=f"{col_rate:.1f}%")

        self._on_bill_selected()

    def _on_bill_selected(self, event=None):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.selected_bill_id = item["values"][0]
            status = item["values"][10]
            self.btn_mark_paid.config(state=tk.NORMAL if status == "Pending" else tk.DISABLED)
            self.btn_view_receipt.config(state=tk.NORMAL)
        else:
            self.selected_bill_id = None
            self.btn_mark_paid.config(state=tk.DISABLED)
            self.btn_view_receipt.config(state=tk.DISABLED)

    def _action_mark_paid(self):
        if self.selected_bill_id:
            update_payment_status(self.selected_bill_id, "Paid")
            messagebox.showinfo("Success", "Invoice marked as Settled (Paid).")
            self.load_invoices()

    def _action_view_receipt(self):
        if not self.selected_bill_id:
            return
        selected = self.tree.selection()
        if not selected:
            return
        vals = self.tree.item(selected[0])["values"]

        receipt_text = (
            f"=====================================================\n"
            f"          CITY GENERAL HOSPITAL & MEDICAL CENTER       \n"
            f"          BBAT104 TQM - Student: Bhupinder Singh      \n"
            f"=====================================================\n\n"
            f" Invoice Number : {vals[1]}\n"
            f" Invoice Date   : {vals[2]}\n"
            f" Patient Details: {vals[3]}\n"
            f"-----------------------------------------------------\n"
            f" Consultation Fee : {vals[4]}\n"
            f" Pharmacy/Medicine: {vals[5]}\n"
            f" Lab/Diagnostics  : {vals[6]}\n"
            f" Tax (GST 5%)     : {vals[7]}\n"
            f"-----------------------------------------------------\n"
            f" TOTAL AMOUNT DUE : {vals[8]}\n"
            f" Payment Method   : {vals[9]}\n"
            f" Settlement Status: {vals[10]}\n"
            f"=====================================================\n"
            f"       Thank you for choosing our healthcare services! \n"
        )
        
        top = tk.Toplevel(self)
        top.title(f"Receipt - {vals[1]}")
        top.geometry("450x420")
        top.configure(bg="white")
        txt = tk.Text(top, font=("Courier New", 10), padx=15, pady=15, bg="#F8FAFC", relief="flat")
        txt.insert("1.0", receipt_text)
        txt.config(state="disabled")
        txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _export_csv(self):
        invoices = get_invoices()
        if not invoices:
            messagebox.showinfo("Export", "No invoice records to export.")
            return
        df = pd.DataFrame(invoices)
        export_file = EXPORTS_DIR / f"Invoices_Export_{date.today().strftime('%Y%m%d')}.csv"
        df.to_csv(export_file, index=False)
        messagebox.showinfo("Export Successful", f"Invoices exported successfully to:\n{export_file}")

    def open_new_bill_modal(self, preselected_appointment_id: Optional[int] = None):
        BillingInvoiceModal(self, preselected_appointment_id=preselected_appointment_id, on_saved=self.load_invoices)


class BillingInvoiceModal(tk.Toplevel):
    """Modal for creating itemized billing invoices."""

    def __init__(self, parent, preselected_appointment_id: Optional[int] = None, on_saved: Optional[Callable] = None):
        super().__init__(parent)
        self.title("Generate Patient Invoice")
        self.geometry("480x540")
        self.resizable(False, False)
        self.configure(bg="white")
        self.grab_set()
        self.preselected_appointment_id = preselected_appointment_id
        self.on_saved = on_saved
        self.patient_map = {}

        self._build_form()

    def _build_form(self):
        form_frame = tk.Frame(self, bg="white", padx=25, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="Patient Billing & Invoicing", font=("Segoe UI", 12, "bold"), fg=THEME["primary"], bg="white").pack(anchor=tk.W, pady=(0, 15))

        tk.Label(form_frame, text="Select Patient *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.cmb_patient = ttk.Combobox(form_frame, state="readonly", width=45)
        self._populate_patients()
        self.cmb_patient.pack(fill=tk.X, pady=(2, 10))

        tk.Label(form_frame, text="Doctor Consultation Fee (₹) *", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_consult = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_consult.insert(0, "500.0")
        self.txt_consult.pack(fill=tk.X, pady=(2, 8), ipady=3)

        tk.Label(form_frame, text="Pharmacy & Medicine Charges (₹)", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_med = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_med.insert(0, "0.0")
        self.txt_med.pack(fill=tk.X, pady=(2, 8), ipady=3)

        tk.Label(form_frame, text="Lab & Diagnostic Tests Charges (₹)", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.txt_lab = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        self.txt_lab.insert(0, "0.0")
        self.txt_lab.pack(fill=tk.X, pady=(2, 8), ipady=3)

        # Mode & Status Row
        row1 = tk.Frame(form_frame, bg="white")
        row1.pack(fill=tk.X, pady=(2, 15))

        col_mode = tk.Frame(row1, bg="white")
        col_mode.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(col_mode, text="Payment Mode", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.cmb_mode = ttk.Combobox(col_mode, values=["Cash", "Card", "UPI", "Insurance", "NetBanking"], state="readonly")
        self.cmb_mode.set("UPI")
        self.cmb_mode.pack(fill=tk.X, pady=2)

        col_status = tk.Frame(row1, bg="white")
        col_status.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(col_status, text="Settlement Status", font=("Segoe UI", 9, "bold"), fg=THEME["text"], bg="white").pack(anchor=tk.W)
        self.cmb_status = ttk.Combobox(col_status, values=["Paid", "Pending"], state="readonly")
        self.cmb_status.set("Paid")
        self.cmb_status.pack(fill=tk.X, pady=2)

        tk.Label(form_frame, text="ℹ️ Applicable 5% GST tax is automatically computed.", font=("Segoe UI", 8), fg="#64748B", bg="white").pack(anchor=tk.W, pady=(0, 15))

        btn_frame = tk.Frame(form_frame, bg="white", pady=10)
        btn_frame.pack(fill=tk.X)

        btn_generate = PillButton(
            btn_frame, text="🧾 Generate & Print Bill", font_size=9,
            bg_color=THEME["primary"], fg_color="white", hover_color=THEME["primary_dark"],
            padx=16, pady=7, command=self.save_invoice
        )
        btn_generate.pack(side=tk.RIGHT, padx=5)

        btn_cancel = PillButton(
            btn_frame, text="Cancel", font_size=9,
            bg_color="#F1F5F9", fg_color=THEME["text"], hover_color="#E2E8F0",
            padx=12, pady=7, command=self.destroy
        )
        btn_cancel.pack(side=tk.RIGHT, padx=5)

    def _populate_patients(self):
        patients, _ = fast_search_patients("", limit=200)
        options = []
        for p in patients:
            label = f"{p['full_name']} | {p['uhid']} | {p['phone']}"
            self.patient_map[label] = p["id"]
            options.append(label)

        self.cmb_patient["values"] = options
        if options:
            self.cmb_patient.current(0)

    def save_invoice(self):
        p_str = self.cmb_patient.get()
        if not p_str:
            messagebox.showerror("Error", "Please select a patient.")
            return

        patient_id = self.patient_map.get(p_str)
        try:
            consult_fee = float(self.txt_consult.get().strip())
            med_fee = float(self.txt_med.get().strip() or 0.0)
            lab_fee = float(self.txt_lab.get().strip() or 0.0)
        except ValueError:
            messagebox.showerror("Error", "Fees must be numeric values.")
            return

        mode = self.cmb_mode.get()
        status = self.cmb_status.get()

        try:
            b_id, inv_num, total = create_invoice(
                patient_id=patient_id,
                appointment_id=self.preselected_appointment_id,
                consultation_amount=consult_fee,
                medicine_amount=med_fee,
                lab_amount=lab_fee,
                tax_rate=0.05,
                payment_mode=mode,
                payment_status=status
            )
            messagebox.showinfo("Invoice Generated", f"Invoice #{inv_num} created successfully!\nTotal Amount: ₹{total:.2f}")
            if self.on_saved:
                self.on_saved()
            self.destroy()

        except Exception as ex:
            messagebox.showerror("Error", f"Failed to generate invoice: {ex}")
