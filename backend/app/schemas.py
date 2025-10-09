from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional, Literal, List
from datetime import date

class RegisterIn(BaseModel):
    name: str
    email: str
    password: str
    phone: constr(pattern=r'^[6-9]\d{9}$')
    gender: Optional[str] = None
    dob: Optional[str] = None
    state: str
    district: str
    aadhar: Optional[constr(pattern=r'^\d{12}$')] = None   # ✅ must exist
    doc_path: Optional[str] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    gender: Optional[str]
    dob: Optional[str]
    state: Optional[str]
    district: Optional[str]
    aadhar: Optional[str] = None
    role: str

    class Config:
        from_attributes = True

class ForgotPasswordIn(BaseModel):
    email: str

class ResetPasswordIn(BaseModel):
    token: str
    new_password: str

class LoginIn(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut

class RefreshTokenIn(BaseModel):
    refresh_token: str

class FarmIn(BaseModel):
    land_size_acres: float
    address: Optional[str] = None

class CropOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class ProgramOut(BaseModel):
    id: int
    title: str
    description: str
    authority: str
    season: Optional[str] = None
    min_land_size: Optional[float] = None
    max_land_size: Optional[float] = None
    is_active: bool
    class Config:
        from_attributes = True

class ApplicationCreate(BaseModel):
    program_id: int
    crop_id: int
    acreage: float
    season: Literal["Kharif","Rabi","Zaid","Any"]

class ApplicationOut(BaseModel):
    id: int
    program_id: int
    crop_id: int
    acreage: float
    season: str
    status: str
    score: Optional[float] = None
    remarks: Optional[str] = None
    class Config:
        from_attributes = True

class StatusUpdateIn(BaseModel):
    status: Literal["pending","under_review","approved","rejected"]
    remarks: Optional[str] = None  # ✅ shown to farmers via ApplicationOut.remarks

class NotificationOut(BaseModel):
    id: int
    type: str
    title: str
    body: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    aadhar: Optional[str] = None
    doc_path: Optional[str] = None

    class Config:
        orm_mode = True

# ===== Admin Review Detail =====

class DocumentOut(BaseModel):
    id: int
    kind: str
    file_path: str
    class Config:
        from_attributes = True

class AdminApplicationDetailOut(BaseModel):
    # A single payload that returns everything the admin needs to see
    application: ApplicationOut
    user: UserOut
    program: ProgramOut
    crop: CropOut
    documents: List[DocumentOut]