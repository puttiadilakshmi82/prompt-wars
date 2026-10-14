"""
Predictive Community Problem & Infrastructure Degradation Engine
Forecasts future civic failures, recurring hotspots, and ward-level deterioration risks.
"""

from collections import defaultdict
from datetime import datetime
from civicpulse.config import WARDS, CATEGORIES


def run_predictive_risk_assessment(reports):
    """
    Analyzes historical and current incident patterns to forecast upcoming infrastructure failures.
    Returns:
    - ward_forecasts: dictionary of predictions by ward
    - top_emerging_threats: ranked list of high-risk preventative alerts
    - city_health_index: composite 0-100 urban infrastructure stability score
    """
    if not reports:
        return {}, [], 80.0

    # Group reports by ward and category
    ward_cat_counts = defaultdict(lambda: defaultdict(int))
    ward_cat_urgency = defaultdict(lambda: defaultdict(list))
    unresolved_count = 0
    total_urgency_sum = 0

    for rep in reports:
        w = rep.get("ward", "General")
        c = rep.get("category", "General")
        u = rep.get("urgency_score", 50)
        status = rep.get("status", "Reported")
        
        ward_cat_counts[w][c] += 1
        ward_cat_urgency[w][c].append(u)
        
        if status != "Resolved":
            unresolved_count += 1
            total_urgency_sum += u

    ward_forecasts = {}
    top_emerging_threats = []

    for ward_name, ward_meta in WARDS.items():
        cat_stats = ward_cat_counts[ward_name]
        total_ward_reports = sum(cat_stats.values())
        
        # Calculate Ward Deterioration Index (0-100)
        ward_risk_factor = ward_meta.get("risk_factor", 1.0)
        unresolved_weight = 0
        cat_breakdown = {}

        for cat_name, count in cat_stats.items():
            urg_list = ward_cat_urgency[ward_name][cat_name]
            avg_u = sum(urg_list) / len(urg_list) if urg_list else 50
            
            # Predict 7-day failure likelihood (logistic approximation)
            # High frequency + high urgency = imminent cascading failure
            risk_score = min(96, int((count * 9.5 + avg_u * 0.45) * ward_risk_factor))
            
            cat_breakdown[cat_name] = {
                "count": count,
                "avg_urgency": round(avg_u, 1),
                "failure_probability_7d": risk_score,
                "trend": "Surging" if count >= 4 else ("Elevated" if count >= 2 else "Stable")
            }

            # If risk is elevated, generate predictive warning
            if risk_score >= 68:
                action_advice, financial_impact = get_proactive_advice(cat_name, ward_name, risk_score)
                top_emerging_threats.append({
                    "ward": ward_name,
                    "category": cat_name,
                    "risk_probability": risk_score,
                    "active_incidents": count,
                    "threat_level": "CRITICAL THREAT" if risk_score >= 82 else "ELEVATED RISK",
                    "forecast_window": "Next 48–72 Hours" if risk_score >= 82 else "Next 5–7 Days",
                    "preventative_action": action_advice,
                    "estimated_damage_averted_usd": financial_impact
                })

        # Ward composite vulnerability
        ward_vulnerability = min(99, int(total_ward_reports * 4.8 * ward_risk_factor))
        ward_forecasts[ward_name] = {
            "total_reports": total_ward_reports,
            "vulnerability_score": ward_vulnerability,
            "categories": cat_breakdown,
            "status": "High Fragility" if ward_vulnerability >= 70 else ("Moderate" if ward_vulnerability >= 40 else "Stable")
        }

    # Sort emerging threats by risk probability descending
    top_emerging_threats.sort(key=lambda x: x["risk_probability"], reverse=True)

    # City Resilience Index: 100 minus penalty for unresolved high-urgency backlog
    avg_unresolved_u = (total_urgency_sum / unresolved_count) if unresolved_count > 0 else 0
    backlog_penalty = (unresolved_count * 0.4) + (avg_unresolved_u * 0.3)
    city_health_index = max(20.0, round(100.0 - backlog_penalty, 1))

    return ward_forecasts, top_emerging_threats, city_health_index


def get_proactive_advice(category, ward, risk_score):
    """Generates concrete preventative engineering suggestions and estimated cost savings."""
    if category == "Water Supply & Drainage":
        return (
            "Deploy mobile acoustic leak inspection van and throttle pressure regulators by 15% during off-peak hours.",
            "$42,000 in road erosion & flood damage averted"
        )
    elif category == "Electrical & Lighting":
        return (
            "Dispatch aerial bucket truck for thermographic infrared scan of transformer bushings and loose feeder lines.",
            "$28,000 in transformer blowout & outage compensation saved"
        )
    elif category == "Roads & Pavements":
        return (
            "Deploy rapid bitumen cold-mix patching truck before forecast rainfall to prevent sub-base asphalt washouts.",
            "$35,000 in emergency resurfacing costs avoided"
        )
    elif category == "Sanitation & Waste":
        return (
            "Re-route secondary waste compaction vehicle and install temporary bio-waste skip bins to avert disease vector bloom.",
            "$18,000 in epidemic fumigation & drainage desilting costs saved"
        )
    elif category == "Public Safety & Hazards":
        return (
            "Deploy emergency tree-pruning unit and erect heavy-duty barricades around deteriorating civil structures.",
            "$65,000 in citizen liability & property damage prevented"
        )
    else:
        return (
            "Conduct preventative maintenance inspection with zonal engineer squad.",
            "$12,000 in downstream maintenance saved"
        )
