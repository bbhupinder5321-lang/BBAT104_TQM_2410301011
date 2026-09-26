from app.services.pareto_service import ParetoService


def test_pareto_calculation():
    service = ParetoService()

    occurrences = {
        "Slow patient search": 18,
        "Duplicate patient record": 15,
        "Slow reports": 12,
        "Dashboard loading slowly": 10,
        "Database query timeout": 8,
        "Slow CSV import": 5,
    }

    results = service.calculate_pareto(occurrences)

    assert len(results) == 6

    # Highest occurrence should come first.
    assert results[0]["defect"] == "Slow patient search"
    assert results[0]["occurrence"] == 18

    # Lowest occurrence should come last.
    assert results[-1]["defect"] == "Slow CSV import"
    assert results[-1]["occurrence"] == 5

    # Total percentage should be approximately 100%.
    assert abs(results[-1]["cumulative_percentage"] - 100) < 0.01

    print("Pareto calculation test passed.")


def test_sorting():
    service = ParetoService()

    occurrences = {
        "Defect A": 5,
        "Defect B": 20,
        "Defect C": 10,
    }

    results = service.calculate_pareto(occurrences)

    assert results[0]["defect"] == "Defect B"
    assert results[1]["defect"] == "Defect C"
    assert results[2]["defect"] == "Defect A"

    print("Pareto sorting test passed.")


def test_total_occurrences():
    service = ParetoService()

    occurrences = {
        "Defect A": 10,
        "Defect B": 20,
        "Defect C": 5,
    }

    total = service.get_total_occurrences(occurrences)

    assert total == 35

    print("Total occurrence test passed.")


def test_negative_occurrence():
    service = ParetoService()

    occurrences = {
        "Defect A": -5,
    }

    try:
        service.calculate_pareto(occurrences)
        assert False, "Negative occurrence should raise ValueError."
    except ValueError:
        print("Negative occurrence validation test passed.")


def test_empty_data():
    service = ParetoService()

    results = service.calculate_pareto({})

    assert results == []

    print("Empty data test passed.")


if __name__ == "__main__":
    test_pareto_calculation()
    test_sorting()
    test_total_occurrences()
    test_negative_occurrence()
    test_empty_data()

    print("\nPareto Service test completed successfully.")