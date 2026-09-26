"""
Q02 Performance Feature #2: Vectorized Reporting Engine with Pandas.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

import time
from datetime import date
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
from src.config import EXPORTS_DIR
from src.database import get_connection, log_performance


def generate_opd_summary_report() -> Tuple[pd.DataFrame, float, Path]:
    """
    Generate OPD Daily Summary Report with patient wait times and appointment statuses.
    Vectorized aggregation using Pandas.
    """
    start_time = time.perf_counter()
    conn = get_connection()

    query = """
        SELECT a.appointment_number, a.appointment_date, a.token_number, a.status,
               a.wait_time_minutes, p.uhid, p.full_name as patient_name,
               d.full_name as doctor_name, d.specialization, d.room_no
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        ORDER BY a.appointment_date DESC, a.token_number ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Export to CSV
    export_path = EXPORTS_DIR / f"OPD_Summary_{date.today().strftime('%Y%m%d')}.csv"
    df.to_csv(export_path, index=False)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    log_performance("Report_OPD_Summary", len(df), elapsed_ms, "SUCCESS", f"Generated in {elapsed_ms:.1f}ms")

    return df, elapsed_ms, export_path


def generate_doctor_workload_report() -> Tuple[pd.DataFrame, float, Path]:
    """
    Doctor Workload & Capacity Utilization report.
    Aggregates appointment counts and average wait times per doctor.
    """
    start_time = time.perf_counter()
    conn = get_connection()

    query = """
        SELECT d.doctor_code, d.full_name as doctor_name, d.specialization, d.room_no, d.status as current_status,
               COUNT(a.id) as total_appointments,
               SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) as completed_consultations,
               SUM(CASE WHEN a.status = 'Waiting' THEN 1 ELSE 0 END) as waiting_patients,
               ROUND(AVG(CASE WHEN a.status = 'Completed' AND a.wait_time_minutes > 0 THEN a.wait_time_minutes ELSE NULL END), 1) as avg_wait_time_min
        FROM doctors d
        LEFT JOIN appointments a ON d.id = a.doctor_id
        GROUP BY d.id
        ORDER BY total_appointments DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    export_path = EXPORTS_DIR / f"Doctor_Workload_{date.today().strftime('%Y%m%d')}.csv"
    df.to_csv(export_path, index=False)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    log_performance("Report_Doctor_Workload", len(df), elapsed_ms, "SUCCESS", f"Generated in {elapsed_ms:.1f}ms")

    return df, elapsed_ms, export_path


def generate_financial_audit_report() -> Tuple[pd.DataFrame, float, Path]:
    """
    Hospital Financial Audit Report: Invoicing, tax collections, and outstanding dues.
    """
    start_time = time.perf_counter()
    conn = get_connection()

    query = """
        SELECT b.invoice_number, b.invoice_date, p.uhid, p.full_name as patient_name,
               b.consultation_amount, b.medicine_amount, b.lab_amount, b.tax_amount,
               b.total_amount, b.payment_mode, b.payment_status
        FROM billing b
        JOIN patients p ON b.patient_id = p.id
        ORDER BY b.id DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    export_path = EXPORTS_DIR / f"Financial_Audit_{date.today().strftime('%Y%m%d')}.csv"
    df.to_csv(export_path, index=False)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    log_performance("Report_Financial_Audit", len(df), elapsed_ms, "SUCCESS", f"Generated in {elapsed_ms:.1f}ms")

    return df, elapsed_ms, export_path


def generate_tqm_sla_report() -> Tuple[pd.DataFrame, float, Path]:
    """
    TQM Performance Telemetry & SLA Audit Report.
    Analyzes historical query execution latencies and compliance rates.
    """
    start_time = time.perf_counter()
    conn = get_connection()

    query = """
        SELECT operation_type, COUNT(*) as total_invocations,
               ROUND(AVG(execution_time_ms), 2) as avg_latency_ms,
               ROUND(MIN(execution_time_ms), 2) as min_latency_ms,
               ROUND(MAX(execution_time_ms), 2) as max_latency_ms,
               SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as sla_passed,
               SUM(CASE WHEN status != 'SUCCESS' THEN 1 ELSE 0 END) as sla_breached
        FROM performance_logs
        GROUP BY operation_type
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    export_path = EXPORTS_DIR / f"TQM_SLA_Telemetry_{date.today().strftime('%Y%m%d')}.csv"
    df.to_csv(export_path, index=False)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return df, elapsed_ms, export_path
