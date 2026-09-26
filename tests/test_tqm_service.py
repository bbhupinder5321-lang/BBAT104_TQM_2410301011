from app.services.tqm_service import TQMService


def main():
    print("Testing TQM Service...\n")

    service = TQMService()

    # ---------------------------------------------------------
    # SIPOC TEST
    # ---------------------------------------------------------

    sipoc = service.get_sipoc_data()

    print("SIPOC Analysis")
    print("-" * 50)

    for category, items in sipoc.items():
        print(f"\n{category.title()}:")

        for item in items:
            print(f"  - {item}")

    # ---------------------------------------------------------
    # FMEA TEST
    # ---------------------------------------------------------

    fmea = service.get_fmea_data()

    print("\n\nFMEA Analysis")
    print("-" * 50)

    for row in fmea:
        print(f"\nFailure Mode: {row['failure_mode']}")
        print(f"Severity: {row['severity']}")
        print(f"Occurrence: {row['occurrence']}")
        print(f"Detection: {row['detection']}")
        print(f"RPN: {row['rpn']}")

    # ---------------------------------------------------------
    # RPN VALIDATION
    # ---------------------------------------------------------

    for row in fmea:
        expected_rpn = (
            row["severity"]
            * row["occurrence"]
            * row["detection"]
        )

        assert row["rpn"] == expected_rpn

    print("\nRPN calculation test passed.")

    # ---------------------------------------------------------
    # PRIORITY TEST
    # ---------------------------------------------------------

    priority = service.get_fmea_priority()

    for index in range(len(priority) - 1):
        assert priority[index]["rpn"] >= priority[index + 1]["rpn"]

    print("FMEA priority sorting test passed.")

    # ---------------------------------------------------------
    # RISK LEVEL TEST
    # ---------------------------------------------------------

    assert service.get_risk_level(250) == "High"
    assert service.get_risk_level(150) == "Medium"
    assert service.get_risk_level(50) == "Low"

    print("Risk-level classification test passed.")

    print("\nTQM Service test completed successfully.")


if __name__ == "__main__":
    main()