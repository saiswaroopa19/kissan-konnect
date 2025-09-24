from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas
from ..deps import current_user

router = APIRouter(prefix="/programs", tags=["Programs"])

@router.get("", response_model=List[schemas.ProgramOut])
def list_programs(crop_id: Optional[int] = None, season: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(models.Program).filter(models.Program.is_active == True)
    if crop_id:
        q = q.join(models.ProgramCrop, models.Program.id == models.ProgramCrop.program_id).filter(models.ProgramCrop.crop_id == crop_id)
    if season and season != "Any":
        q = q.filter(models.Program.season == season)
    return q.order_by(models.Program.title.asc()).all()

@router.get("/{pid}", response_model=schemas.ProgramOut)
def get_program(pid: int, db: Session = Depends(get_db)):
    return db.query(models.Program).get(pid)

@router.get("/match/me", response_model=List[schemas.ProgramOut])
def match_for_me(db: Session = Depends(get_db), user = Depends(current_user), crop_id: Optional[int] = None, land_size: Optional[float] = None, season: Optional[str] = None):
    # simple eligibility: crop in program_crops, land between min/max, season matches
    q = db.query(models.Program).filter(models.Program.is_active == True)
    if crop_id:
        q = q.join(models.ProgramCrop, models.Program.id == models.ProgramCrop.program_id).filter(models.ProgramCrop.crop_id == crop_id)
    progs = q.all()
    res = []
    for p in progs:
        ok = True
        if season and p.season and p.season != "Any" and p.season != season:
            ok = False
        if land_size is not None:
            if p.min_land_size is not None and land_size < p.min_land_size: ok = False
            if p.max_land_size is not None and land_size > p.max_land_size: ok = False
        if ok:
            res.append(p)
    return res
