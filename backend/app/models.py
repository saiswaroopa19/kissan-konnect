from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# =========================================================
# USERS
# =========================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)
    password_hash = Column(String, nullable=False)
    gender = Column(String)
    dob = Column(String)
    state = Column(String)
    district = Column(String)
    aadhar = Column(String, unique=True, nullable=True)
    doc_path = Column(String, nullable=True)  # store uploaded file path
    role = Column(String, default="farmer")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    farms = relationship("Farm", back_populates="user")
    applications = relationship("Application", back_populates="user")
    documents = relationship("Document", back_populates="user", cascade="all, delete")  # ✅ added


# =========================================================
# FARMS
# =========================================================
class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    land_size_acres = Column(Float, nullable=False, default=1.0)
    address = Column(Text)

    user = relationship("User", back_populates="farms")


# =========================================================
# CROPS
# =========================================================
class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


# =========================================================
# PROGRAMS
# =========================================================
class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    authority = Column(String, default="Dept. of Agriculture")
    season = Column(String)  # Kharif | Rabi | Zaid | Any
    min_land_size = Column(Float, nullable=True)
    max_land_size = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ProgramCrop(Base):
    __tablename__ = "program_crops"
    program_id = Column(Integer, ForeignKey("programs.id"), primary_key=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), primary_key=True)


# =========================================================
# APPLICATIONS
# =========================================================
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), index=True, nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), index=True, nullable=False)
    acreage = Column(Float, nullable=False)
    season = Column(String, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending | under_review | approved | rejected
    score = Column(Float, nullable=True)
    remarks = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="applications")
    documents = relationship("Document", back_populates="application", cascade="all, delete")  # ✅ added


# =========================================================
# APPLICATION STATUS HISTORY
# =========================================================
class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), index=True, nullable=False)
    status = Column(String, nullable=False)
    at = Column(DateTime, default=datetime.utcnow)
    by_admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    note = Column(Text, nullable=True)


# =========================================================
# DOCUMENTS
# =========================================================
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    kind = Column(String, nullable=False)  # ID_PROOF | LAND_DOC | BANK | OTHER
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # ✅ NEW FIELDS
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    application_id = Column(Integer, ForeignKey("applications.id"), index=True, nullable=True)

    # ✅ Relationships
    user = relationship("User", back_populates="documents")
    application = relationship("Application", back_populates="documents")


# =========================================================
# TOKENS
# =========================================================
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    used = Column(Boolean, default=False)
