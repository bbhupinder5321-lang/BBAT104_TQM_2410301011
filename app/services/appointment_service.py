from datetime import datetime

from app.database.database import get_connection
from app.repositories.appointment_repository import AppointmentRepository


class AppointmentService:

    def __init__(self):
        self.repository = AppointmentRepository()

    def add_appointment(
        self,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status
    ):
        if not patient_id:
            raise ValueError("Patient is required.")

        if not doctor_id:
            raise ValueError("Doctor is required.")

        if not appointment_date.strip():
            raise ValueError("Appointment date is required.")

        if not appointment_time.strip():
            raise ValueError("Appointment time is required.")

        self.validate_date(appointment_date)
        self.validate_time(appointment_time)

        if not status.strip():
            status = "Scheduled"

        self.validate_patient(patient_id)
        self.validate_doctor(doctor_id)

        return self.repository.add_appointment(
            int(patient_id),
            int(doctor_id),
            appointment_date.strip(),
            appointment_time.strip(),
            status.strip()
        )

    def update_appointment(
        self,
        appointment_id,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status
    ):
        if not appointment_id:
            raise ValueError("Appointment ID is required.")

        if not patient_id:
            raise ValueError("Patient is required.")

        if not doctor_id:
            raise ValueError("Doctor is required.")

        if not appointment_date.strip():
            raise ValueError("Appointment date is required.")

        if not appointment_time.strip():
            raise ValueError("Appointment time is required.")

        self.validate_date(appointment_date)
        self.validate_time(appointment_time)

        if not status.strip():
            status = "Scheduled"

        self.validate_patient(patient_id)
        self.validate_doctor(doctor_id)

        return self.repository.update_appointment(
            int(appointment_id),
            int(patient_id),
            int(doctor_id),
            appointment_date.strip(),
            appointment_time.strip(),
            status.strip()
        )

    def delete_appointment(self, appointment_id):

        if not appointment_id:
            raise ValueError("Appointment ID is required.")

        deleted = self.repository.delete_appointment(
            appointment_id
        )

        if not deleted:
            raise ValueError(
                "Appointment could not be deleted."
            )

        return deleted

    def get_appointment(self, appointment_id):

        if not appointment_id:
            raise ValueError("Appointment ID is required.")

        return self.repository.get_appointment_by_id(
            appointment_id
        )

    def get_all_appointments(self):

        return self.repository.get_all_appointments()

    def search_appointments(self, search_text):

        return self.repository.search_appointments(
            search_text
        )

    def check_in_patient(self, appointment_id):

        if not appointment_id:
            raise ValueError("Appointment ID is required.")

        check_in_time = datetime.now().isoformat(
            timespec="seconds"
        )

        updated = self.repository.update_check_in_time(
            appointment_id,
            check_in_time
        )

        if not updated:
            raise ValueError(
                "Could not record patient check-in."
            )

        return check_in_time

    def start_consultation(self, appointment_id):

        if not appointment_id:
            raise ValueError("Appointment ID is required.")

        consultation_start_time = datetime.now().isoformat(
            timespec="seconds"
        )

        updated = self.repository.update_consultation_start_time(
            appointment_id,
            consultation_start_time
        )

        if not updated:
            raise ValueError(
                "Could not record consultation start."
            )

        return consultation_start_time

    def calculate_waiting_time(
        self,
        check_in_time,
        consultation_start_time
    ):
        if not check_in_time:
            return None

        if not consultation_start_time:
            return None

        check_in = datetime.fromisoformat(
            check_in_time
        )

        consultation_start = datetime.fromisoformat(
            consultation_start_time
        )

        waiting_seconds = (
            consultation_start - check_in
        ).total_seconds()

        if waiting_seconds < 0:
            return None

        return int(waiting_seconds)

    def validate_date(self, appointment_date):

        try:
            datetime.strptime(
                appointment_date.strip(),
                "%Y-%m-%d"
            )

        except ValueError:
            raise ValueError(
                "Date must be in YYYY-MM-DD format."
            )

    def validate_time(self, appointment_time):

        try:
            datetime.strptime(
                appointment_time.strip(),
                "%H:%M"
            )

        except ValueError:
            raise ValueError(
                "Time must be in HH:MM format."
            )

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

    def validate_doctor(self, doctor_id):

        connection = get_connection()

        try:
            doctor = connection.execute(
                """
                SELECT doctor_id
                FROM doctors
                WHERE doctor_id = ?
                """,
                (doctor_id,)
            ).fetchone()

        finally:
            connection.close()

        if doctor is None:
            raise ValueError(
                "Selected doctor does not exist."
            )