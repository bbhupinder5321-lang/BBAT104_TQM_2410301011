# FINAL VIVA VOCE DEFENSE & TALKING POINTS GUIDE
## College Course: BBAT104 – Fundamentals of Total Quality Management (TQM)
### Project: High-Performance Hospital Management System (HMS)
**Student:** Bhupinder Singh | **Roll No:** 2410301011 | **Branch / Class:** CSE - A
**Assigned Quality Goal:** **Q02 – Improve Performance**
**Core TQM Application:** Reduce patient wait times & prevent record duplication

---

## 1. 30-SECOND ELEVATOR PITCH (HOW TO OPEN YOUR VIVA)

> *"Good morning, esteemed evaluators. My name is **Bhupinder Singh** (Roll No: 2410301011). In this BBAT104 project, I developed an optimized **Hospital Management System** specifically engineered to fulfill **Quality Goal Q02: Improve Performance**.*
>
> *Traditional healthcare OPDs suffer from two critical quality defects: **unacceptable patient waiting times** and **duplicate medical records**. By applying foundational TQM methodologies—including **Deming's PDCA Cycle**, **Poka-Yoke error-proofing**, **Pareto Analysis**, and **FMEA risk mitigation**—I engineered a software system that eliminates record duplication at the point of entry and slashes patient search latency from **1,850 milliseconds down to 4.2 milliseconds**, achieving an overall **94.1% reduction in system Risk Priority Number (RPN)**.*
>
> *The entire solution is built in Python, Tkinter, and an optimized SQLite Write-Ahead Logging persistence layer, accompanied by complete empirical SLA telemetry."*

---

## 2. DEFENDING YOUR 7 TQM TOOL CHOICES

### Tool 1: SIPOC Process Map
* **Viva Question:** *"Why did you start with a SIPOC diagram instead of immediately drawing flowcharts or coding?"*
* **Defensive Answer:** 
  > *"SIPOC (Suppliers, Inputs, Process, Outputs, Customers) defines the high-level boundary of our system before writing a single line of code. In healthcare, failure often occurs at interfaces—such as inaccurate phone numbers provided by patients or unclear availability schedules from doctors. SIPOC allowed us to translate the **Voice of the Customer (VOC)**—which demands short wait times and zero administrative errors—directly into technical **Critical to Quality (CTQ)** parameters: sub-100ms search latency, sub-1-second dashboard load time, and zero duplicate entries."*

---

### Tool 2: Failure Mode and Effects Analysis (FMEA)
* **Viva Question:** *"How did FMEA guide your software architecture?"*
* **Defensive Answer:**
  > *"FMEA is a proactive risk-prioritization tool. We evaluated failure modes using the Risk Priority Number: $RPN = \text{Severity} \times \text{Occurrence} \times \text{Detection}$.*
  > *In the baseline system, our highest risk failure modes were **FM-5 (Excessive Queue Waiting Time, RPN = 360)**, **FM-1 (Slow Patient Search, RPN = 336)**, and **FM-2 (Duplicate Patient Records, RPN = 320)**.*
  > *FMEA proved that rather than adding cosmetic features, our engineering effort had to focus strictly on database B-Tree indexing, Poka-Yoke schema constraints, and automated token queues. Post-implementation, our cumulative RPN dropped from **2,034 down to 120**, representing a **94.1% reduction in total operational risk**."*

---

### Tool 3: Defect Checksheet
* **Viva Question:** *"What was the role of the Checksheet in your data collection?"*
* **Defensive Answer:**
  > *"TQM is fundamentally data-driven; as Deming famously stated, 'In God we trust; all others must bring data.' Our 30-day observational checksheet logged 384 operational incidents. Crucially, the checksheet revealed that **63.8% of all system failures occurred during the morning rush between 08:00 and 12:00**.*
  > *This provided empirical proof that the primary bottleneck was database contention under concurrent morning read/write loads, directly pointing us to SQLite's Write-Ahead Logging (WAL) and B-Tree indexing."*

---

### Tool 4: Pareto Analysis (80/20 Rule)
* **Viva Question:** *"How did you apply the Pareto Principle to software development?"*
* **Defensive Answer:**
  > *"Our Pareto Chart proved that out of 6 defect categories, just 3 categories—**Slow Search (37.0%)**, **Queue Waiting Delays (30.7%)**, and **Duplicate Profiles (16.7%)**—accounted for **84.4% of all hospital failures**.*
  > *By applying the Pareto 80/20 rule, we did not waste time optimizing minor issues like billing layout adjustments. We solved the **'Vital Few'** defects first, eliminating over four-fifths of the hospital's operational friction."*

---

### Tool 5: Ishikawa (Fishbone / Cause-and-Effect) Diagram
* **Viva Question:** *"Why did you use the Fishbone diagram when you already had the Pareto chart?"*
* **Defensive Answer:**
  > *"The Pareto chart tells us **WHAT** the primary defects are, but the Ishikawa Fishbone diagram tells us **WHY** they happen.*
  > *Using the 4M/4P framework (People, Process, Technology, Environment), we broke down 'Excessive Patient Waiting Time' into actionable root causes:*
  > *Under **Technology**, we identified unindexed full-table scans and UI thread thrashing.*
  > *Under **Process**, we identified unsequenced token distribution and absence of pre-registration checks.*
  > *Under **People**, we identified doctor consultation delays and clerk fatigue.*
  > *This ensured our software countermeasures directly targeted the root causes rather than superficial symptoms."*

---

### Tool 6: Poka-Yoke (Mistake-Proofing)
* **Viva Question:** *"Where is Poka-Yoke implemented in your codebase, and how does it work?"*
* **Defensive Answer:**
  > *"Poka-Yoke means mistake-proofing at the source to make errors impossible. We implemented Poka-Yoke at two distinct layers:*
  > *1. **Database Schema Layer:** We enforced `UNIQUE(phone)` and `UNIQUE(uhid)` in `data/schema.sql`. The database physically refuses duplicate records.*
  > *2. **Real-Time UI Interception Layer:** In `src/modules/patient_view.py`, as a receptionist types a 10-digit mobile number, a background indexed query searches for existing profiles. If a match is found, the system immediately presents an amber warning with the existing patient's name and UHID, preventing duplicate submission.*
  > *This drove duplicate record generation down to **0.0%**, achieving Shigeo Shingo's zero-defect standard."*

---

### Tool 7: Deming's PDCA Continuous Improvement Cycle
* **Viva Question:** *"Explain the 4 phases of your PDCA cycle for this project."*
* **Defensive Answer:**
  > *"• **Plan:** We audited the baseline system, measured an average wait time of 38.4 minutes, 8.4% duplicate records, and 1,850 ms search latency, and set our Q02 performance SLAs.*
  > *• **Do:** We implemented our 5 performance countermeasures: B-Tree indexes, WAL mode, a 200ms debounce timer, Poka-Yoke phone validation, batch CSV ingestion, and the sub-second Executive Dashboard.*
  > *• **Check:** We validated our system using `src/benchmark.py`. Search latency dropped to 4.2 ms, wait times dropped to 11.2 minutes, duplicates dropped to 0%, and CSV import reached 1,240 records/sec.*
  > *• **Act:** We standardized these configurations into `schema.sql` and established standard operating procedures for reception staff to sustain the quality gains."*

---

## 3. DEFENDING YOUR TECHNICAL ARCHITECTURAL DECISIONS (Q02)

| Technical Decision | Why It Was Chosen | What Would Happen Without It | Quantitative Proof / Benchmark |
| :--- | :--- | :--- | :--- |
| **SQLite with WAL Mode** (`PRAGMA journal_mode = WAL`) | Allows concurrent reads and writes. Readers never block writers and writers never block readers. In-process with zero network socket latency. | In default Rollback Journal mode, writing a patient record locks the entire database, causing `OperationalError: database locked` during morning surges. | Zero database timeouts recorded under high concurrency. |
| **B-Tree Composite Indexes** (`idx_patients_phone`, etc.) | Lowers algorithmic complexity from linear scan $O(N)$ to logarithmic tree seek $O(\log N)$. Reduces disk page reads from 50,000 to $\approx 3$. | Without indexes, SQLite must scan every single row on disk, spiking CPU to 100% and taking 1.8 to 2.5 seconds per search. | Search latency dropped from **1,850 ms to 4.2 ms** (**99.7% faster**). |
| **200ms Keystroke Debounce** | Delays search execution until the user pauses typing for 200ms, eliminating redundant queries. | Typing a 10-digit phone number or name fires 10 consecutive database queries, causing severe GUI thread freezing. | Cuts database query invocations by **$85\%$ to $90\%$**; UI runs at smooth 60 FPS. |
| **Vectorized Pandas Processing** | Vectorized C-level algorithms (`pd.read_sql_query`) perform aggregations directly across memory arrays. | Python `for` loops iterating over thousands of tuples in memory freeze the GUI for 4 to 6 seconds. | Complex reports generated in **$< 30\text{ ms}$** (SLA $< 1500\text{ ms}$). |
| **Batch Transaction CSV Import** (`executemany` + `BEGIN/COMMIT`) | Coordinates a single disk flush for the entire dataset rather than committing after each row. | Individual inserts execute a disk write synchronization for every row, crawling at 15–20 records/sec. | Ingestion throughput accelerated to **$1,240\text{ records/sec}$** (**68x faster**). |

---

## 4. TOUGH VIVA QUESTIONS & MODEL ANSWERS

### Q1: "Why did you choose SQLite instead of an enterprise client-server database like PostgreSQL or MySQL?"
* **Model Answer:**
  > *"For a local hospital clinic or OPD department workstation, SQLite in WAL mode offers superior latency and reliability compared to client-server architectures:*
  > *1. **Zero Network Latency:** Client-server databases incur TCP socket round-trips of 1 to 5 ms per query. SQLite runs in-process, accessing cached B-Tree memory pages in microseconds.*
  > *2. **Zero Configuration Deployment:** Clinics cannot afford dedicated database administrators. SQLite is embedded, self-contained, and immune to network disconnects.*
  > *3. **Concurrency:** In WAL mode, SQLite easily supports multiple concurrent threads with zero lock contention, satisfying all Q02 performance requirements."*

---

### Q2: "What is the difference between Deming's PDCA cycle and Juran's Quality Trilogy?"
* **Model Answer:**
  > *"**Deming's PDCA Cycle** is an iterative operational mechanism for continuous, scientific hypothesis testing (Plan, Do, Check, Act).*
  > *In contrast, **Juran's Quality Trilogy** divides quality management into three broad organizational phases:*
  > *1. **Quality Planning:** Identifying customers and designing processes that meet their needs (our Review 1 SRS and SIPOC).*
  > *2. **Quality Control:** Measuring actual performance against targets during operations (our Review 2 Telemetry and Review 4 Checksheet).*
  > *3. **Quality Improvement:** Systematically breaking through to unprecedented levels of performance (our Q02 countermeasures that reduced search latency from 1,850 ms to 4.2 ms)."*

---

### Q3: "How does your system prove that patient wait times are actually reduced?"
* **Model Answer:**
  > *"In `src/models/appointment.py`, we implement automated state timestamping:*
  > *When a patient arrives, the receptionist clicks 'Check-In', which stamps `check_in_time`.*
  > *When the doctor calls the patient, clicking 'Call into Consultation' stamps `consultation_start_time` and automatically computes:*
  > $$\text{Wait Time} = \frac{\text{consultation\_start\_time} - \text{check\_in\_time}}{60}$$
  > *These wait times are aggregated in real time by the **Executive Dashboard**, giving hospital administrators instant visibility if the average wait exceeds the 15-minute SLA."*

---

### Q4: "What is the 80/20 rule and how did you verify it mathematically in your project?"
* **Model Answer:**
  > *"The 80/20 rule (Pareto Principle) states that 80% of problems stem from 20% of causes. In our checksheet data of 384 incidents, we sorted defects by frequency:*
  > *1. Slow Search: 142 incidents (37.0%)*
  > *2. High Wait Times: 118 incidents (30.7%)*
  > *3. Duplicate Records: 64 incidents (16.7%)*
  > *Cumulative sum $= 142 + 118 + 64 = 324$ incidents out of 384, which is **exactly $84.4\%$**.*
  > *Thus, addressing just these 3 defects resolved over 84% of total hospital failures."*

---

## 5. SUMMARY CHECKLIST FOR VIVA DAY
* [x] Know your metadata: **Bhupinder Singh | Roll No: 2410301011 | CSE - A | Course: BBAT104 | Goal: Q02**.
* [x] Have the app ready to run with `python src/main.py` using the 1-click **Admin** login.
* [x] Have the automated benchmark ready with `python src/benchmark.py` to show the **Q02 Quality Scorecard**.
* [x] Open the **Executive Dashboard** to show the live sub-second render badge ($\approx 21\text{ ms}$).
* [x] Demonstrate **Poka-Yoke** live: try registering a patient with an existing phone (`9876543210`) and point out the real-time duplicate warning banner!
