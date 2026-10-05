import time

from app.database.database import get_connection
from app.services.dashboard_service import DashboardService


class PerformanceService:

    def measure_database_query(self):
        """
        Measure a focused indexed patient lookup.
        """
        start_time = time.perf_counter()

        connection = get_connection()

        try:
            connection.execute(
                """
                SELECT
                    patient_id,
                    full_name,
                    phone
                FROM patients
                WHERE phone LIKE ?
                LIMIT 100
                """,
                ("9%",)
            ).fetchall()

        finally:
            connection.close()

        return round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

    def measure_patient_search(self):
        """
        Measure the same filtered search pattern used by the application.
        """
        start_time = time.perf_counter()

        connection = get_connection()

        try:
            connection.execute(
                """
                SELECT
                    patient_id,
                    full_name,
                    dob,
                    gender,
                    phone,
                    address,
                    blood_group,
                    registration_date
                FROM patients
                WHERE
                    full_name LIKE ?
                    OR phone LIKE ?
                    OR CAST(patient_id AS TEXT) LIKE ?
                ORDER BY patient_id DESC
                LIMIT 100
                """,
                ("Rah%", "Rah%", "Rah%")
            ).fetchall()

        finally:
            connection.close()

        return round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

    def measure_dashboard_load(self):
        """
        Measure the actual Q02 dashboard snapshot.

        This intentionally calls DashboardService so the performance
        result represents the real dashboard query path rather than a
        simplified test that omits queue/capacity data.
        """
        start_time = time.perf_counter()

        service = DashboardService()
        service.get_dashboard_metrics()

        return round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

    def measure_report_generation(self):
        """
        Measure the focused report queries used by the report module.
        """
        start_time = time.perf_counter()

        connection = get_connection()

        try:
            connection.execute(
                """
                SELECT COUNT(*) AS total_patients
                FROM patients
                """
            ).fetchone()

            connection.execute(
                """
                SELECT
                    d.doctor_id,
                    d.full_name,
                    COUNT(a.appointment_id)
                FROM doctors d
                LEFT JOIN appointments a
                    ON d.doctor_id = a.doctor_id
                GROUP BY
                    d.doctor_id,
                    d.full_name
                """
            ).fetchall()

            connection.execute(
                """
                SELECT
                    COUNT(*) AS total_bills,
                    COALESCE(SUM(amount), 0) AS revenue,
                    COALESCE(AVG(amount), 0) AS average_bill
                FROM bills
                """
            ).fetchone()

        finally:
            connection.close()

        return round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

    def measure_all(self):
        return {
            "database_query": self.measure_database_query(),
            "patient_search": self.measure_patient_search(),
            "dashboard_load": self.measure_dashboard_load(),
            "report_generation": self.measure_report_generation()
        }

    def get_performance_status(self, dashboard_time):
        """
        Q02 target:
        Dashboard should load in less than 1 second under normal
        local project conditions.
        """
        if dashboard_time < 1000:
            return "Within Target"

        return "Needs Improvement"
