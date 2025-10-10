from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ✅ Get the database URL from environment variables
# If not set, default to local SQLite for development
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./kissan.db")

# ✅ Handle connection arguments based on database type
if DB_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

# ✅ Create the SQLAlchemy engine
engine = create_engine(DB_URL, connect_args=connect_args)

# ✅ Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for all database models
Base = declarative_base()


# ✅ Dependency: get database session for FastAPI routes
def get_db():
    from sqlalchemy.orm import Session
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
