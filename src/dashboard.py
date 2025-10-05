import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# === MetalliQ custom theme styles ===
st.markdown("""
<style>
body {
    background: #f8f9fb !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#132c43 11%,#15447a 100%) !important;
}
.metriccard {
    background: #f5f8fd;
    border-radius: 22px;
    box-shadow: 0 6px 20px #1366b326;
    border: 1.5px solid #e3ebf6;
    padding: 18px 24px 10px 24px;
    margin-bottom: 16px;
    min-height: 100px;
    text-align: center;
    font-family: 'Inter', 'Segoe UI', 'Poppins', sans-serif;
}
.metricheader {
    font-size: 1.15rem;
    color: #15447a;
    margin-bottom: 7px;
}
.metricvalue {
    font-size: 2.1rem;
    font-weight: 900;
    color:#174679;
    letter-spacing: -1px;
}
.leaderboard-badge {
    background: #174679;
    color: #fff;
    border-radius: 15px;
    font-weight: 700;
    font-size: 1.12rem;
    padding: 4px 17px;
    margin-left: 13px;
    letter-spacing: .02em;
}
.bigcard {
    background: linear-gradient(91deg, #1b3662 40%, #1889dd 100%);
    color: #fff;
    border-radius: 22px;
    box-shadow: 0 8px 35px #1b366246;
    font-size: 1.25rem;
    margin-bottom: 18px;
    padding: 30px 22px 25px 28px;
    font-family: 'Inter', 'Segoe UI', 'Poppins', sans-serif;
}
.card-outline {
    border: 1.5px solid #c9d6e5;
    box-shadow: 0 2px 11px #b3d1f51a;
    border-radius: 20px;
    background: #f8fafd;
    padding: 19px 16px;
}
</style>
""", unsafe_allow_html=True)

def dashboard_page(workspace=None):
    col1, col2 = st.columns([8, 2])
    with col2:
        st.markdown("""
        <style>
        .css-1lsmgbg [data-testid="baseButton-primary"] {
            background: linear-gradient(90deg,#1c9ae5 60%,#1689c4 100%) !important;
            border-radius: 9px !important;
            font-size: 1.14rem;
            font-weight: 800;
            box-shadow: 0 2px 10px #048be219;
            margin-top: .33rem;
            margin-bottom: .4rem;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("+ New Study", key="dashboard_new_study", use_container_width=True):
            st.session_state["page"] = "Create Study"
            st.rerun()
    results = st.session_state.get('simulation_results')

    # ----------- MOCK DATA -------------
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
                'Global Warming Potential': {'mean': 2293, 'unit': 'kg CO2-eq', 'ci': [2100, 2480]},
                'Circularity Score': {'mean': 50, 'unit': '%', 'ci': [45, 60]},
                'Particulate Matter': {'mean': 0.76, 'unit': 'kg PM2.5-eq','ci': [0.7, 0.83]},
                'Water Consumption': {'mean': 4.7, 'unit': 'm³', 'ci': [4.2, 5.17]}
            }
        }

    st.title("John's Workspace Dashboard")
    st.markdown("<small style='color:#15447a;'>An overview of your workspace's sustainability metrics.</small>", unsafe_allow_html=True)

    # ===== Card metrics block at the top =====
    col1, col2, col3 = st.columns([3, 3, 3])
    col1.markdown(
        f'<div class="metriccard"><div class="metricheader">Average Recycling Rate</div><div class="metricvalue">{results["metrics"]["avg_recycling_rate"]} %</div></div>', unsafe_allow_html=True)
    col2.markdown(
        f'<div class="metriccard"><div class="metricheader">Total Recycled Material</div><div class="metricvalue">{results["metrics"]["total_recycled_material"]} tonnes</div></div>', unsafe_allow_html=True)
    col3.markdown(
        f'<div class="metriccard"><div class="metricheader">Average Circularity Score</div><div class="metricvalue">{results["metrics"]["avg_circularity_score"]} / 100</div></div>', unsafe_allow_html=True)

    # === Recycling Rate Over Time Chart ===
    with st.container():
        st.markdown("##### Recycling Rate Over Time")
        line_fig = go.Figure()
        trendx = [str(d.date()) for d in results["recycling_rate_trend"].index]
        line_fig.add_trace(go.Scatter(
            x=trendx, y=results["recycling_rate_trend"].values,
            fill='tozeroy', line=dict(color="#1366b3", width=4)))
        line_fig.update_layout(
            xaxis_title=None, yaxis_title="Recycling Rate (%)",
            margin=dict(l=20, r=20, t=10, b=25),
            plot_bgcolor="#f8f9fb",
            paper_bgcolor="#f8f9fb00",
            font=dict(family="Inter,Segoe UI,Poppins,sans-serif", color="#15447a"),
            height=230)
        st.plotly_chart(line_fig, use_container_width=True)

    # === Pie/Donut - Recycled vs Primary ===
    with st.container():
        st.markdown("##### Recycled vs Primary Material Share")
        pie_fig = go.Figure(
            go.Pie(
                labels=["Recycled Route", "Primary Route"],
                values=results["pie_share"],
                hole=0.6,
                marker=dict(colors=["#174679", "#e3ebf6"]),
                textinfo='percent+label'
            )
        )
        pie_fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=220,
            plot_bgcolor="#f8f9fb",
            paper_bgcolor="#f8f9fb00",
            font=dict(family="Inter,Segoe UI,Poppins,sans-serif", color="#15447a")
        )
        st.plotly_chart(pie_fig, use_container_width=True)

    # === Extended Circularity Metrics cards (grid) ===
    st.markdown("""<div style='margin:12px 0 8px 0;font-size:1.18rem;font-weight:600;color:#00796b;'>Extended Circularity Metrics</div>""", unsafe_allow_html=True)
    cardcols = st.columns(4)
    for i, (label, value) in enumerate(results["extended_circularity"]):
        cardcols[i % 4].markdown(
            f"<div style='background:#e4effa;padding:13px 6px;border-radius:18px;text-align:center;margin-bottom:12px;border:1px solid #1366b322;'><b>{label}</b><br>"
            f"<span style='font-size:1.34rem;color:#15447a;font-weight:700'>{value}</span></div>",
            unsafe_allow_html=True
        )

    # === Sustainability Hotspots Table ===
    st.markdown("#### Sustainability Hotspots – Top 3 Materials by Recycled Content")
    hotspot_table = pd.DataFrame(results["hotspots_materials"],
                                 columns=["Material", "Recycled Content (%)"])
    st.table(hotspot_table)

    # === Project Leaderboard for Reuse Potential ===
    st.markdown("#### Projects with Highest Reuse Potential")
    for proj_name, material, pct in results["reuse_projects"]:
        st.markdown(
            f"<div style='background:#f5f6fa;padding:10px 13px;border-radius:14px;margin-bottom:7px;display:flex;justify-content:space-between;align-items:center;'>"
            f"<span><b>{proj_name}</b> ({material})</span>"
            f"<span class='leaderboard-badge'>{pct}%</span></div>",
            unsafe_allow_html=True
        )

    # === General Overview stats cards ===
    colT1, colT2 = st.columns([2, 2])
    colT1.metric("Total Reports", results['metrics']['total_reports'])
    colT2.metric("Total GWP (sum)", f"{results['metrics']['total_gwp_sum']} kg CO2-eq")

    # === Key Impact Profiles Bar chart ===
    st.markdown("#### Key Impact Profiles")
    df_impact = pd.DataFrame(results["key_impact_profiles"], columns=["Category", "Value"])
    bar = px.bar(df_impact, x="Category", y="Value", color="Category", text="Value", template="simple_white",
                 color_discrete_sequence=["#1366b3", "#174679", "#0ca678", "#217a4b", "#e65100"])
    bar.update_traces(texttemplate='%{text:.2s}', marker_line_color='#1366b3', marker_line_width=1.7)
    bar.update_layout(
        showlegend=False,
        yaxis_title=None,
        xaxis_title=None,
        font=dict(family="Inter,Segoe UI,Poppins,sans-serif", color="#15447a"),
        height=310,
        margin=dict(l=32, r=15, t=12, b=8),
        plot_bgcolor="#e8eefa",
        paper_bgcolor="#ffffff00"
    )
    st.plotly_chart(bar, use_container_width=True)

    # === Latest Report Analysis Cards ===
    st.markdown("#### Latest Report Analysis")
    s = results['summary']
    cardcols2 = st.columns(4)
    cardcols2[0].markdown(f"<div class='card-outline' style='margin-top:9px;text-align:center;font-size:1.16rem;'><b>Global Warming Potential</b><br><span style='font-size:1.5rem;color:#e65100;font-weight:800'>{s['Global Warming Potential']['mean']}<small>{s['Global Warming Potential']['unit']}</small></span></div>", unsafe_allow_html=True)
    cardcols2[1].markdown(f"<div class='card-outline' style='margin-top:9px;text-align:center;font-size:1.16rem;'><b>Circularity Score</b><br><span style='font-size:1.45rem;color:#217a4b;font-weight:800'>{s['Circularity Score']['mean']}<small>%</small></span></div>", unsafe_allow_html=True)
    cardcols2[2].markdown(f"<div class='card-outline' style='margin-top:9px;text-align:center;font-size:1.16rem;'><b>Particulate Matter</b><br><span style='font-size:1.18rem;color:#345;font-weight:700'>{s['Particulate Matter']['mean']} {s['Particulate Matter']['unit']}</span></div>", unsafe_allow_html=True)
    cardcols2[3].markdown(f"<div class='card-outline' style='margin-top:9px;text-align:center;font-size:1.12rem;'><b>Water Consumption</b><br><span style='font-size:1.18rem;color:#4e1180;font-weight:700'>{s['Water Consumption']['mean']} {s['Water Consumption']['unit']}</span></div>", unsafe_allow_html=True)

