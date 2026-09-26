from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self):
        self.repository = UserRepository()

    def login(self, username, password):
        username = username.strip()

        if not username:
            raise ValueError("Username is required.")

        if not password:
            raise ValueError("Password is required.")

        user = self.repository.get_user_by_username(username)

        if user is None:
            raise ValueError("Invalid username or password.")

        if user["password"] != password:
            raise ValueError("Invalid username or password.")

        return {
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"]
        }

    def has_permission(self, role, permission):
        permissions = {
            "admin": {
                "manage_patients",
                "manage_doctors",
                "manage_appointments",
                "manage_billing",
                "import_csv",
                "view_reports",
                "view_performance"
            },

            "staff": {
                "manage_patients",
                "manage_appointments",
                "manage_billing",
                "view_reports"
            }
        }

        return permission in permissions.get(role, set())