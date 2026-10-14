"""
CivicPulse AI — Main Streamlit Application
Predictive Community Problem Resolution & Urban Intelligence Engine
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Streamlit Page Configuration - Must be first Streamlit call
st.set_page_config(
    page_title="CivicPulse AI | Predictive Community Problem Resolution",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from civicpulse.config import (
    APP_NAME, APP_TAGLINE, WARDS, CATEGORIES, STATUS_FLOW,
    STATUS_COLORS, SEVERITY_LEVELS, CITY_CENTER
)
from civicpulse.data.sample_data import (
    load_civic_data, save_civic_data, add_new_report,
    update_report_status, upvote_report
)
from civicpulse.models.deduplication import find_duplicate_candidates
from civicpulse.models.urgency_scoring import compute_urgency_score
from civicpulse.models.clustering import cluster_civic_reports
from civicpulse.models.predictive_engine import run_predictive_risk_assessment
from civicpulse.services.dispatch_router import compute_sla_status, route_incident_to_department
from civicpulse.services.ai_assistant import query_pulse_assistant
from civicpulse.components.ui_styles import get_custom_css
from civicpulse.components.maps import render_civic_map
from civicpulse.components.charts import (
    render_category_chart, render_urgency_histogram, render_ward_comparison_chart
)

# Apply CSS styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize Session State
if "civic_data" not in st.session_state:
    st.session_state.civic_data = load_civic_data()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I am **PulseAssistant**, your Municipal AI Analyst. "
                "I can analyze civic problem clusters, compute SLA breach risks, "
                "or forecast infrastructure failures across any ward. How can I assist you today?"
            )
        }
    ]

# Reload data helper
reports = st.session_state.civic_data

# Run clustering and predictive models
hotspots, clustered_reports = cluster_civic_reports(reports)
ward_forecasts, emerging_threats, city_health = run_predictive_risk_assessment(reports)

# -------------------------------------------------------------
# Top Hero Header & Key Performance Indicators
# -------------------------------------------------------------
st.markdown(f"""
<div class="civic-hero">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1>🏛️ {APP_NAME}</h1>
            <p>{APP_TAGLINE}</p>
        </div>
        <div style="text-align: right; margin-top: 8px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">
                🌆 {CITY_CENTER['name']} Central Hub
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top KPI Summary Cards
total_issues = len(reports)
active_issues = len([r for r in reports if r.get("status") != "Resolved"])
critical_issues = len([r for r in reports if r.get("urgency_score", 0) >= 80 and r.get("status") != "Resolved"])
total_hotspots = len(hotspots)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">City Resilience</div>
        <div class="metric-value" style="color: {'#16a34a' if city_health >= 75 else '#ea580c'};">{city_health}%</div>
        <div class="metric-sub" style="color: #64748b;">Infrastructure stability</div>
    </div>
    """, unsafe_allow_html=True)
with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Active Grievances</div>
        <div class="metric-value">{active_issues} <span style="font-size: 1rem; color: #64748b;">/ {total_issues}</span></div>
        <div class="metric-sub" style="color: #64748b;">{total_issues - active_issues} resolved</div>
    </div>
    """, unsafe_allow_html=True)
with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Critical Emergencies</div>
        <div class="metric-value" style="color: #dc2626;">{critical_issues}</div>
        <div class="metric-sub" style="color: #dc2626;">P1 Rapid squads deployed</div>
    </div>
    """, unsafe_allow_html=True)
with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Macro Hotspots</div>
        <div class="metric-value" style="color: #7c3aed;">{total_hotspots}</div>
        <div class="metric-sub" style="color: #64748b;">DBSCAN spatial clusters</div>
    </div>
    """, unsafe_allow_html=True)
with kpi5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Preventative Savings</div>
        <div class="metric-value" style="color: #0284c7;">$115K+</div>
        <div class="metric-sub" style="color: #64748b;">Averted damage potential</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------------
# Sidebar: Controls, Quick Ingestion & Filters
# -------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/smart-city.png", width=70)
    st.title("CivicPulse Controls")
    
    st.subheader("⚡ Live Incident Simulator")
    st.caption("Demonstrate real-time ingestion, AI auto-scoring, and immediate re-clustering.")
    
    if st.button("🚨 Simulate New Incident Event", use_container_width=True):
        sim_scenarios = [
            ("Water Supply & Drainage", "Severe water main burst near School Crossing", "Underground main line ruptured, flooding street and causing road cave-in risk.", "Ward 3 - East Riverfront District"),
            ("Electrical & Lighting", "Sparking feeder line touching pedestrian footbridge", "High voltage cable rubbing against metal railing, sparks flying on commuters.", "Ward 1 - Downtown Commercial"),
            ("Roads & Pavements", "Deep jagged pothole causing motorcycle skid", "10-inch pothole at highway off-ramp causing severe hazard.", "Ward 2 - Tech Corridor North"),
            ("Sanitation & Waste", "Hospital medical waste dumped in public alleyway", "Unlabeled red hazard bags leaking fluids near residential perimeter.", "Ward 5 - West Industrial Zone")
        ]
        chosen = random.choice(sim_scenarios)
        cat, title_s, desc_s, ward_s = chosen
        w_info = WARDS[ward_s]
        
        sim_lat = w_info["lat"] + random.uniform(-0.003, 0.003)
        sim_lon = w_info["lon"] + random.uniform(-0.003, 0.003)
        
        score_info = compute_urgency_score(title_s, desc_s, cat, ward_s, upvotes=1)
        routing = route_incident_to_department(cat, score_info["severity"], score_info["urgency_score"])
        
        new_inc = {
            "id": f"CIVIC-{len(reports) + 1001}",
            "title": title_s,
            "description": desc_s,
            "category": cat,
            "ward": ward_s,
            "latitude": round(sim_lat, 6),
            "longitude": round(sim_lon, 6),
            "urgency_score": score_info["urgency_score"],
            "status": "Reported",
            "upvotes": 1,
            "reported_at": datetime.now().isoformat(),
            "assigned_dept": routing["assigned_department"],
            "sla_hours": score_info["sla_hours"],
            "citizen_reporter": f"SimulatedCitizen_{random.randint(100, 999)}",
            "ai_confidence": 0.97,
            "ai_summary": f"Simulated live event: {score_info['recommendation']}",
            "estimated_repair_cost_usd": 1200
        }
        st.session_state.civic_data = add_new_report(new_inc)
        st.success(f"Simulated new incident: **{new_inc['id']}** ({cat})")
        st.rerun()

    if st.button("🔄 Reset Seed Database", use_container_width=True):
        st.session_state.civic_data = load_civic_data(force_refresh=True)
        st.info("Civic database reset to baseline seed records.")
        st.rerun()

    st.markdown("---")
    st.subheader("Global Filters")
    selected_ward_filter = st.selectbox(
        "Filter by Ward",
        ["All Wards"] + list(WARDS.keys()),
        index=0
    )
    selected_cat_filter = st.selectbox(
        "Filter by Category",
        ["All Categories"] + list(CATEGORIES.keys()),
        index=0
    )
    status_filter = st.multiselect(
        "Filter Status",
        STATUS_FLOW,
        default=["Reported", "Triaged", "Dispatched", "In Progress"]
    )

# Filter dataset for views
filtered_reports = [r for r in reports]
if selected_ward_filter != "All Wards":
    filtered_reports = [r for r in filtered_reports if r.get("ward") == selected_ward_filter]
if selected_cat_filter != "All Categories":
    filtered_reports = [r for r in filtered_reports if r.get("category") == selected_cat_filter]
if status_filter:
    filtered_reports = [r for r in filtered_reports if r.get("status") in status_filter]

# -------------------------------------------------------------
# Main Navigation Tabs
# -------------------------------------------------------------
tab_map, tab_report, tab_predict, tab_kanban, tab_ai = st.tabs([
    "🗺️ Geospatial Command Center",
    "📝 Smart Citizen Report & Deduplication",
    "🔮 Predictive Deterioration Engine",
    "📋 Municipal Kanban & Dispatch",
    "🤖 PulseAssistant RAG Analyst"
])

# =============================================================
# TAB 1: GEOSPATIAL COMMAND CENTER & HOTSPOTS
# =============================================================
with tab_map:
    col_map_opts, col_map_kpis = st.columns([3, 1])
    with col_map_opts:
        map_view_mode = st.radio(
            "Layer Mode:",
            ["🔴 Incident Markers (Colored by Urgency)", "🏙️ 3D Hexagon Density Grid (Elevated Hotspots)"],
            horizontal=True
        )
    with col_map_kpis:
        st.caption(f"Displaying **{len(filtered_reports)}** filtered issues out of {len(reports)} total")

    deck = render_civic_map(
        filtered_reports,
        hotspots=hotspots if selected_ward_filter == "All Wards" and selected_cat_filter == "All Categories" else None,
        show_3d_hex=("3D Hexagon" in map_view_mode)
    )
    if deck:
        st.pydeck_chart(deck, use_container_width=True)

    # Hotspot / Macro-incident Cluster Drawer
    st.markdown("### 🔥 Detected Macro-Incident Hotspots (Unsupervised DBSCAN)")
    st.caption("CivicPulse AI automatically groups multiple proximate reports into high-urgency operational clusters.")

    if hotspots:
        cols = st.columns(min(3, len(hotspots)))
        for i, hs in enumerate(hotspots[:3]):
            with cols[i]:
                st.markdown(f"""
                <div class="hotspot-banner">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b style="font-size: 1.1rem; color: #9a3412;">{hs['cluster_id']}</b>
                        <span style="background: {hs['color']}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: bold;">
                            {hs['risk_tier']}
                        </span>
                    </div>
                    <div style="margin-top: 6px;">
                        <b>{hs['top_category']}</b> in <i>{hs['ward'].split(' - ')[-1]}</i><br/>
                        <b>Reports:</b> {hs['report_count']} complaints ({hs['total_upvotes']} citizen upvotes)<br/>
                        <b>Urgency Index:</b> <span style="font-weight: bold; color: {hs['color']};">{hs['composite_urgency_index']}/100</span><br/>
                        <b>Radius:</b> ~{hs['radius_meters']}m span
                    </div>
                    <div style="font-size: 0.82rem; margin-top: 8px; color: #4b5563; background: #ffffff; padding: 8px; border-radius: 6px;">
                        🎯 <b>Action:</b> {hs['action_plan']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No dense clusters currently detected under selected filters.")

    # Analytical Charts Row
    st.markdown("---")
    st.markdown("### 📊 City Health & Category Analytics")
    c_chart1, c_chart2, c_chart3 = st.columns(3)
    with c_chart1:
        st.markdown("**Incident Volume by Category**")
        cat_chart = render_category_chart(filtered_reports)
        if cat_chart:
            st.altair_chart(cat_chart, use_container_width=True)
    with c_chart2:
        st.markdown("**Urgency Score Distribution (0-100)**")
        urg_chart = render_urgency_histogram(filtered_reports)
        if urg_chart:
            st.altair_chart(urg_chart, use_container_width=True)
    with c_chart3:
        st.markdown("**Ward Vulnerability Comparison**")
        ward_chart = render_ward_comparison_chart(filtered_reports)
        if ward_chart:
            st.altair_chart(ward_chart, use_container_width=True)

# =============================================================
# TAB 2: SMART CITIZEN REPORT & DEDUPLICATION PORTAL
# =============================================================
with tab_report:
    st.markdown("### 📝 Smart Resident Grievance Portal with AI Pre-Screening")
    st.write(
        "CivicPulse AI prevents municipal system clutter by detecting duplicate reports in real time "
        "and evaluating urgency before ticket submission."
    )

    col_form, col_eval = st.columns([1.1, 1])

    with col_form:
        st.subheader("Report a Civic Problem")
        
        rep_ward = st.selectbox("Select Neighborhood / Ward", list(WARDS.keys()), key="rep_ward")
        ward_meta = WARDS[rep_ward]
        
        # Approximate lat/lon near ward center
        rep_lat = st.number_input("Latitude", value=round(ward_meta["lat"] + random.uniform(-0.001, 0.001), 6), format="%.6f")
        rep_lon = st.number_input("Longitude", value=round(ward_meta["lon"] + random.uniform(-0.001, 0.001), 6), format="%.6f")

        rep_title = st.text_input(
            "Issue Headline",
            placeholder="e.g. Major sewage overflow flooding pedestrian sidewalk"
        )
        rep_desc = st.text_area(
            "Detailed Description",
            placeholder="Describe the severity, duration, and any hazards (e.g., exposed wires, open pits, foul smell, traffic stall)...",
            height=120
        )
        
        # Pre-select category or let AI suggest
        suggested_cat = "Roads & Pavements"
        for c_name, c_meta in CATEGORIES.items():
            if any(k in (rep_title + " " + rep_desc).lower() for k in c_meta["keywords"]):
                suggested_cat = c_name
                break

        rep_cat = st.selectbox(
            "Category (AI Suggested)",
            list(CATEGORIES.keys()),
            index=list(CATEGORIES.keys()).index(suggested_cat)
        )

        rep_photo = st.file_uploader(
            "Upload Photo (Simulated Computer Vision Detection)",
            type=["jpg", "jpeg", "png"]
        )

    with col_eval:
        st.subheader("⚡ Real-Time AI Pre-Screening & Duplicate Analysis")

        if rep_title.strip() or rep_desc.strip():
            # 1. Compute AI Urgency Analysis
            score_res = compute_urgency_score(rep_title, rep_desc, rep_cat, rep_ward, upvotes=1)
            urg_val = score_res["urgency_score"]
            sev_tier = score_res["severity"]
            sev_badge = SEVERITY_LEVELS[sev_tier]["badge"]
            sev_color = SEVERITY_LEVELS[sev_tier]["color"]

            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; font-size: 0.95rem;">AI Priority Assessment</span>
                    <span style="font-weight: bold; color: {sev_color};">{sev_badge} ({urg_val}/100)</span>
                </div>
                <div style="margin-top: 6px; font-size: 0.88rem; color: #475569;">
                    <b>Target SLA:</b> {score_res['sla_hours']} Hours &nbsp;|&nbsp;
                    <b>Ward Multiplier:</b> {score_res['ward_risk_factor']}x
                </div>
                <div style="font-size: 0.85rem; color: #334155; margin-top: 6px;">
                    <b>Operational Directive:</b> {score_res['recommendation']}
                </div>
                {f"<div style='margin-top: 6px; color: #dc2626; font-size: 0.82rem;'><b>⚠️ Detected Hazard Triggers:</b> {', '.join(score_res['detected_hazards'])}</div>" if score_res['detected_hazards'] else ""}
            </div>
            """, unsafe_allow_html=True)

            # 2. Duplicate Detection Engine Check
            duplicates = find_duplicate_candidates(rep_title, rep_desc, rep_lat, rep_lon, reports, top_k=2)
            
            if duplicates and duplicates[0]["is_duplicate"]:
                top_match = duplicates[0]
                existing = top_match["existing_report"]
                
                st.markdown(f"""
                <div style="background: #fff7ed; border: 2px solid #ea580c; border-radius: 10px; padding: 14px; margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b style="color: #c2410c; font-size: 1rem;">⚠️ Similar Issue Already Reported!</b>
                        <span style="background: #fed7aa; color: #9a3412; font-weight: bold; font-size: 0.75rem; padding: 2px 8px; border-radius: 6px;">
                            {top_match['match_confidence']}% Match
                        </span>
                    </div>
                    <p style="margin: 6px 0; font-size: 0.88rem; color: #374151;">
                        <b>{existing['id']}</b>: <i>"{existing['title']}"</i><br/>
                        <b>Distance:</b> {top_match['distance_meters']}m away &nbsp;|&nbsp; 
                        <b>Existing Status:</b> {existing['status']} &nbsp;|&nbsp; 
                        <b>Confirmations:</b> {existing.get('upvotes', 1)}
                    </p>
                    <div style="font-size: 0.82rem; color: #4b5563; margin-bottom: 8px;">
                        Instead of creating a duplicate ticket, you can upvote this existing report to increase its priority!
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"👍 Upvote & Confirm Existing Ticket ({existing['id']})", use_container_width=True):
                    upvote_report(existing["id"])
                    st.success(f"Thank you! You upvoted ticket {existing['id']}. Municipal priority increased.")
                    st.session_state.civic_data = load_civic_data()
                    st.rerun()

            else:
                st.success("✅ Smart Deduplication Check: No conflicting duplicate reports within 400m.")

            # Simulated Photo CV Tagging
            if rep_photo:
                st.markdown(f"""
                <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 10px; font-size: 0.85rem; color: #166534;">
                    📷 <b>Computer Vision Detection Result:</b><br/>
                    • Surface Damage Classification: <b>Verified ({rep_cat})</b><br/>
                    • Visual Hazard Severity: <b>High Confidence ({random.randint(91, 98)}%)</b><br/>
                    • Bounding Box: <code>[x: 120, y: 84, w: 410, h: 320]</code>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("Enter issue headline and description to activate live AI screening.")

    # Submit Button
    st.write("")
    if st.button("🚀 Submit Citizen Grievance", type="primary", use_container_width=True):
        if not rep_title.strip():
            st.error("Please enter an issue headline before submitting.")
        else:
            score_res = compute_urgency_score(rep_title, rep_desc, rep_cat, rep_ward, upvotes=1)
            routing = route_incident_to_department(rep_cat, score_res["severity"], score_res["urgency_score"])

            new_rep = {
                "id": f"CIVIC-{len(reports) + 1001}",
                "title": rep_title,
                "description": rep_desc,
                "category": rep_cat,
                "ward": rep_ward,
                "latitude": round(rep_lat, 6),
                "longitude": round(rep_lon, 6),
                "urgency_score": score_res["urgency_score"],
                "status": "Reported",
                "upvotes": 1,
                "reported_at": datetime.now().isoformat(),
                "assigned_dept": routing["assigned_department"],
                "sla_hours": score_res["sla_hours"],
                "citizen_reporter": f"Resident_{random.randint(100, 999)}",
                "ai_confidence": round(random.uniform(0.92, 0.99), 2),
                "ai_summary": score_res["recommendation"],
                "estimated_repair_cost_usd": random.choice([350, 750, 1400, 2800])
            }
            st.session_state.civic_data = add_new_report(new_rep)
            st.balloons()
            st.success(f"🎉 Grievance filed successfully! Assigned Ticket ID: **{new_rep['id']}** (Priority: {score_res['severity']})")
            st.rerun()

# =============================================================
# TAB 3: PREDICTIVE DETERIORATION & RISK FORECASTER
# =============================================================
with tab_predict:
    st.markdown("### 🔮 Proactive Infrastructure Deterioration & Failure Forecaster")
    st.write(
        "Traditional civic systems wait for citizen complaints. CivicPulse AI forecasts cascading failures "
        "7 to 14 days in advance by analyzing micro-leak frequencies, temporal spikes, and spatial stress indices."
    )

    st.markdown("#### 🚨 Imminent Failure Warning Directives (Next 48–72 Hours)")
    if emerging_threats:
        for threat in emerging_threats[:4]:
            t_color = "#dc2626" if threat["risk_probability"] >= 80 else "#ea580c"
            st.markdown(f"""
            <div style="background: #ffffff; border-left: 6px solid {t_color}; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b style="font-size: 1.05rem; color: #1e293b;">{threat['ward']} &mdash; {threat['category']}</b>
                    <span style="background: {t_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: bold;">
                        {threat['threat_level']} ({threat['risk_probability']}% Failure Risk)
                    </span>
                </div>
                <div style="margin-top: 6px; font-size: 0.9rem; color: #334155;">
                    <b>Forecast Time Window:</b> {threat['forecast_window']} &nbsp;|&nbsp; 
                    <b>Correlated Precursor Incidents:</b> {threat['active_incidents']}
                </div>
                <div style="margin-top: 6px; font-size: 0.88rem; color: #15803d; background: #f0fdf4; padding: 8px 12px; border-radius: 6px;">
                    🛡️ <b>Preventative Maintenance Action:</b> {threat['preventative_action']}<br/>
                    💰 <b>Fiscal Value:</b> <b>{threat['estimated_damage_averted_usd']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No critical deterioration threats detected across monitored wards.")

    st.markdown("---")
    st.markdown("#### 📊 Ward Deterioration Vulnerability Matrix")
    
    matrix_rows = []
    for w_name, w_data in ward_forecasts.items():
        top_fragile_cat = "None"
        max_p = 0
        for c_name, c_info in w_data["categories"].items():
            if c_info["failure_probability_7d"] > max_p:
                max_p = c_info["failure_probability_7d"]
                top_fragile_cat = f"{c_name} ({max_p}%)"

        matrix_rows.append({
            "Ward": w_name,
            "Total Issues Logged": w_data["total_reports"],
            "Vulnerability Score": f"{w_data['vulnerability_score']}/100",
            "Highest Risk Asset": top_fragile_cat,
            "Status": w_data["status"]
        })

    m_df = pd.DataFrame(matrix_rows)
    st.dataframe(m_df, use_container_width=True, hide_index=True)

# =============================================================
# TAB 4: MUNICIPAL ADMIN KANBAN & DISPATCH WORKFLOW
# =============================================================
with tab_kanban:
    st.markdown("### 📋 Municipal Operations Kanban & SLA Dispatch Board")
    st.write("Track municipal work tickets across real-time SLA lifecycles and advance dispatch statuses.")

    kanban_cols = st.columns(len(STATUS_FLOW))

    for idx, status_step in enumerate(STATUS_FLOW):
        with kanban_cols[idx]:
            step_reports = [r for r in filtered_reports if r.get("status") == status_step]
            st.markdown(f"""
            <div style="background: #f1f5f9; padding: 8px 12px; border-radius: 8px; margin-bottom: 10px; border-top: 4px solid {STATUS_COLORS.get(status_step, '#cbd5e1')};">
                <b style="font-size: 0.95rem;">{status_step}</b> 
                <span style="background: #e2e8f0; padding: 2px 7px; border-radius: 10px; font-size: 0.78rem; font-weight: bold; margin-left: 4px;">
                    {len(step_reports)}
                </span>
            </div>
            """, unsafe_allow_html=True)

            for rep in step_reports[:6]:  # Show top 6 per column
                urg = rep.get("urgency_score", 50)
                sla_info = compute_sla_status(rep.get("reported_at", ""), rep.get("sla_hours", 24), rep.get("status"))
                
                with st.container():
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; margin-bottom: 10px; font-size: 0.85rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                        <div style="display: flex; justify-content: space-between;">
                            <b>{rep['id']}</b>
                            <span style="color: {'#dc2626' if urg >= 80 else '#ea580c'}; font-weight: bold;">{urg}/100</span>
                        </div>
                        <div style="font-weight: 600; margin: 4px 0; color: #1e293b; font-size: 0.82rem;">{rep['title'][:48]}...</div>
                        <div style="color: #64748b; font-size: 0.75rem;">
                            🏢 {rep['assigned_dept']}<br/>
                            ⏱️ <span style="color: {sla_info['color']}; font-weight: bold;">{sla_info['badge']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Action buttons to transition status
                    if status_step != "Resolved":
                        next_status_idx = STATUS_FLOW.index(status_step) + 1
                        next_status = STATUS_FLOW[next_status_idx]
                        if st.button(f"Advance ➔ {next_status}", key=f"adv_{rep['id']}", use_container_width=True):
                            update_report_status(rep["id"], next_status)
                            st.session_state.civic_data = load_civic_data()
                            st.rerun()

# =============================================================
# TAB 5: PULSEASSISTANT RAG ANALYST (MUNICIPAL AI CHAT)
# =============================================================
with tab_ai:
    st.markdown("### 🤖 PulseAssistant — Natural Language Municipal Intelligence")
    st.write(
        "Chat with your civic database. Ask questions about spatial clusters, department backlogs, "
        "SLA performance, or preventative budget savings."
    )

    # Quick prompt buttons
    st.caption("Quick Queries:")
    qp_cols = st.columns(4)
    with qp_cols[0]:
        if st.button("📊 Executive Briefing", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Give me a daily executive briefing on city grievances."})
            ans = query_pulse_assistant("Give me a daily executive briefing", reports)
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
            st.rerun()
    with qp_cols[1]:
        if st.button("📍 Highest Risk Ward", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Which ward has the most critical civic problems right now?"})
            ans = query_pulse_assistant("Which ward has the most critical civic problems?", reports)
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
            st.rerun()
    with qp_cols[2]:
        if st.button("🚰 Water & Drainage Sector", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Summarize all water and drainage issues across the city."})
            ans = query_pulse_assistant("Summarize water and drainage issues", reports)
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
            st.rerun()
    with qp_cols[3]:
        if st.button("🔮 Preventative Cost Savings", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "How much can predictive maintenance save our city this month?"})
            ans = query_pulse_assistant("How much can predictive maintenance save our city budget?", reports)
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
            st.rerun()

    # Chat messages display
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User chat input
    if prompt := st.chat_input("Ask PulseAssistant about municipal data, hotspots, or SLAs..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = query_pulse_assistant(prompt, reports)
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Data export utility
    st.markdown("---")
    st.markdown("#### 📥 Export Civic Intelligence Dataset")
    export_df = pd.DataFrame(reports)
    csv_bytes = export_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Municipal Dataset (CSV)",
        data=csv_bytes,
        file_name=f"civicpulse_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=False
    )
