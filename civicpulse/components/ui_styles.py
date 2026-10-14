"""
UI Styling, CSS injected themes, and badge renderers for CivicPulse AI.
"""

def get_custom_css():
    return """
    <style>
    /* Main container styling */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }
    
    /* Hero Header */
    .civic-hero {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(30, 60, 114, 0.15);
    }
    .civic-hero h1 {
        color: #ffffff;
        font-size: 2.3rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .civic-hero p {
        color: #e0e9f8;
        font-size: 1.05rem;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(0,0,0,0.06);
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #1a202c;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #718096;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .metric-sub {
        font-size: 0.8rem;
        margin-top: 4px;
    }
    
    /* Issue Card */
    .issue-card {
        background: #ffffff;
        border-left: 5px solid #3498db;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    
    /* Badges */
    .badge-critical {
        background-color: #fee2e2;
        color: #dc2626;
        padding: 3px 9px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-high {
        background-color: #ffedd5;
        color: #ea580c;
        padding: 3px 9px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-medium {
        background-color: #fef9c3;
        color: #ca8a04;
        padding: 3px 9px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-low {
        background-color: #dcfce7;
        color: #16a34a;
        padding: 3px 9px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
    }

    /* Hotspot Alert Banner */
    .hotspot-banner {
        background: #fff7ed;
        border-left: 5px solid #f97316;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    </style>
    """
