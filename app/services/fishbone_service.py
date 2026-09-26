class FishboneService:

    def __init__(self):
        self.categories = {
            "People": [
                "Insufficient staff training",
                "Manual patient data entry",
                "Human entry errors",
            ],
            "Process": [
                "Unoptimized hospital workflow",
                "Repeated data entry",
                "Manual record verification",
            ],
            "Technology": [
                "Slow database queries",
                "Missing database indexes",
                "Inefficient report generation",
            ],
            "Database": [
                "Duplicate patient records",
                "Unoptimized SQL queries",
                "Unnecessary data retrieval",
            ],
            "Environment": [
                "High system workload",
                "Limited computer resources",
                "Multiple operations running simultaneously",
            ],
            "Measurement": [
                "Performance not monitored regularly",
                "No response-time targets",
                "Defects not tracked systematically",
            ],
        }

    # =========================================================
    # GET ALL CATEGORIES
    # =========================================================

    def get_categories(self):
        """Return all Fishbone analysis categories."""

        return self.categories

    # =========================================================
    # GET CAUSES FOR CATEGORY
    # =========================================================

    def get_causes(self, category):
        """Return causes belonging to a specific category."""

        if category not in self.categories:
            raise ValueError(
                f"Unknown Fishbone category: {category}"
            )

        return self.categories[category]

    # =========================================================
    # ADD CAUSE
    # =========================================================

    def add_cause(self, category, cause):
        """Add a new cause to an existing category."""

        if category not in self.categories:
            raise ValueError(
                f"Unknown Fishbone category: {category}"
            )

        if not isinstance(cause, str) or not cause.strip():
            raise ValueError(
                "Cause cannot be empty."
            )

        cause = cause.strip()

        if cause in self.categories[category]:
            raise ValueError(
                "This cause already exists."
            )

        self.categories[category].append(cause)

    # =========================================================
    # REMOVE CAUSE
    # =========================================================

    def remove_cause(self, category, cause):
        """Remove an existing cause from a category."""

        if category not in self.categories:
            raise ValueError(
                f"Unknown Fishbone category: {category}"
            )

        if cause not in self.categories[category]:
            raise ValueError(
                "Cause does not exist."
            )

        self.categories[category].remove(cause)

    # =========================================================
    # GET TOTAL CAUSES
    # =========================================================

    def get_total_causes(self):
        """Return the total number of identified causes."""

        return sum(
            len(causes)
            for causes in self.categories.values()
        )

    # =========================================================
    # GET SUMMARY
    # =========================================================

    def get_summary(self):
        """Return a summary of categories and cause counts."""

        return {
            category: len(causes)
            for category, causes in self.categories.items()
        }


if __name__ == "__main__":

    service = FishboneService()

    print("Fishbone Analysis")
    print("-" * 40)

    for category, causes in service.get_categories().items():

        print(f"\n{category}:")

        for cause in causes:
            print(f"  - {cause}")

    print("\nTotal causes:", service.get_total_causes())