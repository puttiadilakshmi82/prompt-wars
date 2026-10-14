"""
Urgency & Multi-Factor Risk Scoring Engine for CivicPulse AI
Calculates real-time municipal priority score (0-100) and SLA deadlines based on
semantic risk triggers, population exposure, and community upvotes.
"""

from datetime import datetime, timedelta
from civicpulse.config import CATEGORIES, WARDS, SEVERITY_LEVELS

CRITICAL_HAZARDS = {
    "live wire": 30,
    "exposed wire": 25,
    "spark": 20,
    "gas leak": 35,
    "sinkhole": 30,
    "open manhole": 28,
    "collaps": 30,
    "sewage backflow": 22,
    "toxic": 28,
    "carcass": 18,
    "landslide": 30,
    "geyser": 20,
    "fracture": 18,
    "fire": 35,
    "submerged": 15,
    "crater": 20,
    "school": 12,
    "hospital": 15,
    "children": 12
}


def compute_urgency_score(title, description, category, ward, upvotes=0):
    """
    Computes holistic priority score (0-100) combining:
    - Base category urgency (30%)
    - Text semantic hazard triggers (35%)
    - Ward vulnerability & density multiplier (15%)
    - Community confirmation boost (20%)
    """
    text = f"{title.lower()} {description.lower()}"
    
    # 1. Base category score
    cat_info = CATEGORIES.get(category, {"base_urgency": 50, "default_sla_hours": 24})
    base_score = cat_info["base_urgency"]

    # 2. Semantic Hazard Triggers
    detected_hazards = []
    hazard_score = 0
    for keyword, bonus in CRITICAL_HAZARDS.items():
        if keyword in text:
            hazard_score += bonus
            detected_hazards.append(keyword)
    
    # Cap hazard boost to 40
    hazard_score = min(40, hazard_score)

    # 3. Ward Risk Multiplier
    ward_info = WARDS.get(ward, {"risk_factor": 1.0})
    ward_multiplier = ward_info.get("risk_factor", 1.0)

    # 4. Community Upvote / Confirmation Boost
    # Logarithmic-style scaling: upvotes add quick impact up to 20 pts
    upvote_boost = min(22, int(upvotes * 0.75))

    # Composite formula
    raw_score = (base_score * 0.35) + (hazard_score * 0.35) + (upvote_boost * 0.30)
    adjusted_score = raw_score * ward_multiplier

    # Bound strictly between 15 and 99
    final_score = int(min(99, max(15, round(adjusted_score))))

    # Map to Severity Tier
    severity = "Low"
    for tier, conf in SEVERITY_LEVELS.items():
        if conf["min"] <= final_score <= conf["max"]:
            severity = tier
            break

    # Calculate SLA target
    base_sla = cat_info.get("default_sla_hours", 24)
    if severity == "Critical":
        sla_hours = max(4, int(base_sla * 0.25))
    elif severity == "High":
        sla_hours = max(8, int(base_sla * 0.50))
    elif severity == "Medium":
        sla_hours = base_sla
    else:
        sla_hours = int(base_sla * 1.5)

    return {
        "urgency_score": final_score,
        "severity": severity,
        "sla_hours": sla_hours,
        "detected_hazards": detected_hazards,
        "ward_risk_factor": ward_multiplier,
        "recommendation": get_triage_recommendation(severity, category)
    }


def get_triage_recommendation(severity, category):
    """Provides automated municipal operational action directives."""
    if severity == "Critical":
        return f"IMMEDIATE DISPATCH REQUIRED: Auto-alert field emergency team for {category}. Secure cordon perimeter within 60 mins."
    elif severity == "High":
        return f"HIGH PRIORITY: Route to nearest municipal zonal unit. Dispatch work order on current shift."
    elif severity == "Medium":
        return f"SCHEDULED MAINTENANCE: Queue for inspection and routine batch repair within standard SLA."
    else:
        return "ROUTINE MONITORING: Logged for civic maintenance round."
