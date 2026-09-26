"""
Doctor Model and Management Module.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from typing import List, Dict, Any, Optional
from src.database import get_db_cursor


def get_all_doctors(status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve list of doctors with optional availability status filtering."""
    query = "SELECT * FROM doctors"
    params = []
    if status_filter and status_filter != "All":
        query += " WHERE status = ?"
        params.append(status_filter)
    query += " ORDER BY specialization, full_name"

    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]


def get_available_doctors() -> List[Dict[str, Any]]:
    """Retrieve doctors currently active and available for OPD consultation."""
    return get_all_doctors(status_filter="Available")


def get_doctor_by_id(doctor_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve doctor by ID."""
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def create_doctor(doctor_code: str, full_name: str, specialization: str, 
                  phone: str, email: str, room_no: str, consultation_fee: float, status: str = "Available"):
    """Register a new medical doctor in the hospital roster."""
    code_clean = doctor_code.strip()
    name_clean = full_name.strip()
    if not code_clean or not name_clean:
        raise ValueError("Doctor code and name are required.")
    if consultation_fee < 0:
        raise ValueError("Consultation fee cannot be negative.")

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO doctors (doctor_code, full_name, specialization, phone, email, room_no, consultation_fee, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (code_clean, name_clean, specialization.strip(), phone.strip(), email.strip(), room_no.strip(), consultation_fee, status)
        )


def update_doctor(doctor_id: int, full_name: str, specialization: str, 
                  phone: str, email: str, room_no: str, consultation_fee: float, status: str):
    """Update doctor demographic and availability information."""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            UPDATE doctors
            SET full_name = ?, specialization = ?, phone = ?, email = ?, room_no = ?, consultation_fee = ?, status = ?
            WHERE id = ?
            """,
            (full_name.strip(), specialization.strip(), phone.strip(), email.strip(), room_no.strip(), consultation_fee, status, doctor_id)
        )


def toggle_doctor_status(doctor_id: int, new_status: str):
    """Fast status toggle for clinical coordination (Available, On Leave, In Surgery)."""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("UPDATE doctors SET status = ? WHERE id = ?", (new_status, doctor_id))


def delete_doctor(doctor_id: int):
    """Delete a doctor record if no active appointments exist."""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
