from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .security import decode_token
from .database import get_db
from . import models

bearer = HTTPBearer(auto_error=True)

def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> models.User:
    token = creds.credentials
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        user = db.query(models.User).get(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid user")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def require_admin(user: models.User = Depends(current_user)) -> models.User:
    if user.role != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    return user
