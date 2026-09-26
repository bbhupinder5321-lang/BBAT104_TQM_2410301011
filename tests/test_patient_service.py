from app.services.patient_service import PatientService


service = PatientService()

# Test 1: Add a valid patient
patient_id = service.add_patient(
    "Rahul Kumar",
    "2001-05-10",
    "Male",
    "9999999999",
    "Haldwani",
    "B+",
    "2026-09-25"
)

print("Valid patient added. ID:", patient_id)


# Test 2: Try duplicate phone number
try:
    service.add_patient(
        "Another Patient",
        "2002-01-01",
        "Female",
        "8888888888",
        "Haldwani",
        "O+",
        "2026-09-25"
    )

except ValueError as error:
    print("Duplicate test passed:", error)


# Test 3: Try invalid phone number
try:
    service.add_patient(
        "Invalid Patient",
        "2000-01-01",
        "Male",
        "12345",
        "Haldwani",
        "A+",
        "2026-09-25"
    )

except ValueError as error:
    print("Validation test passed:", error)