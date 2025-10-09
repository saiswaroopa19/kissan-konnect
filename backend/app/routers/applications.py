from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime

from ..database import get_db
from .. import models, schemas
from ..deps import current_user, require_admin

router = APIRouter(prefix="/applications", tags=["Applications"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# Farmer-side endpoints
# =========================

@router.post("", response_model=schemas.ApplicationOut, status_code=201)
def create_application(
    payload: schemas.ApplicationCreate,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(current_user)
):
    # 1️⃣ Prevent duplicate pending/under_review for same program
    exists = db.query(models.Application).filter(
        models.Application.user_id == user.id,
        models.Application.program_id == payload.program_id,
        models.Application.status.in_(["pending", "under_review"])
    ).first()
    if exists:
        raise HTTPException(
            status_code=400,
            detail="You already have an application in progress for this program."
        )

    # 2️⃣ Create the new application
    app = models.Application(
        user_id=user.id,
        program_id=payload.program_id,
        crop_id=payload.crop_id,
        acreage=payload.acreage,
        season=payload.season,
        status="pending"
    )
    db.add(app)
    db.commit()
    db.refresh(app)

    # 3️⃣ Record initial status history
    db.add(models.ApplicationStatusHistory(
        application_id=app.id,
        status="pending",
        note="Submitted"
    ))
    db.commit()

    # 4️⃣ ✅ Link the user's uploaded document (if they have one)
    if getattr(user, "doc_path", None):
        existing_doc = db.query(models.Document).filter(
            models.Document.user_id == user.id,
            models.Document.application_id == app.id
        ).first()

        if not existing_doc:
            doc = models.Document(
                kind="Govt ID",
                file_path=user.doc_path,
                user_id=user.id,
                application_id=app.id
            )
            db.add(doc)
            db.commit()
            db.refresh(doc)

    # 5️⃣ Return the created application
    return app


@router.get("", response_model=List[schemas.ApplicationOut])
def my_applications(db: Session = Depends(get_db), user=Depends(current_user)):
    apps = db.query(models.Application).filter(
        models.Application.user_id == user.id
    ).order_by(models.Application.submitted_at.desc()).all()
    return apps


@router.get("/{app_id}", response_model=schemas.ApplicationOut)
def get_application(app_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    app = db.query(models.Application).get(app_id)
    if not app or app.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    return app


@router.post("/{app_id}/documents")
def upload_document(
    app_id: int,
    kind: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(current_user)
):
    app = db.query(models.Application).get(app_id)
    if not app or app.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")

    filename_safe = file.filename.replace(" ", "_")
    fname = os.path.join(UPLOAD_DIR, f"app{app.id}_{kind}_{filename_safe}")

    with open(fname, "wb") as f:
        f.write(file.file.read())

    doc = models.Document(application_id=app.id, kind=kind, file_path=fname)
    db.add(doc)
    db.commit()
    return {"ok": True, "path": fname}


# (Legacy) raw upload – leaving as-is if used elsewhere
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

# =========================
# Admin endpoints
# =========================

@router.get("/admin/list", response_model=List[schemas.ApplicationOut])
def list_all(status: Optional[str] = None, db: Session = Depends(get_db), admin=Depends(require_admin)):
    q = db.query(models.Application)
    if status:
        q = q.filter(models.Application.status == status)
    return q.order_by(models.Application.submitted_at.desc()).all()


@router.get("/admin/{app_id}/details", response_model=schemas.AdminApplicationDetailOut)
def admin_application_details(app_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    app = db.query(models.Application).get(app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    user = db.query(models.User).get(app.user_id)
    program = db.query(models.Program).get(app.program_id)
    crop = db.query(models.Crop).get(app.crop_id)

    # ✅ Slightly improved query: show docs linked by either app_id or user_id
    documents = db.query(models.Document).filter(
        (models.Document.application_id == app.id) |
        (models.Document.user_id == app.user_id)
    ).all()

    if not user or not program or not crop:
        raise HTTPException(status_code=500, detail="Related data missing")

    return {
        "application": app,
        "user": user,
        "program": program,
        "crop": crop,
        "documents": documents
    }


@router.post("/admin/{app_id}/status", response_model=schemas.ApplicationOut)
def update_status(
    app_id: int,
    payload: schemas.StatusUpdateIn,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """
    Transition rules:
      - 'under_review'   -> always allowed
      - 'approved'       -> requires basic checks to pass
      - 'rejected'       -> requires remarks (visible to farmer)
    Remarks are saved on the Application and returned to the farmer via ApplicationOut.
    """
    app = db.query(models.Application).get(app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Not found")

    # Quick lookups for validation
    program = db.query(models.Program).get(app.program_id)
    user = db.query(models.User).get(app.user_id)
    docs = db.query(models.Document).filter(models.Document.application_id == app.id).all()

    new_status = payload.status
    remarks = payload.remarks or None

    # Require remarks when rejecting
    if new_status == "rejected" and not remarks:
        raise HTTPException(status_code=400, detail="Remarks are required when rejecting an application.")

    # Basic guardrails when approving
    if new_status == "approved":
        # 1) Land-size within program bounds (if configured)
        if program:
            if program.min_land_size is not None and app.acreage < program.min_land_size:
                raise HTTPException(status_code=400, detail=f"Acreage {app.acreage} < program min {program.min_land_size}")
            if program.max_land_size is not None and app.acreage > program.max_land_size:
                raise HTTPException(status_code=400, detail=f"Acreage {app.acreage} > program max {program.max_land_size}")
            # 2) Season match if program has a fixed season
            if program.season and program.season != "Any" and app.season != program.season:
                raise HTTPException(status_code=400, detail=f"Season must be {program.season} for this program.")

        # 3) Minimal identity/doc check
        if not user or not user.aadhar:
            raise HTTPException(status_code=400, detail="User Aadhar missing; cannot approve.")
        if len(docs) == 0:
            raise HTTPException(status_code=400, detail="No supporting documents uploaded; cannot approve.")

    # Apply update
    app.status = new_status
    app.remarks = remarks  # ✅ visible to farmer via ApplicationOut
    db.add(models.ApplicationStatusHistory(
        application_id=app.id,
        status=new_status,
        note=remarks,
        by_admin_id=admin.id
    ))
    db.commit()
    db.refresh(app)
    return app
