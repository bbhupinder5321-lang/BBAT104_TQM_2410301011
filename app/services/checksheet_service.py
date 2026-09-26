class ChecksheetService:

    def __init__(self):
        self.records = {
            "Slow patient search": 18,
            "Duplicate patient record": 15,
            "Slow reports": 12,
            "Dashboard loading slowly": 10,
            "Database query timeout": 8,
            "Slow CSV import": 5
        }

    # =========================================================
    # GET ALL RECORDS
    # =========================================================

    def get_records(self):
        return self.records.copy()

    # =========================================================
    # GET TOTAL DEFECTS
    # =========================================================

    def get_total_defects(self):
        return sum(self.records.values())

    # =========================================================
    # GET MOST FREQUENT DEFECT
    # =========================================================

    def get_most_frequent_defect(self):

        if not self.records:
            return None

        return max(
            self.records,
            key=self.records.get
        )

    # =========================================================
    # GET COUNT FOR A DEFECT
    # =========================================================

    def get_count(self, defect):

        if defect not in self.records:
            raise ValueError(
                f"Unknown defect: {defect}"
            )

        return self.records[defect]

    # =========================================================
    # ADD DEFECT
    # =========================================================

    def add_defect(self, defect, count=1):

        if not isinstance(defect, str):
            raise ValueError(
                "Defect name must be text."
            )

        defect = defect.strip()

        if not defect:
            raise ValueError(
                "Defect name cannot be empty."
            )

        if not isinstance(count, int):
            raise ValueError(
                "Count must be an integer."
            )

        if count < 0:
            raise ValueError(
                "Count cannot be negative."
            )

        if defect in self.records:
            self.records[defect] += count
        else:
            self.records[defect] = count

    # =========================================================
    # RECORD ONE OCCURRENCE
    # =========================================================

    def record_occurrence(self, defect):

        if defect not in self.records:
            raise ValueError(
                f"Unknown defect: {defect}"
            )

        self.records[defect] += 1

    # =========================================================
    # REMOVE DEFECT
    # =========================================================

    def remove_defect(self, defect):

        if defect not in self.records:
            raise ValueError(
                f"Unknown defect: {defect}"
            )

        del self.records[defect]

    # =========================================================
    # CLEAR ALL DATA
    # =========================================================

    def clear_records(self):
        self.records.clear()

    # =========================================================
    # GET SUMMARY
    # =========================================================

    def get_summary(self):

        total = self.get_total_defects()

        if total == 0:
            return {
                "total_defects": 0,
                "defect_types": 0,
                "most_frequent": None,
                "highest_count": 0
            }

        most_frequent = self.get_most_frequent_defect()

        return {
            "total_defects": total,
            "defect_types": len(self.records),
            "most_frequent": most_frequent,
            "highest_count": self.records[most_frequent]
        }