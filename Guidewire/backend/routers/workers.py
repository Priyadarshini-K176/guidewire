from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/workers",
    tags=["workers"],
)

@router.post("/register", response_model=schemas.Worker)
def register_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    # Check if worker already exists
    db_worker = db.query(models.Worker).filter(models.Worker.phone_number == worker.phone_number).first()
    if db_worker:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    new_worker = models.Worker(
        phone_number=worker.phone_number,
        name=worker.name,
        platform=worker.platform,
        location_zone=worker.location_zone
    )
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)
    return new_worker

@router.post("/{worker_id}/kyc", response_model=schemas.Worker)
def upload_kyc(worker_id: int, document_id: str, db: Session = Depends(get_db)):
    """Mock endpoint to simulate KYC / Platform ID verification"""
    db_worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    db_worker.kyc_document_id = document_id
    db_worker.is_verified = True
    
    db.commit()
    db.refresh(db_worker)
    return db_worker

@router.get("/{worker_id}", response_model=schemas.WorkerWithPolicies)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    db_worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker
