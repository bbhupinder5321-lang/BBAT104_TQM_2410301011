from app.services.pdca_service import PDCAService


def main():
    print("Testing PDCA Service...")

    service = PDCAService()

    # Get cycles
    cycles = service.get_cycles()

    assert len(cycles) == 4
    print("Get cycles test passed.")

    # Check phases
    phases = [
        cycle["phase"]
        for cycle in cycles
    ]

    assert phases == [
        "Plan",
        "Do",
        "Check",
        "Act"
    ]

    print("PDCA phase test passed.")

    # Get cycle by ID
    cycle = service.get_cycle(1)

    assert cycle["phase"] == "Plan"

    print("Get cycle by ID test passed.")

    # Get phase
    check_phase = service.get_phase("Check")

    assert check_phase["phase"] == "Check"

    print("Get phase test passed.")

    # Add cycle
    new_cycle = service.add_cycle(
        "Plan",
        "Define a new performance improvement target.",
        "Target documented."
    )

    assert new_cycle["id"] == 5
    assert new_cycle["phase"] == "Plan"

    print("Add cycle test passed.")

    # Update cycle
    updated_cycle = service.update_cycle(
        5,
        "Do",
        "Implement the planned improvement.",
        "Improvement implemented."
    )

    assert updated_cycle["phase"] == "Do"

    print("Update cycle test passed.")

    # Invalid phase
    try:
        service.add_cycle(
            "Invalid",
            "Test activity",
            "Test result"
        )

        assert False

    except ValueError:
        print("Invalid phase validation test passed.")

    # Empty activity
    try:
        service.add_cycle(
            "Plan",
            "",
            "Test result"
        )

        assert False

    except ValueError:
        print("Empty activity validation test passed.")

    # Unknown cycle
    try:
        service.get_cycle(999)

        assert False

    except ValueError:
        print("Unknown cycle validation test passed.")

    # Summary
    summary = service.get_summary()

    assert summary["total_cycles"] == 5

    print("Summary test passed.")

    # Remove cycle
    service.remove_cycle(5)

    assert len(service.get_cycles()) == 4

    print("Remove cycle test passed.")

    print("PDCA Service test completed successfully.")


if __name__ == "__main__":
    main()