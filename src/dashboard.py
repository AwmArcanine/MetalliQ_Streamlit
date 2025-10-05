import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# === MetalliQ Futuristic Minimal Neon Theme ===
st.markdown("""
<style>
html, body, .stApp {
    background: linear-gradient(135deg, #00393D 0%, #007C91 100%) !important;
    font-family: 'Poppins', sans-serif;
    color: #E8FEFB;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #7CF4E3 !important;
}

/* Main Title */
.main-title {
    font-size: 2.8rem;
    font-weight: 900;
    text-align: center;
    color: #7CF4E3;
    text-shadow: 0 0 12px rgba(124, 244, 227, 0.55);
    margin-bottom: 0.3em;
}

/* Subheader */
.subheader {
    text-align: center;
    color: #B9FFF4;
    font-weight: 500;
    font-size: 1.05rem;
    margin-bottom: 2rem;
}

/* Metric Cards */
.metriccard {
    background: rgba(255, 255, 255, 0.07);
    border: 1.5px solid rgba(63, 255, 255, 0.45);
    border-radius: 18px;
    padding: 18px 20px;
    text-align: center;
    box-shadow: 0 0 18px rgba(63, 255, 255, 0.05);
    backdrop-filter: blur(12px);
}

.metricheader {
    font-size: 1.1rem;
    color: #9CF9F2;
    margin-bottom: 6px;
}

.metricvalue {
    font-size: 2.1rem;
    font-weight: 800;
    color: #3EF5FF;
    letter-spacing: -0.8px;
}

/* Section Titles */
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #7CF4E3;
    margin-top: 30px;
    margin-bottom: 15px;
}

/* Extended Metrics & Report Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    border: 1.6px solid rgba(63, 255, 255, 0.4);
    box-shadow: 0 0 20px rgba(63,255,255,0.05);
    backdrop-filter: blur(10px);
    padding: 14px 10px;
    text-align: center;
    color: #E8FEFB;
}

/* Table Styling */
table {
    border-collapse: collapse !important;
    width: 100%;
    margin-bottom: 15px;
    border: 2px solid rgba(63,255,255,0.3) !important;
    border-radius: 10px !important;
}

thead tr th {
    background: rgba(0, 120, 130, 0.55) !important;
    color: #E8FEFB !important;
    font-weight: 700;
    text-align: center;
    border-bottom: 2px solid rgba(63,255,255,0.45);
}

tbody tr td {
    color: #EAFDFC !important;
    text-align: center;
    padding: 8px !important;
    border-top: 1px solid rgba(63,255,255,0.15);
}

/* Leaderboard Badge */
.leaderboard-badge {
    background: linear-gradient(90deg,#00E0C6,#00FFF6);
    color: #00373D;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
    padding: 4px 15px;
}

/* Buttons */
[data-testid="baseButton-primary"] {
    background: linear-gradient(90deg, #00FFF6, #00A896) !important;
    color: #00373D !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    box-shadow: 0 0 15px rgba(0,255,230,0.15);
}
</style>
""", unsafe_allow_html=True)


def dashboard_page(workspace=None):
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("+ New Study", key="dashboard_new_study", use_container_width=True):
            st.session_state["page"] = "Create Study"
            st.rerun()

    # ----------- MOCK DATA -------------
    results = st.session_state.get('simulation_results')
    if not results:
        recycling_rate_data = pd.Series(
            [82, 81, 83, 86, 86, 88, 90, 91, 93, 95, 97],
            index=pd.date_range("2024-10-01", periods=11, freq="M"))
        recycled_share, primary_share = 68, 32
        top_materials = [("Steel", 65.6), ("Aluminum", 56.0), ("Copper", 53.5)]
        reuse_projects = [
            ("New Building Frame", "Steel", 90),
            ("Residential Building", "Steel", 85),
            ("Project Gamma", "Copper", 85)
        ]
        results = {
            "metrics": {
                "avg_recycling_rate": 85.0,
                "total_recycled_material": 66.7,
                "avg_circularity_score": 68.8,
                "total_reports": 4,
                "total_gwp_sum": 8755
            },
            "recycling_rate_trend": recycling_rate_data,
            "pie_share": [recycled_share, primary_share],
            "hotspots_materials": top_materials,
            "reuse_projects": reuse_projects,
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

    # === Title ===
    st.markdown("<div class='main-title'>John's Workspace Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader'>An overview of your workspace's sustainability metrics.</div>", unsafe_allow_html=True)

    # === Metric Cards ===
    col1, col2, col3 = st.columns([3, 3, 3])
    col1.markdown(f'<div class="metriccard"><div class="metricheader">Average Recycling Rate</div><div class="metricvalue">{results["metrics"]["avg_recycling_rate"]}%</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metriccard"><div class="metricheader">Total Recycled Material</div><div class="metricvalue">{results["metrics"]["total_recycled_material"]} tonnes</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metriccard"><div class="metricheader">Circularity Score</div><div class="metricvalue">{results["metrics"]["avg_circularity_score"]}/100</div></div>', unsafe_allow_html=True)

    # === Line Chart ===
    st.markdown("<div class='section-title'>Recycling Rate Over Time</div>", unsafe_allow_html=True)
    line_fig = go.Figure()
    trendx = [str(d.date()) for d in results["recycling_rate_trend"].index]
    line_fig.add_trace(go.Scatter(x=trendx, y=results["recycling_rate_trend"].values,
                                  fill='tozeroy', line=dict(color="#3EF5FF", width=4)))
    line_fig.update_layout(
        yaxis_title="Recycling Rate (%)",
        margin=dict(l=20, r=20, t=10, b=25),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#E8FEFB",
        height=230)
    st.plotly_chart(line_fig, use_container_width=True)

    # === Pie Chart ===
    st.markdown("<div class='section-title'>Recycled vs Primary Material Share</div>", unsafe_allow_html=True)
    pie_fig = go.Figure(go.Pie(
        labels=["Recycled Route", "Primary Route"],
        values=results["pie_share"],
        hole=0.6,
        marker=dict(colors=["#3EF5FF", "#004F55"]),
        textinfo='percent+label'))
    pie_fig.update_layout(margin=dict(l=10, r=10, t=10, b=10),
                          height=220, paper_bgcolor="rgba(0,0,0,0)", font_color="#E8FEFB")
    st.plotly_chart(pie_fig, use_container_width=True)

    # === Extended Circularity Metrics ===
    st.markdown("<div class='section-title'>Extended Circularity Metrics</div>", unsafe_allow_html=True)
    cardcols = st.columns(4)
    for i, (label, value) in enumerate(results["extended_circularity"]):
        cardcols[i % 4].markdown(
            f"<div class='glass-card'><b>{label}</b><br><span style='font-size:1.25rem;color:#3EF5FF;font-weight:700'>{value}</span></div>",
            unsafe_allow_html=True
        )

    # === Hotspots Table ===
    st.markdown("<div class='section-title'>Sustainability Hotspots – Top 3 Materials</div>", unsafe_allow_html=True)
    hotspot_table = pd.DataFrame(results["hotspots_materials"], columns=["Material", "Recycled Content (%)"])
    st.table(hotspot_table)

    # === Reuse Projects ===
    st.markdown("<div class='section-title'>Projects with Highest Reuse Potential</div>", unsafe_allow_html=True)
    for proj_name, material, pct in results["reuse_projects"]:
        st.markdown(
            f"<div class='glass-card' style='display:flex;justify-content:space-between;align-items:center;'>"
            f"<span><b>{proj_name}</b> ({material})</span>"
            f"<span class='leaderboard-badge'>{pct}%</span></div>", unsafe_allow_html=True
        )

    # === Key Impact Profiles ===
    st.markdown("<div class='section-title'>Key Impact Profiles</div>", unsafe_allow_html=True)
    df_impact = pd.DataFrame(results["key_impact_profiles"], columns=["Category", "Value"])
    bar = px.bar(df_impact, x="Category", y="Value", text="Value", template="simple_white",
                 color_discrete_sequence=["#3EF5FF", "#7CF4E3", "#59FFC2", "#00E0C6", "#83C5BE"])
    bar.update_traces(texttemplate='%{text:.2s}', marker_line_color='#00E0C6', marker_line_width=1.6)
    bar.update_layout(showlegend=False, yaxis_title=None, xaxis_title=None,
                      font_color="#E8FEFB", height=310,
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(bar, use_container_width=True)

    # === Summary Cards ===
    st.markdown("<div class='section-title'>Latest Report Analysis</div>", unsafe_allow_html=True)
    s = results['summary']
    cardcols2 = st.columns(4)
    cardcols2[0].markdown(f"<div class='glass-card'><b>Global Warming Potential</b><br><span style='font-size:1.45rem;color:#3EF5FF;font-weight:800'>{s['Global Warming Potential']['mean']} {s['Global Warming Potential']['unit']}</span></div>", unsafe_allow_html=True)
    cardcols2[1].markdown(f"<div class='glass-card'><b>Circularity Score</b><br><span style='font-size:1.45rem;color:#59FFC2;font-weight:800'>{s['Circularity Score']['mean']} %</span></div>", unsafe_allow_html=True)
    cardcols2[2].markdown(f"<div class='glass-card'><b>Particulate Matter</b><br><span style='font-size:1.2rem;color:#A9FFF7;font-weight:700'>{s['Particulate Matter']['mean']} {s['Particulate Matter']['unit']}</span></div>", unsafe_allow_html=True)
    cardcols2[3].markdown(f"<div class='glass-card'><b>Water Consumption</b><br><span style='font-size:1.2rem;color:#7CF4E3;font-weight:700'>{s['Water Consumption']['mean']} {s['Water Consumption']['unit']}</span></div>", unsafe_allow_html=True)
