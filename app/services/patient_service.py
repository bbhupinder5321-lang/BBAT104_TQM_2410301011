from app.repositories.patient_repository import PatientRepository


class PatientService:
    def __init__(self):
        self.repository = PatientRepository()

    @staticmethod
    def _validate_patient_details(full_name, dob, gender, phone):
        if not full_name.strip():
            raise ValueError("Patient name is required.")

        if not dob.strip():
            raise ValueError("Date of birth is required.")

        if not gender.strip():
            raise ValueError("Gender is required.")

        if not phone.strip():
            raise ValueError("Phone number is required.")

        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")

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
        self._validate_patient_details(full_name, dob, gender, phone)

        existing_patients = self.repository.search_patients(phone)

        for patient in existing_patients:
            if patient["phone"] == phone:
                raise ValueError(
                    "A patient with this phone number already exists."
                )

        return self.repository.add_patient(
            full_name.strip(),
            dob.strip(),
            gender.strip(),
            phone.strip(),
            address.strip(),
            blood_group.strip(),
            registration_date.strip()
        )

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
        self._validate_patient_details(full_name, dob, gender, phone)

        existing_patients = self.repository.search_patients(phone)

        for patient in existing_patients:
            if (
                patient["phone"] == phone
                and patient["patient_id"] != patient_id
            ):
                raise ValueError(
                    "Another patient is already using this phone number."
                )

        return self.repository.update_patient(
            patient_id,
            full_name.strip(),
            dob.strip(),
            gender.strip(),
            phone.strip(),
            address.strip(),
            blood_group.strip()
        )

    def delete_patient(self, patient_id):
        if not patient_id:
            raise ValueError("Patient ID is required.")

        if not (deleted := self.repository.delete_patient(patient_id)):
            raise ValueError("Patient record could not be deleted.")

        return deleted

    def get_patient(self, patient_id):
        if not patient_id:
            raise ValueError("Patient ID is required.")

        return self.repository.get_patient_by_id(patient_id)

    def get_all_patients(self):
        return self.repository.get_all_patients()

    def search_patients(self, search_text):
        return self.repository.search_patients(search_text)