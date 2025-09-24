import os, jwt
from datetime import datetime, timedelta, timezone
from passlib.hash import bcrypt
from typing import Tuple

JWT_SECRET = os.getenv("KK_JWT_SECRET", "change_me")
ALGO = "HS256"
ACCESS_TTL_MIN = 30
REFRESH_TTL_DAYS = 7

def hash_pw(pw: str) -> str:
    return bcrypt.hash(pw)

def verify_pw(pw: str, hashed: str) -> bool:
    return bcrypt.verify(pw, hashed)

def make_access_token(sub: int, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": sub, "role": role, "iat": int(now.timestamp()), "exp": int((now + timedelta(minutes=ACCESS_TTL_MIN)).timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)

def make_refresh_token(sub: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": sub, "typ": "refresh", "iat": int(now.timestamp()), "exp": int((now + timedelta(days=REFRESH_TTL_DAYS)).timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
