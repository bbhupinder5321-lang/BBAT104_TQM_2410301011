import sqlite3
from pathlib import Path


# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Database file
DATABASE_PATH = PROJECT_ROOT / "data" / "hospital.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create all required HMS tables if they do not already exist."""

    connection = get_connection()

    connection.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
        );

        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            address TEXT,
            blood_group TEXT,
            registration_date TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL DEFAULT 'Active'
        );

        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Scheduled',
            check_in_time TEXT,
            consultation_start_time TEXT,

            FOREIGN KEY (patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE,

            FOREIGN KEY (doctor_id)
                REFERENCES doctors(doctor_id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS bills (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            bill_date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount >= 0),

            FOREIGN KEY (patient_id)
                REFERENCES patients(patient_id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS beds (
            bed_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bed_number TEXT NOT NULL UNIQUE,
            ward TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available'
        );

        -- Q02 performance indexes
        CREATE INDEX IF NOT EXISTS idx_patients_name
            ON patients(full_name);

        CREATE INDEX IF NOT EXISTS idx_patients_phone
            ON patients(phone);

        CREATE INDEX IF NOT EXISTS idx_patients_registration_date
            ON patients(registration_date);

        CREATE INDEX IF NOT EXISTS idx_appointments_date
            ON appointments(appointment_date);

        CREATE INDEX IF NOT EXISTS idx_appointments_date_status
            ON appointments(appointment_date, status);

        CREATE INDEX IF NOT EXISTS idx_appointments_patient
            ON appointments(patient_id);

        CREATE INDEX IF NOT EXISTS idx_appointments_doctor
            ON appointments(doctor_id);

        CREATE INDEX IF NOT EXISTS idx_appointments_waiting_times
            ON appointments(check_in_time, consultation_start_time);

        CREATE INDEX IF NOT EXISTS idx_bills_patient
            ON bills(patient_id);

        CREATE INDEX IF NOT EXISTS idx_bills_date
            ON bills(bill_date);

        CREATE INDEX IF NOT EXISTS idx_doctors_specialization
            ON doctors(specialization);

        CREATE INDEX IF NOT EXISTS idx_doctors_status
            ON doctors(status);
    """)

    # Create demo accounts for the two supported application roles.
    # These are development/demo credentials for the academic project.
    connection.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES ('admin', 'admin123', 'admin')
    """)

    connection.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES ('staff', 'staff123', 'staff')
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Hospital Management System database initialized successfully.")