"""
Smart Deduplication Engine for CivicPulse AI
Combines Geospatial Proximity (Haversine) with Semantic TF-IDF Vector Similarity.
"""

import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from civicpulse.config import DEDUP_TEXT_SIMILARITY_THRESHOLD, DEDUP_DISTANCE_METERS_THRESHOLD


def haversine_distance_meters(lat1, lon1, lat2, lon2):
    """Calculates great-circle distance between two GPS coordinates in meters."""
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return R * c


def find_duplicate_candidates(new_title, new_desc, new_lat, new_lon, existing_reports, top_k=3):
    """
    Evaluates whether an incoming complaint matches an already filed community issue.
    Returns matched candidates sorted by combined similarity score.
    """
    if not existing_reports:
        return []

    # 1. Filter spatially viable candidates within 1200 meters to reduce overhead
    spatial_candidates = []
    for rep in existing_reports:
        dist_m = haversine_distance_meters(new_lat, new_lon, rep["latitude"], rep["longitude"])
        if dist_m <= 1200:  # within 1.2km
            spatial_candidates.append((rep, dist_m))

    if not spatial_candidates:
        return []

    # 2. Textual Similarity via TF-IDF Vectorizer
    corpus = [f"{new_title} {new_desc}"] + [
        f"{rep['title']} {rep['description']} {rep.get('category', '')}" for rep, _ in spatial_candidates
    ]

    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(corpus)
        sim_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
    except Exception:
        sim_scores = [0.0] * len(spatial_candidates)

    matches = []
    for i, (rep, dist_m) in enumerate(spatial_candidates):
        text_sim = float(sim_scores[i])
        
        # Spatial factor (1.0 at 0m, decaying to 0.0 at 1000m)
        spatial_sim = max(0.0, 1.0 - (dist_m / 1000.0))

        # Composite match confidence
        # Heuristic: 65% text semantics, 35% spatial proximity
        combined_score = (text_sim * 0.65) + (spatial_sim * 0.35)

        # Classify match severity
        is_duplicate = False
        match_tier = "Low"

        if dist_m <= DEDUP_DISTANCE_METERS_THRESHOLD and text_sim >= DEDUP_TEXT_SIMILARITY_THRESHOLD:
            is_duplicate = True
            match_tier = "High"
        elif dist_m <= 400 and text_sim >= 0.45:
            is_duplicate = True
            match_tier = "Moderate"
        elif text_sim >= 0.75 and dist_m <= 600:
            is_duplicate = True
            match_tier = "Moderate"

        matches.append({
            "existing_report": rep,
            "distance_meters": round(dist_m, 1),
            "text_similarity": round(text_sim * 100, 1),
            "match_confidence": round(combined_score * 100, 1),
            "is_duplicate": is_duplicate,
            "match_tier": match_tier
        })

    # Sort by combined match confidence descending
    matches.sort(key=lambda x: x["match_confidence"], reverse=True)
    return matches[:top_k]
