from app.services.appointment_service import AppointmentService


service = AppointmentService()


# Test 1: Add appointment
appointment_id = service.add_appointment(
    4,
    1,
    "2026-09-26",
    "10:30",
    "Scheduled"
)

print("Valid appointment added. ID:", appointment_id)


# Test 2: Invalid date
try:
    service.add_appointment(
        4,
        1,
        "26-09-2026",
        "11:00",
        "Scheduled"
    )
except ValueError as error:
    print("Date validation test passed:", error)


# Test 3: Invalid time
try:
    service.add_appointment(
        4,
        1,
        "2026-09-26",
        "25:00",
        "Scheduled"
    )
except ValueError as error:
    print("Time validation test passed:", error)


# Test 4: Invalid patient
try:
    service.add_appointment(
        9999,
        1,
        "2026-09-26",
        "12:00",
        "Scheduled"
    )
except ValueError as error:
    print("Patient validation test passed:", error)


# Test 5: Invalid doctor
try:
    service.add_appointment(
        4,
        9999,
        "2026-09-26",
        "13:00",
        "Scheduled"
    )
except ValueError as error:
    print("Doctor validation test passed:", error)


# Test 6: Get appointments
appointments = service.get_all_appointments()

print("Total appointments:", len(appointments))

for appointment in appointments:
    print(
        appointment["appointment_id"],
        appointment["patient_name"],
        appointment["doctor_name"],
        appointment["appointment_date"],
        appointment["appointment_time"],
        appointment["status"]
    )