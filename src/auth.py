"""
Authentication and Role-Based Access Control (RBAC) Module.
BBAT104: Fundamentals of Total Quality Management
Student: Bhupinder Singh | Roll No: 2410301011 | CSE - A
"""

from typing import Optional, Dict, Any
from src.database import get_db_cursor, hash_password


class SessionManager:
    """Manages global user session and role-based permissions."""
    _current_user: Optional[Dict[str, Any]] = None

    @classmethod
    def set_user(cls, user_data: Dict[str, Any]):
        cls._current_user = user_data

    @classmethod
    def get_user(cls) -> Optional[Dict[str, Any]]:
        return cls._current_user

    @classmethod
    def clear(cls):
        cls._current_user = None

    @classmethod
    def is_authenticated(cls) -> bool:
        return cls._current_user is not None

    @classmethod
    def get_role(cls) -> str:
        return cls._current_user.get("role", "Guest") if cls._current_user else "Guest"

    @classmethod
    def is_admin(cls) -> bool:
        return cls.get_role() == "Admin"

    @classmethod
    def can_manage_doctors(cls) -> bool:
        return cls.get_role() in ("Admin",)

    @classmethod
    def can_register_patients(cls) -> bool:
        return cls.get_role() in ("Admin", "Receptionist")

    @classmethod
    def can_manage_appointments(cls) -> bool:
        return cls.get_role() in ("Admin", "Receptionist", "Doctor")

    @classmethod
    def can_bill(cls) -> bool:
        return cls.get_role() in ("Admin", "Billing")


def authenticate(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate user against the SQLite database using SHA-256 password hash.
    """
    pwd_hash = hash_password(password)
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, username, full_name, role, status
            FROM users
            WHERE username = ? AND password_hash = ? AND status = 'Active'
            """,
            (username.strip(), pwd_hash)
        )
        row = cursor.fetchone()
        if row:
            user_data = dict(row)
            SessionManager.set_user(user_data)
            return user_data
    return None
