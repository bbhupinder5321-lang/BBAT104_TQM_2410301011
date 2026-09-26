from app.services.performance_service import PerformanceService


def main():
    print("Testing Performance Service...\n")

    service = PerformanceService()

    results = service.measure_all()

    print(f"Database Query Time: {results['database_query']} ms")
    print(f"Patient Search Time: {results['patient_search']} ms")
    print(f"Dashboard Load Time: {results['dashboard_load']} ms")
    print(f"Report Generation Time: {results['report_generation']} ms")

    status = service.get_performance_status(
        results["dashboard_load"]
    )

    print(f"\nDashboard Performance Status: {status}")

    if results["dashboard_load"] < 1000:
        print("Performance target test passed.")
    else:
        print("Performance target test needs improvement.")

    print("\nPerformance Service test completed.")


if __name__ == "__main__":
    main()