from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

# 🔐 Must match what's in deps.py
SECRET_KEY = "supersecret"          # ⚠️ Change this to a long, random string in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------
# ✅ Password Hashing
# -----------------------
def hash_pw(password: str) -> str:
    return pwd_context.hash(password)

def verify_pw(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -----------------------
# ✅ Token Creation
# -----------------------
def make_access_token(user_id: int, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),       # 👈 required by deps.py
        "role": role,
        "exp": expire,
        "typ": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def make_refresh_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": str(user_id),       # 👈 required
        "exp": expire,
        "typ": "refresh"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# -----------------------
# ✅ Token Decoding
# -----------------------
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Invalid or expired token")
