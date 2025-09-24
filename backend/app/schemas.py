from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List
from pydantic import BaseModel
from pydantic import BaseModel, constr
from typing import Optional

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
    state: str
    district: str
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
    remarks: Optional[str] = None

class NotificationOut(BaseModel):
    id: int
    type: str
    title: str
    body: str
