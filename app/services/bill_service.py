from datetime import datetime

from app.database.database import get_connection
from app.repositories.bill_repository import BillRepository


class BillService:

    def __init__(self):
        self.repository = BillRepository()

    def add_bill(
        self,
        patient_id,
        bill_date,
        description,
        amount
    ):
        if not patient_id:
            raise ValueError("Patient is required.")

        if not bill_date.strip():
            raise ValueError("Bill date is required.")

        if not description.strip():
            raise ValueError("Bill description is required.")

        if not str(amount).strip():
            raise ValueError("Bill amount is required.")

        self.validate_date(bill_date)

        amount = self.validate_amount(amount)

        self.validate_patient(patient_id)

        return self.repository.add_bill(
            int(patient_id),
            bill_date.strip(),
            description.strip(),
            amount
        )

    def update_bill(
        self,
        bill_id,
        patient_id,
        bill_date,
        description,
        amount
    ):
        if not bill_id:
            raise ValueError("Bill ID is required.")

        if not patient_id:
            raise ValueError("Patient is required.")

        if not bill_date.strip():
            raise ValueError("Bill date is required.")

        if not description.strip():
            raise ValueError("Bill description is required.")

        if not str(amount).strip():
            raise ValueError("Bill amount is required.")

        self.validate_date(bill_date)

        amount = self.validate_amount(amount)

        self.validate_patient(patient_id)

        updated = self.repository.update_bill(
            int(bill_id),
            int(patient_id),
            bill_date.strip(),
            description.strip(),
            amount
        )

        if not updated:
            raise ValueError(
                "Bill could not be updated."
            )

        return updated

    def delete_bill(self, bill_id):

        if not bill_id:
            raise ValueError("Bill ID is required.")

        deleted = self.repository.delete_bill(
            int(bill_id)
        )

        if not deleted:
            raise ValueError(
                "Bill could not be deleted."
            )

        return deleted

    def get_bill(self, bill_id):

        if not bill_id:
            raise ValueError("Bill ID is required.")

        return self.repository.get_bill_by_id(
            int(bill_id)
        )

    def get_all_bills(self):

        return self.repository.get_all_bills()

    def search_bills(self, search_text):

        return self.repository.search_bills(
            search_text
        )

    def validate_date(self, bill_date):

        try:

            datetime.strptime(
                bill_date.strip(),
                "%Y-%m-%d"
            )

        except ValueError:

            raise ValueError(
                "Date must be in YYYY-MM-DD format."
            )

    def validate_amount(self, amount):

        try:

            amount = float(amount)

        except (ValueError, TypeError):

            raise ValueError(
                "Amount must be a valid number."
            )

        if amount < 0:

            raise ValueError(
                "Amount cannot be negative."
            )

        return round(amount, 2)

    def validate_patient(self, patient_id):

        connection = get_connection()

        try:

            patient = connection.execute(
                """
                SELECT patient_id
                FROM patients
                WHERE patient_id = ?
                """,
                (patient_id,)
            ).fetchone()

        finally:

            connection.close()

        if patient is None:

            raise ValueError(
                "Selected patient does not exist."
            )