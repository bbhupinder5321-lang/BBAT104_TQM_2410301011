import pandas as pd

from app.database.database import get_connection


class CSVImportService:

    REQUIRED_COLUMNS = [
        "full_name",
        "dob",
        "gender",
        "phone",
        "address",
        "blood_group"
    ]

    def import_patients(self, csv_path):

        try:
            dataframe = pd.read_csv(csv_path)

        except Exception as error:
            raise ValueError(
                f"Could not read CSV file: {error}"
            )

        # -----------------------------------------------------
        # Validate Columns
        # -----------------------------------------------------

        missing_columns = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(missing_columns)
            )

        dataframe = dataframe[
            self.REQUIRED_COLUMNS
        ].copy()

        # -----------------------------------------------------
        # Clean Data
        # -----------------------------------------------------

        dataframe = dataframe.fillna("")

        for column in self.REQUIRED_COLUMNS:

            dataframe[column] = (
                dataframe[column]
                .astype(str)
                .str.strip()
            )

        # -----------------------------------------------------
        # Counters
        # -----------------------------------------------------

        imported_count = 0
        duplicate_count = 0
        rejected_count = 0

        rejected_rows = []

        # Track phone numbers already processed
        # during this CSV import.
        processed_phones = set()

        connection = get_connection()

        try:

            for index, row in dataframe.iterrows():

                row_number = index + 2

                full_name = row["full_name"]
                dob = row["dob"]
                gender = row["gender"]
                phone = row["phone"]
                address = row["address"]
                blood_group = row["blood_group"]

                # -------------------------------------------------
                # Required fields
                # -------------------------------------------------

                if not full_name:

                    rejected_count += 1

                    rejected_rows.append(
                        {
                            "row": row_number,
                            "reason": "Patient name is required."
                        }
                    )

                    continue

                if not dob:

                    rejected_count += 1

                    rejected_rows.append(
                        {
                            "row": row_number,
                            "reason": "Date of birth is required."
                        }
                    )

                    continue

                if not gender:

                    rejected_count += 1

                    rejected_rows.append(
                        {
                            "row": row_number,
                            "reason": "Gender is required."
                        }
                    )

                    continue

                if not phone:

                    rejected_count += 1

                    rejected_rows.append(
                        {
                            "row": row_number,
                            "reason": "Phone number is required."
                        }
                    )

                    continue

                # -------------------------------------------------
                # Phone validation
                # -------------------------------------------------

                if not phone.isdigit() or len(phone) != 10:

                    rejected_count += 1

                    rejected_rows.append(
                        {
                            "row": row_number,
                            "reason": (
                                "Phone number must contain "
                                "exactly 10 digits."
                            )
                        }
                    )

                    continue

                # -------------------------------------------------
                # Duplicate inside current CSV
                # -------------------------------------------------

                if phone in processed_phones:

                    duplicate_count += 1

                    continue

                # -------------------------------------------------
                # Duplicate in database
                # -------------------------------------------------

                existing_patient = connection.execute(
                    """
                    SELECT patient_id
                    FROM patients
                    WHERE phone = ?
                    """,
                    (phone,)
                ).fetchone()

                if existing_patient is not None:

                    duplicate_count += 1

                    continue

                # Mark phone as processed
                processed_phones.add(phone)

                # -------------------------------------------------
                # Insert patient
                # -------------------------------------------------

                registration_date = (
                    pd.Timestamp.now()
                    .date()
                    .isoformat()
                )

                connection.execute(
                    """
                    INSERT INTO patients (
                        full_name,
                        dob,
                        gender,
                        phone,
                        address,
                        blood_group,
                        registration_date
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        full_name,
                        dob,
                        gender,
                        phone,
                        address,
                        blood_group,
                        registration_date
                    )
                )

                imported_count += 1

            connection.commit()

        except Exception:

            connection.rollback()

            raise

        finally:

            connection.close()

        return {
            "imported": imported_count,
            "duplicates": duplicate_count,
            "rejected": rejected_count,
            "rejected_rows": rejected_rows
        }