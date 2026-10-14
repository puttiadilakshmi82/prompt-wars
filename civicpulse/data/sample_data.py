"""
Sample Data Generator & Repository for CivicPulse AI
Generates realistic historical and live municipal grievance reports with rich metadata.
"""

import os
import json
import random
from datetime import datetime, timedelta
from civicpulse.config import WARDS, CATEGORIES, STATUS_FLOW

DATA_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(DATA_DIR, "civic_data.json")

SEED_SCENARIOS = [
    # Cluster 1: Water pipeline burst near East Riverfront
    {
        "category": "Water Supply & Drainage",
        "ward": "Ward 3 - East Riverfront District",
        "title": "Severe sewage backflow flooding 3rd Main Road",
        "desc": "Heavy black wastewater overflowing from storm drain onto pedestrian walkway. Horrible odor and creating disease hazard for nearby apartments.",
        "cluster_bias": (0.0012, -0.0008),
        "severity_hint": "Critical",
        "upvotes": 34
    },
    {
        "category": "Water Supply & Drainage",
        "ward": "Ward 3 - East Riverfront District",
        "title": "Main supply line rupture with high pressure geyser",
        "desc": "Potable water line fractured under road surface, water gushing out 4 feet high. Road foundation sinking and clean water wasting rapidly.",
        "cluster_bias": (0.0015, -0.0010),
        "severity_hint": "Critical",
        "upvotes": 42
    },
    {
        "category": "Water Supply & Drainage",
        "ward": "Ward 3 - East Riverfront District",
        "title": "Flooded street intersection with murky water",
        "desc": "Intersection of 2nd Cross and Riverfront Boulevard submerged under 1 foot of water. Vehicles stalling and children unable to cross to school.",
        "cluster_bias": (0.0009, -0.0005),
        "severity_hint": "High",
        "upvotes": 19
    },
    {
        "category": "Water Supply & Drainage",
        "ward": "Ward 3 - East Riverfront District",
        "title": "Manhole cover dislodged under floodwater",
        "desc": "Open drain manhole completely hidden under muddy water on Riverfront Road. Severe life risk for two-wheelers and pedestrians.",
        "cluster_bias": (0.0014, -0.0007),
        "severity_hint": "Critical",
        "upvotes": 58
    },
    {
        "category": "Water Supply & Drainage",
        "ward": "Ward 3 - East Riverfront District",
        "title": "Contaminated brown tap water in residential block",
        "desc": "Drinking water coming from municipal taps is dark yellow-brown and smelling foul. Multiple residents experiencing gastrointestinal illness.",
        "cluster_bias": (0.0018, -0.0012),
        "severity_hint": "High",
        "upvotes": 27
    },

    # Cluster 2: Electrical hazards in Downtown Commercial
    {
        "category": "Electrical & Lighting",
        "ward": "Ward 1 - Downtown Commercial",
        "title": "Fallen high tension power cable dangling on sidewalk",
        "desc": "Live overhead wire snapped during storm and is hanging 4 feet above sidewalk in front of Metro Station exit. Sparks visible intermittently.",
        "cluster_bias": (-0.0008, 0.0012),
        "severity_hint": "Critical",
        "upvotes": 73
    },
    {
        "category": "Electrical & Lighting",
        "ward": "Ward 1 - Downtown Commercial",
        "title": "Transformer box sparking violently near commercial complex",
        "desc": "Distribution transformer buzzing loud with smoke and electrical arcs. Buzzing sound can be heard 100 meters away.",
        "cluster_bias": (-0.0006, 0.0015),
        "severity_hint": "Critical",
        "upvotes": 49
    },
    {
        "category": "Electrical & Lighting",
        "ward": "Ward 1 - Downtown Commercial",
        "title": "Complete blackout of 8 streetlights on Central Avenue",
        "desc": "Entire 500-meter commercial stretch pitch dark after sunset. Increasing mugging concerns and pedestrian stumble accidents.",
        "cluster_bias": (-0.0010, 0.0010),
        "severity_hint": "High",
        "upvotes": 22
    },
    {
        "category": "Electrical & Lighting",
        "ward": "Ward 1 - Downtown Commercial",
        "title": "Exposed underground feeder cable junction box",
        "desc": "Metal cover of pavement electrical box stolen, exposed 440V copper busbars open to rain and pedestrians.",
        "cluster_bias": (-0.0007, 0.0014),
        "severity_hint": "Critical",
        "upvotes": 36
    },

    # Cluster 3: Massive Road Potholes in North Tech Corridor
    {
        "category": "Roads & Pavements",
        "ward": "Ward 2 - Tech Corridor North",
        "title": "Deep crater pothole causing vehicle axle damage",
        "desc": "Pothole over 2 feet wide and 8 inches deep on flyover descent. Three cars suffered burst tires and an auto rickshaw overturned yesterday.",
        "cluster_bias": (0.0020, 0.0018),
        "severity_hint": "Critical",
        "upvotes": 61
    },
    {
        "category": "Roads & Pavements",
        "ward": "Ward 2 - Tech Corridor North",
        "title": "Crumbling road shoulder and broken asphalt ridge",
        "desc": "Outer lane of Tech Park Ring Road has completely disintegrated into loose gravel and jagged asphalt edges. Danger for bike commuters.",
        "cluster_bias": (0.0023, 0.0015),
        "severity_hint": "High",
        "upvotes": 38
    },
    {
        "category": "Roads & Pavements",
        "ward": "Ward 2 - Tech Corridor North",
        "title": "Sunken trench across highway lane left by utility excavation",
        "desc": "Contractor dug trench for fiber optic cables and filled it with loose mud. Heavy rains turned it into a 10-inch wheel trap.",
        "cluster_bias": (0.0018, 0.0022),
        "severity_hint": "High",
        "upvotes": 44
    },
    {
        "category": "Roads & Pavements",
        "ward": "Ward 2 - Tech Corridor North",
        "title": "Damaged pedestrian median barrier and missing curb",
        "desc": "Concrete median shattered by truck impact 2 weeks ago; rubble spilling into fast lane and obstructing pedestrian crossing.",
        "cluster_bias": (0.0022, 0.0020),
        "severity_hint": "Medium",
        "upvotes": 15
    },

    # Cluster 4: Sanitation & Waste Crisis in West Industrial Zone
    {
        "category": "Sanitation & Waste",
        "ward": "Ward 5 - West Industrial Zone",
        "title": "Illegal toxic chemical dumping by roadside factory",
        "desc": "Drums containing unidentified pungent chemical sludge abandoned by night near railway crossing. Chemical fumes burning eyes of workers.",
        "cluster_bias": (-0.0015, -0.0025),
        "severity_hint": "Critical",
        "upvotes": 52
    },
    {
        "category": "Sanitation & Waste",
        "ward": "Ward 5 - West Industrial Zone",
        "title": "Massive uncollected garbage mountain blocking service lane",
        "desc": "Garbage has accumulated for 18 days without municipal pickup. Stray dogs and rodents infesting area, waste spilling into roadway.",
        "cluster_bias": (-0.0018, -0.0022),
        "severity_hint": "High",
        "upvotes": 31
    },
    {
        "category": "Sanitation & Waste",
        "ward": "Ward 5 - West Industrial Zone",
        "title": "Open burning of plastic and rubber scrap generating toxic smoke",
        "desc": "Commercial dump set on fire, thick black carcinogenic smoke suffocating adjacent residential quarters. Air quality index alarming.",
        "cluster_bias": (-0.0012, -0.0028),
        "severity_hint": "Critical",
        "upvotes": 68
    },

    # Cluster 5: Public Safety & Hazards in South Greens
    {
        "category": "Public Safety & Hazards",
        "ward": "Ward 4 - South Residential Greens",
        "title": "Ancient banyan tree split, precarious branch hanging over school bus stop",
        "desc": "Huge 2-ton dead limb fractured during windstorm, resting precariously on overhead cables directly above where 50 children wait for school buses daily.",
        "cluster_bias": (0.0005, -0.0010),
        "severity_hint": "Critical",
        "upvotes": 81
    },
    {
        "category": "Public Safety & Hazards",
        "ward": "Ward 4 - South Residential Greens",
        "title": "Collapsing storm retaining wall bordering playground",
        "desc": "Stone masonry retaining wall bulging out by 15 degrees. Signs of imminent landslide into children's play area if heavy rain continues.",
        "cluster_bias": (0.0008, -0.0007),
        "severity_hint": "High",
        "upvotes": 41
    },
    {
        "category": "Parks & Environment",
        "ward": "Ward 4 - South Residential Greens",
        "title": "Vandalized playground equipment with sharp exposed metal",
        "desc": "Children's slide broken in half leaving jagged metal shears. Two toddlers suffered cuts over the weekend.",
        "cluster_bias": (0.0003, -0.0014),
        "severity_hint": "Medium",
        "upvotes": 25
    }
]

GENERAL_TEMPLATES = [
    ("Roads & Pavements", "Deep pothole outside supermarket", "Pothole causing severe traffic slowdown and bike skids during peak morning hours.", 45, 68),
    ("Roads & Pavements", "Missing storm drain grate on roadside", "Metal grate stolen, creating an open 3-foot drop directly in cycling lane.", 65, 88),
    ("Roads & Pavements", "Cracked concrete footpath with trip hazards", "Pavement slabs broken and uneven. Senior citizens struggling to walk safely.", 30, 52),
    ("Water Supply & Drainage", "Underground pipe leaking clean drinking water", "Continuous stream of fresh water flowing down slope for 4 days. Waste of thousands of liters.", 50, 72),
    ("Water Supply & Drainage", "Blocked storm drain causing rainwater backup", "Drain clogged with construction debris, water rising to shop doorsteps during light showers.", 55, 78),
    ("Water Supply & Drainage", "Low water pressure in residential sector", "Water reaching only ground floor taps, upper floors receiving zero water for 72 hours.", 40, 60),
    ("Sanitation & Waste", "Overflowing public dumpster spilling into street", "Waste bin overflowing, cows and dogs spreading trash onto road, horrible stench.", 42, 65),
    ("Sanitation & Waste", "Dead animal carcass on road median", "Decomposing carcass emitting unbearable smell, creating hygiene and health hazard.", 60, 80),
    ("Sanitation & Waste", "Construction debris dumped on public footpath", "Tons of brick rubble and sand obstructing entire pedestrian path.", 35, 55),
    ("Electrical & Lighting", "Flickering streetlight creating blind spot", "Streetlight strobe-flickering for weeks, road becomes pitch black every 5 seconds.", 38, 58),
    ("Electrical & Lighting", "Transformer oil leak onto pedestrian path", "Cooling oil dripping continuously from pole-mounted transformer.", 62, 82),
    ("Electrical & Lighting", "Hanging telecom and power cables entangled", "Bundle of loose cables sagging within head-height of pedestrians.", 50, 74),
    ("Public Safety & Hazards", "Uncovered construction pit near bus stop", "Deep excavation pit left without safety barricades or warning lights.", 75, 92),
    ("Public Safety & Hazards", "Fallen traffic signal pole blocking left lane", "Signal pole damaged in collision lying across roadway, obstructing emergency vehicles.", 70, 88),
    ("Parks & Environment", "Dead dry pine tree leaning towards high-voltage line", "Dying tree tilted at 30 degrees towards overhead line, spark risk in windy conditions.", 60, 80),
    ("Parks & Environment", "Broken park boundary fence allowing stray cattle entry", "Chainlink fence cut open, cattle entering and destroying community garden beds.", 25, 45),
    ("Parks & Environment", "Dry community park sprinkler system and dying turf", "Park irrigation non-functional for 2 months, valuable lawn and saplings drying up.", 20, 40)
]


def generate_initial_dataset(target_count=75):
    """Generates a rich, realistic municipal dataset with spatial clustering and timestamps."""
    reports = []
    now = datetime.now()
    report_id = 1001

    # First add the rich seed scenario clusters
    for item in SEED_SCENARIOS:
        ward_info = WARDS[item["ward"]]
        bias_lat, bias_lon = item.get("cluster_bias", (0.0, 0.0))
        lat = ward_info["lat"] + bias_lat + random.uniform(-0.0003, 0.0003)
        lon = ward_info["lon"] + bias_lon + random.uniform(-0.0003, 0.0003)
        
        days_ago = random.randint(0, 18)
        created_at = (now - timedelta(days=days_ago, hours=random.randint(1, 23), minutes=random.randint(0, 59))).isoformat()
        
        cat_meta = CATEGORIES[item["category"]]
        base_urgency = cat_meta["base_urgency"]
        urgency = min(98, max(25, int(base_urgency + (item["upvotes"] * 0.4) + random.randint(-5, 12))))
        
        # Determine status realistically based on age and urgency
        if days_ago > 12 and random.random() > 0.4:
            status = "Resolved"
        elif days_ago > 6:
            status = random.choice(["Dispatched", "In Progress", "Triaged"])
        else:
            status = random.choice(["Reported", "Triaged", "Dispatched"])
            
        reports.append({
            "id": f"CIVIC-{report_id}",
            "title": item["title"],
            "description": item["desc"],
            "category": item["category"],
            "ward": item["ward"],
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "urgency_score": urgency,
            "status": status,
            "upvotes": item["upvotes"],
            "reported_at": created_at,
            "assigned_dept": cat_meta["dept"],
            "sla_hours": cat_meta["default_sla_hours"],
            "citizen_reporter": f"Resident_{random.randint(100, 999)}",
            "ai_confidence": round(random.uniform(0.88, 0.99), 2),
            "ai_summary": f"Detected: {item['category']} anomaly. High public hazard factor identified.",
            "estimated_repair_cost_usd": random.choice([250, 450, 800, 1500, 3200, 6000])
        })
        report_id += 1

    # Now populate remaining realistic complaints across all wards
    while len(reports) < target_count:
        cat_name, title_t, desc_t, min_u, max_u = random.choice(GENERAL_TEMPLATES)
        ward_name, ward_info = random.choice(list(WARDS.items()))
        cat_meta = CATEGORIES[cat_name]
        
        # Spatial scatter within ~1.2km radius of ward center
        lat = ward_info["lat"] + random.uniform(-0.012, 0.012)
        lon = ward_info["lon"] + random.uniform(-0.012, 0.012)
        
        days_ago = random.randint(0, 28)
        created_at = (now - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))).isoformat()
        
        upvotes = random.randint(1, 35)
        urgency = random.randint(min_u, max_u)
        
        if days_ago > 14 and random.random() > 0.35:
            status = "Resolved"
        elif days_ago > 7:
            status = random.choice(["Dispatched", "In Progress", "Triaged"])
        else:
            status = random.choice(["Reported", "Triaged", "Reported"])
            
        reports.append({
            "id": f"CIVIC-{report_id}",
            "title": f"{title_t} near {ward_name.split(' - ')[1]}",
            "description": desc_t,
            "category": cat_name,
            "ward": ward_name,
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "urgency_score": urgency,
            "status": status,
            "upvotes": upvotes,
            "reported_at": created_at,
            "assigned_dept": cat_meta["dept"],
            "sla_hours": cat_meta["default_sla_hours"],
            "citizen_reporter": f"Resident_{random.randint(100, 999)}",
            "ai_confidence": round(random.uniform(0.85, 0.98), 2),
            "ai_summary": f"Classified under {cat_name} with priority rating based on urban density and citizen confirmations.",
            "estimated_repair_cost_usd": random.choice([150, 300, 650, 1200, 2500])
        })
        report_id += 1
        
    return reports


def load_civic_data(force_refresh=False):
    """Loads existing civic complaints from JSON file, or creates new seed data if not present."""
    if not os.path.exists(DATA_FILE) or force_refresh:
        data = generate_initial_dataset(85)
        save_civic_data(data)
        return data
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        data = generate_initial_dataset(85)
        save_civic_data(data)
        return data


def save_civic_data(data):
    """Persists complaints list to JSON disk."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_new_report(report_dict):
    """Adds a new citizen report to the database."""
    data = load_civic_data()
    data.insert(0, report_dict)
    save_civic_data(data)
    return data


def update_report_status(report_id, new_status):
    """Updates the workflow status of an existing ticket."""
    data = load_civic_data()
    updated = False
    for item in data:
        if item["id"] == report_id:
            item["status"] = new_status
            item["last_updated"] = datetime.now().isoformat()
            updated = True
            break
    if updated:
        save_civic_data(data)
    return updated


def upvote_report(report_id):
    """Increments confirmation/upvote counter for an existing issue."""
    data = load_civic_data()
    updated = False
    for item in data:
        if item["id"] == report_id:
            item["upvotes"] = item.get("upvotes", 0) + 1
            # Slightly boost urgency score when confirmed by multiple citizens
            item["urgency_score"] = min(100, item.get("urgency_score", 50) + 2)
            updated = True
            break
    if updated:
        save_civic_data(data)
    return updated
