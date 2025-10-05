import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- Neon Futuristic Theme with Pulse Glow ---



def dashboard_page(workspace=None):
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;500;600&display=swap');

    body, .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #83C5BE 100%) !important;
        color: #E0FFFF;
        font-family: 'Poppins', sans-serif;
        overflow-x: hidden;
    }

    /* Text Styles */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif;
        color: #00EFFF;
        text-shadow: 0 0 18px rgba(0, 239, 255, 0.8);
    }

    .section-title {
        color: #00EFFF !important;
        font-weight: 700;
        margin-top: 40px;
        margin-bottom: 10px;
        font-size: 1.4rem !important;
    }

    /* Pulse Animation */
    @keyframes pulseGlow {
    0% { box-shadow: 0 0 10px rgba(0,239,255,0.4), 0 0 20px rgba(0,239,255,0.2); }
    50% { box-shadow: 0 0 25px rgba(0,239,255,0.7), 0 0 40px rgba(0,239,255,0.5); }
    100% { box-shadow: 0 0 10px rgba(0,239,255,0.4), 0 0 20px rgba(0,239,255,0.2); }
    }

    /* Metric Cards */
    .metriccard {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        border: 1px solid rgba(0, 239, 255, 0.25);
        padding: 18px 22px;
        text-align: left;
        margin-top: 8px;
        animation: pulseGlow 4s infinite ease-in-out;
    }

    .metricheader {
        font-size: 1.15rem;
        color: #A7FAFF;
        margin-bottom: 7px;
    }

    .metricvalue {
        font-size: 2rem;
        font-weight: 800;
        color: #00EFFF;
    }

    /* Extended Circularity Cards */
    .ext-card {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(0, 239, 255, 0.2);
        border-radius: 14px;
        text-align: center;
        padding: 15px 8px;
        margin-bottom: 10px;
        animation: pulseGlow 5s infinite ease-in-out;
        color: #E0FFFF;
    }

    .ext-card b {
        color: #00EFFF;
    }

    /* Table Styles */
    table {
        border: 1.5px solid rgba(0, 239, 255, 0.3) !important;
        border-radius: 12px;
        background: rgba(255,255,255,0.05);
    }
    thead tr {
        background: rgba(0,239,255,0.15) !important;
        color: #00EFFF !important;
        font-weight: 600;
    }
    tbody tr {
        color: #E0FFFF !important;
    }

    /* Project Leaderboard */
    .leaderboard-badge {
        background: rgba(0, 239, 255, 0.2);
        border: 1px solid rgba(0,239,255,0.4);
        border-radius: 14px;
        color: #00EFFF;
        font-weight: 600;
        padding: 4px 14px;
    }

    /* Latest Report Cards */
    .report-card {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(0,239,255,0.3);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        animation: pulseGlow 6s infinite ease-in-out;
        color: #E0FFFF;
    }

    /* Chart Container */
    .stPlotlyChart {
        margin-top: 10px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    # --- Header ---
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown("<h1 style='color: #00EFFF;text-shadow: 0 0 18px rgba(0, 239, 255, 0.8);margin-bottom:2px;'>John's Workspace Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#00EFFF;font-size:0.9rem;'>An overview of your workspace's sustainability metrics.</p>", unsafe_allow_html=True)
    with col2:
        if st.button("➕ New Study", use_container_width=True):
            st.session_state["page"] = "Create Study"
            st.rerun()

    # --- Mock Data ---
    recycling_rate_data = pd.Series(
        [82, 81, 83, 86, 86, 88, 90, 91, 93, 95, 97],
        index=pd.date_range("2024-10-01", periods=11, freq="M"))
    results = {
        "metrics": {"avg_recycling_rate": 85.0, "total_recycled_material": 66.7, "avg_circularity_score": 68.8},
        "recycling_rate_trend": recycling_rate_data,
        "pie_share": [68, 32],
        "hotspots_materials": [("Steel", 65.6), ("Aluminum", 56.0), ("Copper", 53.5)],
        "reuse_projects": [("New Building Frame", "Steel", 90),
                           ("Residential Building", "Steel", 85),
                           ("Project Gamma", "Copper", 85)],
        "extended_circularity": [("Resource Efficiency", 92),
                                 ("Extended Product Life", 110),
                                 ("Reuse Potential", "40/50"),
                                 ("Material Recovery", 90),
                                 ("Closed-Loop Potential", 75),
                                 ("Recycling Content", 10),
                                 ("Landfill Rate", 8),
                                 ("Energy Recovery", 2)],
        "key_impact_profiles": [("GWP", 2293), ("Energy", 26454),
                                ("Water", 4.7), ("Eutrophication", 1.15),
                                ("Acidification", 4.10)],
        "summary": {'Global Warming Potential': {'mean': 2293, 'unit': 'kg CO2-eq'},
                    'Circularity Score': {'mean': 50, 'unit': '%'},
                    'Particulate Matter': {'mean': 0.76, 'unit': 'kg PM2.5-eq'},
                    'Water Consumption': {'mean': 4.7, 'unit': 'm³'}}
    }

    # --- Metric Cards ---
    st.markdown("<h3 class='section-title'>Core Metrics</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='metriccard'><div class='metricheader'>Average Recycling Rate</div><div class='metricvalue'>{results['metrics']['avg_recycling_rate']}%</div></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metriccard'><div class='metricheader'>Total Recycled Material</div><div class='metricvalue'>{results['metrics']['total_recycled_material']} tonnes</div></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metriccard'><div class='metricheader'>Average Circularity Score</div><div class='metricvalue'>{results['metrics']['avg_circularity_score']}/100</div></div>", unsafe_allow_html=True)

    # --- Line Chart ---
    st.markdown("<h3 class='section-title'>Recycling Rate Over Time</h3>", unsafe_allow_html=True)
    line_fig = go.Figure()
    trendx = [str(d.date()) for d in results["recycling_rate_trend"].index]
    line_fig.add_trace(go.Scatter(x=trendx, y=results["recycling_rate_trend"].values,
                                  fill='tozeroy', line=dict(color="#00EFFF", width=3)))
    line_fig.update_layout(xaxis_title=None, yaxis_title="Recycling Rate (%)",
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#C8FFFF"), height=350)
    st.plotly_chart(line_fig, use_container_width=True)

    # --- Pie Chart ---
    st.markdown("<h3 class='section-title'>Recycled vs Primary Material Share</h3>", unsafe_allow_html=True)
    pie_fig = go.Figure(go.Pie(labels=["Recycled Route", "Primary Route"],
                               values=results["pie_share"], hole=0.6,
                               marker=dict(colors=["#00EFFF", "#00494D"]),
                               textinfo='percent+label'))
    pie_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="#E0FFFF"), height=350)
    st.plotly_chart(pie_fig, use_container_width=True)

    # --- Extended Circularity ---
    st.markdown("<h3 class='section-title'>Extended Circularity Metrics</h3>", unsafe_allow_html=True)
    cardcols = st.columns(4)
    for i, (label, value) in enumerate(results["extended_circularity"]):
        cardcols[i % 4].markdown(f"<div class='ext-card'><b>{label}</b><br><span style='font-size:1.3rem;font-weight:700;'>{value}</span></div>", unsafe_allow_html=True)

    # --- Table ---
    st.markdown("<h3 class='section-title'>Sustainability Hotspots – Top 3 Materials</h3>", unsafe_allow_html=True)
    df = pd.DataFrame(results["hotspots_materials"], columns=["Material", "Recycled Content (%)"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- Projects ---
    st.markdown("<h3 class='section-title'>Projects with Highest Reuse Potential</h3>", unsafe_allow_html=True)
    for proj, mat, pct in results["reuse_projects"]:
        st.markdown(f"<div style='background:rgba(255,255,255,0.05);border:1px solid rgba(0,239,255,0.2);border-radius:14px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;'><span><b>{proj}</b> ({mat})</span><span class='leaderboard-badge'>{pct}%</span></div>", unsafe_allow_html=True)

    # --- Impact Bar Chart ---
    st.markdown("<h3 class='section-title'>Key Impact Profiles</h3>", unsafe_allow_html=True)
    df_impact = pd.DataFrame(results["key_impact_profiles"], columns=["Category", "Value"])
    bar = px.bar(df_impact, x="Category", y="Value", color="Category",
                 color_discrete_sequence=["#00EFFF", "#00B8CC", "#009EBB", "#0080A4", "#00494D"])
    bar.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#C8FFFF"))
    st.plotly_chart(bar, use_container_width=True)

    # --- Latest Report ---
    st.markdown("<h3 class='section-title'>Latest Report Analysis</h3>", unsafe_allow_html=True)
    s = results["summary"]
    cols = st.columns(4)
    for i, (k, v) in enumerate(s.items()):
        cols[i % 4].markdown(
            f"<div class='report-card'><b>{k}</b><br><span style='font-size:1.35rem;font-weight:700;color:#00EFFF;'>{v['mean']} <small>{v['unit']}</small></span></div>",
            unsafe_allow_html=True
        )
