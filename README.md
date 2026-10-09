# BBAT104 TQM Hospital Management System

**Student:** Bhupinder Singh  
**Roll No:** 2410301011  
**Branch/Section:** CSE - A  
**Course:** BBAT104 – Fundamentals of TQM

## Project Overview

MediCare is a desktop Hospital Management System built for BBAT104 – Fundamentals of TQM. Its assigned quality objective is **Q02 – Improve Performance**, with a focus on reducing patient waiting time and preventing duplicate patient records.

The application follows a layered architecture:

**PySide6 GUI → Services → Repositories → SQLite**

The newer PySide6 interface is being introduced alongside the previous CustomTkinter screens so the interface can be migrated and validated without deleting the existing implementation.

## Main Modules

- Authentication with administrator and staff roles
- Patient management and duplicate-phone validation
- Doctor management
- Appointment scheduling and patient check-in / consultation timestamps
- Billing management
- CSV patient import with duplicate detection and rejected-row feedback
- Operational reports
- Q02 performance measurements
- TQM analysis including SIPOC, FMEA, and PDCA overview
- Legacy screens remain in the repository while the Qt migration progresses

## Q02 Performance Features

- Patient search by name, phone, or patient ID
- Focused SQL reporting queries
- Dashboard snapshot for today's registrations and appointments, queue status, bed capacity, and measured waiting time
- Bulk CSV validation and insert workflow
- SQLite indexes for frequently queried fields
- Performance checks for database lookup, patient search, dashboard load, and report generation

Waiting time is calculated as **consultation start time − check-in time** when both timestamps are available and valid. The application does not generate artificial waiting-time values.

## Technology Stack

- Python 3.x
- **PySide6 (Qt for Python)** — new desktop interface
- CustomTkinter / Tkinter — legacy interface during migration
- SQLite3
- Pandas
- Matplotlib and Seaborn

## Installation

Open PowerShell in the project directory and activate the existing virtual environment:

\`\`\`powershell
cd D:\BBAT104_TQM_2410301011
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
\`\`\`

If the virtual environment does not exist, create it first:

\`\`\`powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
\`\`\`

## Run the PySide6 interface

\`\`\`powershell
python -m app.gui.qt_main
\`\`\`

The Qt launcher initializes the SQLite database before showing the login screen.

### Development login

\`\`\`text
Administrator
Username: admin
Password: admin123

Staff
Username: staff
Password: staff123
\`\`\`

These are demonstration credentials for the academic project, not production-ready authentication.

## Run the legacy interface

The previous interface remains available while PySide6 migration continues:

\`\`\`powershell
python -m app.gui.login_gui
\`\`\`

## Tests

Service-level test scripts are stored in the \`tests/\` directory. For example:

\`\`\`powershell
python tests\test_dashboard_service.py
python tests\test_performance_service.py
python tests\test_patient_service.py
\`\`\`

The dashboard performance objective is under 1,000 ms under normal local project conditions. Actual measurements depend on the computer and dataset.

## Project Structure

\`\`\`text
BBAT104_TQM_2410301011/
├── app/
│   ├── database/
│   ├── repositories/
│   ├── services/
│   └── gui/
│       ├── qt_app.py
│       ├── qt_main.py
│       └── legacy Tkinter screens
├── data/
├── docs/
├── tests/
├── requirements.txt
└── README.md
\`\`\`

## Migration status

The initial PySide6 shell, sign-in screen, dashboard, and service-backed patient, doctor, appointment, billing, CSV, report, performance, and TQM screens have been added. The original interface has not been deleted. The Qt interface still needs to be run on Windows and validated against the existing assignment requirements before it should be treated as a fully verified replacement.
