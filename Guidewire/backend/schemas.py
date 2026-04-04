from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# --- Worker Schemas ---
class WorkerBase(BaseModel):
    phone_number: str
    name: str
    platform: str
    location_zone: str

class WorkerCreate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int
    is_verified: bool
    kyc_document_id: Optional[str] = None
    active_weeks: int

    class Config:
        from_attributes = True

# --- Claim Schemas ---
class ClaimBase(BaseModel):
    trigger_type: str
    zone: str

class ClaimCreate(ClaimBase):
    pass

class ClaimResponse(ClaimBase):
    id: int
    policy_id: int
    timestamp: datetime
    status: str
    amount: float
    anomaly_score: Optional[float] = None

    class Config:
        from_attributes = True

# --- Policy Schemas ---
class PolicyBase(BaseModel):
    tier: str
    weekly_premium: float
    start_date: date
    end_date: date

class PolicyCreate(BaseModel):
    worker_id: int
    tier: str # "Base", "Plus", "Pro" 

class Policy(PolicyBase):
    id: int
    worker_id: int
    is_active: bool

    class Config:
        from_attributes = True

class PolicyWithClaims(Policy):
    claims: List[ClaimResponse] = []

    class Config:
        from_attributes = True

# Extended Worker Schema to include policies
class WorkerWithPolicies(Worker):
    policies: List[PolicyWithClaims] = []

    class Config:
        from_attributes = True
