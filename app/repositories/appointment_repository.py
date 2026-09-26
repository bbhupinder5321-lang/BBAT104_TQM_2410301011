from app.database.database import get_connection


class AppointmentRepository:

    def add_appointment(
        self,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status
    ):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO appointments
                (
                    patient_id,
                    doctor_id,
                    appointment_date,
                    appointment_time,
                    status
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    patient_id,
                    doctor_id,
                    appointment_date,
                    appointment_time,
                    status
                )
            )

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    def get_all_appointments(self):

        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    a.appointment_id,
                    a.patient_id,
                    p.full_name AS patient_name,
                    a.doctor_id,
                    d.full_name AS doctor_name,
                    d.specialization,
                    a.appointment_date,
                    a.appointment_time,
                    a.status,
                    a.check_in_time,
                    a.consultation_start_time
                FROM appointments a
                JOIN patients p
                    ON a.patient_id = p.patient_id
                JOIN doctors d
                    ON a.doctor_id = d.doctor_id
                ORDER BY
                    a.appointment_date DESC,
                    a.appointment_time DESC
                """
            ).fetchall()

        finally:
            connection.close()

    def get_appointment_by_id(self, appointment_id):

        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    a.appointment_id,
                    a.patient_id,
                    p.full_name AS patient_name,
                    a.doctor_id,
                    d.full_name AS doctor_name,
                    d.specialization,
                    a.appointment_date,
                    a.appointment_time,
                    a.status,
                    a.check_in_time,
                    a.consultation_start_time
                FROM appointments a
                JOIN patients p
                    ON a.patient_id = p.patient_id
                JOIN doctors d
                    ON a.doctor_id = d.doctor_id
                WHERE a.appointment_id = ?
                """,
                (appointment_id,)
            ).fetchone()

        finally:
            connection.close()

    def update_appointment(
        self,
        appointment_id,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status
    ):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE appointments
                SET
                    patient_id = ?,
                    doctor_id = ?,
                    appointment_date = ?,
                    appointment_time = ?,
                    status = ?
                WHERE appointment_id = ?
                """,
                (
                    patient_id,
                    doctor_id,
                    appointment_date,
                    appointment_time,
                    status,
                    appointment_id
                )
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    def delete_appointment(self, appointment_id):

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM appointments
                WHERE appointment_id = ?
                """,
                (appointment_id,)
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    def search_appointments(self, search_text):

        connection = get_connection()

        try:
            search = f"{search_text.strip()}%"

            return connection.execute(
                """
                SELECT
                    a.appointment_id,
                    a.patient_id,
                    p.full_name AS patient_name,
                    a.doctor_id,
                    d.full_name AS doctor_name,
                    d.specialization,
                    a.appointment_date,
                    a.appointment_time,
                    a.status,
                    a.check_in_time,
                    a.consultation_start_time
                FROM appointments a
                JOIN patients p
                    ON a.patient_id = p.patient_id
                JOIN doctors d
                    ON a.doctor_id = d.doctor_id
                WHERE p.full_name LIKE ?
                   OR d.full_name LIKE ?
                   OR d.specialization LIKE ?
                   OR CAST(a.appointment_id AS TEXT) LIKE ?
                ORDER BY
                    a.appointment_date DESC,
                    a.appointment_time DESC
                LIMIT 100
                """,
                (
                    search,
                    search,
                    search,
                    search
                )
            ).fetchall()

        finally:
            connection.close()

    def update_check_in_time(
        self,
        appointment_id,
        check_in_time
    ):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE appointments
                SET
                    check_in_time = ?
                WHERE appointment_id = ?
                """,
                (
                    check_in_time,
                    appointment_id
                )
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    def update_consultation_start_time(
        self,
        appointment_id,
        consultation_start_time
    ):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE appointments
                SET
                    consultation_start_time = ?
                WHERE appointment_id = ?
                """,
                (
                    consultation_start_time,
                    appointment_id
                )
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()