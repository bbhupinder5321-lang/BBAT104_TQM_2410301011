"""
Billing and Patient Invoicing Module.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from datetime import date
from typing import List, Dict, Any, Optional, Tuple
from src.database import get_db_cursor


def generate_invoice_number() -> str:
    """Generate sequential standardized invoice number (e.g., INV-2026-0001)."""
    current_year = date.today().year
    with get_db_cursor() as cursor:
        cursor.execute("SELECT MAX(id) as max_id FROM billing")
        row = cursor.fetchone()
        next_num = (row["max_id"] or 0) + 1
        return f"INV-{current_year}-{next_num:04d}"


def create_invoice(patient_id: int, appointment_id: Optional[int], consultation_amount: float,
                   medicine_amount: float = 0.0, lab_amount: float = 0.0, tax_rate: float = 0.05,
                   payment_mode: str = "Cash", payment_status: str = "Paid") -> Tuple[int, str, float]:
    """
    Generate itemized patient invoice with automated tax and total calculation.
    Returns: (billing_id, invoice_number, total_amount)
    """
    subtotal = consultation_amount + medicine_amount + lab_amount
    tax_amount = round(subtotal * tax_rate, 2)
    total_amount = round(subtotal + tax_amount, 2)
    inv_num = generate_invoice_number()
    today_str = date.today().isoformat()

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO billing (invoice_number, appointment_id, patient_id, 
                                consultation_amount, medicine_amount, lab_amount, 
                                tax_amount, total_amount, payment_mode, payment_status, invoice_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (inv_num, appointment_id, patient_id, consultation_amount, medicine_amount, 
             lab_amount, tax_amount, total_amount, payment_mode, payment_status, today_str)
        )
        bill_id = cursor.lastrowid
        return bill_id, inv_num, total_amount


def get_invoices(patient_id: Optional[int] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch itemized billing list with patient and doctor details."""
    query = """
        SELECT b.*, p.uhid, p.full_name as patient_name, p.phone as patient_phone,
               d.full_name as doctor_name
        FROM billing b
        JOIN patients p ON b.patient_id = p.id
        LEFT JOIN appointments a ON b.appointment_id = a.id
        LEFT JOIN doctors d ON a.doctor_id = d.id
        WHERE 1=1
    """
    params = []
    if patient_id:
        query += " AND b.patient_id = ?"
        params.append(patient_id)
    if status and status != "All":
        query += " AND b.payment_status = ?"
        params.append(status)

    query += " ORDER BY b.id DESC"

    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]


def update_payment_status(billing_id: int, new_status: str, payment_mode: Optional[str] = None):
    """Update invoice settlement status (Paid/Pending)."""
    with get_db_cursor(commit=True) as cursor:
        if payment_mode:
            cursor.execute(
                "UPDATE billing SET payment_status = ?, payment_mode = ? WHERE id = ?",
                (new_status, payment_mode, billing_id)
            )
        else:
            cursor.execute("UPDATE billing SET payment_status = ? WHERE id = ?", (new_status, billing_id))
