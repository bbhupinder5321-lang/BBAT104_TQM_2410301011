from app.database.database import get_connection


class DoctorRepository:

    def add_doctor(
        self,
        full_name,
        specialization,
        phone,
        status
    ):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO doctors
                (full_name, specialization, phone, status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    full_name,
                    specialization,
                    phone,
                    status
                )
            )

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    def get_all_doctors(self):

        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    doctor_id,
                    full_name,
                    specialization,
                    phone,
                    status
                FROM doctors
                ORDER BY doctor_id DESC
                """
            ).fetchall()

        finally:
            connection.close()

    def get_doctor_by_id(self, doctor_id):

        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    doctor_id,
                    full_name,
                    specialization,
                    phone,
                    status
                FROM doctors
                WHERE doctor_id = ?
                """,
                (doctor_id,)
            ).fetchone()

        finally:
            connection.close()

    def update_doctor(
        self,
        doctor_id,
        full_name,
        specialization,
        phone,
        status
    ):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE doctors
                SET
                    full_name = ?,
                    specialization = ?,
                    phone = ?,
                    status = ?
                WHERE doctor_id = ?
                """,
                (
                    full_name,
                    specialization,
                    phone,
                    status,
                    doctor_id
                )
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    def delete_doctor(self, doctor_id):

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM doctors
                WHERE doctor_id = ?
                """,
                (doctor_id,)
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    def search_doctors(self, search_text):

        connection = get_connection()

        try:
            search = f"{search_text.strip()}%"

            return connection.execute(
                """
                SELECT
                    doctor_id,
                    full_name,
                    specialization,
                    phone,
                    status
                FROM doctors
                WHERE full_name LIKE ?
                   OR specialization LIKE ?
                   OR phone LIKE ?
                   OR CAST(doctor_id AS TEXT) LIKE ?
                ORDER BY full_name
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