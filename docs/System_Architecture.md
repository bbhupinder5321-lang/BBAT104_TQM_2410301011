# SYSTEM ARCHITECTURE & PROCESS FLOWCHARTS
## College Course: BBAT104 – Fundamentals of Total Quality Management (TQM)
### Project Title: High-Performance Hospital Management System (HMS)
**Focus Area:** Quality Goal Q02 – Improve Performance (Wait-Time Reduction & Duplicate Prevention)

---

### Academic & Student Metadata
* **Student Name:** Bhupinder Singh
* **Roll Number:** 2410301011
* **Course Code & Title:** BBAT104 – Fundamentals of Total Quality Management
* **Department / Class:** Computer Science & Engineering (CSE - A)
* **Assigned Quality Goal:** Q02 – Improve Performance
* **Deliverable Milestone:** Review 1 – System Architecture Flowcharts & Technical Design
* **Repository Name:** `BBAT104_TQM_2410301011`
* **Version:** 1.0.0
* **Date:** September 2026

---

## 1. HIGH-LEVEL ARCHITECTURAL OVERVIEW

The High-Performance Hospital Management System (HMS) is architected using a decoupled **3-Tier Layered Architecture** engineered specifically to satisfy the strict throughput and latency targets defined under **Quality Goal Q02**.

```mermaid
graph TD
    subgraph Presentation_Layer["1. Presentation Tier (Modern Responsive GUI)"]
        UI_Login["Authentication & RBAC Gateway"]
        UI_Dash["Performance Dashboard (Sub-1s Cockpit)"]
        UI_Patients["Patient Management & Fast Search-as-you-type"]
        UI_Doctors["Doctor Directory & Availability Grid"]
        UI_Scheduler["Appointment Queue & Token Dispatcher"]
        UI_Billing["Invoicing & Payment Processing"]
        UI_Reports["Analytical Reporting & Data Export"]
    end

    subgraph Business_Logic_Layer["2. Business Logic & Performance Engine"]
        Engine_Auth["Auth & Session Manager (SHA-256)"]
        Engine_Search["Debounced Fast Search Controller (200ms)"]
        Engine_PokaYoke["Poka-Yoke Duplicate Validation Guard"]
        Engine_Queue["Queue Sequencer & Wait-Time Calculator"]
        Engine_CSV["High-Throughput Batch CSV Ingestion Engine"]
        Engine_Pandas["Vectorized Analytical Aggregator (Pandas)"]
        Engine_Telemetry["Performance Telemetry & SLA Logger"]
    end

    subgraph Data_Persistence_Layer["3. Data Persistence Tier (Optimized SQLite)"]
        PRAGMA_WAL["WAL Mode & 64MB Cache PRAGMA Settings"]
        DB_Core[("SQLite Database File: hms_database.db")]
        BTree_Idx["B-Tree Indexes:<br/>idx_patients_name, idx_patients_phone, idx_appointments_date_status"]
    end

    Presentation_Layer --> Business_Logic_Layer
    Business_Logic_Layer --> Data_Persistence_Layer
```

---

## 2. DETAILED PROCESS FLOWCHARTS

### 2.1 Patient Ingestion & Poka-Yoke Duplicate Prevention Flowchart
* **TQM Focus:** Error-Proofing (Poka-Yoke) at entry point to prevent record duplication and reduce search confusion.

```mermaid
flowchart TD
    Start([User Initiates Patient Registration]) --> Input[Fill Patient Details:<br/>Name, Gender, Age, Phone, Address, Blood Group]
    Input --> ValidateFormat{Client-side Format Validation<br/>Valid Phone: 10 Digits?<br/>Age: 0 to 125?}
    
    ValidateFormat -- "No (Invalid Data)" --> AlertFormat[Display Inline Error:<br/>'Invalid Phone or Age Format'] --> Input
    ValidateFormat -- "Yes (Valid Data)" --> CheckDB{Execute Indexed Duplicate Check<br/>SELECT id FROM patients WHERE phone = ?}
    
    CheckDB -- "Record Found (Duplicate)" --> PokaYokeAlert["Poka-Yoke Triggered!<br/>Warning: Patient with this phone already exists.<br/>Display Existing UHID & Profile"]
    PokaYokeAlert --> UserChoice{Action Selection}
    UserChoice -- "View Existing Record" --> OpenExisting[Load Existing Patient Profile] --> End([Process Concluded])
    UserChoice -- "Correct Phone Number" --> Input
    
    CheckDB -- "No Record Found (Unique)" --> GenUHID["Generate Standardized UHID<br/>(e.g., UHID-2026-0042)"]
    GenUHID --> InsertDB["Execute INSERT INTO patients<br/>inside Atomic Transaction"]
    InsertDB --> RefreshCache[Update Local View & Telemetry]
    RefreshCache --> SuccessMsg[Display Success Banner & Token Ready]
    SuccessMsg --> End
```

---

### 2.2 Fast Search-as-You-Type Engine Flowchart
* **TQM Focus:** Reducing Front-Desk Waiting Bottleneck ($< 100\text{ ms}$ response time via Debounce + B-Tree Index).

```mermaid
flowchart TD
    KeyStroke([User Types Keystroke in Search Bar]) --> ResetTimer[Reset Active Debounce Timer]
    ResetTimer --> StartTimer[Start 200ms Delay Timer]
    StartTimer --> WaitInput{Did User Type Another Key<br/>within 200ms?}
    
    WaitInput -- "Yes" --> KeyStroke
    WaitInput -- "No (Timer Expired)" --> CaptureQuery[Capture Query String & Trim Whitespace]
    
    CaptureQuery --> CheckLength{Length >= 1 Character?}
    CheckLength -- "No (Empty)" --> LoadDefault["Load Recent 50 Records<br/>(LIMIT 50)"] --> RenderGrid[Render Results in Virtualized Grid]
    
    CheckLength -- "Yes" --> StartStopwatch[Start Execution Microsecond Timer]
    StartStopwatch --> QueryType{Query Type Pattern?}
    
    QueryType -- "Numeric" --> SearchPhone["Query using idx_patients_phone:<br/>SELECT * FROM patients WHERE phone LIKE 'query%'"]
    QueryType -- "Starts with UHID-" --> SearchUHID["Query using idx_patients_uhid:<br/>SELECT * FROM patients WHERE uhid = 'query'"]
    QueryType -- "Alphabetic" --> SearchName["Query using idx_patients_name:<br/>SELECT * FROM patients WHERE full_name LIKE '%query%'"]
    
    SearchPhone --> ExecDB[(SQLite B-Tree Index Scan)]
    SearchUHID --> ExecDB
    SearchName --> ExecDB
    
    ExecDB --> FetchResults[Fetch Matched Rows]
    FetchResults --> StopStopwatch[Stop Timer & Compute Latency ms]
    StopStopwatch --> LogTelemetry["Record in performance_logs<br/>(e.g., Latency: 12.4 ms)"]
    LogTelemetry --> RenderGrid
    RenderGrid --> DisplayLatency[Update Status Bar: 'Found N records in X.X ms']
    DisplayLatency --> Done([Ready for Selection])
```

---

### 2.3 Appointment Scheduling & Wait-Time Minimization Flowchart
* **TQM Focus:** Cycle Time Reduction & Queue Optimization.

```mermaid
flowchart TD
    ApptStart([Patient Arrives / Books Appointment]) --> SelectDoc[Select Available Doctor & Department]
    SelectDoc --> CheckDocStatus{Is Doctor 'Available'?}
    
    CheckDocStatus -- "No (On Leave / Surgery)" --> AlertDoc[Prompt Alternative Doctor] --> SelectDoc
    CheckDocStatus -- "Yes" --> AssignSlot[Select Appointment Date & Time Slot]
    
    AssignSlot --> GenToken["Generate Sequential Token Number<br/>Token # = Current Max + 1"]
    GenToken --> SaveAppt["INSERT INTO appointments<br/>(status = 'Scheduled')"]
    SaveAppt --> PatientArrives([Patient Arrives at Clinic OPD])
    
    PatientArrives --> ReceptionCheckIn["Receptionist Clicks 'Check-In'<br/>Set status = 'Waiting'<br/>Record check_in_time = CURRENT_TIMESTAMP"]
    ReceptionCheckIn --> QueueDisplay[Patient Added to Doctor's Waiting Queue Display]
    
    QueueDisplay --> DocCalls["Doctor Clicks 'Call Next Patient'<br/>Set status = 'In-Consultation'<br/>Record consultation_start_time = CURRENT_TIMESTAMP"]
    DocCalls --> CalcWait["Calculate Wait Time (Minutes):<br/>wait_time_minutes = (consultation_start - check_in)"]
    
    CalcWait --> Consultation([Doctor Conducts Medical Consultation])
    Consultation --> DocCompletes["Doctor Clicks 'Complete Consultation'<br/>Set status = 'Completed'<br/>Record consultation_end_time = CURRENT_TIMESTAMP"]
    
    DocCompletes --> TriggerBilling[Forward to Billing Desk with Fee Structure]
    TriggerBilling --> UpdateKPI["Update Today's Avg Wait Time KPI on Dashboard"]
    UpdateKPI --> ApptDone([Cycle Complete])
```

---

### 2.4 High-Throughput Bulk CSV Import Flowchart
* **TQM Focus:** Eliminating Manual Data Entry Errors and Accelerating Ingestion ($> 500\text{ records/sec}$).

```mermaid
flowchart TD
    CSVStart([User Selects CSV File for Bulk Import]) --> ReadFile[Read CSV Header & Rows into Memory via Pandas]
    ReadFile --> ValidateHeader{Header Schema Matches<br/>uhid, full_name, gender, age, phone, etc.?}
    
    ValidateHeader -- "No" --> RejectFile[Display Error: 'Invalid CSV Column Format'] --> CSVDone([Process Aborted])
    ValidateHeader -- "Yes" --> StartBatchTimer[Start Throughput Benchmark Timer]
    
    StartBatchTimer --> OpenTx["Open SQLite Transaction<br/>BEGIN TRANSACTION;"]
    OpenTx --> FetchExisting["Fetch Existing Phone & UHID Set<br/>into In-Memory Hash Set (O(1) lookup)"]
    
    FetchExisting --> LoopRow[Iterate through CSV Rows]
    LoopRow --> CheckCollision{Phone or UHID in<br/>Existing Hash Set?}
    
    CheckCollision -- "Yes (Duplicate)" --> LogDup["Append to duplicates_list<br/>(Skip Row)"]
    CheckCollision -- "No (Unique)" --> SanitizeRow[Sanitize & Format Row Data] --> AddToBatch[Add to Batch Buffer]
    
    LogDup --> HasMore{More Rows in CSV?}
    AddToBatch --> HasMore
    
    HasMore -- "Yes" --> LoopRow
    HasMore -- "No" --> ExecBatch["Execute Bulk Insertion via<br/>cursor.executemany(INSERT INTO patients...)"]
    
    ExecBatch --> CommitTx["Commit SQLite Transaction<br/>COMMIT;"]
    CommitTx --> StopBatchTimer[Stop Benchmark Timer]
    
    StopBatchTimer --> CalcMetrics["Calculate Ingestion Rate:<br/>Throughput = Valid Rows / Elapsed Seconds"]
    CalcMetrics --> ShowSummaryModal["Display Ingestion Summary:<br/>Total Processed: N<br/>Successful: S<br/>Duplicates Skipped: D<br/>Throughput: X records/sec"]
    ShowSummaryModal --> CSVDone
```

---

### 2.5 Real-Time Performance Dashboard Aggregation Flowchart
* **TQM Focus:** Executive Transparency & Real-Time Quality Metric Monitoring ($< 1.0\text{ s}$ SLA).

```mermaid
flowchart TD
    DashInit([Dashboard Tab Opened or Refreshed]) --> StartBench[Start Stopwatch Timer]
    StartBench --> ParallelQuery["Execute Single Optimized Aggregate Query:<br/>1. Today's Patient Count (COUNT(*))<br/>2. Active Waiting Queue (status = 'Waiting')<br/>3. Available Doctors & Rooms (status = 'Available')<br/>4. Today's Mean Waiting Time (AVG(wait_time_minutes))"]
    
    ParallelQuery --> IndexSeek[(B-Tree Index Scan on idx_appointments_date_status)]
    IndexSeek --> ResultsReady[Extract Tuple: (Patients, Queue, ActiveDocs, AvgWait)]
    
    ResultsReady --> ComputeOccupancy["Compute Room Occupancy Rate:<br/>Occupancy % = (Busy Rooms / Total Rooms) * 100"]
    ComputeOccupancy --> StopBench[Stop Stopwatch Timer]
    
    StopBench --> CheckSLA{Elapsed Time < 1000 ms?}
    CheckSLA -- "Yes (Meets SLA)" --> SetGreen[Status: SLA COMPLIANT (Green Indicator)]
    CheckSLA -- "No (SLA Breach)" --> SetRed[Status: PERFORMANCE DEGRADED (Amber/Red)]
    
    SetGreen --> UpdateCards[Update UI Metric Cards & Progress Bars]
    SetRed --> UpdateCards
    UpdateCards --> DashFinish([Dashboard Rendered])
```

---

## 3. DATA FLOW DIAGRAMS (DFD)

### 3.1 DFD Level 0: Context Diagram
The Level 0 Context Diagram establishes the boundaries of the Hospital Management System, identifying external entities (Receptionist, Doctor, Billing Clerk, Super Admin, External CSV) and the primary data streams entering and exiting the boundary.

```mermaid
graph TD
    subgraph External_Entities["External System Actors"]
        Receptionist["Receptionist / Front Desk"]
        Doctor["Attending Doctor / Physician"]
        BillingClerk["Billing Clerk / Cashier"]
        Admin["Hospital Administrator"]
        CSVFile["External Patient CSV Files"]
    end

    HMS(("High-Performance<br/>Hospital Management System<br/>(BBAT104 - Q02)"))

    Receptionist -- "Patient Details, Appointment Request, Check-in" --> HMS
    HMS -- "UHID, Token Slip, Search Results, Queue Status" --> Receptionist

    Doctor -- "Consultation Status (Start, End, Notes)" --> HMS
    HMS -- "Assigned Patient Queue, Medical History" --> Doctor

    BillingClerk -- "Payment Mode, Tax Adjustments" --> HMS
    HMS -- "Itemized Bills, Outstanding Dues, Receipts" --> BillingClerk

    Admin -- "Doctor Onboarding, User Roles, SQC Thresholds" --> HMS
    HMS -- "Real-Time Dashboard, SQC Charts, Audit Logs" --> Admin

    CSVFile -- "Bulk Patient Records (CSV)" --> HMS
    HMS -- "Ingestion & Duplicate Rejection Summary" --> Admin
```

---

### 3.2 DFD Level 1: Subsystem Decomposition
The Level 1 DFD decomposes the system into its primary operational sub-processes and data stores.

```mermaid
graph TD
    subgraph Processes["Core Subsystems"]
        P1["1.0 Patient Ingestion & Poka-Yoke Duplicate Validation"]
        P2["2.0 Fast Search & Indexed Retrieval Engine"]
        P3["3.0 Doctor Directory & Slot Scheduling"]
        P4["4.0 OPD Queue Management & Wait-Time Tracker"]
        P5["5.0 Billing & Invoice Generation"]
        P6["6.0 Real-time KPI Dashboard & Pandas Analytics"]
    end

    subgraph DataStores["Relational Database Stores (SQLite WAL)"]
        D1[("D1: Patients Store (Indexed)")]
        D2[("D2: Doctors Store")]
        D3[("D3: Appointments & Queue Store")]
        D4[("D4: Billing & Invoicing Store")]
        D5[("D5: Performance Telemetry Store")]
    end

    %% Flow connections
    P1 -- "Validated Unique Patient" --> D1
    D1 -- "Phone/UHID Collision Check" --> P1

    P2 -- "B-Tree Index Scan" --> D1
    D1 -- "Matched Patient Tuples (< 100ms)" --> P2

    P3 -- "Doctor Availability & Details" --> D2
    D2 -- "Active Doctor Roster" --> P4

    P4 -- "Create Scheduled Token" --> D3
    P4 -- "Log check_in & consult_start" --> D3
    D3 -- "Queue Position & Elapsed Minutes" --> P4

    P4 -- "Completed Consultation Event" --> P5
    P5 -- "Itemized Invoice Record" --> D4

    D3 -- "Today's Wait Times & Queue Count" --> P6
    D4 -- "Revenue Aggregate" --> P6
    D5 -- "Query Latencies" --> P6
    P6 -- "Write SLA Metrics" --> D5
```

---

## 4. ENTITY-RELATIONSHIP (ER) DIAGRAM & DATABASE ARCHITECTURE

The relational schema implements third normal form (3NF) structures with strict referential integrity and covering B-Tree indexes to ensure optimal query plans.

```mermaid
erDiagram
    USERS {
        int id PK
        string username UK
        string password_hash
        string full_name
        string role
        string status
        timestamp created_at
    }

    PATIENTS {
        int id PK
        string uhid UK
        string full_name
        string gender
        int age
        string phone UK
        string email
        string address
        string blood_group
        timestamp created_at
        timestamp updated_at
    }

    DOCTORS {
        int id PK
        string doctor_code UK
        string full_name
        string specialization
        string phone
        string email
        string room_no
        float consultation_fee
        string status
        timestamp created_at
    }

    APPOINTMENTS {
        int id PK
        string appointment_number UK
        int patient_id FK
        int doctor_id FK
        date appointment_date
        time appointment_time
        int token_number
        string status
        timestamp check_in_time
        timestamp consultation_start_time
        timestamp consultation_end_time
        float wait_time_minutes
        string notes
        timestamp created_at
    }

    BILLING {
        int id PK
        string invoice_number UK
        int appointment_id FK
        int patient_id FK
        float consultation_amount
        float medicine_amount
        float lab_amount
        float tax_amount
        float total_amount
        string payment_mode
        string payment_status
        date invoice_date
        timestamp created_at
    }

    PERFORMANCE_LOGS {
        int id PK
        string operation_type
        int record_count
        float execution_time_ms
        string status
        string details
        timestamp logged_at
    }

    PATIENTS ||--o{ APPOINTMENTS : "schedules"
    DOCTORS ||--o{ APPOINTMENTS : "attends"
    PATIENTS ||--o{ BILLING : "billed_for"
    APPOINTMENTS ||--o| BILLING : "invoiced_under"
```

---

## 5. TECHNICAL DEFENSE OF PERFORMANCE DESIGN DECISIONS

### 5.1 Why SQLite in WAL Mode?
For an on-premise healthcare clinic or OPD workstation, SQLite in Write-Ahead Logging mode (`PRAGMA journal_mode = WAL;`) provides major advantages:
1. **Concurrent Read/Write Isolation:** Readers do not block writers, and writers do not block readers. When the reception desk writes new patient records, the doctor's queue monitor can read appointments simultaneously with zero locking latency.
2. **Zero Network Latency Overhead:** Client-server databases (e.g. MySQL, PostgreSQL) introduce TCP socket overhead (typically 1–5 ms per round-trip). Embedded SQLite executes in-process, reading cached B-Tree pages directly in microsecond timeframes.
3. **Zero Configuration Deployment:** Clinics require turnkey software with no database server daemon configuration, making it robust against network disconnects.

### 5.2 How B-Tree Indexing Transforms Latency ($O(N) \rightarrow O(\log N)$)
In a baseline, un-indexed table with 50,000 patient records:
* An un-indexed search like `SELECT * FROM patients WHERE phone = '9876543210'` forces SQLite to perform a **Full Table Scan**, reading all 50,000 pages from disk into RAM.
* With the B-Tree index `idx_patients_phone`, SQLite traverses an index tree of depth $\approx 3$ to $4$, reducing disk page reads from 50,000 to under 5. This brings query latency down from $\approx 850\text{ ms}$ to **$< 2\text{ ms}$**.

### 5.3 Debounce Strategy for UI Responsiveness
In a standard GUI, triggering a database query on every keystroke causes search thread thrashing when an operator types quickly (e.g., typing a 10-digit phone number fires 10 consecutive queries).
* By introducing a **200 ms debounce timer**, queries fire only when typing pauses.
* This cuts database operations by **$80\%$ to $90\%$**, keeping CPU utilization minimal and maintaining a smooth 60 FPS user interface.

### 5.4 Batch Transaction Processing vs. Individual Inserts
When importing a CSV with 5,000 patient rows:
* Executing individual `INSERT` statements commits a transaction for every row, resulting in 5,000 disk sync writes ($\approx 40$ seconds total, or 125 records/sec).
* By wrapping the batch inside a single transaction (`BEGIN TRANSACTION` followed by `cursor.executemany(...)` and `COMMIT`), SQLite performs a single coordinated disk flush. This achieves ingestion rates of **$1,200+$ records/sec** ($\approx 4$ seconds total), representing an order-of-magnitude performance gain.

---

## 6. REVIEW 1 VERIFICATION & SIGN-OFF
* **Submitted By:** Bhupinder Singh (Roll No: 2410301011)
* **Status:** Complete for Review 1 Presentation.
