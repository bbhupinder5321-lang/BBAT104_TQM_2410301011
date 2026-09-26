"""
Patient Model and Service Layer with Q02 Fast Search & Poka-Yoke Duplicate Prevention.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

import time
from typing import List, Dict, Any, Tuple, Optional
from src.database import get_db_cursor, log_performance


def generate_next_uhid() -> str:
    """Generate next standardized Unique Hospital Identification Number (UHID)."""
    with get_db_cursor() as cursor:
        cursor.execute("SELECT MAX(id) as max_id FROM patients")
        row = cursor.fetchone()
        next_num = (row["max_id"] or 0) + 1
        return f"UHID-2026-{next_num:04d}"


def check_duplicate_phone(phone: str, exclude_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """
    TQM Poka-Yoke: Real-time duplicate verification on phone number.
    Returns existing patient dict if duplicate is detected, else None.
    """
    clean_phone = phone.strip()
    if not clean_phone:
        return None

    query = "SELECT id, uhid, full_name, phone, created_at FROM patients WHERE phone = ?"
    params = [clean_phone]
    if exclude_id:
        query += " AND id != ?"
        params.append(exclude_id)

    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None


def create_patient(full_name: str, gender: str, age: int, phone: str, 
                   email: str = "", address: str = "", blood_group: str = "Unknown") -> Tuple[int, str]:
    """
    Add a new patient with Poka-Yoke duplicate validation.
    Raises ValueError if phone is already registered.
    """
    # Validation
    name_clean = full_name.strip()
    phone_clean = phone.strip()
    if not name_clean:
        raise ValueError("Patient name cannot be empty.")
    if not phone_clean or len(phone_clean) < 7:
        raise ValueError("Valid phone number is required (min 7 digits).")
    if age < 0 or age > 125:
        raise ValueError("Age must be between 0 and 125.")

    # Poka-Yoke Duplicate Detection
    existing = check_duplicate_phone(phone_clean)
    if existing:
        raise ValueError(
            f"POKA-YOKE WARNING: A patient with phone {phone_clean} is already registered!\n"
            f"Existing Patient: {existing['full_name']} (UHID: {existing['uhid']})"
        )

    uhid = generate_next_uhid()
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO patients (uhid, full_name, gender, age, phone, email, address, blood_group)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (uhid, name_clean, gender, age, phone_clean, email.strip(), address.strip(), blood_group)
        )
        patient_id = cursor.lastrowid
        return patient_id, uhid


def update_patient(patient_id: int, full_name: str, gender: str, age: int, 
                   phone: str, email: str = "", address: str = "", blood_group: str = "Unknown"):
    """Update patient demographic details with duplicate collision check."""
    name_clean = full_name.strip()
    phone_clean = phone.strip()
    if not name_clean:
        raise ValueError("Patient name cannot be empty.")

    existing = check_duplicate_phone(phone_clean, exclude_id=patient_id)
    if existing:
        raise ValueError(f"Phone number {phone_clean} is already assigned to {existing['full_name']} ({existing['uhid']}).")

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            UPDATE patients
            SET full_name = ?, gender = ?, age = ?, phone = ?, email = ?, address = ?, blood_group = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (name_clean, gender, age, phone_clean, email.strip(), address.strip(), blood_group, patient_id)
        )


def delete_patient(patient_id: int):
    """Delete a patient record (cascading deletes appointments and billing)."""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM billing WHERE patient_id = ?", (patient_id,))
        cursor.execute("DELETE FROM appointments WHERE patient_id = ?", (patient_id,))
        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))


def get_patient_by_id(patient_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve complete patient profile by primary key."""
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def fast_search_patients(query_str: str, limit: int = 50) -> Tuple[List[Dict[str, Any]], float]:
    """
    Q02 Performance Feature #1: Fast Search Engine with microsecond telemetry.
    Leverages B-Tree composite indexes:
    - idx_patients_name for patient name prefix match
    - idx_patients_phone for direct phone lookup
    - idx_patients_uhid for UHID exact lookup
    Returns: (list_of_patients, latency_in_ms)
    """
    clean_q = query_str.strip()
    start_time = time.perf_counter()

    with get_db_cursor() as cursor:
        if not clean_q:
            cursor.execute(
                """
                SELECT id, uhid, full_name, gender, age, phone, blood_group, created_at
                FROM patients
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            )
        elif clean_q.upper().startswith("UHID-"):
            cursor.execute(
                """
                SELECT id, uhid, full_name, gender, age, phone, blood_group, created_at
                FROM patients
                WHERE uhid LIKE ?
                LIMIT ?
                """,
                (f"{clean_q.upper()}%", limit)
            )
        elif clean_q.isdigit():
            # Phone index seek
            cursor.execute(
                """
                SELECT id, uhid, full_name, gender, age, phone, blood_group, created_at
                FROM patients
                WHERE phone LIKE ?
                LIMIT ?
                """,
                (f"{clean_q}%", limit)
            )
        else:
            # Name and general index seek
            cursor.execute(
                """
                SELECT id, uhid, full_name, gender, age, phone, blood_group, created_at
                FROM patients
                WHERE full_name LIKE ? OR phone LIKE ?
                LIMIT ?
                """,
                (f"%{clean_q}%", f"{clean_q}%", limit)
            )

        rows = [dict(r) for r in cursor.fetchall()]

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    # Telemetry logging for Q02 SLA audit
    if clean_q:
        log_performance(
            operation_type="Fast_Search",
            record_count=len(rows),
            execution_time_ms=elapsed_ms,
            status="SUCCESS" if elapsed_ms <= 100.0 else "DEGRADED",
            details=f"Query: '{clean_q}' | Results: {len(rows)}"
        )

    return rows, elapsed_ms
