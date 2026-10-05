from app.database.database import get_connection


class DashboardRepository:

    def get_dashboard_snapshot(self, today):
        """
        Load the complete dashboard snapshot through one SQLite connection.

        This keeps the Q02 dashboard fast by avoiding one database connection
        per metric while still using focused aggregate queries.
        """
        connection = get_connection()

        try:
            metrics = connection.execute(
                """
                SELECT
                    (
                        SELECT COUNT(*)
                        FROM patients
                        WHERE registration_date = ?
                    ) AS today_patients,

                    (
                        SELECT COUNT(*)
                        FROM appointments
                        WHERE appointment_date = ?
                    ) AS today_appointments,

                    (
                        SELECT COUNT(*)
                        FROM appointments
                        WHERE appointment_date = ?
                          AND status = 'Scheduled'
                    ) AS pending_appointments,

                    (
                        SELECT COUNT(*)
                        FROM appointments
                        WHERE appointment_date = ?
                          AND status = 'Completed'
                    ) AS completed_appointments,

                    (
                        SELECT COUNT(*)
                        FROM appointments
                        WHERE appointment_date = ?
                          AND status = 'Cancelled'
                    ) AS cancelled_appointments,

                    (
                        SELECT COUNT(*)
                        FROM appointments
                        WHERE appointment_date = ?
                          AND check_in_time IS NOT NULL
                          AND consultation_start_time IS NULL
                    ) AS checked_in_appointments,

                    (
                        SELECT COUNT(*)
                        FROM appointments
                        WHERE appointment_date = ?
                          AND check_in_time IS NOT NULL
                          AND consultation_start_time IS NOT NULL
                          AND consultation_start_time >= check_in_time
                    ) AS measured_waits,

                    (
                        SELECT AVG(
                            (
                                julianday(consultation_start_time)
                                - julianday(check_in_time)
                            ) * 86400
                        )
                        FROM appointments
                        WHERE appointment_date = ?
                          AND check_in_time IS NOT NULL
                          AND consultation_start_time IS NOT NULL
                          AND consultation_start_time >= check_in_time
                    ) AS average_waiting_seconds,

                    (
                        SELECT COUNT(*)
                        FROM beds
                    ) AS total_beds,

                    (
                        SELECT COUNT(*)
                        FROM beds
                        WHERE status = 'Occupied'
                    ) AS occupied_beds
                """,
                (
                    today,
                    today,
                    today,
                    today,
                    today,
                    today,
                    today,
                    today
                )
            ).fetchone()

            queue = connection.execute(
                """
                SELECT
                    a.appointment_id,
                    p.full_name AS patient_name,
                    d.full_name AS doctor_name,
                    a.appointment_time,
                    CASE
                        WHEN a.consultation_start_time IS NOT NULL
                            THEN 'Completed'
                        WHEN a.check_in_time IS NOT NULL
                            THEN 'Checked In'
                        ELSE a.status
                    END AS status,
                    a.check_in_time,
                    a.consultation_start_time
                FROM appointments a
                INNER JOIN patients p
                    ON a.patient_id = p.patient_id
                INNER JOIN doctors d
                    ON a.doctor_id = d.doctor_id
                WHERE a.appointment_date = ?
                ORDER BY
                    CASE a.status
                        WHEN 'Scheduled' THEN 1
                        WHEN 'Checked In' THEN 2
                        WHEN 'Completed' THEN 3
                        WHEN 'Cancelled' THEN 4
                        ELSE 5
                    END,
                    a.appointment_time ASC
                LIMIT 8
                """,
                (today,)
            ).fetchall()

            bed_wards = connection.execute(
                """
                SELECT
                    ward,
                    COUNT(*) AS total_beds,
                    SUM(
                        CASE
                            WHEN status = 'Occupied'
                            THEN 1
                            ELSE 0
                        END
                    ) AS occupied_beds
                FROM beds
                GROUP BY ward
                ORDER BY ward
                """
            ).fetchall()

            latest_patients = connection.execute(
                """
                SELECT
                    patient_id,
                    full_name,
                    registration_date
                FROM patients
                ORDER BY patient_id DESC
                LIMIT 5
                """
            ).fetchall()

            return {
                "today_patients": metrics["today_patients"] or 0,
                "today_appointments": metrics["today_appointments"] or 0,
                "pending_appointments": metrics["pending_appointments"] or 0,
                "completed_appointments": metrics["completed_appointments"] or 0,
                "cancelled_appointments": metrics["cancelled_appointments"] or 0,
                "checked_in_appointments": metrics["checked_in_appointments"] or 0,
                "measured_waits": metrics["measured_waits"] or 0,
                "average_waiting_seconds": round(
                    metrics["average_waiting_seconds"] or 0
                ),
                "total_beds": metrics["total_beds"] or 0,
                "occupied_beds": metrics["occupied_beds"] or 0,
                "available_beds": max(
                    (metrics["total_beds"] or 0)
                    - (metrics["occupied_beds"] or 0),
                    0
                ),
                "queue": queue,
                "bed_wards": bed_wards,
                "latest_patients": latest_patients
            }

        finally:
            connection.close()

    def get_today_patient_count(self, today):
        snapshot = self.get_dashboard_snapshot(today)
        return snapshot["today_patients"]

    def get_today_appointment_count(self, today):
        snapshot = self.get_dashboard_snapshot(today)
        return snapshot["today_appointments"]

    def get_pending_appointment_count(self, today):
        snapshot = self.get_dashboard_snapshot(today)
        return snapshot["pending_appointments"]

    def get_bed_occupancy(self):
        connection = get_connection()

        try:
            result = connection.execute(
                """
                SELECT
                    COUNT(*) AS total_beds,
                    SUM(
                        CASE
                            WHEN status = 'Occupied' THEN 1
                            ELSE 0
                        END
                    ) AS occupied_beds
                FROM beds
                """
            ).fetchone()

            return {
                "total_beds": result["total_beds"] or 0,
                "occupied_beds": result["occupied_beds"] or 0
            }

        finally:
            connection.close()

    def get_average_waiting_time(self):
        connection = get_connection()

        try:
            result = connection.execute(
                """
                SELECT
                    AVG(
                        (
                            julianday(consultation_start_time)
                            - julianday(check_in_time)
                        ) * 86400
                    ) AS average_waiting_seconds
                FROM appointments
                WHERE
                    check_in_time IS NOT NULL
                    AND consultation_start_time IS NOT NULL
                    AND consultation_start_time >= check_in_time
                """
            ).fetchone()

            return round(result["average_waiting_seconds"] or 0)

        finally:
            connection.close()
