from app.services.checksheet_service import ChecksheetService


def test_get_records():
    service = ChecksheetService()

    records = service.get_records()

    assert len(records) == 6
    assert records["Slow patient search"] == 18

    print("Get records test passed.")


def test_total_defects():
    service = ChecksheetService()

    total = service.get_total_defects()

    assert total == 68

    print("Total defects test passed.")


def test_most_frequent_defect():
    service = ChecksheetService()

    defect = service.get_most_frequent_defect()

    assert defect == "Slow patient search"

    print("Most frequent defect test passed.")


def test_get_count():
    service = ChecksheetService()

    count = service.get_count(
        "Duplicate patient record"
    )

    assert count == 15

    print("Get count test passed.")


def test_record_occurrence():
    service = ChecksheetService()

    service.record_occurrence(
        "Slow patient search"
    )

    assert service.get_count(
        "Slow patient search"
    ) == 19

    print("Record occurrence test passed.")


def test_add_new_defect():
    service = ChecksheetService()

    service.add_defect(
        "Slow login",
        4
    )

    assert service.get_count(
        "Slow login"
    ) == 4

    print("Add new defect test passed.")


def test_add_existing_defect():
    service = ChecksheetService()

    service.add_defect(
        "Slow reports",
        3
    )

    assert service.get_count(
        "Slow reports"
    ) == 15

    print("Add existing defect test passed.")


def test_negative_count_validation():
    service = ChecksheetService()

    try:
        service.add_defect(
            "Test defect",
            -1
        )

        assert False

    except ValueError as error:

        assert str(error) == "Count cannot be negative."

        print(
            "Negative count validation test passed."
        )


def test_empty_defect_validation():
    service = ChecksheetService()

    try:
        service.add_defect(
            "   ",
            1
        )

        assert False

    except ValueError as error:

        assert str(error) == "Defect name cannot be empty."

        print(
            "Empty defect validation test passed."
        )


def test_unknown_defect():
    service = ChecksheetService()

    try:
        service.get_count(
            "Unknown defect"
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Unknown defect: Unknown defect"
        )

        print(
            "Unknown defect validation test passed."
        )


def test_remove_defect():
    service = ChecksheetService()

    service.remove_defect(
        "Slow CSV import"
    )

    assert (
        "Slow CSV import"
        not in service.get_records()
    )

    print("Remove defect test passed.")


def test_summary():
    service = ChecksheetService()

    summary = service.get_summary()

    assert summary["total_defects"] == 68
    assert summary["defect_types"] == 6
    assert summary["most_frequent"] == (
        "Slow patient search"
    )
    assert summary["highest_count"] == 18

    print("Summary test passed.")


if __name__ == "__main__":

    print("Testing Checksheet Service...")

    test_get_records()
    test_total_defects()
    test_most_frequent_defect()
    test_get_count()
    test_record_occurrence()
    test_add_new_defect()
    test_add_existing_defect()
    test_negative_count_validation()
    test_empty_defect_validation()
    test_unknown_defect()
    test_remove_defect()
    test_summary()

    print(
        "Checksheet Service test completed successfully."
    )
    