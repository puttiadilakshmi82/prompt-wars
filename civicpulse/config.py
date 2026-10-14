"""
CivicPulse AI Configuration
Constants, category definitions, department mappings, SLA standards, and geospatial anchors.
"""

from datetime import timedelta

APP_NAME = "CivicPulse AI"
APP_TAGLINE = "Predictive Community Problem Resolution & Urban Intelligence Engine"
APP_VERSION = "1.0.0"

# Target City Reference: Metro City Central Hub
CITY_CENTER = {"lat": 12.9716, "lon": 77.5946, "name": "Metro City"}

# Ward Definitions with Boundary Centers
WARDS = {
    "Ward 1 - Downtown Commercial": {"lat": 12.9735, "lon": 77.5980, "pop_density": "Very High", "risk_factor": 1.25},
    "Ward 2 - Tech Corridor North": {"lat": 12.9980, "lon": 77.6150, "pop_density": "High", "risk_factor": 1.10},
    "Ward 3 - East Riverfront District": {"lat": 12.9650, "lon": 77.6350, "pop_density": "Moderate", "risk_factor": 1.35},
    "Ward 4 - South Residential Greens": {"lat": 12.9320, "lon": 77.5850, "pop_density": "High", "risk_factor": 1.05},
    "Ward 5 - West Industrial Zone": {"lat": 12.9550, "lon": 77.5450, "pop_density": "Moderate", "risk_factor": 1.40},
}

CATEGORIES = {
    "Roads & Pavements": {
        "icon": "🛣️",
        "color": "#e67e22",
        "dept": "Public Works Department (PWD)",
        "default_sla_hours": 48,
        "base_urgency": 55,
        "keywords": ["pothole", "asphalt", "crater", "sinkhole", "road crack", "speedbreaker", "curb", "sidewalk", "divider"]
    },
    "Water Supply & Drainage": {
        "icon": "🚰",
        "color": "#2980b9",
        "dept": "Water Supply & Sewerage Board (WSSB)",
        "default_sla_hours": 24,
        "base_urgency": 70,
        "keywords": ["leak", "burst pipe", "sewage", "drain overflow", "dirty water", "flooding", "low pressure", "manhole", "water logging"]
    },
    "Sanitation & Waste": {
        "icon": "🗑️",
        "color": "#27ae60",
        "dept": "Solid Waste Management Authority",
        "default_sla_hours": 24,
        "base_urgency": 50,
        "keywords": ["garbage pile", "dump", "stench", "overflowing bin", "debris", "dead animal", "uncollected trash", "litter"]
    },
    "Electrical & Lighting": {
        "icon": "⚡",
        "color": "#f39c12",
        "dept": "Municipal Electric & Grid Utility",
        "default_sla_hours": 12,
        "base_urgency": 75,
        "keywords": ["streetlight", "dark street", "exposed wire", "transformer spark", "power outage", "pole tilted", "short circuit", "hanging cable"]
    },
    "Public Safety & Hazards": {
        "icon": "🚨",
        "color": "#e74c3c",
        "dept": "Emergency Civic Response Unit",
        "default_sla_hours": 6,
        "base_urgency": 85,
        "keywords": ["open manhole", "fallen tree", "structural collapse", "gas leak", "construction hazard", "live wire", "unfenced pit"]
    },
    "Parks & Environment": {
        "icon": "🌳",
        "color": "#16a085",
        "dept": "Urban Forestry & Horticulture Dept",
        "default_sla_hours": 72,
        "base_urgency": 40,
        "keywords": ["broken bench", "overgrown weeds", "playground swing", "illegal tree cutting", "dead vegetation", "dry fountain"]
    }
}

STATUS_FLOW = ["Reported", "Triaged", "Dispatched", "In Progress", "Resolved"]

STATUS_COLORS = {
    "Reported": "#3498db",
    "Triaged": "#9b59b6",
    "Dispatched": "#e67e22",
    "In Progress": "#f1c40f",
    "Resolved": "#2ecc71"
}

# Deduplication Thresholds
DEDUP_TEXT_SIMILARITY_THRESHOLD = 0.58  # Cosine similarity on TF-IDF
DEDUP_DISTANCE_METERS_THRESHOLD = 180   # Haversine distance in meters

# Urgency Score Ranges
SEVERITY_LEVELS = {
    "Critical": {"min": 80, "max": 100, "badge": "🔴 Critical", "color": "#e74c3c"},
    "High": {"min": 60, "max": 79, "badge": "🟠 High", "color": "#e67e22"},
    "Medium": {"min": 40, "max": 59, "badge": "🟡 Medium", "color": "#f1c40f"},
    "Low": {"min": 0, "max": 39, "badge": "🟢 Low", "color": "#2ecc71"}
}
