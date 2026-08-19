import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

from database import get_connection
from config import Config


def register_user(full_name, email, password, role="Customer"):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Check if email already exists
        cursor.execute(
            "SELECT UserId FROM User WHERE Email = %s",
            (email,)
        )

        if cursor.fetchone():
            return None, "Email already registered"

        # Hash password
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        query = """
            INSERT INTO User
            (FullName, Email, PasswordHash, Role)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                full_name,
                email,
                password_hash,
                role
            )
        )

        connection.commit()

        return cursor.lastrowid, None

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def login_user(email, password):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT UserId, FullName, Email, PasswordHash, Role
            FROM User
            WHERE Email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if not user:
            return None, "Invalid email or password"

        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            user["PasswordHash"].encode("utf-8")
        )

        if not password_valid:
            return None, "Invalid email or password"

        payload = {
            "user_id": user["UserId"],
            "email": user["Email"],
            "role": user["Role"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=2)
        }

        token = jwt.encode(
            payload,
            Config.JWT_SECRET,
            algorithm="HS256"
        )

        user.pop("PasswordHash")

        return {
            "user": user,
            "token": token
        }, None

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()