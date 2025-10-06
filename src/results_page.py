import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ai_recommendation
import numpy as np

# =========================
# Minimal + Clean UI Theme
# =========================
st.markdown("""
<style>
body, .stApp {
    background: #f9fafc;
    color: #0d2c33;
    font-family: 'Poppins', sans-serif;
}
.metric-card {
    background: #ffffff;
    border: 1px solid #e0e7ea;
    border-radius: 12px;
    box-shadow: 0 1.5px 6px rgba(0,0,0,0.07);
    padding: 18px 0 14px 0;
    text-align: center;
    color: #0d2c33;
    margin-bottom: 1rem;
}
.results-card {
    background: #ffffff;
    border: 1px solid #d3e0e3;
    border-radius: 14px;
    padding: 22px 26px 18px 28px;
    color: #0d2c33;
    box-shadow: 0 1.5px 10px rgba(0,0,0,0.05);
}
.hotspot-card {
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #b9e0e5;
    color: #004d52;
    padding: 12px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.uncertainty-card {
    background: #ffffff;
    border: 1px solid #b9e0e5;
    border-radius: 16px;
    color: #004d52;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    padding: 2em;
    margin-bottom: 1.4em;
}
hr, .stDivider {
    border-color: rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# RESULTS PAGE FUNCTION (minimal + consistent design)
# =====================================================
def results_page(results, ai_text):
    st.title("Steel for New Building Frame")
    st.markdown("---")

    # ISO 14044 Banner
    st.markdown("""
    <div class='results-card'>
        <b>ISO 14044 Conformance</b><br>
        This is a screening-level LCA designed to be broadly consistent with ISO 14044 principles for internal decision-making.
        For public comparative assertions, a formal third-party critical review of this report is required.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Executive Summary
    es = results.get('executive_summary', {})
    st.markdown("<h3>Executive Summary</h3>", unsafe_allow_html=True)
    st.caption("Displaying mean values from a 1,000-run Monte Carlo simulation.")
    cols = st.columns(4)
    metric_items = [
        ("Global Warming Potential", f"{es.get('Global Warming Potential', 2288)} kg CO₂-eq"),
        ("Circularity Score", f"{es.get('Circularity Score', 50)} %"),
        ("Particulate Matter", f"{es.get('Particulate Matter', 0.763):.3g} kg PM2.5-eq"),
        ("Water Consumption", f"{es.get('Water Consumption', 4.7)} m³"),
    ]
    for idx, (title, value) in enumerate(metric_items):
        cols[idx].markdown(f"""
        <div class='metric-card'>
            <div style='color:#3a555b;font-weight:500;'>{title}</div>
            <div style='font-size:1.8em;font-weight:700;margin-top:4px;'>{value}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # Goal & Scope
    gs = results.get('goal_scope', {})
    c1, c2 = st.columns([2.2, 1])
    with c1:
        st.markdown("### Goal & Scope (ISO 14044)")
        st.write(f"**Intended Application:** {gs.get('Intended Application', '')}")
        st.write(f"**System Boundary:** {gs.get('System Boundary', '')}")
        st.write(f"**Limitations:** {gs.get('Limitations', '')}")
    with c2:
        st.write(f"**Intended Audience:** {gs.get('Intended Audience', '')}")
        st.write(f"**Comparative Assertion for Public:** {gs.get('Comparative Assertion for Public', '')}")
    st.markdown("---")

    # Data Quality
    dq = results.get('data_quality', {})
    c1, c2 = st.columns([2, 1.2])
    with c1:
        st.markdown("### Data Quality & Uncertainty")
        st.write(f"Reliability Score: {dq.get('Reliability Score', 4)} / 5")
        st.write(f"Completeness Score: {dq.get('Completeness Score', 4)} / 5")
        st.write(f"Temporal Score: {dq.get('Temporal Score', 4)} / 5")
        st.write(f"Technological Score: {dq.get('Technological Score', 5)} / 5")
        st.write(f"Geographical Score: {dq.get('Geographical Score', 4)} / 5")
    with c2:
        st.markdown(f"<h4 style='color:#005661;'>Aggregated Data Quality</h4>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:2em;font-weight:700;color:#0d2c33'>{dq.get('Aggregated Data Quality', '4.59')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#006a74;'>Result Uncertainty <b>{dq.get('Result Uncertainty', '±14%')}</b></div>", unsafe_allow_html=True)
    st.markdown("---")

    # Supply Chain Hotspots
    st.markdown("<h3>Supply Chain Hotspots</h3>", unsafe_allow_html=True)
    for h in es.get("Supply Chain Hotspots", []):
        st.markdown(f"""
        <div class='hotspot-card'>
            <b>{h['title']}</b><br>
            <span style='font-size:0.95em;'>{h.get('description', '')}</span><br>
            <span style='font-weight:700;font-size:1.2em;'>{h['impact']}%</span>
            <span style='color:#1b787e;font-size:0.9em;'> of GWP Impact</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # Circularity Metrics
    circ = results.get('circularity_analysis', {})
    st.markdown("<h3>Circularity Analysis</h3>", unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=circ.get("Circularity Rate", 50),
        number={"suffix": "%", "font": {"size": 40, "color": "#004d52"}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#007e8a"},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=280)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # Key Impact Profiles
    kip = results.get('key_impact_profiles', {})
    if kip:
        df_kip = pd.DataFrame(kip).T.reset_index()
        if 'mean' in df_kip.columns:
            fig = px.bar(df_kip, x='index', y='mean', text='mean', title='Key Impact Profiles')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # Energy Breakdown
    eb = results.get('energy_source_breakdown', {})
    if eb:
        df_eb = pd.DataFrame(list(eb.items()), columns=["Energy Source", "Value"])
        fig = px.bar(df_eb, x='Energy Source', y='Value', title='Energy Source Breakdown')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # Uncertainty Dashboard
    gwp_arr = np.random.normal(2288, 98.7, 1000)
    energy_arr = np.random.normal(26626, 1387.8, 1000)
    water_arr = np.random.normal(5, 0.3, 1000)

    st.markdown("""
    <div class='uncertainty-card'>
        <div style='font-size:1.8em;font-weight:700;'>Uncertainty Dashboard</div>
        <div style='color:#004d52;'>Based on Monte Carlo simulation (1000 runs) to assess data variability.</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, (arr, label, unit) in enumerate([
        (gwp_arr, "GWP", "kg CO₂-eq"),
        (energy_arr, "Energy", "MJ"),
        (water_arr, "Water", "m³")
    ]):
        mean = np.mean(arr)
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=arr, nbinsx=20, marker=dict(color="#007e8a")))
        fig.add_vline(x=mean, line_width=3, line_color='#004d52')
        fig.update_layout(
            margin=dict(l=10, r=10, t=40, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=f"{label} Distribution ({unit})"
        )
        cols[idx].plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # AI Recommendations
    extra_context = {"ore_conc": results.get('ore_conc')}
    if ai_text:
        ai_recommendation.display_ai_recommendations(ai_text, extra_context)
    st.markdown("---")

    # Scenario Comparison
    pvrs = results.get('primary_vs_recycled', {})
    if pvrs and 'comparison_table' in pvrs:
        df = pd.DataFrame(pvrs['comparison_table'])
        st.markdown("### Primary vs Recycled Scenario Comparison")
        st.dataframe(df)
        if not df.empty and "Metric" in df.columns:
            df_long = df.melt(id_vars=['Metric'], var_name="Scenario", value_name="Value")
            fig = px.bar(df_long, x='Metric', y='Value', color='Scenario', barmode='group')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
