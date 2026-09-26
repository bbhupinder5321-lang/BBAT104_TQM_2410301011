from app.database.database import get_connection


class BillRepository:

    def add_bill(
        self,
        patient_id,
        bill_date,
        description,
        amount
    ):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO bills (
                    patient_id,
                    bill_date,
                    description,
                    amount
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    patient_id,
                    bill_date,
                    description,
                    amount
                )
            )

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    def get_all_bills(self):

        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    bills.bill_id,
                    bills.patient_id,
                    patients.full_name AS patient_name,
                    bills.bill_date,
                    bills.description,
                    bills.amount
                FROM bills
                INNER JOIN patients
                    ON bills.patient_id = patients.patient_id
                ORDER BY bills.bill_id DESC
                """
            ).fetchall()

        finally:
            connection.close()

    def get_bill_by_id(self, bill_id):

        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    bills.bill_id,
                    bills.patient_id,
                    patients.full_name AS patient_name,
                    bills.bill_date,
                    bills.description,
                    bills.amount
                FROM bills
                INNER JOIN patients
                    ON bills.patient_id = patients.patient_id
                WHERE bills.bill_id = ?
                """,
                (bill_id,)
            ).fetchone()

        finally:
            connection.close()

    def update_bill(
        self,
        bill_id,
        patient_id,
        bill_date,
        description,
        amount
    ):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE bills
                SET
                    patient_id = ?,
                    bill_date = ?,
                    description = ?,
                    amount = ?
                WHERE bill_id = ?
                """,
                (
                    patient_id,
                    bill_date,
                    description,
                    amount,
                    bill_id
                )
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    def delete_bill(self, bill_id):

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM bills
                WHERE bill_id = ?
                """,
                (bill_id,)
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    def search_bills(self, search_text):

        connection = get_connection()

        try:
            search_pattern = f"{search_text}%"

            return connection.execute(
                """
                SELECT
                    bills.bill_id,
                    bills.patient_id,
                    patients.full_name AS patient_name,
                    bills.bill_date,
                    bills.description,
                    bills.amount
                FROM bills
                INNER JOIN patients
                    ON bills.patient_id = patients.patient_id
                WHERE
                    CAST(bills.bill_id AS TEXT) LIKE ?
                    OR patients.full_name LIKE ?
                    OR bills.description LIKE ?
                    OR bills.bill_date LIKE ?
                ORDER BY bills.bill_id DESC
                LIMIT 100
                """,
                (
                    search_pattern,
                    search_pattern,
                    search_pattern,
                    search_pattern
                )
            ).fetchall()

        finally:
            connection.close()