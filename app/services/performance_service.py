import time

from app.database.database import get_connection


class PerformanceService:

    def measure_database_query(self):
        """
        Measures the time required to execute
        an optimized database query.
        """

        start_time = time.perf_counter()

        connection = get_connection()

        try:
            connection.execute(
                """
                SELECT patient_id, full_name, phone
                FROM patients
                WHERE phone LIKE ?
                LIMIT 100
                """,
                ("9%",)
            ).fetchall()

        finally:
            connection.close()

        end_time = time.perf_counter()

        return round(
            (end_time - start_time) * 1000,
            2
        )

    def measure_patient_search(self):
        """
        Measures patient search performance.
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

        end_time = time.perf_counter()

        return round(
            (end_time - start_time) * 1000,
            2
        )

    def measure_dashboard_load(self):
        """
        Measures dashboard metric calculation time.
        """

        start_time = time.perf_counter()

        connection = get_connection()

        try:

            connection.execute(
                """
                SELECT COUNT(*)
                FROM patients
                WHERE registration_date = date('now')
                """
            ).fetchone()

            connection.execute(
                """
                SELECT COUNT(*)
                FROM appointments
                WHERE appointment_date = date('now')
                """
            ).fetchone()

            connection.execute(
                """
                SELECT COUNT(*)
                FROM appointments
                WHERE
                    appointment_date = date('now')
                    AND status = 'Scheduled'
                """
            ).fetchone()

            connection.execute(
                """
                SELECT
                    COUNT(*) AS total_beds,
                    SUM(
                        CASE
                            WHEN status = 'Occupied'
                            THEN 1
                            ELSE 0
                        END
                    ) AS occupied_beds
                FROM beds
                """
            ).fetchone()

        finally:
            connection.close()

        end_time = time.perf_counter()

        return round(
            (end_time - start_time) * 1000,
            2
        )

    def measure_report_generation(self):
        """
        Measures optimized report query performance.
        """

        start_time = time.perf_counter()

        connection = get_connection()

        try:

            connection.execute(
                """
                SELECT
                    COUNT(*) AS total_patients
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

        end_time = time.perf_counter()

        return round(
            (end_time - start_time) * 1000,
            2
        )

    def measure_all(self):

        return {
            "database_query": self.measure_database_query(),
            "patient_search": self.measure_patient_search(),
            "dashboard_load": self.measure_dashboard_load(),
            "report_generation": self.measure_report_generation()
        }

    def get_performance_status(
        self,
        dashboard_time
    ):
        """
        Q02 target:
        Dashboard should load in less than 1 second.
        """

        if dashboard_time < 1000:
            return "Within Target"

        return "Needs Improvement"