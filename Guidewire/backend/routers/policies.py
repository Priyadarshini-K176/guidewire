from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/policies",
    tags=["policies"],
)

# Mock static pricing based on tier
TIER_PRICING = {
    "Base": 29.0,
    "Plus": 59.0,
    "Pro": 99.0
}

@router.post("/create", response_model=schemas.Policy)
def create_policy(policy: schemas.PolicyCreate, db: Session = Depends(get_db)):
    db_worker = db.query(models.Worker).filter(models.Worker.id == policy.worker_id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    if not db_worker.is_verified:
        raise HTTPException(status_code=400, detail="Worker must complete KYC verification before buying a policy")
    
    if policy.tier not in TIER_PRICING:
        raise HTTPException(status_code=400, detail="Invalid policy tier")
        
    start_date = date.today()
    # Weekly coverage = 7 days
    end_date = start_date + timedelta(days=7)
    
    # Mocking static premium logic
    premium = TIER_PRICING[policy.tier]
    
    new_policy = models.Policy(
        worker_id=policy.worker_id,
        tier=policy.tier,
        weekly_premium=premium,
        start_date=start_date,
        end_date=end_date,
        is_active=True
    )
    
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy

@router.get("/worker/{worker_id}", response_model=list[schemas.Policy])
def get_worker_policies(worker_id: int, db: Session = Depends(get_db)):
    db_worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
        
    policies = db.query(models.Policy).filter(models.Policy.worker_id == worker_id).all()
    return policies
