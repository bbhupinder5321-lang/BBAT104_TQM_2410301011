from datetime import date

from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self):
        self.repository = DashboardRepository()

    def get_dashboard_metrics(self):
        """
        Return one coherent operational snapshot for the dashboard.

        The repository intentionally loads the dashboard metrics, queue,
        bed capacity and recent registrations through one connection so
        the Q02 performance goal is measured against a focused query path.
        """
        today = date.today().isoformat()
        return self.repository.get_dashboard_snapshot(today)

    def format_waiting_time(self, seconds):
        if seconds is None or seconds <= 0:
            return "No measured waits"

        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)

        if minutes == 0:
            return f"{remaining_seconds} sec"

        if remaining_seconds == 0:
            return f"{minutes} min"

        return f"{minutes} min {remaining_seconds} sec"

    def get_bed_occupancy_percentage(self, occupied_beds, total_beds):
        if total_beds <= 0:
            return 0

        return round((occupied_beds / total_beds) * 100, 1)

    def get_wait_status(self, seconds):
        """
        Dashboard interpretation for the Q02 waiting-time objective.

        This is an operational indicator, not a clinical threshold.
        """
        minutes = (seconds or 0) / 60

        if minutes <= 15:
            return "On track", "success"

        if minutes <= 30:
            return "Monitor", "warning"

        return "Attention", "danger"

    def get_occupancy_status(self, occupied_beds, total_beds):
        percentage = self.get_bed_occupancy_percentage(
            occupied_beds,
            total_beds
        )

        if percentage < 85:
            return "Capacity available", "success"

        if percentage < 95:
            return "High utilization", "warning"

        return "Near capacity", "danger"
