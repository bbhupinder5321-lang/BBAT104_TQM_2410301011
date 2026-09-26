from app.database.database import get_connection


class PatientRepository:

    def add_patient(
        self,
        full_name,
        dob,
        gender,
        phone,
        address,
        blood_group,
        registration_date
    ):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO patients
                (
                    full_name,
                    dob,
                    gender,
                    phone,
                    address,
                    blood_group,
                    registration_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    full_name,
                    dob,
                    gender,
                    phone,
                    address,
                    blood_group,
                    registration_date
                )
            )

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    def get_all_patients(self):

        connection = get_connection()

        try:
            return connection.execute(
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
                ORDER BY patient_id DESC
                """
            ).fetchall()

        finally:
            connection.close()

    def get_patient_by_id(self, patient_id):

        connection = get_connection()

        try:
            return connection.execute(
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
                WHERE patient_id = ?
                """,
                (patient_id,)
            ).fetchone()

        finally:
            connection.close()

    def update_patient(
        self,
        patient_id,
        full_name,
        dob,
        gender,
        phone,
        address,
        blood_group
    ):

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE patients
                SET
                    full_name = ?,
                    dob = ?,
                    gender = ?,
                    phone = ?,
                    address = ?,
                    blood_group = ?
                WHERE patient_id = ?
                """,
                (
                    full_name,
                    dob,
                    gender,
                    phone,
                    address,
                    blood_group,
                    patient_id
                )
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    def delete_patient(self, patient_id):

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM patients
                WHERE patient_id = ?
                """,
                (patient_id,)
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    def search_patients(self, search_text):

        connection = get_connection()

        try:
            search = f"{search_text.strip()}%"

            return connection.execute(
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
                WHERE full_name LIKE ?
                   OR phone LIKE ?
                   OR CAST(patient_id AS TEXT) LIKE ?
                ORDER BY full_name
                LIMIT 100
                """,
                (
                    search,
                    search,
                    search
                )
            ).fetchall()

        finally:
            connection.close()