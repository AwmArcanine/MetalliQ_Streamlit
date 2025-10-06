import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def dashboard_page(workspace=None):
    st.set_page_config(layout="wide")
    st.cache_data.clear()

    # --- THEME (matches Collaborative Workspace) ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        body, .stApp {
            background: linear-gradient(120deg, #f7fdfc 0%, #e6fffb 100%) !important;
            color: #003E3E;
            font-family: 'Poppins', sans-serif;
        }

        /* Center Header */
        h1 {
            text-align: center;
            color: #006D77 !important;
            font-weight: 700;
            margin-bottom: 4px;
            letter-spacing: -0.3px;
        }

        h3.section-title {
            color: #00494D !important;
            font-weight: 600;
            font-size: 1.2rem;
            margin-top: 32px;
            border-left: 4px solid #00A896;
            padding-left: 8px;
        }

        /* Card Styling */
        .metriccard, .ext-card, .report-card {
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 16px;
            border: 1px solid rgba(0, 73, 77, 0.15);
            padding: 18px 22px;
            box-shadow: 0 4px 20px rgba(0, 109, 119, 0.08);
            transition: all 0.3s ease-in-out;
        }
        .metriccard:hover, .ext-card:hover, .report-card:hover {
            box-shadow: 0 4px 25px rgba(0, 168, 150, 0.25);
            transform: translateY(-3px);
        }

        .metricheader {
            font-size: 1rem;
            color: #00494D;
            margin-bottom: 4px;
        }

        .metricvalue {
            font-size: 1.9rem;
            font-weight: 700;
            color: #00A896;
        }

        .ext-card {
            text-align: center;
            margin-bottom: 12px;
        }

        /* Table */
        table {
            border: 1.5px solid rgba(0, 168, 150, 0.25) !important;
            border-radius: 10px;
            background: rgba(255,255,255,0.6);
        }
        thead tr {
            background: rgba(0,168,150,0.1) !important;
            color: #00494D !important;
            font-weight: 600;
        }
        tbody tr {
            color: #00494D !important;
        }

        /* Project Badge */
        .leaderboard-badge {
            background: rgba(0, 168, 150, 0.1);
            border-radius: 12px;
            color: #006D77;
            font-weight: 600;
            padding: 3px 12px;
        }

        /* Chart Margins */
        .stPlotlyChart {
            margin-top: 10px;
            margin-bottom: 40px;
        }

        /* Button */
        .stButton button {
            background: linear-gradient(90deg,#00A896,#02C39A);
            color: white !important;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 1.3rem;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            box-shadow: 0 0 12px rgba(0,168,150,0.6);
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Header ---
    st.markdown("<h1>🌍 MetalliQ Sustainability Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#00494D;font-size:0.95rem;'>Your workspace’s unified sustainability intelligence overview</p>", unsafe_allow_html=True)

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
    line_fig.add_trace(go.Scatter(
        x=trendx,
        y=results["recycling_rate_trend"].values,
        fill='tozeroy',
        mode='lines+markers',
        line=dict(color="#00A896", width=3),
        marker=dict(size=7, color="#006D77", line=dict(color="#00F5D4", width=1.5))
    ))
    line_fig.update_layout(
        yaxis_title="Recycling Rate (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.4)",
        font=dict(color="#00494D"),
        xaxis=dict(showgrid=True, gridcolor="rgba(0,73,77,0.1)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,73,77,0.1)"),
        height=400
    )
    st.plotly_chart(line_fig, use_container_width=True)

    # --- Pie Chart ---
    st.markdown("<h3 class='section-title'>Recycled vs Primary Material Share</h3>", unsafe_allow_html=True)
    pie_fig = go.Figure(go.Pie(
        labels=["Recycled Route", "Primary Route"],
        values=results["pie_share"],
        hole=0.6,
        marker=dict(colors=["#00A896", "#83C5BE"]),
        textinfo='percent+label'
    ))
    pie_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#00494D"),
        height=350
    )
    st.plotly_chart(pie_fig, use_container_width=True)

    # --- Extended Circularity ---
    st.markdown("<h3 class='section-title'>Extended Circularity Metrics</h3>", unsafe_allow_html=True)
    cardcols = st.columns(4)
    for i, (label, value) in enumerate(results["extended_circularity"]):
        cardcols[i % 4].markdown(
            f"<div class='ext-card'><b style='color:#00494D'>{label}</b><br><span style='font-size:1.25rem;font-weight:700;color:#00A896;'>{value}</span></div>",
            unsafe_allow_html=True
        )

    # --- Table ---
    st.markdown("<h3 class='section-title'>Sustainability Hotspots – Top 3 Materials</h3>", unsafe_allow_html=True)
    df = pd.DataFrame(results["hotspots_materials"], columns=["Material", "Recycled Content (%)"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- Projects ---
    st.markdown("<h3 class='section-title'>Projects with Highest Reuse Potential</h3>", unsafe_allow_html=True)
    for proj, mat, pct in results["reuse_projects"]:
        st.markdown(
            f"<div style='background:rgba(255,255,255,0.65);border:1px solid rgba(0,109,119,0.15);border-radius:14px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;'>"
            f"<span style='color:#00494D'><b>{proj}</b> ({mat})</span><span class='leaderboard-badge'>{pct}%</span></div>",
            unsafe_allow_html=True
        )

    # --- Impact Bar Chart ---
    st.markdown("<h3 class='section-title'>Key Impact Profiles</h3>", unsafe_allow_html=True)
    df_impact = pd.DataFrame(results["key_impact_profiles"], columns=["Category", "Value"])
    bar = px.bar(
        df_impact,
        x="Category",
        y="Value",
        color="Category",
        color_discrete_sequence=["#00A896", "#006D77", "#02C39A", "#83C5BE", "#00F5D4"]
    )
    bar.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.4)",
        font=dict(color="#00494D"),
        xaxis=dict(gridcolor="rgba(0,73,77,0.1)"),
        yaxis=dict(gridcolor="rgba(0,73,77,0.1)"),
        height=400
    )
    st.plotly_chart(bar, use_container_width=True)

    # --- Latest Report ---
    st.markdown("<h3 class='section-title'>Latest Report Analysis</h3>", unsafe_allow_html=True)
    s = results["summary"]
    cols = st.columns(4)
    for i, (k, v) in enumerate(s.items()):
        cols[i % 4].markdown(
            f"<div class='report-card'><b style='color:#00494D'>{k}</b><br><span style='font-size:1.35rem;font-weight:700;color:#00A896;'>{v['mean']} <small>{v['unit']}</small></span></div>",
            unsafe_allow_html=True
        )
