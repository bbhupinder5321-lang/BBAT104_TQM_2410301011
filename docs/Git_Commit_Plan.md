# GIT COMMIT PLAN (MINIMUM 30 COMMITS)
## College Course: BBAT104 – Fundamentals of Total Quality Management (TQM)
### Project: High-Performance Hospital Management System (HMS)
**Student:** Bhupinder Singh | **Roll No:** 2410301011 | **Branch:** CSE - A
**Repo Name:** `BBAT104_TQM_2410301011`

---

This commit plan outlines a realistic, progressive engineering workflow mapping directly across the academic project reviews. It ensures your GitHub repository maintains a clean, professional commit history with descriptive Conventional Commit messages.

| # | Commit Type | Scope | Commit Message & Description | Targeted Phase |
| :-: | :--- | :--- | :--- | :---: |
| **01** | `chore` | repo | `initial commit: configure .gitignore and repository layout` | Review 1 Setup |
| **02** | `chore` | deps | `build: specify python dependencies in requirements.txt` | Review 1 Setup |
| **03** | `docs` | readme | `docs: add comprehensive project README with student details and TQM Q02 goals` | Review 1 Setup |
| **04** | `feat` | schema | `schema: define optimized SQLite DDL with B-Tree indexes and unique constraints` | Review 1 Setup |
| **05** | `data` | seed | `data: add realistic sample patient CSV dataset for bulk ingestion testing` | Review 1 Setup |
| **06** | `docs` | srs | `docs(review-1): author IEEE 830-compliant Software Requirements Specification` | Review 1 Delivery |
| **07** | `docs` | arch | `docs(review-1): author 3-tier system architecture and process flowcharts` | Review 1 Delivery |
| **08** | `docs` | dfd | `docs(review-1): add DFD level 0, level 1, and ER diagrams with Poka-Yoke logic` | Review 1 Delivery |
| **09** | `feat` | db | `feat(core): implement SQLite connection manager with WAL mode PRAGMAs` | Review 2 App Build |
| **10** | `feat` | auth | `feat(auth): implement role-based authentication module with SHA-256 hashing` | Review 2 App Build |
| **11** | `feat` | models | `feat(models): create patient and doctor relational data models` | Review 2 App Build |
| **12** | `feat` | models | `feat(models): create appointment queue and billing invoice data models` | Review 2 App Build |
| **13** | `feat` | poka-yoke | `feat(patients): implement Poka-Yoke duplicate validation on phone and UHID` | Review 2 App Build |
| **14** | `feat` | gui | `feat(gui): build modern main application shell and navigation bar` | Review 2 App Build |
| **15** | `feat` | gui | `feat(gui): create secure login window with role-based view routing` | Review 2 App Build |
| **16** | `feat` | search | `feat(q02): implement debounced fast search-as-you-type (< 100ms response)` | Review 2 Q02 Build |
| **17** | `perf` | indexing | `perf(q02): bind covering B-Tree indexes to patient lookup and appointment queries` | Review 2 Q02 Build |
| **18** | `feat` | doctors | `feat(doctors): add doctor directory management and availability status toggle` | Review 2 App Build |
| **19** | `feat` | scheduler | `feat(appointments): implement appointment booking with sequential token issuance` | Review 2 App Build |
| **20** | `feat` | telemetry | `feat(queue): implement check-in and consultation wait-time telemetry tracking` | Review 2 App Build |
| **21** | `feat` | billing | `feat(billing): create itemized billing module with payment reconciliation` | Review 2 App Build |
| **22** | `feat` | csv | `feat(q02): implement high-throughput transactional CSV bulk importer (> 500 rps)` | Review 2 Q02 Build |
| **23** | `feat` | reports | `feat(q02): implement vectorized Pandas report generator with CSV/Excel export` | Review 2 Q02 Build |
| **24** | `feat` | dashboard | `feat(q02): build real-time executive dashboard loading metrics in under 1 second` | Review 2 Q02 Build |
| **25** | `test` | benchmark | `test(benchmark): benchmark query latencies and verify Q02 SLA compliance` | Review 2 Verification |
| **26** | `docs` | sipoc | `docs(review-3): author detailed SIPOC process map for OPD patient flow` | Review 3 Delivery |
| **27** | `docs` | fmea | `docs(review-3): construct FMEA matrix evaluating RPN for performance defects` | Review 3 Delivery |
| **28** | `feat` | sqc | `feat(review-4): create interactive Matplotlib Pareto Chart of system defects` | Review 4 Delivery |
| **29** | `feat` | sqc | `feat(review-4): create Ishikawa Fishbone diagram for patient waiting delays` | Review 4 Delivery |
| **30** | `docs` | pdca | `docs(review-4): document Deming PDCA continuous improvement cycle log` | Review 4 Delivery |
| **31** | `docs` | manual | `docs(review-5): compile comprehensive user manual and operations handbook` | Review 5 Delivery |
| **32** | `docs` | viva | `docs(review-5): add final viva voce defense guide and TQM justification points` | Review 5 Delivery |

---

### Suggested Git Commands for Step-by-Step Commit Execution:
```bash
# Example for Commit 01
git init
git add .gitignore
git commit -m "chore: configure .gitignore and repository layout"

# Example for Commit 02
git add requirements.txt
git commit -m "build: specify python dependencies in requirements.txt"

# Example for Commit 03
git add README.md
git commit -m "docs: add comprehensive project README with student details and TQM Q02 goals"

# Example for Commits 04 - 05
git add data/
git commit -m "schema: define optimized SQLite DDL with B-Tree indexes and sample dataset"

# Example for Commits 06 - 08 (Review 1)
git add docs/SRS_Document.md docs/System_Architecture.md docs/Git_Commit_Plan.md
git commit -m "docs(review-1): author IEEE 830 SRS document, system architecture flowcharts, and commit plan"
```
