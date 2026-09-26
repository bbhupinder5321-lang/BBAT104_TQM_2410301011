from datetime import date

from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self):
        self.repository = DashboardRepository()

    def get_dashboard_metrics(self):
        today = date.today().isoformat()

        today_patients = self.repository.get_today_patient_count(today)

        today_appointments = self.repository.get_today_appointment_count(
            today
        )

        pending_appointments = self.repository.get_pending_appointment_count(
            today
        )

        bed_data = self.repository.get_bed_occupancy()

        average_waiting_seconds = (
            self.repository.get_average_waiting_time()
        )

        return {
            "today_patients": today_patients,
            "today_appointments": today_appointments,
            "pending_appointments": pending_appointments,
            "total_beds": bed_data["total_beds"],
            "occupied_beds": bed_data["occupied_beds"],
            "average_waiting_seconds": average_waiting_seconds
        }

    def format_waiting_time(self, seconds):
        if seconds is None or seconds <= 0:
            return "0 min"

        minutes = seconds // 60
        remaining_seconds = seconds % 60

        if minutes == 0:
            return f"{remaining_seconds} sec"

        return f"{minutes} min {remaining_seconds} sec"

    def get_bed_occupancy_percentage(self, occupied_beds, total_beds):
        if total_beds <= 0:
            return 0

        percentage = (occupied_beds / total_beds) * 100

        return round(percentage, 1)