from app.services.dashboard_service import DashboardService


def main():
    print("Testing Dashboard Service...\n")

    service = DashboardService()

    metrics = service.get_dashboard_metrics()

    print("Today's patients:", metrics["today_patients"])
    print("Today's appointments:", metrics["today_appointments"])
    print("Pending appointments:", metrics["pending_appointments"])

    print(
        "Total beds:",
        metrics["total_beds"]
    )

    print(
        "Occupied beds:",
        metrics["occupied_beds"]
    )

    print(
        "Average waiting time:",
        service.format_waiting_time(
            metrics["average_waiting_seconds"]
        )
    )

    occupancy = service.get_bed_occupancy_percentage(
        metrics["occupied_beds"],
        metrics["total_beds"]
    )

    print(
        "Bed occupancy:",
        f"{occupancy}%"
    )

    print("\nDashboard Service test completed.")


if __name__ == "__main__":
    main()