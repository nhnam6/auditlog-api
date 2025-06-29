"""Utility functions for the authentication service"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from config import settings


def hash_password(password: str) -> str:
    """Hash password with bcrypt and return string"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, stored_password: str):
    """Verify password"""
    plain_password_bytes = plain_password.encode("utf-8")

    if isinstance(stored_password, str):
        stored_password_bytes = stored_password.encode("utf-8")
    else:
        stored_password_bytes = stored_password
    return bcrypt.checkpw(plain_password_bytes, stored_password_bytes)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create access token"""

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError as err:
        raise ValueError("Invalid token") from err
