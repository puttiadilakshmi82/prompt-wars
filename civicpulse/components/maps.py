"""
Geospatial PyDeck 3D Map Visualizations for CivicPulse AI
Renders interactive incident scatter plots, 3D cluster elevation grids, and demand hotspots.
"""

import pydeck as pdk
import pandas as pd
from civicpulse.config import CITY_CENTER


def get_severity_rgba(urgency):
    """Maps urgency score (0-100) to PyDeck RGBA color."""
    if urgency >= 80:
        return [231, 76, 60, 220]    # Red
    elif urgency >= 60:
        return [230, 126, 34, 200]   # Orange
    elif urgency >= 40:
        return [241, 196, 15, 190]   # Yellow
    else:
        return [46, 204, 113, 180]   # Green


def render_civic_map(reports, hotspots=None, map_style="mapbox://styles/mapbox/light-v10", show_3d_hex=False):
    """
    Builds and returns a PyDeck Deck object for Streamlit.
    """
    if not reports:
        return None

    # Prepare DataFrame
    data_list = []
    for r in reports:
        urg = r.get("urgency_score", 50)
        rgba = get_severity_rgba(urg)
        upv = r.get("upvotes", 1)
        radius = max(35, min(140, 35 + (upv * 2.5)))

        data_list.append({
            "id": r.get("id"),
            "title": r.get("title"),
            "category": r.get("category"),
            "ward": r.get("ward"),
            "status": r.get("status"),
            "urgency": urg,
            "upvotes": upv,
            "lat": r.get("latitude"),
            "lon": r.get("longitude"),
            "color": rgba,
            "radius": radius
        })

    df = pd.DataFrame(data_list)
    avg_lat = df["lat"].mean() if not df.empty else CITY_CENTER["lat"]
    avg_lon = df["lon"].mean() if not df.empty else CITY_CENTER["lon"]

    layers = []

    # 1. Individual Reports Layer (Color coded by Urgency)
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius="radius",
        pickable=True,
        opacity=0.85,
        stroked=True,
        filled=True,
        radius_min_pixels=6,
        radius_max_pixels=25,
        line_width_min_pixels=1,
        get_line_color=[255, 255, 255, 200],
    )
    layers.append(scatter_layer)

    # 2. Optional 3D Hexagon Density Grid Layer
    if show_3d_hex and not df.empty:
        hex_layer = pdk.Layer(
            "HexagonLayer",
            data=df,
            get_position=["lon", "lat"],
            radius=220,
            elevation_scale=15,
            elevation_range=[0, 800],
            extruded=True,
            coverage=0.88,
            pickable=True,
            auto_highlight=True,
        )
        layers.append(hex_layer)

    # 3. Macro-Incident Hotspot Circles Layer
    if hotspots:
        hs_data = []
        for h in hotspots:
            hs_data.append({
                "cluster_id": h["cluster_id"],
                "category": h["top_category"],
                "ward": h["ward"],
                "urgency": h["composite_urgency_index"],
                "count": h["report_count"],
                "lat": h["center_lat"],
                "lon": h["center_lon"],
                "radius": max(150, h["radius_meters"]),
                "color": [231, 76, 60, 75] if "CRITICAL" in h["risk_tier"] else [230, 126, 34, 65]
            })
        if hs_data:
            hs_df = pd.DataFrame(hs_data)
            hotspot_layer = pdk.Layer(
                "ScatterplotLayer",
                data=hs_df,
                get_position=["lon", "lat"],
                get_color="color",
                get_radius="radius",
                pickable=True,
                stroked=True,
                filled=True,
                get_line_color=[231, 76, 60, 220],
                line_width_min_pixels=2,
            )
            layers.insert(0, hotspot_layer)

    # View State
    view_state = pdk.ViewState(
        latitude=avg_lat,
        longitude=avg_lon,
        zoom=12.2,
        pitch=40 if show_3d_hex else 15,
        bearing=0,
    )

    tooltip = {
        "html": """
        <div style="font-family: sans-serif; font-size: 12px; padding: 6px;">
            <b style="color: #2b6cb0;">{id}</b>: <b>{title}</b><br/>
            <span><b>Category:</b> {category}</span><br/>
            <span><b>Ward:</b> {ward}</span><br/>
            <span><b>Urgency:</b> <span style="font-weight: bold; color: #c53030;">{urgency}/100</span></span><br/>
            <span><b>Status:</b> {status} | <b>Confirmations:</b> {upvotes}</span>
        </div>
        """,
        "style": {
            "backgroundColor": "#ffffff",
            "color": "#1a202c",
            "boxShadow": "0 4px 12px rgba(0,0,0,0.15)",
            "borderRadius": "6px",
            "border": "1px solid #cbd5e0"
        }
    }

    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="light"
    )
