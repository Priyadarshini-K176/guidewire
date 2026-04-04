# services/premium_service.py

TIER_BASE_RATES = {
    "Base": 29,
    "Plus": 59,
    "Pro": 99
}

def calculate_premium(data):
    base_premium = TIER_BASE_RATES.get(data.tier, 29)

    # Loyalty factor
    loyalty_factor = 1 - (min(data.active_weeks, 52) * 0.002)

    # Final premium
    final_premium = base_premium * data.zone_risk * data.weather_risk * loyalty_factor
    final_premium = round(final_premium, 2)

    # Messages (AI feel)
    messages = []

    if data.zone_risk > 1.2:
        messages.append("High flood-risk area")

    if data.weather_risk > 1.3:
        messages.append("Severe weather forecast")

    if data.active_weeks > 20:
        messages.append("Loyalty discount applied")

    return {
        "weekly_premium": final_premium,
        "breakdown": {
            "base": base_premium,
            "zone_risk": data.zone_risk,
            "weather_risk": data.weather_risk,
            "loyalty_factor": round(loyalty_factor, 2)
        },
        "message": messages
    }