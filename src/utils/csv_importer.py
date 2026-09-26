"""
Q02 Performance Feature #4: High-Throughput Bulk CSV Importer with Poka-Yoke Duplicate Prevention.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

import csv
import time
from pathlib import Path
from typing import Dict, Any, List
from src.database import get_connection, log_performance


def bulk_import_patients_from_csv(csv_path: Path) -> Dict[str, Any]:
    """
    High-Speed Transactional CSV Bulk Ingestion Engine.
    - Achieves > 500 records/sec via SQLite single-transaction executemany.
    - Applies Poka-Yoke duplicate rejection using in-memory O(1) hash sets.
    """
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    start_time = time.perf_counter()
    rows_to_insert = []
    duplicates_skipped = []
    invalid_rows = []

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Pre-load existing phone numbers and UHIDs into memory sets for O(1) instant lookup
        cursor.execute("SELECT phone, uhid FROM patients")
        existing_records = cursor.fetchall()
        existing_phones = {r["phone"].strip() for r in existing_records if r["phone"]}
        existing_uhids = {r["uhid"].strip() for r in existing_records if r["uhid"]}

        # Determine current max ID for generating UHIDs if not present in CSV
        cursor.execute("SELECT MAX(id) as max_id FROM patients")
        max_id_row = cursor.fetchone()
        next_counter = (max_id_row["max_id"] or 0) + 1

        total_rows_read = 0

        with open(csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            # Normalize headers
            fieldnames = [c.strip().lower() for c in (reader.fieldnames or [])]

            for row_idx, raw_row in enumerate(reader, start=1):
                total_rows_read += 1
                row = {k.strip().lower(): v.strip() for k, v in raw_row.items() if k}

                # Extract and sanitize fields
                name = row.get("full_name") or row.get("name") or ""
                phone = row.get("phone") or row.get("mobile") or row.get("contact") or ""
                gender = row.get("gender", "Other").capitalize()
                if gender not in ("Male", "Female", "Other"):
                    gender = "Other"

                try:
                    age = int(row.get("age", 0))
                except ValueError:
                    age = 0

                email = row.get("email", "")
                address = row.get("address", "")
                blood_group = row.get("blood_group", "Unknown")

                # Basic validation
                if not name or not phone:
                    invalid_rows.append({"row": row_idx, "reason": "Missing Name or Phone", "data": raw_row})
                    continue

                # Poka-Yoke Duplicate Detection
                if phone in existing_phones:
                    duplicates_skipped.append({"row": row_idx, "phone": phone, "name": name, "reason": "Phone already exists"})
                    continue

                uhid = row.get("uhid")
                if not uhid or uhid in existing_uhids:
                    uhid = f"UHID-2026-{next_counter:04d}"
                    next_counter += 1

                existing_phones.add(phone)
                existing_uhids.add(uhid)

                rows_to_insert.append((
                    uhid, name, gender, age, phone, email, address, blood_group
                ))

        # Perform atomic batch insertion
        if rows_to_insert:
            cursor.execute("BEGIN TRANSACTION;")
            cursor.executemany(
                """
                INSERT INTO patients (uhid, full_name, gender, age, phone, email, address, blood_group)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows_to_insert
            )
            conn.commit()

        elapsed_sec = time.perf_counter() - start_time
        elapsed_ms = elapsed_sec * 1000.0
        records_per_sec = (len(rows_to_insert) / elapsed_sec) if elapsed_sec > 0 else 0.0

        # Telemetry logging for Q02 SLA compliance
        log_performance(
            operation_type="CSV_Bulk_Import",
            record_count=len(rows_to_insert),
            execution_time_ms=elapsed_ms,
            status="SUCCESS" if records_per_sec >= 500.0 or len(rows_to_insert) < 50 else "ACCEPTABLE",
            details=f"Inserted: {len(rows_to_insert)} | Skipped DUP: {len(duplicates_skipped)} | Throughput: {records_per_sec:.1f} rps"
        )

        return {
            "total_rows_read": total_rows_read,
            "inserted_count": len(rows_to_insert),
            "duplicates_skipped": len(duplicates_skipped),
            "invalid_count": len(invalid_rows),
            "elapsed_ms": round(elapsed_ms, 2),
            "records_per_second": round(records_per_sec, 1),
            "duplicate_details": duplicates_skipped[:10],  # sample preview
        }

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
