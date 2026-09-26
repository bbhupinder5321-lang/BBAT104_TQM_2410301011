from app.database.database import get_connection


class DashboardRepository:

    def get_today_patient_count(self, today):
        connection = get_connection()

        try:
            result = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM patients
                WHERE registration_date = ?
                """,
                (today,)
            ).fetchone()

            return result["total"]

        finally:
            connection.close()

    def get_today_appointment_count(self, today):
        connection = get_connection()

        try:
            result = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM appointments
                WHERE appointment_date = ?
                """,
                (today,)
            ).fetchone()

            return result["total"]

        finally:
            connection.close()

    def get_pending_appointment_count(self, today):
        connection = get_connection()

        try:
            result = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM appointments
                WHERE appointment_date = ?
                AND status = 'Scheduled'
                """,
                (today,)
            ).fetchone()

            return result["total"]

        finally:
            connection.close()

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

            total_beds = result["total_beds"]
            occupied_beds = result["occupied_beds"] or 0

            return {
                "total_beds": total_beds,
                "occupied_beds": occupied_beds
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

            average_waiting_seconds = result["average_waiting_seconds"]

            if average_waiting_seconds is None:
                return 0

            return round(average_waiting_seconds)

        finally:
            connection.close()