from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
from ..database import get_db
from .. import models, schemas
from ..deps import current_user, require_admin
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from datetime import datetime
router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/applications", tags=["Applications"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("", response_model=schemas.ApplicationOut, status_code=201)
def create_application(payload: schemas.ApplicationCreate, db: Session = Depends(get_db), user=Depends(current_user)):
    # prevent duplicate pending for same program
    exists = db.query(models.Application).filter(models.Application.user_id == user.id, models.Application.program_id == payload.program_id, models.Application.status.in_(["pending", "under_review"])).first()
    if exists:
        raise HTTPException(status_code=400, detail="You already have an application in progress for this program.")
    app = models.Application(
        user_id=user.id,
        program_id=payload.program_id,
        crop_id=payload.crop_id,
        acreage=payload.acreage,
        season=payload.season,
        status="pending"
    )
    db.add(app); db.commit(); db.refresh(app)
    hist = models.ApplicationStatusHistory(application_id=app.id, status="pending", note="Submitted")
    db.add(hist); db.commit()
    return app

@router.get("", response_model=List[schemas.ApplicationOut])
def my_applications(db: Session = Depends(get_db), user=Depends(current_user)):
    apps = db.query(models.Application).filter(models.Application.user_id == user.id).order_by(models.Application.submitted_at.desc()).all()
    return apps

@router.get("/{app_id}", response_model=schemas.ApplicationOut)
def get_application(app_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    app = db.query(models.Application).get(app_id)
    if not app or app.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    return app

@router.post("/{app_id}/documents")
def upload_document(app_id: int, kind: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(current_user)):
    app = db.query(models.Application).get(app_id)
    if not app or app.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    fname = f"{UPLOAD_DIR}/app{app.id}_{kind}_{file.filename}"
    with open(fname, "wb") as f:
        f.write(file.file.read())
    doc = models.Document(application_id=app.id, kind=kind, file_path=fname)
    db.add(doc); db.commit()
    return {"ok": True, "path": fname}

# Admin routes
@router.get("/admin/list", response_model=List[schemas.ApplicationOut])
def list_all(status: str | None = None, db: Session = Depends(get_db), admin=Depends(require_admin)):
    q = db.query(models.Application)
    if status:
        q = q.filter(models.Application.status == status)
    return q.order_by(models.Application.submitted_at.desc()).all()

@router.post("/admin/{app_id}/status", response_model=schemas.ApplicationOut)
def update_status(app_id: int, payload: schemas.StatusUpdateIn, db: Session = Depends(get_db), admin=Depends(require_admin)):
    app = db.query(models.Application).get(app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Not found")
    app.status = payload.status
    app.remarks = payload.remarks
    db.add(models.ApplicationStatusHistory(application_id=app.id, status=payload.status, note=payload.remarks, by_admin_id=admin.id))
    db.commit(); db.refresh(app)
    return app

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())

        return {"msg": "File uploaded", "path": filepath}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
