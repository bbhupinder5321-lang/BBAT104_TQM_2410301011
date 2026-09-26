# System Architecture

## Architecture Pattern

The Hospital Management System follows a layered architecture:

```text
┌──────────────────────────────────────┐
│              GUI Layer               │
│ CustomTkinter / Tkinter screens      │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│            Service Layer              │
│ Validation + business rules          │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Repository Layer             │
│ Parameterized SQL + data access      │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│              SQLite                  │
│ Patients • Doctors • Appointments    │
│ Bills • Beds • Users                 │
└──────────────────────────────────────┘
```

## Design Rule

**GUI shows → Service decides → Repository queries → Database stores.**

Keeping database operations out of the GUI makes the application easier to test, maintain and optimize.

## Application Flow

1. The user starts the login module.
2. The database schema is initialized automatically.
3. Authentication validates the username and password.
4. The authenticated user is passed to the main application.
5. The sidebar exposes features allowed by the user's role.
6. A selected screen calls its service layer.
7. The service validates input and applies business rules.
8. The repository executes parameterized SQLite queries.
9. Results are displayed by the GUI.

## Core Modules

### Authentication
Provides login and role-based access for administrator and staff accounts.

### Patients
Supports patient registration, update, deletion and fast search by name, phone or ID.

### Doctors
Supports doctor registration, specialization and status management.

### Appointments
Supports appointment scheduling, updates, deletion, search, patient check-in and consultation-start recording.

### Billing
Supports bill creation, updates, deletion, patient validation and billing reports.

### CSV Import
Supports bulk patient-record processing with validation and duplicate protection.

### Reports
Provides aggregated patient, doctor, appointment, billing and waiting-time reports.

### Performance
Measures database query, patient search, dashboard and report execution time for Q02 evaluation.

### TQM
Integrates SIPOC, FMEA, Fishbone, Pareto, Checksheet and PDCA analysis.

## Database Design

Main entities:

- `users`
- `patients`
- `doctors`
- `appointments`
- `bills`
- `beds`

Appointments connect patients and doctors using foreign keys.

Patient phone numbers and doctor phone numbers are unique to support duplicate prevention.

## Q02 Optimization

Frequently accessed fields have SQLite indexes.

The dashboard uses a dedicated repository so the GUI does not execute SQL directly.

Search and report queries use filtered/limited results where appropriate.

Waiting-time data is calculated from recorded check-in and consultation-start timestamps.

## Performance Target

The Q02 requirement defines a dashboard loading target of **less than 1000 ms** under normal local operating conditions.

The Performance screen measures the relevant execution times in milliseconds.
