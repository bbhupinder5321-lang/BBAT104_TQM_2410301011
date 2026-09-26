from app.services.report_service import ReportService


def main():

    print("Testing Report Service...")
    print()

    service = ReportService()

    patient_report = service.get_patient_report()

    print(
        "Total patients:",
        patient_report["total_patients"]
    )

    doctor_report = service.get_doctor_report()

    print(
        "Total doctors:",
        doctor_report["total_doctors"]
    )

    appointment_report = service.get_appointment_report()

    print(
        "Total appointments:",
        appointment_report["total_appointments"]
    )

    print(
        "Scheduled:",
        appointment_report["scheduled"]
    )

    print(
        "Cancelled:",
        appointment_report["cancelled"]
    )

    print(
        "Completed:",
        appointment_report["completed"]
    )

    billing_report = service.get_billing_report()

    print(
        "Total bills:",
        billing_report["total_bills"]
    )

    print(
        "Total revenue:",
        billing_report["total_revenue"]
    )

    print(
        "Average bill:",
        billing_report["average_bill"]
    )

    waiting_report = service.get_waiting_time_report()

    print(
        "Waiting-time records:",
        len(waiting_report)
    )

    recent_patients = service.get_recent_patients()

    print(
        "Recent patients:",
        len(recent_patients)
    )

    print()
    print("Report Service test completed.")


if __name__ == "__main__":
    main()