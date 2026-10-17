from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from .config import settings


def hash_password(p: str) -> str:
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()


def verify_password(p: str, h: str) -> bool:
    try:
        return bcrypt.checkpw(p.encode(), h.encode())
    except ValueError:
        return False


def create_token(uid: str, email: str, rol: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "uid": uid,
        "email": email,
        "rol": rol,
        "iat": now,
        "exp": now + timedelta(hours=settings.JWT_EXP_HOURS),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None