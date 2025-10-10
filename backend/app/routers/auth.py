from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid, traceback

from ..database import get_db
from .. import models, schemas, security

router = APIRouter(prefix="/auth", tags=["Auth"])

# ----------------------------------------------------------
# ✅ REGISTER FARMER (Public - No auth required)
# ----------------------------------------------------------
@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(payload: schemas.RegisterIn, db: Session = Depends(get_db)):
    print("📩 Register payload received:", payload.dict())

    # Check if email already exists
    existing_email = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if Aadhaar already exists
    if payload.aadhar:
        existing_aadhar = db.query(models.User).filter(models.User.aadhar == payload.aadhar).first()
        if existing_aadhar:
            raise HTTPException(status_code=400, detail="Aadhaar already registered")

    try:
        user = models.User(
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            gender=payload.gender,
            dob=str(payload.dob) if payload.dob else None,   # ✅ Convert date to string if needed
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
        print(f"✅ User registered successfully: {user.email}")
        return user

    except IntegrityError as e:
        db.rollback()
        print("❌ IntegrityError during registration:", e.orig)
        raise HTTPException(status_code=400, detail="Duplicate or invalid user data")
    except Exception as e:
        db.rollback()
        print("❌ Unexpected Error in register():", traceback.format_exc())
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")


# ----------------------------------------------------------
# ✅ LOGIN (works for both admin and farmer)
# ----------------------------------------------------------
@router.post("/login", response_model=schemas.TokenOut)
def login(payload: schemas.LoginIn, db: Session = Depends(get_db)):
    print("🔑 Login attempt:", payload.dict())
    user = db.query(models.User).filter(models.User.email == payload.email).first()

    if not user:
        print("❌ Login failed: User not found")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not security.verify_pw(payload.password, user.password_hash):
        print("❌ Login failed: Incorrect password")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = security.make_access_token(user.id, user.role)
    refresh_token = security.make_refresh_token(user.id)

    db.add(models.RefreshToken(user_id=user.id, token=refresh_token))
    db.commit()

    print(f"✅ Login successful for: {user.email}")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user
    }


# ----------------------------------------------------------
# ✅ REFRESH TOKEN
# ----------------------------------------------------------
@router.post("/refresh", response_model=schemas.TokenOut)
def refresh_token(payload: schemas.RefreshTokenIn, db: Session = Depends(get_db)):
    try:
        data = security.decode_token(payload.refresh_token)
        if data.get("typ") != "refresh":
            raise ValueError("Invalid token type")

        rt = db.query(models.RefreshToken).filter(
            models.RefreshToken.token == payload.refresh_token,
            models.RefreshToken.revoked == False
        ).first()
        if not rt:
            raise ValueError("Refresh token revoked or not found")

        user = db.query(models.User).get(int(data["sub"]))
        if not user:
            raise ValueError("User not found")

        rt.revoked = True
        new_refresh = security.make_refresh_token(user.id)
        db.add(models.RefreshToken(user_id=user.id, token=new_refresh))
        db.commit()

        new_access = security.make_access_token(user.id, user.role)
        print(f"♻️ Tokens refreshed for user: {user.email}")
        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "user": user
        }

    except Exception as e:
        print("❌ Refresh token error:", traceback.format_exc())
        raise HTTPException(status_code=401, detail=f"Invalid refresh token: {str(e)}")


# ----------------------------------------------------------
# ✅ FORGOT PASSWORD
# ----------------------------------------------------------
@router.post("/forgot-password")
def forgot_password(payload: schemas.ForgotPasswordIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user:
        return {"msg": "If this email exists, a reset link has been sent."}

    token = str(uuid.uuid4())
    reset = models.PasswordResetToken(user_id=user.id, token=token)
    db.add(reset)
    db.commit()

    print(f"🔗 Password reset token generated for {user.email}: {token}")
    return {"msg": "Reset token generated", "token": token}


# ----------------------------------------------------------
# ✅ RESET PASSWORD
# ----------------------------------------------------------
@router.post("/reset-password")
def reset_password(payload: schemas.ResetPasswordIn, db: Session = Depends(get_db)):
    reset = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token == payload.token,
        models.PasswordResetToken.used == False
    ).first()

    if not reset:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == reset.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = security.hash_pw(payload.new_password)
    reset.used = True
    db.commit()

    print(f"🔐 Password reset successful for {user.email}")
    return {"msg": "Password reset successful"}
