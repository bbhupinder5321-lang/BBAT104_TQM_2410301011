class PDCAService:

    def __init__(self):
        self.cycles = [
            {
                "id": 1,
                "phase": "Plan",
                "activity": "Identify slow patient search and define performance target.",
                "result": "Search response target set below 1 second."
            },
            {
                "id": 2,
                "phase": "Do",
                "activity": "Implement database indexes and filtered SQL queries.",
                "result": "Patient search and database operations optimized."
            },
            {
                "id": 3,
                "phase": "Check",
                "activity": "Measure search, dashboard, report and database response times.",
                "result": "Performance measured against the 1 second target."
            },
            {
                "id": 4,
                "phase": "Act",
                "activity": "Standardize successful optimizations and identify further improvements.",
                "result": "Performance improvements documented for continuous improvement."
            }
        ]

    def get_cycles(self):
        return [cycle.copy() for cycle in self.cycles]

    def get_cycle(self, cycle_id):
        for cycle in self.cycles:
            if cycle["id"] == cycle_id:
                return cycle.copy()

        raise ValueError(
            f"PDCA cycle with ID {cycle_id} does not exist."
        )

    def get_phase(self, phase):
        if not isinstance(phase, str):
            raise ValueError("Phase must be text.")

        phase = phase.strip()

        for cycle in self.cycles:
            if cycle["phase"].lower() == phase.lower():
                return cycle.copy()

        raise ValueError(
            f"Unknown PDCA phase: {phase}"
        )

    def add_cycle(self, phase, activity, result):
        if not isinstance(phase, str) or not phase.strip():
            raise ValueError(
                "Phase cannot be empty."
            )

        if not isinstance(activity, str) or not activity.strip():
            raise ValueError(
                "Activity cannot be empty."
            )

        if not isinstance(result, str) or not result.strip():
            raise ValueError(
                "Result cannot be empty."
            )

        valid_phases = {
            "Plan",
            "Do",
            "Check",
            "Act"
        }

        phase = phase.strip().title()
        activity = activity.strip()
        result = result.strip()

        if phase not in valid_phases:
            raise ValueError(
                "Phase must be Plan, Do, Check, or Act."
            )

        next_id = max(
            [cycle["id"] for cycle in self.cycles],
            default=0
        ) + 1

        cycle = {
            "id": next_id,
            "phase": phase,
            "activity": activity,
            "result": result
        }

        self.cycles.append(cycle)

        return cycle.copy()

    def update_cycle(self, cycle_id, phase, activity, result):
        cycle = self.get_cycle(cycle_id)

        if not isinstance(phase, str) or not phase.strip():
            raise ValueError(
                "Phase cannot be empty."
            )

        if not isinstance(activity, str) or not activity.strip():
            raise ValueError(
                "Activity cannot be empty."
            )

        if not isinstance(result, str) or not result.strip():
            raise ValueError(
                "Result cannot be empty."
            )

        valid_phases = {
            "Plan",
            "Do",
            "Check",
            "Act"
        }

        phase = phase.strip().title()

        if phase not in valid_phases:
            raise ValueError(
                "Phase must be Plan, Do, Check, or Act."
            )

        for existing_cycle in self.cycles:
            if existing_cycle["id"] == cycle_id:
                existing_cycle["phase"] = phase
                existing_cycle["activity"] = activity.strip()
                existing_cycle["result"] = result.strip()

                return existing_cycle.copy()

        return cycle

    def remove_cycle(self, cycle_id):
        self.get_cycle(cycle_id)

        self.cycles = [
            cycle
            for cycle in self.cycles
            if cycle["id"] != cycle_id
        ]

    def get_summary(self):
        phase_counts = {
            "Plan": 0,
            "Do": 0,
            "Check": 0,
            "Act": 0
        }

        for cycle in self.cycles:
            phase = cycle["phase"]

            if phase in phase_counts:
                phase_counts[phase] += 1

        return {
            "total_cycles": len(self.cycles),
            "plan": phase_counts["Plan"],
            "do": phase_counts["Do"],
            "check": phase_counts["Check"],
            "act": phase_counts["Act"]
        }