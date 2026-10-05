from app.services.dashboard_service import DashboardService


def main():
    print("Testing Dashboard Service...\n")

    service = DashboardService()
    metrics = service.get_dashboard_metrics()

    required_keys = [
        "today_patients",
        "today_appointments",
        "pending_appointments",
        "completed_appointments",
        "cancelled_appointments",
        "checked_in_appointments",
        "measured_waits",
        "average_waiting_seconds",
        "total_beds",
        "occupied_beds",
        "available_beds",
        "queue",
        "bed_wards",
        "latest_patients"
    ]

    for key in required_keys:
        if key not in metrics:
            raise AssertionError(
                f"Dashboard snapshot is missing: {key}"
            )

    print("Today's patients:", metrics["today_patients"])
    print("Today's appointments:", metrics["today_appointments"])
    print("Pending appointments:", metrics["pending_appointments"])
    print("Checked-in appointments:", metrics["checked_in_appointments"])
    print("Completed appointments:", metrics["completed_appointments"])
    print("Cancelled appointments:", metrics["cancelled_appointments"])

    print(
        "Total beds:",
        metrics["total_beds"]
    )

    print(
        "Occupied beds:",
        metrics["occupied_beds"]
    )

    print(
        "Available beds:",
        metrics["available_beds"]
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

    wait_status, _ = service.get_wait_status(
        metrics["average_waiting_seconds"]
    )
    print("Waiting-time signal:", wait_status)

    occupancy_status, _ = service.get_occupancy_status(
        metrics["occupied_beds"],
        metrics["total_beds"]
    )
    print("Capacity signal:", occupancy_status)

    print(
        "Queue records returned:",
        len(metrics["queue"])
    )

    print(
        "Ward summaries returned:",
        len(metrics["bed_wards"])
    )

    print("\nDashboard Service test completed successfully.")


if __name__ == "__main__":
    main()
