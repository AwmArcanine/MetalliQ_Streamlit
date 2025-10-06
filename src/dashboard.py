import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def dashboard_page(workspace=None):
    st.set_page_config(layout="wide")
    st.cache_data.clear()

    # ---------------------- THEME STYLING ----------------------
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Orbitron:wght@600&display=swap');

        body, .stApp {
            background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #83C5BE 100%) !important;
            color: #E6FFFF !important;
            font-family: 'Poppins', sans-serif;
        }

        /* Headings */
        h1, h2, h3, h4 {
            font-family: 'Orbitron', sans-serif;
            color: #7CF4E3 !important;
            text-shadow: 0 0 10px rgba(124, 244, 227, 0.6);
        }

        /* Section Titles */
        .section-title {
            color: #7CF4E3 !important;
            font-weight: 700;
            margin-top: 40px;
            margin-bottom: 15px;
            font-size: 1.35rem !important;
        }

        /* Glass Cards */
        .metriccard, .ext-card, .report-card {
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            padding: 18px 22px;
            box-shadow: 0 8px 25px rgba(0, 109, 119, 0.25);
            transition: 0.3s;
        }
        .metriccard:hover, .ext-card:hover, .report-card:hover {
            box-shadow: 0 0 25px rgba(124, 244, 227, 0.85);
            transform: translateY(-3px);
        }

        /* Metric text */
        .metricheader { font-size: 1.1rem; color: #D8FFFF; margin-bottom: 6px; }
        .metricvalue { font-size: 1.9rem; font-weight: 800; color: #00F5D4; }

        /* Tables */
        table {
            border: 1.5px solid rgba(124, 244, 227, 0.35) !important;
            border-radius: 10px;
            background: rgba(255,255,255,0.05);
        }
        thead tr {
            background: rgba(124, 244, 227, 0.15) !important;
            color: #7CF4E3 !important;
            font-weight: 600;
        }
        tbody tr { color: #E6FFFF !important; }

        /* Reuse badges */
        .leaderboard-badge {
            background: rgba(124, 244, 227, 0.25);
            border-radius: 12px;
            color: #7CF4E3;
            font-weight: 600;
            padding: 3px 12px;
        }

        /* Button */
        div.stButton > button {
            background: linear-gradient(90deg, #00A896, #02C39A);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 8px 16px;
            box-shadow: 0 0 8px rgba(124, 244, 227, 0.3);
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg, #02C39A, #00F5D4);
            box-shadow: 0 0 15px rgba(124, 244, 227, 0.8);
            transform: translateY(-2px);
        }

        .stPlotlyChart { margin-top: 10px; margin-bottom: 40px; }
        </style>
    """, unsafe_allow_html=True)

    # ---------------------- HEADER ----------------------
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown("<h1>MetalliQ Sustainability Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#E6FFFF;font-size:0.95rem;'>An overview of your workspace’s sustainability intelligence.</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='margin-top:20px;'>", unsafe_allow_html=True)
        st.button("➕ New Study", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------- MOCK DATA ----------------------
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

    # ---------------------- METRIC CARDS ----------------------
    st.markdown("<h3 class='section-title'>Core Metrics</h3>", unsafe_allow_html=True)
    cols = st.columns(3)
    metrics = [
        ("Average Recycling Rate", f"{results['metrics']['avg_recycling_rate']}%"),
        ("Total Recycled Material", f"{results['metrics']['total_recycled_material']} tonnes"),
        ("Average Circularity Score", f"{results['metrics']['avg_circularity_score']}/100")
    ]
    for i, (label, val) in enumerate(metrics):
        cols[i].markdown(f"<div class='metriccard'><div class='metricheader'>{label}</div><div class='metricvalue'>{val}</div></div>", unsafe_allow_html=True)

    # ---------------------- LINE CHART ----------------------
    st.markdown("<h3 class='section-title'>Recycling Rate Over Time</h3>", unsafe_allow_html=True)
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(
        x=[str(d.date()) for d in results["recycling_rate_trend"].index],
        y=results["recycling_rate_trend"].values,
        fill='tozeroy',
        mode='lines+markers',
        line=dict(color="#00F5D4", width=3),
        marker=dict(size=7, color="#7CF4E3", line=dict(color="#00494D", width=1.5))
    ))
    line_fig.update_layout(
        yaxis_title="Recycling Rate (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6FFFF"),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#E6FFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#E6FFFF")),
        height=400
    )
    st.plotly_chart(line_fig, use_container_width=True)

    # ---------------------- PIE CHART ----------------------
    st.markdown("<h3 class='section-title'>Recycled vs Primary Material Share</h3>", unsafe_allow_html=True)
    pie_fig = go.Figure(go.Pie(
        labels=["Recycled Route", "Primary Route"],
        values=results["pie_share"],
        hole=0.6,
        marker=dict(colors=["#00F5D4", "#006D77"]),
        textinfo='percent+label'
    ))
    pie_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E6FFFF"), height=350)
    st.plotly_chart(pie_fig, use_container_width=True)

    # ---------------------- EXTENDED CIRCULARITY ----------------------
    st.markdown("<h3 class='section-title'>Extended Circularity Metrics</h3>", unsafe_allow_html=True)
    cardcols = st.columns(4)
    for i, (label, value) in enumerate(results["extended_circularity"]):
        cardcols[i % 4].markdown(
            f"<div class='ext-card'><b>{label}</b><br><span style='font-size:1.25rem;font-weight:700;color:#00F5D4;'>{value}</span></div>",
            unsafe_allow_html=True
        )

    # ---------------------- HOTSPOT TABLE ----------------------
    st.markdown("<h3 class='section-title'>Sustainability Hotspots – Top 3 Materials</h3>", unsafe_allow_html=True)
    df = pd.DataFrame(results["hotspots_materials"], columns=["Material", "Recycled Content (%)"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ---------------------- REUSE PROJECTS ----------------------
    st.markdown("<h3 class='section-title'>Projects with Highest Reuse Potential</h3>", unsafe_allow_html=True)
    for proj, mat, pct in results["reuse_projects"]:
        st.markdown(
            f"<div style='background:rgba(255,255,255,0.1);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,0.25);border-radius:14px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;'>"
            f"<span><b>{proj}</b> ({mat})</span><span class='leaderboard-badge'>{pct}%</span></div>",
            unsafe_allow_html=True
        )

    # ---------------------- IMPACT BAR CHART ----------------------
    st.markdown("<h3 class='section-title'>Key Impact Profiles</h3>", unsafe_allow_html=True)
    df_impact = pd.DataFrame(results["key_impact_profiles"], columns=["Category", "Value"])
    bar = px.bar(
        df_impact,
        x="Category",
        y="Value",
        color="Category",
        color_discrete_sequence=["#00F5D4", "#7CF4E3", "#02C39A", "#00A896", "#006D77"]
    )
    bar.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6FFFF"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#E6FFFF")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#E6FFFF")),
        height=400
    )
    st.plotly_chart(bar, use_container_width=True)

    # ---------------------- SUMMARY CARDS ----------------------
    st.markdown("<h3 class='section-title'>Latest Report Analysis</h3>", unsafe_allow_html=True)
    s = results["summary"]
    cols = st.columns(4)
    for i, (k, v) in enumerate(s.items()):
        cols[i % 4].markdown(
            f"<div class='report-card'><b>{k}</b><br><span style='font-size:1.35rem;font-weight:700;color:#00F5D4;'>{v['mean']} <small>{v['unit']}</small></span></div>",
            unsafe_allow_html=True
        )
