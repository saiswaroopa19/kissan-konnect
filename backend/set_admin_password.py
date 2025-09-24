# set_admin_password.py
from app.database import SessionLocal
from app import models, security

def set_pw(email, new_pw):
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        print("User not found:", email)
        return
    user.password_hash = security.hash_pw(new_pw)
    db.add(user)
    db.commit()
    print(f"Password updated for {email}")

if __name__ == "__main__":
    # EDIT these values (or pass via sys.argv if you want)
    email_to_update = "admin@kissan.com"
    new_password = "Admin@12345"   # choose a secure password here
    set_pw(email_to_update, new_password)
