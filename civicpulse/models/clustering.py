"""
Unsupervised Spatial & Issue Clustering Engine for CivicPulse AI
Uses DBSCAN on geospatial coordinates to consolidate isolated grievances into
actionable, high-impact Municipal Hotspots and macro-incidents.
"""

import numpy as np
from collections import Counter
from sklearn.cluster import DBSCAN
from civicpulse.models.deduplication import haversine_distance_meters


def cluster_civic_reports(reports, eps_meters=450, min_samples=2):
    """
    Performs geospatial density-based clustering (DBSCAN) on active complaints.
    eps_meters: maximum distance between two reports for them to be considered neighbors.
    min_samples: minimum reports required to form a macro-incident hotspot.
    """
    if not reports:
        return [], reports

    # Convert coordinates to radians for spherical DBSCAN
    coords = np.array([[rep["latitude"], rep["longitude"]] for rep in reports])
    coords_rad = np.radians(coords)

    # Earth radius in meters
    kms_per_radian = 6371000.0
    epsilon = eps_meters / kms_per_radian

    db = DBSCAN(eps=epsilon, min_samples=min_samples, metric='haversine')
    labels = db.fit_predict(coords_rad)

    # Attach cluster labels back to report objects
    clustered_reports = []
    clusters_map = {}

    for idx, rep in enumerate(reports):
        c_id = int(labels[idx])
        rep_copy = dict(rep)
        rep_copy["cluster_id"] = f"HOTSPOT-{c_id + 1:02d}" if c_id >= 0 else "ISOLATED"
        clustered_reports.append(rep_copy)

        if c_id >= 0:
            if c_id not in clusters_map:
                clusters_map[c_id] = []
            clusters_map[c_id].append(rep_copy)

    # Synthesize cluster / hotspot metadata summaries
    hotspots = []
    for c_id, members in sorted(clusters_map.items()):
        lats = [m["latitude"] for m in members]
        lons = [m["longitude"] for m in members]
        urgencies = [m.get("urgency_score", 50) for m in members]
        categories = [m.get("category", "General") for m in members]
        wards = [m.get("ward", "General") for m in members]

        center_lat = float(np.mean(lats))
        center_lon = float(np.mean(lons))
        avg_urgency = float(np.mean(urgencies))
        
        # Calculate cluster radius (max distance from centroid)
        max_dist = max(
            [haversine_distance_meters(center_lat, center_lon, m["latitude"], m["longitude"]) for m in members]
        )
        radius_m = max(50.0, round(max_dist, 1))

        # Most prevalent category and ward
        top_category = Counter(categories).most_common(1)[0][0]
        top_ward = Counter(wards).most_common(1)[0][0]

        # Hotspot Composite Urgency Index (combines average urgency + volume scale)
        volume_factor = min(20.0, len(members) * 3.5)
        hotspot_urgency_index = min(100.0, avg_urgency + volume_factor)

        if hotspot_urgency_index >= 80:
            risk_tier = "CRITICAL EMERGENCY"
            color = "#e74c3c"
        elif hotspot_urgency_index >= 60:
            risk_tier = "ELEVATED ALERT"
            color = "#e67e22"
        else:
            risk_tier = "MONITORED ZONE"
            color = "#f39c12"

        hotspots.append({
            "cluster_id": f"HOTSPOT-{c_id + 1:02d}",
            "center_lat": round(center_lat, 6),
            "center_lon": round(center_lon, 6),
            "report_count": len(members),
            "top_category": top_category,
            "ward": top_ward,
            "avg_urgency": round(avg_urgency, 1),
            "composite_urgency_index": round(hotspot_urgency_index, 1),
            "risk_tier": risk_tier,
            "radius_meters": radius_m,
            "color": color,
            "total_upvotes": sum(m.get("upvotes", 0) for m in members),
            "members": members,
            "action_plan": generate_cluster_action_plan(top_category, len(members), risk_tier)
        })

    # Sort hotspots by composite urgency index descending
    hotspots.sort(key=lambda x: x["composite_urgency_index"], reverse=True)

    return hotspots, clustered_reports


def generate_cluster_action_plan(category, count, risk_tier):
    """Generates municipal dispatch optimization directive for grouped issues."""
    if risk_tier == "CRITICAL EMERGENCY":
        return (f"DEPLOY CONSOLIDATED WORK ORDER: {count} clustered reports indicate an infrastructural breakdown in {category}. "
                f"Dispatch senior rapid response crew with heavy machinery immediately.")
    elif risk_tier == "ELEVATED ALERT":
        return (f"BATCH ASSIGNMENT: Combine {count} nearby {category} work tickets to prevent duplicate transit costs. "
                f"Assign to zonal maintenance truck.")
    else:
        return f"ROUTINE CONSOLIDATION: Group {count} minor {category} tickets for end-of-week inspection sweep."
