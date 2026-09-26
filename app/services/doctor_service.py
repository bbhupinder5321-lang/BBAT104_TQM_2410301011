from app.repositories.doctor_repository import DoctorRepository


class DoctorService:

    def __init__(self):
        self.repository = DoctorRepository()

    def add_doctor(
        self,
        full_name,
        specialization,
        phone,
        status
    ):
        if not full_name.strip():
            raise ValueError("Doctor name is required.")

        if not specialization.strip():
            raise ValueError("Specialization is required.")

        if not phone.strip():
            raise ValueError("Phone number is required.")

        if not phone.isdigit() or len(phone) != 10:
            raise ValueError(
                "Phone number must contain exactly 10 digits."
            )

        if not status.strip():
            status = "Active"

        existing_doctors = self.repository.search_doctors(phone)

        for doctor in existing_doctors:
            if doctor["phone"] == phone:
                raise ValueError(
                    "A doctor with this phone number already exists."
                )

        return self.repository.add_doctor(
            full_name.strip(),
            specialization.strip(),
            phone.strip(),
            status.strip()
        )

    def update_doctor(
        self,
        doctor_id,
        full_name,
        specialization,
        phone,
        status
    ):
        if not full_name.strip():
            raise ValueError("Doctor name is required.")

        if not specialization.strip():
            raise ValueError("Specialization is required.")

        if not phone.strip():
            raise ValueError("Phone number is required.")

        if not phone.isdigit() or len(phone) != 10:
            raise ValueError(
                "Phone number must contain exactly 10 digits."
            )

        if not status.strip():
            status = "Active"

        existing_doctors = self.repository.search_doctors(phone)

        for doctor in existing_doctors:
            if (
                doctor["phone"] == phone
                and doctor["doctor_id"] != doctor_id
            ):
                raise ValueError(
                    "Another doctor is already using this phone number."
                )

        return self.repository.update_doctor(
            doctor_id,
            full_name.strip(),
            specialization.strip(),
            phone.strip(),
            status.strip()
        )

    def delete_doctor(self, doctor_id):

        if not doctor_id:
            raise ValueError("Doctor ID is required.")

        deleted = self.repository.delete_doctor(
            doctor_id
        )

        if not deleted:
            raise ValueError(
                "Doctor record could not be deleted."
            )

        return deleted

    def get_doctor(self, doctor_id):

        if not doctor_id:
            raise ValueError("Doctor ID is required.")

        return self.repository.get_doctor_by_id(
            doctor_id
        )

    def get_all_doctors(self):

        return self.repository.get_all_doctors()

    def search_doctors(self, search_text):

        return self.repository.search_doctors(
            search_text
        )