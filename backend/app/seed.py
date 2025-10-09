from .database import Base, engine, SessionLocal
from . import models
from passlib.hash import bcrypt


def seed():
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # ----------------------------------------------------------------------
    # Crops
    # ----------------------------------------------------------------------
    crops = ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Pulses"]
    for c in crops:
        if not db.query(models.Crop).filter_by(name=c).first():
            db.add(models.Crop(name=c))
    db.commit()

    # ----------------------------------------------------------------------
    # Programs
    # ----------------------------------------------------------------------
    if not db.query(models.Program).first():
        progs = [
            (
                "Kharif Input Subsidy",
                "Support for input costs during Kharif season for smallholders.",
                "State Agriculture Dept.",
                "Kharif",
                0.5,
                5.0,
            ),
            (
                "Smallholder Equipment Grant",
                "Grant for small-scale farm equipment purchase.",
                "Central Agri Scheme",
                "Any",
                0.0,
                10.0,
            ),
            (
                "Soil Health Card",
                "Soil testing and advisory services subsidy.",
                "State Agriculture Dept.",
                "Any",
                None,
                None,
            ),
        ]
        for t, d, a, s, minl, maxl in progs:
            p = models.Program(
                title=t,
                description=d,
                authority=a,
                season=s,
                min_land_size=minl,
                max_land_size=maxl,
                is_active=True,
            )
            db.add(p)
        db.commit()

        # Link crops (simple: all programs support Rice + Wheat)
        rice = db.query(models.Crop).filter_by(name="Rice").first()
        wheat = db.query(models.Crop).filter_by(name="Wheat").first()
        for prog in db.query(models.Program).all():
            db.add(models.ProgramCrop(program_id=prog.id, crop_id=rice.id))
            db.add(models.ProgramCrop(program_id=prog.id, crop_id=wheat.id))
        db.commit()

    # ----------------------------------------------------------------------
    # Admin User
    # ----------------------------------------------------------------------
    if not db.query(models.User).filter_by(email="admin@kissan.com").first():
        db.add(
            models.User(
            name="Admin",
            email="admin@kissan.com",
            password_hash=bcrypt.hash("Admin@12345"),
            role="admin",
            state="Andhra Pradesh",
            district="HQ"     
            )
        )
    db.commit()

    db.close()


if __name__ == "__main__":
    seed()
