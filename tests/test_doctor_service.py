from app.services.doctor_service import DoctorService


service = DoctorService()


doctor_id = service.add_doctor(
    "Dr. Amit Sharma",
    "Cardiologist",
    "8888888888",
    "Active"
)

print("Valid doctor added. ID:", doctor_id)


try:
    service.add_doctor(
        "Dr. Another Doctor",
        "Neurologist",
        "8888888888",
        "Active"
    )
except ValueError as error:
    print("Duplicate test passed:", error)


try:
    service.add_doctor(
        "Invalid Doctor",
        "Dentist",
        "12345",
        "Active"
    )
except ValueError as error:
    print("Validation test passed:", error)


doctors = service.get_all_doctors()

print("Total doctors:", len(doctors))

for doctor in doctors:
    print(
        doctor["doctor_id"],
        doctor["full_name"],
        doctor["specialization"],
        doctor["phone"],
        doctor["status"]
    )