from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from ..database import get_db
from .. import models, schemas, security

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(payload: schemas.RegisterIn, db: Session = Depends(get_db)):
    try:
        print(payload)
        if db.query(models.User).filter(models.User.email == payload.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        if payload.aadhar and db.query(models.User).filter(models.User.aadhar == payload.aadhar).first():
            raise HTTPException(status_code=400, detail="Aadhaar already registered")

        user = models.User(
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            gender=payload.gender,
            dob=payload.dob,
            state=payload.state,
            district=payload.district,
            password_hash=security.hash_pw(payload.password),
            role="farmer",
            aadhar=payload.aadhar,
            doc_path=payload.doc_path
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid register")

@router.post("/login", response_model=schemas.TokenOut)
def login(payload: schemas.LoginIn, db: Session = Depends(get_db)):
    print(payload)
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not security.verify_pw(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = security.make_access_token(user.id, user.role)
    refresh = security.make_refresh_token(user.id)
    db.add(models.RefreshToken(user_id=user.id, token=refresh))
    db.commit()
    return {"access_token": access, "refresh_token": refresh, "user": user}

@router.post("/refresh", response_model=schemas.TokenOut)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        data = security.decode_token(refresh_token)
        if data.get("typ") != "refresh":
            raise ValueError("not refresh")
        rt = db.query(models.RefreshToken).filter(
            models.RefreshToken.token == refresh_token,
            models.RefreshToken.revoked == False
        ).first()
        if not rt:
            raise ValueError("revoked or not found")
        user = db.query(models.User).get(int(data["sub"]))
        access = security.make_access_token(user.id, user.role)
        rt.revoked = True
        new_refresh = security.make_refresh_token(user.id)
        db.add(models.RefreshToken(user_id=user.id, token=new_refresh))
        db.commit()
        return {"access_token": access, "refresh_token": new_refresh, "user": user}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


# -------------------------
# Forgot/Reset Password Flow
# -------------------------

@router.post("/forgot-password")
def forgot_password(payload: schemas.ForgotPasswordIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user:
        # don’t reveal if user exists (security best practice)
        return {"msg": "If this email exists, a reset link has been sent."}
    
    token = str(uuid.uuid4())
    reset = models.PasswordResetToken(user_id=user.id, token=token)
    db.add(reset)
    db.commit()

    # ⚠️ For demo: return token in response
    # In production: send email/SMS instead
    return {"msg": "Reset token generated", "token": token}

@router.post("/reset-password")
def reset_password(payload: schemas.ResetPasswordIn, db: Session = Depends(get_db)):
    reset = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token == payload.token,
        models.PasswordResetToken.used == False
    ).first()

    if not reset:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == reset.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # update password
    user.password_hash = security.hash_pw(payload.new_password)
    reset.used = True
    db.commit()

    return {"msg": "Password reset successful"}
