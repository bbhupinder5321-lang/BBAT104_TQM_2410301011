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

        imported_count = 0
        duplicate_count = 0
        rejected_count = 0
        rejected_rows = []

        # -----------------------------------------------------
        # Phase 1: Validate the CSV in memory
        # -----------------------------------------------------

        valid_rows = []
        processed_phones = set()

        for index, row in dataframe.iterrows():

            row_number = index + 2

            full_name = row["full_name"]
            dob = row["dob"]
            gender = row["gender"]
            phone = row["phone"]
            address = row["address"]
            blood_group = row["blood_group"]

            if not full_name:
                rejected_count += 1
                rejected_rows.append({
                    "row": row_number,
                    "reason": "Patient name is required."
                })
                continue

            if not dob:
                rejected_count += 1
                rejected_rows.append({
                    "row": row_number,
                    "reason": "Date of birth is required."
                })
                continue

            if not gender:
                rejected_count += 1
                rejected_rows.append({
                    "row": row_number,
                    "reason": "Gender is required."
                })
                continue

            if not phone:
                rejected_count += 1
                rejected_rows.append({
                    "row": row_number,
                    "reason": "Phone number is required."
                })
                continue

            if not phone.isdigit() or len(phone) != 10:
                rejected_count += 1
                rejected_rows.append({
                    "row": row_number,
                    "reason": (
                        "Phone number must contain "
                        "exactly 10 digits."
                    )
                })
                continue

            if phone in processed_phones:
                duplicate_count += 1
                continue

            processed_phones.add(phone)

            valid_rows.append({
                "row": row_number,
                "full_name": full_name,
                "dob": dob,
                "gender": gender,
                "phone": phone,
                "address": address,
                "blood_group": blood_group
            })

        if not valid_rows:
            return {
                "imported": 0,
                "duplicates": duplicate_count,
                "rejected": rejected_count,
                "rejected_rows": rejected_rows
            }

        # -----------------------------------------------------
        # Phase 2: One indexed database lookup for duplicates
        # -----------------------------------------------------

        connection = get_connection()

        try:
            placeholders = ",".join(
                "?" for _ in valid_rows
            )

            existing_rows = connection.execute(
                f"""
                SELECT phone
                FROM patients
                WHERE phone IN ({placeholders})
                """,
                tuple(
                    row["phone"]
                    for row in valid_rows
                )
            ).fetchall()

            existing_phones = {
                row["phone"]
                for row in existing_rows
            }

            rows_to_insert = []

            registration_date = (
                pd.Timestamp.now()
                .date()
                .isoformat()
            )

            for row in valid_rows:

                if row["phone"] in existing_phones:
                    duplicate_count += 1
                    continue

                rows_to_insert.append(
                    (
                        row["full_name"],
                        row["dob"],
                        row["gender"],
                        row["phone"],
                        row["address"],
                        row["blood_group"],
                        registration_date
                    )
                )

            # -------------------------------------------------
            # Phase 3: One efficient bulk insert
            # -------------------------------------------------

            if rows_to_insert:
                connection.executemany(
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
                    rows_to_insert
                )

                imported_count = len(rows_to_insert)

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
