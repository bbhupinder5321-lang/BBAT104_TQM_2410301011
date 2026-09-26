from collections import Counter


class ParetoService:

    def __init__(self):
        self.defects = [
            "Slow patient search",
            "Duplicate patient record",
            "Slow reports",
            "Dashboard loading slowly",
            "Database query timeout",
            "Slow CSV import",
        ]

    def calculate_pareto(self, occurrences=None):
        """
        Calculate Pareto analysis.

        Returns defects sorted from highest occurrence
        to lowest occurrence, with percentage and
        cumulative percentage.
        """

        if occurrences is None:
            occurrences = {
                "Slow patient search": 18,
                "Duplicate patient record": 15,
                "Slow reports": 12,
                "Dashboard loading slowly": 10,
                "Database query timeout": 8,
                "Slow CSV import": 5,
            }

        if not isinstance(occurrences, dict):
            raise ValueError("Occurrences must be provided as a dictionary.")

        if not occurrences:
            return []

        for defect, count in occurrences.items():
            if not isinstance(defect, str) or not defect.strip():
                raise ValueError("Defect name cannot be empty.")

            if not isinstance(count, (int, float)):
                raise ValueError(
                    f"Occurrence count for '{defect}' must be numeric."
                )

            if count < 0:
                raise ValueError(
                    f"Occurrence count for '{defect}' cannot be negative."
                )

        total = sum(occurrences.values())

        if total == 0:
            return [
                {
                    "defect": defect,
                    "occurrence": count,
                    "percentage": 0,
                    "cumulative_percentage": 0,
                }
                for defect, count in occurrences.items()
            ]

        sorted_defects = sorted(
            occurrences.items(),
            key=lambda item: item[1],
            reverse=True
        )

        results = []
        cumulative = 0

        for defect, count in sorted_defects:

            percentage = (count / total) * 100
            cumulative += percentage

            results.append(
                {
                    "defect": defect,
                    "occurrence": count,
                    "percentage": round(percentage, 2),
                    "cumulative_percentage": round(cumulative, 2),
                }
            )

        return results

    def get_total_occurrences(self, occurrences=None):
        """Return the total number of recorded defects."""

        if occurrences is None:
            occurrences = {
                "Slow patient search": 18,
                "Duplicate patient record": 15,
                "Slow reports": 12,
                "Dashboard loading slowly": 10,
                "Database query timeout": 8,
                "Slow CSV import": 5,
            }

        return sum(occurrences.values())

    def get_major_defects(self, occurrences=None, threshold=80):
        """
        Return defects that fall within the specified
        cumulative Pareto percentage.
        """

        results = self.calculate_pareto(occurrences)

        return [
            result
            for result in results
            if result["cumulative_percentage"] <= threshold
        ]