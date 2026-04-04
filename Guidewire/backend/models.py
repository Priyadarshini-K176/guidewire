from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime
import datetime
from sqlalchemy.orm import relationship
from .database import Base

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    name = Column(String)
    platform = Column(String) # e.g., "Zomato", "Swiggy"
    is_verified = Column(Boolean, default=False)
    kyc_document_id = Column(String, nullable=True) # Mock document ID
    location_zone = Column(String)
    active_weeks = Column(Integer, default=0)

    policies = relationship("Policy", back_populates="worker")

class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    tier = Column(String) # Base, Plus, Pro, Dynamic
    weekly_premium = Column(Float)
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)

    worker = relationship("Worker", back_populates="policies")
    claims = relationship("Claim", back_populates="policy")

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"))
    trigger_type = Column(String) 
    zone = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String) # "APPROVED", "FLAGGED_FOR_REVIEW", "REJECTED"
    amount = Column(Float)
    anomaly_score = Column(Float, nullable=True)

    policy = relationship("Policy", back_populates="claims")
