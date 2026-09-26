from app.services.fishbone_service import FishboneService


def test_get_categories():

    service = FishboneService()

    categories = service.get_categories()

    assert len(categories) == 6
    assert "People" in categories
    assert "Process" in categories
    assert "Technology" in categories
    assert "Database" in categories
    assert "Environment" in categories
    assert "Measurement" in categories

    print("Fishbone categories test passed.")


def test_get_causes():

    service = FishboneService()

    causes = service.get_causes("Technology")

    assert len(causes) > 0
    assert "Slow database queries" in causes

    print("Fishbone causes test passed.")


def test_add_cause():

    service = FishboneService()

    service.add_cause(
        "People",
        "Insufficient staffing"
    )

    causes = service.get_causes("People")

    assert "Insufficient staffing" in causes

    print("Add cause test passed.")


def test_duplicate_cause():

    service = FishboneService()

    try:
        service.add_cause(
            "People",
            "Manual patient data entry"
        )

        assert False, "Duplicate cause should raise ValueError."

    except ValueError:
        print("Duplicate cause validation test passed.")


def test_empty_cause():

    service = FishboneService()

    try:
        service.add_cause(
            "People",
            ""
        )

        assert False, "Empty cause should raise ValueError."

    except ValueError:
        print("Empty cause validation test passed.")


def test_invalid_category():

    service = FishboneService()

    try:
        service.get_causes("Invalid")

        assert False, "Invalid category should raise ValueError."

    except ValueError:
        print("Invalid category validation test passed.")


def test_total_causes():

    service = FishboneService()

    total = service.get_total_causes()

    assert total == 18

    print("Total causes test passed.")


def test_remove_cause():

    service = FishboneService()

    service.add_cause(
        "People",
        "Temporary test cause"
    )

    service.remove_cause(
        "People",
        "Temporary test cause"
    )

    assert "Temporary test cause" not in service.get_causes("People")

    print("Remove cause test passed.")


if __name__ == "__main__":

    test_get_categories()
    test_get_causes()
    test_add_cause()
    test_duplicate_cause()
    test_empty_cause()
    test_invalid_category()
    test_total_causes()
    test_remove_cause()

    print("\nFishbone Service test completed successfully.")