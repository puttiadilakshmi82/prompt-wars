"""
Analytics and Altair Visualization Components for CivicPulse AI
"""

import pandas as pd
import altair as alt
from civicpulse.config import STATUS_FLOW, CATEGORIES


def render_category_chart(reports):
    """Horizontal bar chart showing incident distribution across categories."""
    if not reports:
        return None
    df = pd.DataFrame(reports)
    cat_df = df["category"].value_counts().reset_index()
    cat_df.columns = ["Category", "Incident Count"]

    chart = alt.Chart(cat_df).mark_bar(cornerRadius=4).encode(
        x=alt.X("Incident Count:Q", title="Total Reports"),
        y=alt.Y("Category:N", sort="-x", title=None),
        color=alt.Color("Category:N", legend=None, scale=alt.Scale(
            domain=list(CATEGORIES.keys()),
            range=[c["color"] for c in CATEGORIES.values()]
        )),
        tooltip=["Category", "Incident Count"]
    ).properties(height=260)

    return chart


def render_urgency_histogram(reports):
    """Histogram showing distribution of urgency scores across 0-100."""
    if not reports:
        return None
    df = pd.DataFrame(reports)
    
    chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X("urgency_score:Q", bin=alt.Bin(maxbins=15), title="Urgency Score (0 - 100)"),
        y=alt.Y("count()", title="Number of Issues"),
        color=alt.Color("urgency_score:Q", scale=alt.Scale(scheme="redyellowgreen", reverse=True), legend=None),
        tooltip=[alt.Tooltip("count()", title="Count"), alt.Tooltip("urgency_score:Q", bin=alt.Bin(maxbins=15), title="Range")]
    ).properties(height=240)

    return chart


def render_ward_comparison_chart(reports):
    """Grouped bar chart showing total and critical issues by ward."""
    if not reports:
        return None
    df = pd.DataFrame(reports)
    
    # Calculate ward total and critical counts
    records = []
    for ward, group in df.groupby("ward"):
        ward_clean = ward.split(" - ")[-1]
        total = len(group)
        critical = len(group[group["urgency_score"] >= 80])
        records.append({"Ward": ward_clean, "Type": "Total Issues", "Count": total})
        records.append({"Ward": ward_clean, "Type": "Critical (≥80)", "Count": critical})

    chart_df = pd.DataFrame(records)
    chart = alt.Chart(chart_df).mark_bar(cornerRadius=3).encode(
        x=alt.X("Ward:N", title=None, axis=alt.Axis(labelAngle=-25)),
        y=alt.Y("Count:Q", title="Issues Count"),
        color=alt.Color("Type:N", scale=alt.Scale(domain=["Total Issues", "Critical (≥80)"], range=["#3b82f6", "#ef4444"])),
        xOffset="Type:N",
        tooltip=["Ward", "Type", "Count"]
    ).properties(height=240)

    return chart
