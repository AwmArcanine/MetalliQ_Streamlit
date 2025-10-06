import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import ai_recommendation  # separate glossy AI module

# ===========================
# GLOBAL PAGE CONFIG + STYLE
# ===========================
st.set_page_config(layout="wide")
st.markdown("""
<style>
/* Base gradient */
.reportview-container, .main {
    background: linear-gradient(120deg, #d9f4f1 0%, #eef9f8 100%) !important;
    color: #FFFFFF !important;
}

/* Neon Border Card (Transparent) */
.neon-card {
    border: 2px solid rgba(0,255,224,0.65);
    border-radius: 16px;
    padding: 22px 22px 18px 22px;
    margin-bottom: 22px;
    background: rgba(255,255,255,0.05);
    box-shadow: 0 0 14px rgba(0,255,224,0.25);
    backdrop-filter: blur(8px);
    animation: fadeInUp 0.6s ease both;
}

/* Glass metric cards (unchanged aesthetic) */
.metric-card {
    background: rgba(255,255,255,0.9);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
    text-align: left;
    box-shadow: 0 6px 18px rgba(8,45,64,0.08);
}
.metric-title { color:#024944; font-weight:700; font-size:0.95rem; }
.metric-value { color:#012c29; font-weight:900; font-size:1.9rem; }

/* Titles */
.section-title {
    font-size:1.25rem;
    font-weight:800;
    color:#00FFE0;
    text-shadow:0 0 10px rgba(0,255,224,0.6);
    letter-spacing:-0.3px;
}
.muted {
    color:#cde8e5;
    font-size:0.95rem;
}

/* Fade animation */
@keyframes fadeInUp {
    from { opacity:0; transform:translateY(8px); }
    to { opacity:1; transform:translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ===========================
# Helper Functions
# ===========================
def ensure_ai_data(ai_input):
    if ai_input is None:
        return None
    if isinstance(ai_input, dict):
        return ai_input
    if isinstance(ai_input, str):
        try:
            return json.loads(ai_input)
        except Exception:
            return {"summary": ai_input}
    return {"summary": str(ai_input)}

def plotly_style(fig, title=None, x_title=None, y_title=None, height=None):
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16, color="#053c38")),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#053c38"),
        margin=dict(l=20, r=20, t=50, b=30)
    )
    if x_title: fig.update_xaxes(title=x_title)
    if y_title: fig.update_yaxes(title=y_title)
    if height: fig.update_layout(height=height)
    return fig

# ===========================
# MAIN FUNCTION
# ===========================
def results_page(results: dict, ai_text=None):
    results = results or {}
    ai_data = ensure_ai_data(ai_text)

    # ================= TITLE =================
    st.markdown("<div class='neon-card'><h2 class='section-title'>Steel for New Building Frame</h2><p class='muted'>Life Cycle Assessment — Results Dashboard</p></div>", unsafe_allow_html=True)

    # ================= 1️⃣ EXECUTIVE SUMMARY =================
    with st.container():
        st.markdown("<div class='neon-card'><div class='section-title'>1️⃣ Executive Summary</div><div class='muted'>Monte Carlo mean results (1,000 runs).</div>", unsafe_allow_html=True)

        es = results.get('executive_summary', {})
        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            ("Global Warming Potential", f"{es.get('Global Warming Potential', 2293)}", "kg CO₂-eq"),
            ("Circularity Score", f"{es.get('Circularity Score', 50)}", "%"),
            ("Particulate Matter", f"{es.get('Particulate Matter', 0.763)}", "kg PM2.5-eq"),
            ("Water Consumption", f"{es.get('Water Consumption', 4.7)}", "m³"),
        ]
        for (col, (title, value, unit)) in zip([c1, c2, c3, c4], metrics):
            col.markdown(f"<div class='metric-card'><div class='metric-title'>{title}</div><div class='metric-value'>{value}<span style='font-size:0.5em;color:#2f615c;'> {unit}</span></div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ================= 2️⃣ GOAL & SCOPE =================
    gs = results.get('goal_scope', {})
    with st.container():
        st.markdown("<div class='neon-card'><div class='section-title'>2️⃣ Goal & Scope (ISO 14044)</div>", unsafe_allow_html=True)
        st.write(f"**Intended Application:** {gs.get('Intended Application', 'Screening assessment for internal R&D')}")
        st.write(f"**System Boundary:** {gs.get('System Boundary', 'Cradle-to-Grave')}")
        st.write(f"**Limitations:** {gs.get('Limitations', 'Uses industry-average data')}")
        st.write(f"**Audience:** {gs.get('Intended Audience', 'Sustainability Dept')}")
        st.markdown("</div>", unsafe_allow_html=True)

    # ================= 3️⃣ DATA QUALITY =================
    dq = results.get('data_quality', {})
    with st.container():
        st.markdown("<div class='neon-card'><div class='section-title'>3️⃣ Data Quality & Uncertainty</div>", unsafe_allow_html=True)
        st.write(f"Reliability: {dq.get('Reliability Score', 5)} / 5")
        st.write(f"Completeness: {dq.get('Completeness Score', 5)} / 5")
        st.write(f"Temporal: {dq.get('Temporal Score', 5)} / 5")
        st.write(f"Uncertainty: {dq.get('Result Uncertainty', '±14%')}")
        st.markdown("</div>", unsafe_allow_html=True)

    # ================= 4️⃣ SUPPLY CHAIN HOTSPOTS =================
    with st.container():
        st.markdown("<div class='neon-card'><div class='section-title'>4️⃣ Supply Chain Hotspots</div>", unsafe_allow_html=True)
        for h in results.get("executive_summary", {}).get("Supply Chain Hotspots", []):
            st.markdown(f"""
                <div style='border-left:4px solid #00FFE0;padding-left:12px;margin:8px 0;'>
                    <b>{h.get('title')}</b><br>
                    <span class='muted'>{h.get('description','')}</span>
                    <div style='color:#00FFE0;font-weight:700;margin-top:4px;'>{h.get('impact','')}% of GWP</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ================= 5️⃣ PRODUCTION METRICS =================
    with st.container():
        st.markdown("<div class='neon-card'><div class='section-title'>5️⃣ Production Metrics</div>", unsafe_allow_html=True)
        st.write(f"**Production Phase GWP:** {results.get('Production Phase GWP', 2200)} kg CO₂-eq")
        st.write(f"**Overall Energy Demand:** {results.get('Overall Energy Demand', 26454)} MJ")
        st.write(f"**Circular Score:** {results.get('Circular Score', 50)}%")
        st.markdown("</div>", unsafe_allow_html=True)

    # ================= 6️⃣ AI RECOMMENDATIONS =================
    with st.container():
        st.markdown("<div class='neon-card'><div class='section-title'>6️⃣ AI Generated Life Cycle Interpretation</div><div class='muted'>AI insights and recommendations</div></div>", unsafe_allow_html=True)
        ai_recommendation.display_ai_recommendations(
            ai_data or ai_recommendation.ai_data_example,
            extra_context={"ore_conc": results.get('ore_conc', 2.4)}
        )

    # ================= 7️⃣ MATERIAL FLOW =================
    mf = results.get('material_flow_analysis', {})
    if mf:
        with st.container():
            st.markdown("<div class='neon-card'><div class='section-title'>7️⃣ Material Flow (Sankey)</div></div>", unsafe_allow_html=True)
            sankey = go.Figure(go.Sankey(
                node=dict(label=mf['labels'], pad=15, thickness=15),
                link=dict(source=mf['source'], target=mf['target'], value=mf['value'])
            ))
            st.plotly_chart(plotly_style(sankey, "Process Material Flow", height=420), use_container_width=True)

    # ================= 8️⃣ CIRCULARITY =================
    with st.container():
        st.markdown("<div class='neon-card'><div class='section-title'>8️⃣ Circularity Analysis & Extended Metrics</div></div>", unsafe_allow_html=True)
        circ = results.get('circularity_analysis', {"Circularity Rate":48,"Recyclability Rate":88})
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=circ["Circularity Rate"], number={"suffix":"%"},
            gauge={"axis":{"range":[0,100]}, "bar":{"color":"#00FFE0"}}
        ))
        st.plotly_chart(plotly_style(gauge, "Circularity Rate"), use_container_width=True)

    # ================= 9️⃣ CHARTS =================
    with st.container():
        st.markdown("<div class='neon-card'><div class='section-title'>9️⃣ Key Charts — GWP & Energy Breakdown</div></div>", unsafe_allow_html=True)
        df = pd.DataFrame({"Category":["Production","Transport","Use"],"Value":[2293,600,150]})
        pie = px.pie(df, names="Category", values="Value", hole=0.4)
        st.plotly_chart(plotly_style(pie, "GWP Contribution Analysis"), use_container_width=True)

        energy = pd.DataFrame({"Energy Source":["Coal","Solar","Wind"],"Value":[18000,5000,3400]})
        bar = px.bar(energy, x="Energy Source", y="Value", text="Value")
        st.plotly_chart(plotly_style(bar, "Energy Breakdown", "Source", "MJ"), use_container_width=True)

    # ================= 🔟 DETAILED IMPACT TABLE =================
    with st.container():
        st.markdown("<div class='neon-card'><div class='section-title'>🔟 Detailed Impact Assessment</div></div>", unsafe_allow_html=True)
        impact_data = results.get('impact_data', [
            ("Global Warming Potential", 2293, "kg CO₂-eq"),
            ("Energy Demand", 26454, "MJ"),
            ("Water Consumption", 4.7, "m³"),
        ])
        st.dataframe(pd.DataFrame(impact_data, columns=["Impact Metric","Value","Unit"]),
                     hide_index=True, use_container_width=True)

    # ================= 11️⃣ UNCERTAINTY DASHBOARD =================
    with st.container():
        st.markdown("<div class='neon-card'><div class='section-title'>11️⃣ Uncertainty Dashboard</div><div class='muted'>Monte Carlo Distributions</div></div>", unsafe_allow_html=True)
        gwp_arr = np.random.normal(2293, 100, 1000)
        energy_arr = np.random.normal(26000, 1200, 1000)
        water_arr = np.random.normal(4.7, 0.2, 1000)
        for (arr, lbl, unit) in [(gwp_arr,"GWP","kg CO₂-eq"),(energy_arr,"Energy","MJ"),(water_arr,"Water","m³")]:
            fig = go.Figure(go.Histogram(x=arr, nbinsx=25, marker_color="#00FFE0"))
            fig.add_vline(x=np.mean(arr), line_color="#053c38", line_width=3)
            st.plotly_chart(plotly_style(fig, lbl, lbl, unit), use_container_width=True)

    # ================= 12️⃣ SCENARIO COMPARISON =================
    pvrs = results.get("primary_vs_recycled", {})
    if pvrs and "comparison_table" in pvrs:
        with st.container():
            st.markdown("<div class='neon-card'><div class='section-title'>12️⃣ Scenario Comparison — Primary vs Recycled</div></div>", unsafe_allow_html=True)
            df = pd.DataFrame(pvrs["comparison_table"])
            st.dataframe(df, use_container_width=True)
            df_long = df.melt(id_vars=['Metric'], var_name='Scenario', value_name='Value')
            fig = px.bar(df_long, x="Metric", y="Value", color="Scenario", barmode="group", text="Value")
            st.plotly_chart(plotly_style(fig, "Scenario Comparison"), use_container_width=True)

    st.markdown("<p style='color:#88c7c3;margin-top:18px;'>Tip: Export full PDF/CSV reports from the platform toolbar.</p>", unsafe_allow_html=True)

# ===========================
# LOCAL PREVIEW
# ===========================
if __name__ == "__main__":
    demo_results = {
        "executive_summary": {"Global Warming Potential": 2293, "Circularity Score": 50, "Particulate Matter": 0.763, "Water Consumption": 4.7,
                              "Supply Chain Hotspots": [{"title":"Production Phase GWP","description":"Dominant contributor","impact":65}]},
        "material_flow_analysis": {"labels":["Ore","Processing","Manufacture","Use","End-of-life"],"source":[0,1,2,2],"target":[1,2,3,4],"value":[100,85,80,20]},
        "circularity_analysis": {"Circularity Rate":48,"Recyclability Rate":88},
        "primary_vs_recycled": {"comparison_table":[{"Metric":"GWP","Primary":2200,"Recycled":600},{"Metric":"Energy","Primary":27000,"Recycled":9800}]}
    }
    results_page(demo_results, ai_recommendation.ai_data_example)
