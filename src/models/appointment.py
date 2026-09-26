"""
Appointment Scheduling, Queue Management, and Wait-Time Telemetry Module.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple
from src.database import get_db_cursor


def generate_appointment_number(target_date: str) -> str:
    """Generate sequential daily appointment number (e.g., APT-20260926-001)."""
    date_clean = target_date.replace("-", "")
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) as count FROM appointments WHERE appointment_date = ?", 
            (target_date,)
        )
        count = cursor.fetchone()["count"] + 1
        return f"APT-{date_clean}-{count:03d}"


def get_next_token_number(doctor_id: int, target_date: str) -> int:
    """Issue sequential OPD daily token for specific doctor on target date."""
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT MAX(token_number) as max_token
            FROM appointments
            WHERE doctor_id = ? AND appointment_date = ?
            """,
            (doctor_id, target_date)
        )
        row = cursor.fetchone()
        return (row["max_token"] or 0) + 1


def book_appointment(patient_id: int, doctor_id: int, appointment_date: str, 
                     appointment_time: str, notes: str = "") -> Tuple[int, str, int]:
    """
    Schedule a new outpatient appointment and assign sequential token.
    Returns: (appointment_id, appointment_number, token_number)
    """
    appt_num = generate_appointment_number(appointment_date)
    token_num = get_next_token_number(doctor_id, appointment_date)

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO appointments (appointment_number, patient_id, doctor_id, appointment_date, appointment_time, token_number, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, 'Scheduled', ?)
            """,
            (appt_num, patient_id, doctor_id, appointment_date, appointment_time, token_num, notes)
        )
        appt_id = cursor.lastrowid
        return appt_id, appt_num, token_num


def check_in_patient(appointment_id: int):
    """
    Record patient arrival at the clinic.
    Transitions status to 'Waiting' and captures check_in_time for wait-time analysis.
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            UPDATE appointments
            SET status = 'Waiting', check_in_time = ?
            WHERE id = ?
            """,
            (now_str, appointment_id)
        )


def start_consultation(appointment_id: int):
    """
    Doctor calls patient into the consultation chamber.
    Transitions status to 'In-Consultation', records consultation_start_time,
    and calculates elapsed waiting duration in minutes.
    """
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    with get_db_cursor() as cursor:
        cursor.execute("SELECT check_in_time FROM appointments WHERE id = ?", (appointment_id,))
        row = cursor.fetchone()
        check_in_str = row["check_in_time"] if row else None

    wait_minutes = 0.0
    if check_in_str:
        try:
            check_in_dt = datetime.strptime(check_in_str, "%Y-%m-%d %H:%M:%S")
            wait_minutes = max(0.0, round((now - check_in_dt).total_seconds() / 60.0, 1))
        except Exception:
            wait_minutes = 0.0

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            UPDATE appointments
            SET status = 'In-Consultation', consultation_start_time = ?, wait_time_minutes = ?
            WHERE id = ?
            """,
            (now_str, wait_minutes, appointment_id)
        )


def complete_consultation(appointment_id: int, clinical_notes: str = "") -> float:
    """Mark appointment consultation as completed and record completion timestamp."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            UPDATE appointments
            SET status = 'Completed', consultation_end_time = ?, notes = COALESCE(notes || ' | ' || ?, ?)
            WHERE id = ?
            """,
            (now_str, clinical_notes, clinical_notes, appointment_id)
        )
        cursor.execute("SELECT wait_time_minutes FROM appointments WHERE id = ?", (appointment_id,))
        row = cursor.fetchone()
        return row["wait_time_minutes"] if row and row["wait_time_minutes"] is not None else 0.0


def cancel_appointment(appointment_id: int, reason: str = "Cancelled by patient"):
    """Cancel appointment and record reason."""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            UPDATE appointments
            SET status = 'Cancelled', notes = COALESCE(notes || ' | Cancelled: ' || ?, 'Cancelled: ' || ?)
            WHERE id = ?
            """,
            (reason, reason, appointment_id)
        )


def get_appointments_list(target_date: Optional[str] = None, doctor_id: Optional[int] = None, 
                          status: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Optimized appointment query using B-Tree index idx_appointments_date_status.
    """
    query = """
        SELECT a.id, a.appointment_number, a.appointment_date, a.appointment_time, 
               a.token_number, a.status, a.wait_time_minutes, a.check_in_time,
               p.id as patient_id, p.uhid, p.full_name as patient_name, p.phone as patient_phone,
               d.id as doctor_id, d.full_name as doctor_name, d.specialization, d.room_no, d.consultation_fee
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        WHERE 1=1
    """
    params = []
    if target_date:
        query += " AND a.appointment_date = ?"
        params.append(target_date)
    if doctor_id:
        query += " AND a.doctor_id = ?"
        params.append(doctor_id)
    if status and status != "All":
        query += " AND a.status = ?"
        params.append(status)

    query += " ORDER BY a.appointment_date DESC, a.token_number ASC"

    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]


def get_waiting_time_kpi(target_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Compute key TQM wait-time metrics for today's OPD consultations.
    """
    if not target_date:
        target_date = date.today().isoformat()

    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total_completed,
                AVG(wait_time_minutes) as avg_wait_min,
                MIN(wait_time_minutes) as min_wait_min,
                MAX(wait_time_minutes) as max_wait_min
            FROM appointments
            WHERE appointment_date = ? AND status = 'Completed' AND wait_time_minutes > 0
            """,
            (target_date,)
        )
        row = cursor.fetchone()
        return {
            "target_date": target_date,
            "total_completed": row["total_completed"] or 0,
            "avg_wait_min": round(row["avg_wait_min"] or 0.0, 1),
            "min_wait_min": round(row["min_wait_min"] or 0.0, 1),
            "max_wait_min": round(row["max_wait_min"] or 0.0, 1),
        }
