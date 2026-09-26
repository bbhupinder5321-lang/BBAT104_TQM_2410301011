from app.repositories.report_repository import ReportRepository


class ReportService:

    def __init__(self):
        self.repository = ReportRepository()

    def get_patient_report(self):
        summary = self.repository.get_patient_summary()
        gender_data = self.repository.get_patients_by_gender()

        return {
            "total_patients": summary["total_patients"],
            "gender_categories": summary["gender_categories"],
            "gender_data": gender_data
        }

    def get_doctor_report(self):
        summary = self.repository.get_doctor_summary()
        doctor_data = self.repository.get_doctor_appointment_report()

        return {
            "total_doctors": summary["total_doctors"],
            "specializations": summary["specializations"],
            "doctor_data": doctor_data
        }

    def get_appointment_report(self):
        summary = self.repository.get_appointment_summary()

        return {
            "total_appointments": summary["total_appointments"] or 0,
            "scheduled": summary["scheduled"] or 0,
            "cancelled": summary["cancelled"] or 0,
            "completed": summary["completed"] or 0
        }

    def get_billing_report(self):
        summary = self.repository.get_billing_summary()

        return {
            "total_bills": summary["total_bills"] or 0,
            "total_revenue": round(
                summary["total_revenue"] or 0,
                2
            ),
            "average_bill": round(
                summary["average_bill"] or 0,
                2
            )
        }

    def get_waiting_time_report(self):
        return self.repository.get_waiting_time_report()

    def get_recent_patients(self):
        return self.repository.get_recent_patients()

    def get_all_reports(self):
        return {
            "patients": self.get_patient_report(),
            "doctors": self.get_doctor_report(),
            "appointments": self.get_appointment_report(),
            "billing": self.get_billing_report(),
            "waiting_time": self.get_waiting_time_report(),
            "recent_patients": self.get_recent_patients()
        }