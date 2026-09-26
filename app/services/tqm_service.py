class TQMService:
    """
    Provides TQM analysis data for the Hospital Management System.

    Current focus:
    Q02 - Improve Performance
    """

    def get_sipoc_data(self):
        """
        Returns SIPOC information for the hospital system's
        patient/appointment performance process.
        """

        return {
            "suppliers": [
                "Reception Staff",
                "Doctors",
                "Hospital Administration",
                "System Administrator"
            ],

            "inputs": [
                "Patient information",
                "Doctor information",
                "Appointment information",
                "Check-in time",
                "Consultation start time",
                "Database records"
            ],

            "process": [
                "Register patient",
                "Search patient record",
                "Book appointment",
                "Patient check-in",
                "Start consultation",
                "Store and retrieve records",
                "Generate reports"
            ],

            "outputs": [
                "Patient record",
                "Appointment record",
                "Waiting-time measurement",
                "Dashboard metrics",
                "Reports",
                "Billing record"
            ],

            "customers": [
                "Patients",
                "Doctors",
                "Reception Staff",
                "Hospital Administration"
            ]
        }

    def get_fmea_data(self):
        """
        Returns FMEA data focused on Q02 performance failures.

        RPN = Severity × Occurrence × Detection
        """

        fmea_rows = [
            {
                "failure_mode": "Patient search is slow",
                "effect": "Staff must wait before patient information appears",
                "cause": "Unoptimized search query or missing index",
                "severity": 8,
                "occurrence": 6,
                "detection": 4,
                "improvement": "Use indexed and filtered SQL search"
            },
            {
                "failure_mode": "Dashboard loads slowly",
                "effect": "Staff cannot quickly view hospital status",
                "cause": "Too many database operations or unnecessary data loading",
                "severity": 7,
                "occurrence": 5,
                "detection": 4,
                "improvement": "Use aggregated queries and measure dashboard load time"
            },
            {
                "failure_mode": "Reports take too long",
                "effect": "Management waits for operational information",
                "cause": "Loading complete tables instead of using SQL aggregation",
                "severity": 6,
                "occurrence": 5,
                "detection": 5,
                "improvement": "Use optimized aggregate SQL queries"
            },
            {
                "failure_mode": "Duplicate patient record created",
                "effect": "Incorrect or repeated patient information",
                "cause": "No duplicate check before insertion",
                "severity": 9,
                "occurrence": 4,
                "detection": 5,
                "improvement": "Use unique phone constraint and duplicate validation"
            },
            {
                "failure_mode": "Database query timeout",
                "effect": "Hospital operation is temporarily delayed",
                "cause": "Inefficient query or excessive database processing",
                "severity": 9,
                "occurrence": 3,
                "detection": 6,
                "improvement": "Optimize SQL queries and database indexes"
            },
            {
                "failure_mode": "Bulk CSV import is slow",
                "effect": "Large patient data import takes excessive time",
                "cause": "Individual processing without efficient data handling",
                "severity": 6,
                "occurrence": 4,
                "detection": 5,
                "improvement": "Use Pandas validation and efficient database insertion"
            }
        ]

        for row in fmea_rows:
            row["rpn"] = (
                row["severity"]
                * row["occurrence"]
                * row["detection"]
            )

        return fmea_rows

    def get_fmea_priority(self):
        """
        Sorts FMEA records by RPN for analysis.

        This does not replace the original FMEA order.
        """

        rows = self.get_fmea_data()

        return sorted(
            rows,
            key=lambda row: row["rpn"],
            reverse=True
        )

    def get_risk_level(self, rpn):
        """
        Converts RPN into a simple risk category.
        """

        if rpn >= 200:
            return "High"

        if rpn >= 100:
            return "Medium"

        return "Low"