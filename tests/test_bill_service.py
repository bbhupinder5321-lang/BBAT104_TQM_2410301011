from app.services.bill_service import BillService


def main():

    service = BillService()

    print("Testing Billing Service...")
    print()

    # -------------------------------------------------
    # Get an existing patient
    # -------------------------------------------------

    patients = service.repository.get_all_bills()

    # We need a patient directly from the database.
    from app.database.database import get_connection

    connection = get_connection()

    try:
        patient = connection.execute(
            """
            SELECT patient_id, full_name
            FROM patients
            ORDER BY patient_id
            LIMIT 1
            """
        ).fetchone()

    finally:
        connection.close()

    if patient is None:
        print("No patients found.")
        print("Add a patient before testing billing.")
        return

    patient_id = patient["patient_id"]
    patient_name = patient["full_name"]

    print(
        f"Using patient: {patient_name} "
        f"(ID: {patient_id})"
    )

    # -------------------------------------------------
    # Test valid bill
    # -------------------------------------------------

    bill_id = service.add_bill(
        patient_id,
        "2026-09-26",
        "Consultation Fee",
        500
    )

    print(
        f"Valid bill added. Bill ID: {bill_id}"
    )

    # -------------------------------------------------
    # Test invalid amount
    # -------------------------------------------------

    try:

        service.add_bill(
            patient_id,
            "2026-09-26",
            "Invalid Test",
            -100
        )

        print(
            "ERROR: Negative amount was accepted."
        )

    except ValueError as error:

        print(
            f"Amount validation test passed: {error}"
        )

    # -------------------------------------------------
    # Test invalid date
    # -------------------------------------------------

    try:

        service.add_bill(
            patient_id,
            "26-09-2026",
            "Invalid Date Test",
            300
        )

        print(
            "ERROR: Invalid date was accepted."
        )

    except ValueError as error:

        print(
            f"Date validation test passed: {error}"
        )

    # -------------------------------------------------
    # Test invalid patient
    # -------------------------------------------------

    try:

        service.add_bill(
            999999,
            "2026-09-26",
            "Invalid Patient Test",
            300
        )

        print(
            "ERROR: Invalid patient was accepted."
        )

    except ValueError as error:

        print(
            f"Patient validation test passed: {error}"
        )

    # -------------------------------------------------
    # Get all bills
    # -------------------------------------------------

    bills = service.get_all_bills()

    print()
    print(
        f"Total bills: {len(bills)}"
    )

    for bill in bills:

        print(
            bill["bill_id"],
            bill["patient_name"],
            bill["bill_date"],
            bill["description"],
            bill["amount"]
        )

    print()
    print("Billing Service test completed.")


if __name__ == "__main__":
    main()