from app.database.database import get_connection


class UserRepository:

    def get_user_by_username(self, username):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    user_id,
                    username,
                    password,
                    role
                FROM users
                WHERE username = ?
                """,
                (username,)
            ).fetchone()

        finally:
            connection.close()

    def add_user(self, username, password, role):
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO users (
                    username,
                    password,
                    role
                )
                VALUES (?, ?, ?)
                """,
                (username, password, role)
            )

            connection.commit()
            return cursor.lastrowid

        finally:
            connection.close()

    def get_all_users(self):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    user_id,
                    username,
                    role
                FROM users
                ORDER BY user_id
                """
            ).fetchall()

        finally:
            connection.close()