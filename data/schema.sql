-- ============================================================================
-- COURSE: BBAT104 - Fundamentals of Total Quality Management (TQM)
-- PROJECT: Hospital Management System (HMS)
-- STUDENT: Bhupinder Singh | Roll No: 2410301011 | CSE - A
-- QUALITY GOAL: Q02 - Improve Performance (Throughput, Latency, Data Integrity)
-- DATABASE: SQLite 3 Optimized Schema with B-Tree Indexing & Unique Constraints
-- ============================================================================

-- Enable Foreign Key constraints
PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- 1. USERS TABLE (Role-Based Access Control)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'Receptionist', 'Doctor', 'Billing')),
    status TEXT NOT NULL DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 2. PATIENTS TABLE (Core TQM Goal: Prevent Duplicate Records via Constraints)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uhid TEXT UNIQUE NOT NULL,              -- Unique Hospital Identification Number (e.g. UHID-2026-0001)
    full_name TEXT NOT NULL,
    gender TEXT NOT NULL CHECK(gender IN ('Male', 'Female', 'Other')),
    age INTEGER NOT NULL CHECK(age >= 0 AND age <= 125),
    phone TEXT UNIQUE NOT NULL,             -- Unique phone prevents accidental duplicate registration
    email TEXT,
    address TEXT,
    blood_group TEXT CHECK(blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'Unknown')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 3. DOCTORS TABLE
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_code TEXT UNIQUE NOT NULL,       -- e.g. DOC-101
    full_name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    room_no TEXT NOT NULL,
    consultation_fee REAL NOT NULL CHECK(consultation_fee >= 0),
    status TEXT NOT NULL DEFAULT 'Available' CHECK(status IN ('Available', 'On Leave', 'In Surgery', 'Inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 4. APPOINTMENTS TABLE (Core TQM Goal: Reduce Waiting Time via Queue & Tokens)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_number TEXT UNIQUE NOT NULL, -- e.g. APT-20260926-001
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    token_number INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'Waiting', 'In-Consultation', 'Completed', 'Cancelled', 'No-Show')),
    check_in_time TIMESTAMP,                 -- Recorded when patient arrives at clinic
    consultation_start_time TIMESTAMP,       -- Recorded when doctor calls patient in
    consultation_end_time TIMESTAMP,         -- Recorded when consultation finishes
    wait_time_minutes REAL DEFAULT 0.0,      -- Calculated: (consultation_start_time - check_in_time) in minutes
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 5. BILLING TABLE
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS billing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE NOT NULL,     -- e.g. INV-2026-0001
    appointment_id INTEGER,
    patient_id INTEGER NOT NULL,
    consultation_amount REAL NOT NULL DEFAULT 0.0,
    medicine_amount REAL NOT NULL DEFAULT 0.0,
    lab_amount REAL NOT NULL DEFAULT 0.0,
    tax_amount REAL NOT NULL DEFAULT 0.0,
    total_amount REAL NOT NULL DEFAULT 0.0,
    payment_mode TEXT NOT NULL CHECK(payment_mode IN ('Cash', 'Card', 'UPI', 'Insurance', 'NetBanking')),
    payment_status TEXT NOT NULL DEFAULT 'Pending' CHECK(payment_status IN ('Paid', 'Pending', 'Cancelled', 'Refunded')),
    invoice_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 6. AUDIT & PERFORMANCE TELEMETRY TABLE (TQM Measurement & Q02 SLA Tracking)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS performance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_type TEXT NOT NULL,           -- 'Fast_Search', 'Dashboard_Load', 'CSV_Import', 'Report_Gen'
    record_count INTEGER NOT NULL DEFAULT 0,
    execution_time_ms REAL NOT NULL,        -- Execution duration in milliseconds
    status TEXT NOT NULL CHECK(status IN ('SUCCESS', 'FAILURE', 'DEGRADED')),
    details TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Q02 PERFORMANCE FEATURE #5: EFFICIENT DB QUERIES & B-TREE INDEXING
-- These indexes drastically reduce full-table scans (O(N) -> O(log N)),
-- enabling instant search-as-you-type and sub-second dashboard rendering.
-- ============================================================================

-- Fast search indexes on Patient Name, Phone, and UHID
CREATE INDEX IF NOT EXISTS idx_patients_name ON patients(full_name COLLATE NOCASE);
CREATE INDEX IF NOT EXISTS idx_patients_phone ON patients(phone);
CREATE INDEX IF NOT EXISTS idx_patients_uhid ON patients(uhid);

-- Optimized scheduling and status lookup indexes
CREATE INDEX IF NOT EXISTS idx_appointments_date_status ON appointments(appointment_date, status);
CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor ON appointments(doctor_id);

-- Financial lookup and aggregation indexes
CREATE INDEX IF NOT EXISTS idx_billing_invoice_date ON billing(invoice_date);
CREATE INDEX IF NOT EXISTS idx_billing_patient ON billing(patient_id);
CREATE INDEX IF NOT EXISTS idx_billing_status ON billing(payment_status);

-- Performance telemetry query index
CREATE INDEX IF NOT EXISTS idx_performance_op ON performance_logs(operation_type, logged_at);
