# Software Requirements Specification (SRS)

## Hospital Management System with TQM Performance Improvement

**Course:** BBAT104 – Fundamentals of Total Quality Management
**Student:** Bhupinder Singh
**Roll No.:** 2410301011
**Branch/Section:** CSE – A
**Assigned Quality Goal:** Q02 – Improve Performance
**Project:** Hospital Management System
**Version:** 1.0

---

# 1. Introduction

## 1.1 Purpose

The purpose of this project is to develop a Hospital Management System (HMS) that manages basic hospital operations while applying Total Quality Management (TQM) principles to improve system performance.

The system will provide modules for patient management, doctor management, appointment scheduling, billing, authentication and performance monitoring.

The primary TQM objective is:

> **Q02 – Improve Performance**

The project particularly focuses on reducing patient waiting time, improving database response time and preventing duplicate patient records.

---

## 1.2 Problem Statement

Traditional or poorly optimized hospital record systems may experience problems such as:

* Slow patient searches
* Long report generation times
* Repeated loading of complete database tables
* Manual entry of large numbers of patient records
* Duplicate patient records
* Delayed access to important hospital statistics
* Inefficient database queries
* Difficulty monitoring operational performance

These problems can increase administrative workload and contribute to patient waiting time.

The proposed system addresses these issues using database indexing, optimized SQL queries, efficient search, CSV-based bulk import, optimized reporting and a performance dashboard.

---

# 2. Objectives

The main objectives of the system are:

1. Digitally manage hospital patient records.
2. Manage doctor information and specializations.
3. Schedule and manage patient appointments.
4. Generate patient billing records.
5. Provide secure administrator login and role-based access.
6. Reduce unnecessary database operations.
7. Provide fast patient searching.
8. Generate reports efficiently.
9. Provide a dashboard containing important hospital statistics.
10. Allow bulk patient registration through CSV files.
11. Reduce the possibility of duplicate patient records.
12. Measure and demonstrate performance improvements as part of the TQM project.

---

# 3. Scope

## 3.1 In Scope

The system will contain the following major modules:

### Patient Management

* Add patient
* Edit patient
* Delete patient
* Search patient
* View patient details
* Detect possible duplicate records
* Search by patient ID, name and phone number

### Doctor Management

* Add doctor
* Edit doctor
* Delete doctor
* Search/view doctors
* Store doctor specialization

### Appointment Management

* Book appointment
* View appointments
* Cancel appointment
* Update appointment status
* Record appointment/check-in timing
* Monitor pending appointments

### Billing Management

* Generate patient bills
* Store billing information
* View bill history
* Calculate total amount

### Authentication

* Administrator login
* Role-based access
* Restriction of administrative operations based on user role

### Performance Features — Q02

The system will implement five selected Q02 performance features:

1. Fast Search
2. Optimized Reports
3. Dashboard
4. CSV Import
5. Efficient Database Queries

---

## 3.2 Out of Scope

The following features are outside the initial project scope:

* Online payment gateway
* Online patient portal
* Real-time integration with external hospitals
* Pharmacy inventory management
* Laboratory management
* Insurance claim processing
* Cloud deployment
* Mobile application
* Real-world medical diagnosis

These features can be considered future enhancements.

---

# 4. TQM Quality Goal

## 4.1 Assigned Quality Goal

**Q02 – Improve Performance**

The performance objective is to improve the efficiency of hospital record management and reduce delays caused by inefficient information retrieval.

---

## 4.2 Performance Problems Addressed

| Problem                               | Proposed Solution                     |
| ------------------------------------- | ------------------------------------- |
| Slow patient search                   | Indexed database search               |
| Loading complete patient table        | Filtered SQL queries                  |
| Slow report generation                | Aggregated/optimized queries          |
| Manual bulk data entry                | Pandas CSV import                     |
| Difficulty monitoring hospital status | Dashboard                             |
| Duplicate patient records             | Unique identifiers + duplicate checks |
| Long database operations              | Query optimization and indexing       |

---

# 5. Functional Requirements

## FR-01: User Authentication

The system shall allow authorized users to log in.

The system shall validate:

* Username
* Password
* User role

The system shall prevent unauthorized access to administrative functions.

---

## FR-02: Patient Registration

The system shall allow authorized users to:

* Add a patient
* Edit patient information
* Delete patient information
* View patient information
* Search patient records

Patient information may include:

* Patient ID
* Full name
* Date of birth
* Gender
* Phone number
* Address
* Blood group
* Registration date

---

## FR-03: Patient Search

The system shall support searching patients using:

* Patient ID
* Patient name
* Phone number

Search results shall be filtered directly through SQL queries instead of loading the complete patient table into application memory.

The search interface shall support instant or near-instant search-as-you-type behavior.

---

## FR-04: Duplicate Patient Prevention

The system shall use unique patient identifiers.

The system shall check important identifying information such as phone number before creating a new patient record where appropriate.

Potential duplicate records shall be flagged to the user before insertion.

---

## FR-05: Doctor Management

The system shall allow authorized users to:

* Add doctors
* Edit doctor details
* Delete doctors
* View doctors
* Search doctors

Doctor information shall include:

* Doctor ID
* Doctor name
* Specialization
* Phone number
* Availability/status

---

## FR-06: Appointment Scheduling

The system shall allow users to:

* Book appointments
* View appointments
* Cancel appointments
* Update appointment status

Appointments shall be associated with both patients and doctors.

The system shall maintain appointment timing information.

---

## FR-07: Patient Waiting-Time Measurement

The system shall store relevant appointment/check-in timestamps.

The system shall calculate waiting time using available timestamps.

Example:

```text
Waiting Time =
Doctor Consultation Start Time - Patient Check-in Time
```

The system shall use collected waiting-time data to calculate average waiting time for the dashboard.

---

## FR-08: Billing

The system shall allow authorized users to:

* Create a bill
* Associate a bill with a patient
* Add applicable charges
* Calculate total amount
* View billing history

---

## FR-09: Dashboard

The system shall provide a dashboard containing key hospital statistics.

The dashboard shall display:

* Today's registered patients
* Pending appointments
* Today's appointments
* Bed occupancy
* Average patient waiting time
* Other relevant performance indicators

The dashboard should load in approximately one second under the defined test dataset and normal local-system conditions.

---

## FR-10: CSV Import

The system shall allow authorized users to import patient records from CSV files.

The import process shall:

1. Read the CSV using Pandas.
2. Validate required columns.
3. Validate data.
4. Detect duplicate records.
5. Insert valid records efficiently.
6. Report rejected/duplicate records.

Bulk import shall reduce the need for manually entering individual records.

---

## FR-11: Optimized Reports

The system shall generate reports for information such as:

* Patient registrations
* Appointments
* Doctor appointments
* Billing
* Waiting-time statistics

Reports shall use filtered and aggregated database queries instead of unnecessarily loading complete tables.

---

## FR-12: Efficient Database Queries

The system shall use optimized SQL queries.

Database indexes shall be created for frequently searched fields.

Potential indexed fields include:

* Patient ID
* Patient name
* Phone number
* Appointment date
* Doctor ID
* Patient ID in appointments

The application shall retrieve only the required records.

---

# 6. Non-Functional Requirements

## NFR-01: Performance

The system should provide fast response for common operations.

Target examples:

* Patient search: near-instant response for normal project dataset
* Dashboard: approximately under 1 second
* Normal CRUD operation: preferably under 1 second
* Reports: optimized to avoid unnecessary delays

Performance measurements will be performed using defined test datasets.

---

## NFR-02: Usability

The graphical user interface shall be simple enough for hospital administrative staff to understand.

The interface shall provide:

* Clearly labeled buttons
* Search fields
* Tables
* Forms
* Validation messages
* Error messages
* Navigation controls

---

## NFR-03: Reliability

The system shall validate user input before database operations.

Database operations shall handle errors without crashing the application.

---

## NFR-04: Data Integrity

The system shall maintain relationships between:

* Patients
* Doctors
* Appointments
* Bills

Foreign keys shall be used where appropriate.

---

## NFR-05: Security

The system shall require authentication before accessing protected functionality.

Passwords shall not be stored as plain text in the final implementation if password hashing is implemented.

Administrative functions shall be restricted according to user roles.

---

## NFR-06: Maintainability

The system shall use modular Python files.

Database operations, business logic and GUI logic should remain separated.

---

## NFR-07: Portability

The application shall run on systems supporting:

* Python 3.x
* Tkinter/CustomTkinter
* SQLite
* Pandas
* Matplotlib/Seaborn

---

# 7. Technology Stack

| Component            | Technology               |
| -------------------- | ------------------------ |
| Programming Language | Python 3.x               |
| GUI                  | Tkinter / CustomTkinter  |
| Database             | SQLite3                  |
| Data Processing      | Pandas                   |
| Visualization        | Matplotlib / Seaborn     |
| Version Control      | Git                      |
| Repository           | GitHub                   |
| Operating System     | Windows/Linux compatible |

---

# 8. High-Level System Architecture

The system will follow a layered architecture.

```text
Presentation Layer
        ↓
Service / Business Logic Layer
        ↓
Repository / Data Access Layer
        ↓
SQLite Database
```

### Presentation Layer

Responsible for:

* Login window
* Dashboard
* Patient interface
* Doctor interface
* Appointment interface
* Billing interface
* CSV import interface
* Report interface

### Service Layer

Responsible for:

* Validation
* Duplicate detection
* Search logic
* Report generation
* CSV processing
* Performance calculations

### Repository Layer

Responsible for:

* SQL queries
* INSERT
* UPDATE
* DELETE
* SELECT
* Aggregation
* Database filtering

### Database Layer

SQLite stores:

* Users
* Patients
* Doctors
* Appointments
* Bills
* Beds
* Performance-related timestamps

---

# 9. Major Database Entities

The initial database design will contain the following entities:

## Users

```text
user_id
username
password_hash
role
```

## Patients

```text
patient_id
name
date_of_birth
gender
phone
address
blood_group
created_at
```

## Doctors

```text
doctor_id
name
specialization
phone
status
```

## Appointments

```text
appointment_id
patient_id
doctor_id
appointment_date
appointment_time
status
check_in_time
consultation_start_time
```

## Bills

```text
bill_id
patient_id
bill_date
consultation_charge
medicine_charge
other_charge
total_amount
```

## Beds

```text
bed_id
bed_number
ward
status
```

## Users/Roles

Example roles:

```text
Admin
Receptionist
```

The exact role permissions will be finalized during implementation.

---

# 10. Performance Optimization Strategy

The system will demonstrate performance improvement through the following techniques.

## 10.1 Database Indexing

Indexes will be created on frequently searched columns.

Example:

```text
Patient phone
Patient name
Appointment date
Patient ID
```

This reduces the amount of data SQLite must scan during common searches.

---

## 10.2 Filtered SQL Queries

Instead of:

```text
Load every patient → Python → search
```

the system will use:

```text
Search input
     ↓
SQL WHERE condition
     ↓
Only matching records
     ↓
GUI
```

This prevents unnecessary transfer of complete tables into memory.

---

## 10.3 Parameterized Queries

SQL parameters will be used instead of directly concatenating user input.

This improves reliability and security.

---

## 10.4 Aggregated Queries

Dashboard statistics will use SQL aggregation functions such as:

```text
COUNT()
AVG()
SUM()
```

where appropriate.

This avoids transferring unnecessary records to Python merely to calculate simple statistics.

---

## 10.5 Bulk CSV Processing

CSV files will be processed using Pandas.

Valid records will be inserted using efficient database operations rather than repeatedly performing individual manual operations through the GUI.

---

# 11. Performance Measurement

The project will measure selected operations before and after optimization.

Possible measurements include:

| Metric                   | Measurement   |
| ------------------------ | ------------- |
| Patient search time      | milliseconds  |
| Dashboard loading time   | milliseconds  |
| Report generation time   | milliseconds  |
| CSV import time          | seconds       |
| Database query execution | milliseconds  |
| Duplicate detection      | response time |

Performance testing will use a controlled sample dataset so that comparisons are meaningful.

---

# 12. User Interface Requirements

The application shall provide the following main navigation:

```text
Login
  ↓
Dashboard
  ├── Patients
  ├── Doctors
  ├── Appointments
  ├── Billing
  ├── CSV Import
  ├── Reports
  └── Performance
```

The interface should provide visual feedback for:

* Successful operations
* Validation errors
* Duplicate records
* Failed database operations
* Import results
* Report generation

---

# 13. Error Handling

The system shall handle:

* Invalid patient information
* Invalid phone numbers
* Missing required fields
* Duplicate records
* Invalid CSV files
* Missing CSV columns
* Database errors
* Invalid login credentials
* Invalid appointment selections

The application should display understandable messages rather than exposing raw Python errors to normal users.

---

# 14. TQM Integration

The project applies the TQM concept of continuous improvement.

The performance-improvement cycle will follow:

```text
Identify Problem
      ↓
Measure Performance
      ↓
Analyze Root Cause
      ↓
Implement Improvement
      ↓
Measure Again
      ↓
Standardize / Improve Further
```

The following TQM tools will be used in later project reviews:

* SIPOC
* FMEA
* Pareto Analysis
* Fishbone/Ishikawa
* Checksheet
* PDCA

These tools will focus specifically on performance-related problems.

---

# 15. Expected Outcomes

The completed system is expected to:

1. Provide a functional Hospital Management System.
2. Reduce unnecessary manual data entry.
3. Provide faster patient searching.
4. Reduce unnecessary database loading.
5. Improve report generation efficiency.
6. Provide quick access to hospital statistics.
7. Support bulk patient data import.
8. Reduce duplicate patient records.
9. Provide measurable performance metrics.
10. Demonstrate practical application of TQM principles.

---

# 16. Future Enhancements

Possible future improvements include:

* Cloud database
* Multi-hospital support
* Web application
* Mobile application
* Online appointment booking
* SMS/email notifications
* Advanced analytics
* Real-time queue management
* Electronic medical records
* Integration with laboratory and pharmacy systems

---

# 17. Acceptance Criteria

The project will be considered successful when:

* Users can authenticate successfully.
* Patients can be added, edited, deleted and searched.
* Doctors can be managed.
* Appointments can be booked and cancelled.
* Bills can be generated.
* Patient CSV files can be imported.
* Duplicate patient records are detected/prevented according to defined rules.
* Dashboard statistics are displayed.
* Reports are generated.
* Database indexes are implemented.
* SQL queries retrieve only required data.
* Performance measurements demonstrate the intended optimization.
* TQM analysis documents are linked to actual system performance defects.

---

# 18. Conclusion

The proposed Hospital Management System combines basic hospital information management with a focused TQM objective of **Q02 – Improve Performance**.

Rather than treating performance as an additional feature, the system incorporates performance considerations into database design, searching, reporting, dashboard generation and bulk data processing.

The project therefore provides both a functional software system and a practical demonstration of continuous quality improvement using TQM techniques.
