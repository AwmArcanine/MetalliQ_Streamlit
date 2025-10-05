import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# === CYBER-GLASS THEME (Electric Blue) ===
st.set_page_config(layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;500;600&display=swap');

/* ==== GLOBAL ==== */
[data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #022C43 100%) !important;
  font-family: 'Poppins', sans-serif !important;
  color: #E6FFFF !important;
  padding: 1rem 2rem 3rem 2rem !important;
}

/* ==== TITLES ==== */
[data-testid="stAppViewContainer"] h1 {
  color: #4EF3FF !important;
  text-shadow: 0 0 12px rgba(78,243,255,0.8);
  font-family: 'Orbitron', sans-serif !important;
  font-size: 2.4rem !important;
  margin-bottom: 0.2em !important;
}
.section-title {
  font-size: 1.3rem !important;
  font-weight: 700;
  color: #4EF3FF !important;
  text-shadow: 0 0 8px rgba(78,243,255,0.7);
  margin-top: 2.2rem;
  margin-bottom: 1rem;
  text-align: left;
  font-family: 'Orbitron', sans-serif !important;
}

/* ==== METRIC CARDS ==== */
.metriccard {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(78,243,255,0.4);
  border-radius: 18px;
  box-shadow: 0 0 20px rgba(78,243,255,0.25);
  backdrop-filter: blur(12px);
  text-align: center;
  padding: 20px 15px;
  margin-bottom: 25px;
}
.metricheader {
  font-size: 1.05rem;
  color: #B7FAFF;
}
.metricvalue {
  font-size: 2rem;
  font-weight: 800;
  color: #4EF3FF;
}

/* ==== GLASS CARDS ==== */
.glass-card {
  background: rgba(255,255,255,0.07);
  border-radius: 16px;
  border: 1px solid rgba(78,243,255,0.35);
  box-shadow: 0 0 18px rgba(78,243,255,0.25);
  backdrop-filter: blur(10px);
  text-align: center;
  padding: 14px 10px;
  color: #E6FFFF;
  font-size: 1.05rem;
}

/* ==== TABLES ==== */
thead tr th {
  background: rgba(1,60,68,0.9) !important;
  color: #4EF3FF !important;
  border-bottom: 2px solid rgba(78,243,255,0.6) !important;
  text-align: center !important;
}
tbody tr td {
  color: #E6FFFF !important;
  border: 1.5px solid rgba(78,243,255,0.4) !important;
}
tbody tr:hover {
  background: rgba(78,243,255,0.08) !important;
}

/* ==== BADGES ==== */
.leaderboard-badge {
  background: linear-gradient(90deg, #00AEEF 0%, #0074A6 100%);
  color: white;
  border-radius: 16px;
  padding: 4px 14px;
  font-weight: 700;
}

/* ==== SMALL TEXT ==== */
small, p {
  color: #C9FBFF !important;
}
</style>
""", unsafe_allow_html=True)


def dashboard_page(workspace=None):
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("+ New Study", use_container_width=True):
            st.session_state["page"] = "Create Study"
            st.rerun()

    # ---- MOCK DATA ----
    results = st.session_state.get('simulation_results')
    if not results:
        recycling_rate_data = pd.Series(
            [82, 81, 83, 86, 86, 88, 90, 91, 93, 95, 97],
            index=pd.date_range("2024-10-01", periods=11, freq="M"))
        results = {
            "metrics": {
                "avg_recycling_rate": 85.0,
                "total_recycled_material": 66.7,
                "avg_circularity_score": 68.8,
                "total_reports": 4,
                "total_gwp_sum": 8755
            },
            "recycling_rate_trend": recycling_rate_data,
            "pie_share": [68, 32],
            "hotspots_materials": [("Steel", 65.6), ("Aluminum", 56.0), ("Copper", 53.5)],
            "reuse_projects": [("New Building Frame", "Steel", 90),
                               ("Residential Building", "Steel", 85),
                               ("Project Gamma", "Copper", 85)],
            "extended_circularity": [
                ("Resource Efficiency", 92),
                ("Extended Product Life", 110),
                ("Reuse Potential", "40/50"),
                ("Material Recovery", 90),
                ("Closed-Loop Potential", 75),
                ("Recycling Content", 10),
                ("Landfill Rate", 8),
                ("Energy Recovery", 2)
            ],
            "key_impact_profiles": [
                ("GWP", 2293),
                ("Energy", 26454),
                ("Water", 4.7),
                ("Eutrophication", 1.15),
                ("Acidification", 4.10),
            ],
            "summary": {
                'Global Warming Potential': {'mean': 2293, 'unit': 'kg CO2-eq'},
                'Circularity Score': {'mean': 50, 'unit': '%'},
                'Particulate Matter': {'mean': 0.76, 'unit': 'kg PM2.5-eq'},
                'Water Consumption': {'mean': 4.7, 'unit': 'm³'}
            }
        }

    # ---- HEADER ----
    st.markdown("<h1>John's Workspace Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<small>An overview of your workspace’s sustainability metrics.</small>", unsafe_allow_html=True)

    # ---- METRICS ----
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='metriccard'><div class='metricheader'>Average Recycling Rate</div><div class='metricvalue'>{results['metrics']['avg_recycling_rate']}%</div></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metriccard'><div class='metricheader'>Total Recycled Material</div><div class='metricvalue'>{results['metrics']['total_recycled_material']} tonnes</div></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metriccard'><div class='metricheader'>Average Circularity Score</div><div class='metricvalue'>{results['metrics']['avg_circularity_score']}/100</div></div>", unsafe_allow_html=True)

    # ---- LINE CHART ----
    st.markdown("<div class='section-title'>Recycling Rate Over Time</div>", unsafe_allow_html=True)
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(
        x=[str(d.date()) for d in results["recycling_rate_trend"].index],
        y=results["recycling_rate_trend"].values,
        line=dict(color="#00F5FF", width=4),
        fill='tozeroy'))
    line_fig.update_layout(
        xaxis_title=None, yaxis_title="Recycling Rate (%)",
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(color="#E6FFFF"), height=250)
    st.plotly_chart(line_fig, use_container_width=True)

    # ---- PIE CHART ----
    st.markdown("<div class='section-title'>Recycled vs Primary Material Share</div>", unsafe_allow_html=True)
    pie_fig = go.Figure(go.Pie(
        labels=["Recycled Route", "Primary Route"],
        values=results["pie_share"],
        hole=0.6,
        marker=dict(colors=["#00EFFF", "#024E5C"]),
        textinfo='percent+label'))
    pie_fig.update_layout(showlegend=True, font=dict(color="#E6FFFF"), height=230,
                          paper_bgcolor='rgba(255,255,255,0)', plot_bgcolor='rgba(255,255,255,0)')
    st.plotly_chart(pie_fig, use_container_width=True)

    # ---- EXTENDED METRICS ----
    st.markdown("<div class='section-title'>Extended Circularity Metrics</div>", unsafe_allow_html=True)
    cardcols = st.columns(4)
    for i, (label, value) in enumerate(results["extended_circularity"]):
        cardcols[i % 4].markdown(f"<div class='glass-card'><b>{label}</b><br><span style='font-size:1.3rem;color:#4EF3FF;font-weight:700'>{value}</span></div>", unsafe_allow_html=True)

    # ---- HOTSPOTS TABLE ----
    st.markdown("<div class='section-title'>Sustainability Hotspots – Top 3 Materials</div>", unsafe_allow_html=True)
    hotspot_table = pd.DataFrame(results["hotspots_materials"], columns=["Material", "Recycled Content (%)"])
    st.table(hotspot_table)

    # ---- PROJECTS ----
    st.markdown("<div class='section-title'>Projects with Highest Reuse Potential</div>", unsafe_allow_html=True)
    for proj, mat, pct in results["reuse_projects"]:
        st.markdown(f"<div class='glass-card' style='display:flex;justify-content:space-between;align-items:center;'><span><b>{proj}</b> ({mat})</span><span class='leaderboard-badge'>{pct}%</span></div>", unsafe_allow_html=True)

    # ---- BAR CHART ----
    st.markdown("<div class='section-title'>Key Impact Profiles</div>", unsafe_allow_html=True)
    df_impact = pd.DataFrame(results["key_impact_profiles"], columns=["Category", "Value"])
    bar = px.bar(df_impact, x="Category", y="Value", color="Category", text="Value",
                 color_discrete_sequence=["#00EFFF", "#4EF3FF", "#33CCFF", "#80FFFF", "#5BE3FF"])
    bar.update_layout(showlegend=False, height=300,
                      font=dict(color="#E6FFFF"),
                      paper_bgcolor='rgba(255,255,255,0)',
                      plot_bgcolor='rgba(255,255,255,0)')
    st.plotly_chart(bar, use_container_width=True)

    # ---- LATEST REPORT ----
    st.markdown("<div class='section-title'>Latest Report Analysis</div>", unsafe_allow_html=True)
    s = results['summary']
    cardcols2 = st.columns(4)
    for i, (key, val) in enumerate(s.items()):
        cardcols2[i].markdown(f"<div class='glass-card'><b>{key}</b><br><span style='font-size:1.4rem;color:#4EF3FF;font-weight:800'>{val['mean']} <small>{val['unit']}</small></span></div>", unsafe_allow_html=True)
