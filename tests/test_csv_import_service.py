import pandas as pd
from pathlib import Path

from app.services.csv_import_service import CSVImportService


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_CSV = PROJECT_ROOT / "data" / "test_patients.csv"


def create_test_csv():

    data = [
        {
            "full_name": "Aman Verma",
            "dob": "2002-05-12",
            "gender": "Male",
            "phone": "9000000001",
            "address": "Haldwani",
            "blood_group": "O+"
        },
        {
            "full_name": "Priya Sharma",
            "dob": "2001-08-20",
            "gender": "Female",
            "phone": "9000000002",
            "address": "Nainital",
            "blood_group": "A+"
        },
        {
            "full_name": "Rohit Singh",
            "dob": "2003-01-15",
            "gender": "Male",
            "phone": "9000000003",
            "address": "Haldwani",
            "blood_group": "B+"
        },
        {
            "full_name": "Duplicate Test",
            "dob": "2000-03-10",
            "gender": "Male",
            "phone": "9000000001",
            "address": "Haldwani",
            "blood_group": "O+"
        },
        {
            "full_name": "Invalid Phone",
            "dob": "2002-04-11",
            "gender": "Male",
            "phone": "12345",
            "address": "Haldwani",
            "blood_group": "AB+"
        }
    ]

    dataframe = pd.DataFrame(data)

    dataframe.to_csv(
        TEST_CSV,
        index=False
    )


def main():

    print("Testing CSV Import Service...")
    print()

    create_test_csv()

    service = CSVImportService()

    result = service.import_patients(
        TEST_CSV
    )

    print(
        "Imported patients:",
        result["imported"]
    )

    print(
        "Duplicate records:",
        result["duplicates"]
    )

    print(
        "Rejected records:",
        result["rejected"]
    )

    print()

    if result["imported"] == 3:
        print("Import test passed.")

    else:
        print(
            "Import test result:",
            result["imported"],
            "records imported."
        )

    if result["duplicates"] == 1:
        print("Duplicate detection test passed.")

    else:
        print(
            "Duplicate detection result:",
            result["duplicates"]
        )

    if result["rejected"] == 1:
        print("Validation test passed.")

    else:
        print(
            "Validation result:",
            result["rejected"]
        )

    print()

    if result["rejected_rows"]:

        print("Rejected rows:")

        for rejected in result["rejected_rows"]:

            print(
                f"Row {rejected['row']}: "
                f"{rejected['reason']}"
            )

    print()

    print(
        "CSV Import Service test completed."
    )


if __name__ == "__main__":
    main()