from data.database import insert_query, read_query
from auth import hash_passowrd
from data.models import CreateUser
from config import settings
from fastapi import HTTPException, status


def create_user(user: CreateUser):
    if user.role == "ADMIN":
        if user.admin_secret != settings.ADMIN_SECRET:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid admin secret"
            )

    user_existence = read_query("SELECT id FROM users WHERE username = ?", (user.username,))
    if user_existence:
        return False

    user_password_hash = hash_passowrd(user.password)
    insert_query(
        "INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
        (user.username, user_password_hash, user.role),
    )
    return True


def get_user_by_username(username: str):
    result = read_query("SELECT * FROM users WHERE username = ?", (username,))
    return result[0] if result else None
    