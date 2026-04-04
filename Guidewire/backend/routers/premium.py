# routers/premium.py

from fastapi import APIRouter
from pydantic import BaseModel
from ..services.premium_service import calculate_premium

router = APIRouter()

class PremiumRequest(BaseModel):
    tier: str
    active_weeks: int
    zone_risk: float
    weather_risk: float

@router.post("/calculate-premium")
def get_premium(data: PremiumRequest):
    return calculate_premium(data)