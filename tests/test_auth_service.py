from app.services.auth_service import AuthService


def main():
    print("Testing Authentication Service...\n")

    service = AuthService()

    # Test valid admin login
    user = service.login("admin", "admin123")

    print("Valid login test passed.")
    print("Username:", user["username"])
    print("Role:", user["role"])

    # Test wrong password
    try:
        service.login("admin", "wrongpassword")
        print("ERROR: Wrong password was accepted.")

    except ValueError as error:
        print("Wrong password test passed:", error)

    # Test invalid username
    try:
        service.login("wronguser", "admin123")
        print("ERROR: Invalid username was accepted.")

    except ValueError as error:
        print("Invalid username test passed:", error)

    # Test empty username
    try:
        service.login("", "admin123")
        print("ERROR: Empty username was accepted.")

    except ValueError as error:
        print("Empty username test passed:", error)

    # Test permissions
    if service.has_permission("admin", "manage_patients"):
        print("Admin permission test passed.")

    else:
        print("ERROR: Admin permission failed.")

    if not service.has_permission("staff", "import_csv"):
        print("Staff restriction test passed.")

    else:
        print("ERROR: Staff received admin-only permission.")

    print("\nAuthentication Service test completed.")


if __name__ == "__main__":
    main()