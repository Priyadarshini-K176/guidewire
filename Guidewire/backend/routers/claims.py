from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
import random
from .. import models, schemas
from ..database import get_db

router = APIRouter()

COVERAGE_MAPPING = {
    "Base": ["Heavy Rainfall", "Severe Air Pollution"],
    "Plus": ["Heavy Rainfall", "Severe Air Pollution", "Extreme Heat"],
    "Pro": ["Heavy Rainfall", "Severe Air Pollution", "Extreme Heat", "Curfew", "App Outage"]
}

MAX_DAILY_PAYOUT = {
    "Base": 250.0,
    "Plus": 500.0,
    "Pro": 800.0
}

@router.post("/evaluate/{worker_id}", response_model=schemas.ClaimResponse)
def evaluate_claim(worker_id: int, claim_req: schemas.ClaimCreate, db: Session = Depends(get_db)):
    db_worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Find active policy for worker
    today = date.today()
    policy = db.query(models.Policy).filter(
        models.Policy.worker_id == worker_id,
        models.Policy.is_active == True,
        models.Policy.start_date <= today,
        models.Policy.end_date >= today
    ).first()

    if not policy:
        raise HTTPException(status_code=400, detail="No active policy found for this worker")

    # Verify if tier covers the trigger type
    covered_triggers = COVERAGE_MAPPING.get(policy.tier, [])
    if claim_req.trigger_type not in covered_triggers:
        raise HTTPException(status_code=400, detail=f"Trigger '{claim_req.trigger_type}' not covered by {policy.tier} tier")

    # Fraud Anomaly Check Simulation
    anomaly_score = random.uniform(0.0, 1.0)
    
    if anomaly_score < 0.35:
        status = "APPROVED"
        # Standard payout simulation based on tier
        amount = MAX_DAILY_PAYOUT.get(policy.tier, 0.0)
    else:
        status = "FLAGGED_FOR_REVIEW"
        amount = 0.0

    new_claim = models.Claim(
        policy_id=policy.id,
        trigger_type=claim_req.trigger_type,
        zone=claim_req.zone,
        status=status,
        amount=amount,
        anomaly_score=anomaly_score
    )

    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)

    # For instant payout simulation we could call a mock payment gateway here
    # MockPaymentGateway.transfer(db_worker.phone_number, amount)

    return new_claim

@router.get("/{worker_id}", response_model=list[schemas.ClaimResponse])
def get_worker_claims(worker_id: int, db: Session = Depends(get_db)):
    # Find policies of worker
    policies = db.query(models.Policy).filter(models.Policy.worker_id == worker_id).all()
    policy_ids = [p.id for p in policies]

    claims = db.query(models.Claim).filter(models.Claim.policy_id.in_(policy_ids)).all()
    return claims
