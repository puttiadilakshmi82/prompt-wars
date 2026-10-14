"""
Automated Municipal Dispatch & SLA Routing Engine for CivicPulse AI
Calculates departmental routing, work crew sizing, and SLA compliance tracking.
"""

from datetime import datetime, timedelta
from civicpulse.config import CATEGORIES


def route_incident_to_department(category, severity, urgency_score):
    """Assigns appropriate department, crew requirements, and estimated turnaround."""
    cat_meta = CATEGORIES.get(category, {
        "dept": "General Municipal Services",
        "default_sla_hours": 24
    })
    
    dept = cat_meta["dept"]
    base_sla = cat_meta["default_sla_hours"]

    # SLA adjustments based on severity
    if severity == "Critical":
        sla_hours = max(4, int(base_sla * 0.25))
        crew_size = "Squad (4-6 technicians + heavy machinery)"
        priority_code = "P1 - EMERGENCY"
    elif severity == "High":
        sla_hours = max(8, int(base_sla * 0.50))
        crew_size = "Team (3 technicians + utility truck)"
        priority_code = "P2 - URGENT"
    elif severity == "Medium":
        sla_hours = base_sla
        crew_size = "Pair (2 technicians + tool kit)"
        priority_code = "P3 - STANDARD"
    else:
        sla_hours = int(base_sla * 1.5)
        crew_size = "Inspector (1 technician)"
        priority_code = "P4 - ROUTINE"

    return {
        "assigned_department": dept,
        "priority_code": priority_code,
        "sla_target_hours": sla_hours,
        "recommended_crew": crew_size,
    }


def compute_sla_status(reported_at_iso, sla_hours, current_status):
    """Calculates whether a ticket is within SLA, approaching deadline, or breached."""
    if current_status == "Resolved":
        return {
            "status_label": "Resolved",
            "badge": "✅ Resolved",
            "color": "#2ecc71",
            "hours_remaining": 0,
            "is_breached": False
        }

    try:
        report_dt = datetime.fromisoformat(reported_at_iso)
    except Exception:
        report_dt = datetime.now() - timedelta(hours=2)

    deadline = report_dt + timedelta(hours=sla_hours)
    now = datetime.now()
    diff = deadline - now
    hours_left = round(diff.total_seconds() / 3600.0, 1)

    if hours_left < 0:
        return {
            "status_label": "SLA Breached",
            "badge": f"🚨 Breached by {abs(hours_left):.1f}h",
            "color": "#e74c3c",
            "hours_remaining": hours_left,
            "is_breached": True
        }
    elif hours_left <= (sla_hours * 0.25):
        return {
            "status_label": "Approaching Breach",
            "badge": f"⚠️ {hours_left:.1f}h left",
            "color": "#f39c12",
            "hours_remaining": hours_left,
            "is_breached": False
        }
    else:
        return {
            "status_label": "On Track",
            "badge": f"🟢 {hours_left:.1f}h left",
            "color": "#2ecc71",
            "hours_remaining": hours_left,
            "is_breached": False
        }
