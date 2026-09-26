from app.database.database import get_connection


class ReportRepository:

    def get_patient_summary(self):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    COUNT(*) AS total_patients,
                    COUNT(DISTINCT gender) AS gender_categories
                FROM patients
                """
            ).fetchone()

        finally:
            connection.close()

    def get_patients_by_gender(self):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    gender,
                    COUNT(*) AS total
                FROM patients
                GROUP BY gender
                ORDER BY total DESC
                """
            ).fetchall()

        finally:
            connection.close()

    def get_doctor_summary(self):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    COUNT(*) AS total_doctors,
                    COUNT(DISTINCT specialization) AS specializations
                FROM doctors
                """
            ).fetchone()

        finally:
            connection.close()

    def get_doctor_appointment_report(self):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    d.doctor_id,
                    d.full_name AS doctor_name,
                    d.specialization,
                    COUNT(a.appointment_id) AS total_appointments
                FROM doctors d
                LEFT JOIN appointments a
                    ON d.doctor_id = a.doctor_id
                GROUP BY
                    d.doctor_id,
                    d.full_name,
                    d.specialization
                ORDER BY total_appointments DESC
                """
            ).fetchall()

        finally:
            connection.close()

    def get_appointment_summary(self):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    COUNT(*) AS total_appointments,
                    SUM(
                        CASE
                            WHEN status = 'Scheduled'
                            THEN 1
                            ELSE 0
                        END
                    ) AS scheduled,
                    SUM(
                        CASE
                            WHEN status = 'Cancelled'
                            THEN 1
                            ELSE 0
                        END
                    ) AS cancelled,
                    SUM(
                        CASE
                            WHEN status = 'Completed'
                            THEN 1
                            ELSE 0
                        END
                    ) AS completed
                FROM appointments
                """
            ).fetchone()

        finally:
            connection.close()

    def get_billing_summary(self):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    COUNT(*) AS total_bills,
                    COALESCE(SUM(amount), 0) AS total_revenue,
                    COALESCE(AVG(amount), 0) AS average_bill
                FROM bills
                """
            ).fetchone()

        finally:
            connection.close()

    def get_waiting_time_report(self):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    a.appointment_id,
                    p.full_name AS patient_name,
                    d.full_name AS doctor_name,
                    a.check_in_time,
                    a.consultation_start_time,
                    ROUND(
                        (
                            julianday(a.consultation_start_time)
                            - julianday(a.check_in_time)
                        ) * 60,
                        2
                    ) AS waiting_minutes
                FROM appointments a
                INNER JOIN patients p
                    ON a.patient_id = p.patient_id
                INNER JOIN doctors d
                    ON a.doctor_id = d.doctor_id
                WHERE
                    a.check_in_time IS NOT NULL
                    AND a.consultation_start_time IS NOT NULL
                    AND a.consultation_start_time >= a.check_in_time
                ORDER BY waiting_minutes DESC
                """
            ).fetchall()

        finally:
            connection.close()

    def get_recent_patients(self, limit=20):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    patient_id,
                    full_name,
                    gender,
                    phone,
                    blood_group,
                    registration_date
                FROM patients
                ORDER BY patient_id DESC
                LIMIT ?
                """,
                (limit,)
            ).fetchall()

        finally:
            connection.close()