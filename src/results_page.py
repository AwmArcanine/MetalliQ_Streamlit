# results_page.py
# Comprehensive, ready-to-paste Streamlit results page implementing the full Final LCA Report
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import ai_recommendation  # uses ai_data_example + display_ai_recommendations

# -------------------------
# Page config & inline CSS
# -------------------------
st.set_page_config(layout="wide")
st.markdown("""
<style>
/* page background */
.reportview-container, .main {
    background: linear-gradient(120deg, #e9fbf8 0%, #f8fefc 100%) !important;
    color: #013a36;
}

/* Neon bordered transparent card */
.neon-card {
    border: 2px solid rgba(0, 230, 200, 0.72);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 18px;
    background: rgba(255,255,255,0.02);
    box-shadow: 0 0 18px rgba(0,230,200,0.08), inset 0 0 8px rgba(0,230,200,0.02);
    backdrop-filter: blur(6px);
    animation: fadeInUp 0.48s ease both;
}
.neon-card:hover { transform: translateY(-3px); box-shadow: 0 0 30px rgba(0,230,200,0.14); }

/* Section title */
.section-title { font-size:1.18rem; font-weight:800; color:#00E6C8; margin-bottom:6px; letter-spacing:-0.3px; text-shadow:0 0 8px rgba(0,230,200,0.18); }
.muted { color:#3c7f77; }

/* Metric (white glass) */
.metric-card {
    background: rgba(255,255,255,0.94);
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 8px 24px rgba(6,45,45,0.04);
    margin-bottom: 8px;
}
.metric-title { color:#0b4f4c; font-weight:700; font-size:0.95rem; }
.metric-value { color:#083b3a; font-weight:900; font-size:1.6rem; }

/* AI glossy cards */
.ai-gloss { background: linear-gradient(180deg,#ffffff,#f3fffd); border-radius:12px; padding:12px 14px; margin-bottom:12px; box-shadow:0 10px 28px rgba(0,70,63,0.06); }
.ai-evidence { background:#f6fffc; padding:8px; border-radius:8px; margin-top:6px; color:#0b4f4c; }

/* AI priority badges */
.badge { padding:6px 10px; border-radius:999px; font-weight:800; font-size:0.88rem; }
.badge-high { background:#ffebee; color:#c62828; border:1px solid rgba(198,40,40,0.06); }
.badge-medium { background:#fff7e6; color:#e65100; border:1px solid rgba(230,81,0,0.06); }
.badge-low { background:#e8f6ef; color:#1b5e20; border:1px solid rgba(27,94,32,0.06); }

/* lifecycle icons */
.stage-icon { width:64px; height:64px; border-radius:99px; display:flex; align-items:center; justify-content:center; font-size:26px; background:rgba(255,255,255,0.96); box-shadow:0 8px 20px rgba(6,40,40,0.05); margin:auto; }
.stage-label { text-align:center; color:#0a5a54; font-weight:700; margin-top:8px; }

/* animations */
@keyframes fadeInUp { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0);} }

/* small helpers */
.small-muted { color:#5f8f88; font-size:0.95rem; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Helpers
# -------------------------
def ensure_ai_dict(ai_input):
    """Normalize AI input to dict."""
    if ai_input is None:
        return None
    if isinstance(ai_input, dict):
        return ai_input
    if isinstance(ai_input, str):
        try:
            parsed = json.loads(ai_input)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            return {"summary": ai_input}
    return {"summary": str(ai_input)}

def plotly_style(fig, title=None, x_title=None, y_title=None, height=None):
    if title:
        fig.update_layout(title=dict(text=title, x=0.5, xanchor='center', font=dict(size=14)))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=60, b=36),
        font=dict(family="Inter, Roboto", size=12, color="#053c38")
    )
    if x_title: fig.update_xaxes(title_text=x_title)
    if y_title: fig.update_yaxes(title_text=y_title)
    if height: fig.update_layout(height=height)
    return fig

# -------------------------
# Main page function
# -------------------------
def results_page(results: dict, ai_text=None):
    # Normalize inputs
    results = results or {}
    ai_data = ensure_ai_dict(ai_text) or ai_recommendation.ai_data_example

    # ----------------- 0) ISO 14044 banner -----------------
    st.markdown("<div class='neon-card'><div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;'><div><div class='section-title'>ISO 14044 Conformance</div><div class='muted'>Screening-level LCA prepared consistent with ISO 14044 principles. For public comparative assertions, a critical review is required.</div></div><div style='text-align:right; min-width:220px;'><div style='font-weight:800;color:#024c49;'>Report ID: AUTO-GEN-001</div><div class='small-muted'>Date: {}</div></div></div></div>".format(pd.Timestamp.now().strftime("%d %b %Y")), unsafe_allow_html=True)

    # ----------------- 1) Executive Summary -----------------
    es = results.get('executive_summary', {
        "Global Warming Potential": 2293,
        "Circularity Score": 50,
        "Particulate Matter": 0.763,
        "Water Consumption": 4.7,
        "Supply Chain Hotspots": [
            {"title":"Production Phase GWP","description":"Dominant contributor","impact":66},
            {"title":"Processing Energy","description":"Secondary contributor","impact":24},
            {"title":"Transport","description":"Minor contributor","impact":10}
        ]
    })

    st.markdown("<div class='neon-card'><div class='section-title'>Executive Summary</div><div class='small-muted'>Monte Carlo mean results (n=1,000)</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("Global Warming Potential", es.get('Global Warming Potential', "N/A"), "kg CO₂-eq"),
        ("Circularity Score", es.get('Circularity Score', "N/A"), "%"),
        ("Particulate Matter", es.get('Particulate Matter', "N/A"), "kg PM2.5-eq"),
        ("Water Consumption", es.get('Water Consumption', "N/A"), "m³")
    ]
    for col, (title, value, unit) in zip([c1, c2, c3, c4], metrics):
        col.markdown(f"<div class='metric-card'><div class='metric-title'>{title}</div><div class='metric-value'>{value} <span style='font-size:0.6rem;color:#2f615c;'> {unit}</span></div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- 2) Goal & Scope -----------------
    gs = results.get('goal_scope', {})
    st.markdown("<div class='neon-card'><div class='section-title'>Goal & Scope (ISO 14044)</div>", unsafe_allow_html=True)
    st.write(f"**Intended Application:** {gs.get('Intended Application', 'Screening assessment for internal R&D')}")
    st.write(f"**System Boundary:** {gs.get('System Boundary', 'Cradle-to-Grave')}")
    st.write(f"**Limitations:** {gs.get('Limitations', 'Analysis uses industry-average datasets; site-specific emissions not included.')}")
    st.write(f"**Intended Audience:** {gs.get('Intended Audience', 'Engineering & Sustainability')}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- 3) Data Quality & Uncertainty (Pedigree) -----------------
    dq = results.get('data_quality', {
        "Reliability Score": 5, "Completeness Score": 5, "Temporal Score": 5,
        "Technological Score": 4, "Geographical Score": 4, "Aggregated Data Quality": 4.51,
        "Result Uncertainty": "±14%"
    })
    st.markdown("<div class='neon-card'><div class='section-title'>Data Quality & Uncertainty</div>", unsafe_allow_html=True)
    colA, colB = st.columns([2, 1])
    with colA:
        st.write(f"Reliability Score: {dq.get('Reliability Score')} / 5")
        st.write(f"Completeness Score: {dq.get('Completeness Score')} / 5")
        st.write(f"Temporal Correlation: {dq.get('Temporal Score')} / 5")
        st.write(f"Technological Correlation: {dq.get('Technological Score')} / 5")
        st.write(f"Geographical Correlation: {dq.get('Geographical Score')} / 5")
    with colB:
        st.markdown(f"<div style='font-weight:800;color:#00E6C8;font-size:1.2rem;'>{dq.get('Aggregated Data Quality')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted'>Result Uncertainty: <b>{dq.get('Result Uncertainty')}</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- 4) Supply Chain Hotspots -----------------
    st.markdown("<div class='neon-card'><div class='section-title'>Supply Chain Hotspots</div>", unsafe_allow_html=True)
    for h in es.get("Supply Chain Hotspots", []):
        st.markdown(f"<div style='padding:8px 0;border-left:4px solid rgba(0,230,200,0.6);margin-bottom:8px;'><b style='color:#00E6C8;'>{h.get('title')}</b><div class='small-muted'>{h.get('description','')}</div><div style='margin-top:6px;font-weight:800;color:#00E6C8;'>{h.get('impact','')}% of GWP</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- 5) Production Metrics -----------------
    prod_gwp = results.get('Production Phase GWP', es.get('Production Phase GWP', 2200))
    overall_energy = results.get('Overall Energy Demand', es.get('Overall Energy Demand', 26700))
    circular_score = results.get('Circular Score', es.get('Circular Score', 50))
    st.markdown("<div class='neon-card'><div class='section-title'>Production Metrics</div><div class='small-muted'>Key production & supply-chain numbers</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='display:flex;gap:14px;flex-wrap:wrap;margin-top:12px;'>
            <div style='min-width:220px;' class='metric-card'><div class='metric-title'>Production Phase GWP</div><div class='metric-value'>{prod_gwp} <span style='font-size:0.6rem;color:#2f615c;'>kg CO₂-eq</span></div></div>
            <div style='min-width:220px;' class='metric-card'><div class='metric-title'>Overall Energy Demand</div><div class='metric-value'>{overall_energy} <span style='font-size:0.6rem;color:#2f615c;'>MJ</span></div></div>
            <div style='min-width:220px;' class='metric-card'><div class='metric-title'>Circular Score</div><div class='metric-value'>{circular_score}<span style='font-size:0.6rem;color:#2f615c;'>%</span></div></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- 6) Interactive Process Lifecycle -----------------
    STAGES = [("Metal Ore Extraction","⛏️"),("Processing","🏭"),("Manufacturing","⚙️"),("Transportation","🚚"),("Use Phase","🔋"),("End of Lifecycle","🗑️")]
    stage_metrics_default = {
        "Metal Ore Extraction": {"GWP": 700, "Energy": 5000, "Water": 1.2},
        "Processing": {"GWP": 900, "Energy": 8000, "Water": 2.0},
        "Manufacturing": {"GWP": 350, "Energy": 6000, "Water": 0.8},
        "Transportation": {"GWP": 150, "Energy": 2000, "Water": 0.2},
        "Use Phase": {"GWP": 50, "Energy": 2000, "Water": 0.3},
        "End of Lifecycle": {"GWP": 43, "Energy": 1500, "Water": 0.1}
    }
    stage_metrics = results.get('stage_metrics', stage_metrics_default)
    st.markdown("<div class='neon-card'><div class='section-title'>Interactive Process Lifecycle</div><div class='small-muted'>Click a stage to view stage-specific metrics and insights</div>", unsafe_allow_html=True)

    cols = st.columns(len(STAGES))
    if "selected_stage" not in st.session_state:
        st.session_state.selected_stage = STAGES[0][0]
    # render icons + buttons
    for i, (name, emoji) in enumerate(STAGES):
        with cols[i]:
            st.markdown(f"<div class='stage-icon'>{emoji}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stage-label'>{name}</div>", unsafe_allow_html=True)
            if st.button(f"View {name}", key=f"stage_{i}"):
                st.session_state.selected_stage = name

    # show selected stage metrics
    sel = st.session_state.selected_stage
    sel_metrics = stage_metrics.get(sel, {"GWP":0,"Energy":0,"Water":0})
    st.markdown(f"<div style='margin-top:12px;'><b>Selected Stage:</b> <span style='color:#00E6C8;font-weight:800;'>{sel}</span></div>", unsafe_allow_html=True)
    df_stage = pd.DataFrame([{"Metric":"GWP","Value":sel_metrics.get("GWP",0)},
                             {"Metric":"Energy","Value":sel_metrics.get("Energy",0)},
                             {"Metric":"Water","Value":sel_metrics.get("Water",0)}])
    fig_stage = px.bar(df_stage, x="Metric", y="Value", text="Value", title=f"{sel} - Stage Breakdown")
    plotly_style(fig_stage, title=f"{sel} - Stage Breakdown", x_title="Metric", y_title="Value", height=360)
    st.plotly_chart(fig_stage, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- 7) AI Generated Life Cycle Interpretation (stage-by-stage) -----------------
    # Build lifecycle-specific AI findings (using ai_recommendation.ai_data_example as base)
    base_ai = ai_recommendation.ai_data_example if ai_data is None else ai_data
    ore_conc = results.get('ore_conc', None)
    lifecycle_findings = []
    for stage_name, _ in STAGES:
        if stage_name in ["Processing","Manufacturing","Metal Ore Extraction"]:
            priority = "High Priority"
            effort = "High Effort" if stage_name == "Manufacturing" else "Medium Effort"
        elif stage_name in ["Transportation","Use Phase"]:
            priority = "Medium Priority"
            effort = "Medium Effort"
        else:
            priority = "Low Priority"
            effort = "Low Effort"
        evidence = f"Estimated GWP: {stage_metrics.get(stage_name,{}).get('GWP','N/A')} kg CO₂-eq."
        if ore_conc is not None and stage_name == "Metal Ore Extraction":
            evidence += f" Ore grade: {ore_conc}%."
        action_plan = [
            {"title": f"Optimize {stage_name} energy", "desc": f"Implement targeted energy-efficiency measures in {stage_name.lower()}.", "impact": "Lowers GWP and energy demand", "effort": effort, "confidence": 80}
        ]
        if stage_name == "Processing":
            action_plan.append({"title":"Switch to renewable electricity","desc":"Procurement of renewable energy for process loads","impact":"Reduces Scope 2 emissions","effort":"High Effort","confidence":75})
        lifecycle_findings.append({
            "title": f"{stage_name} - Key Findings",
            "priority": priority,
            "evidence": evidence,
            "root_cause": f"Primary drivers at {stage_name} identified (energy intensity / feedstock quality).",
            "action_plan": action_plan
        })

    ai_lifecycle_payload = {"summary": base_ai.get("summary","AI suggests targeted interventions across lifecycle."), "findings": lifecycle_findings}
    st.markdown("<div class='neon-card'><div class='section-title'>AI Generated Life Cycle Interpretation</div><div class='small-muted'>Stage-level insights and action plans (mock AI)</div></div>", unsafe_allow_html=True)

    # Render summary
    if ai_lifecycle_payload.get("summary"):
        st.markdown(f"<div class='ai-gloss'><div style='font-weight:800;color:#013a36;'>AI Summary</div><div style='margin-top:6px;'>{ai_lifecycle_payload['summary']}</div></div>", unsafe_allow_html=True)

    # Render each stage finding as a glossy AI card
    for f in ai_lifecycle_payload.get("findings", []):
        p = f.get("priority","").lower()
        badge_class = "badge-high" if "high" in p else ("badge-low" if "low" in p else "badge-medium")
        # action plan html
        ap_html = ""
        for plan in f.get("action_plan", []):
            effort = plan.get("effort","")
            eff_cls = "badge-high" if "High" in effort else ("badge-medium" if "Medium" in effort else "badge-low")
            ap_html += f"<div style='margin-top:8px;padding:10px;border-radius:8px;background:#fff;'><b>{plan['title']}</b><div style='margin-top:6px;color:#234f4b;'>{plan['desc']}</div><div style='margin-top:6px;color:#466b64;font-size:0.9rem;'><i>{plan['impact']}</i><span style='float:right;font-weight:700;'>Confidence: {plan.get('confidence',0)}%</span></div><div style='margin-top:8px;'><span class='badge {eff_cls}' style='padding:6px 10px;'>{effort}</span></div></div>"
        st.markdown(f"""
            <div class='ai-gloss' style='border-left:6px solid {"#d32f2f" if "high" in p else ("#f57c00" if "medium" in p else "#43a047")};'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div style='font-weight:800;color:#013a36;'>{f.get('title')}</div>
                    <div><span class='badge {badge_class}'>{f.get('priority')}</span></div>
                </div>
                <div style='margin-top:8px;'><b>Evidence:</b></div>
                <div class='ai-evidence'>{f.get('evidence')}</div>
                <div style='margin-top:8px;'><b>Root Cause:</b> {f.get('root_cause')}</div>
                <div style='margin-top:8px;'><b>Action Plan:</b>{ap_html}</div>
            </div>
        """, unsafe_allow_html=True)

    # ----------------- 8) Circularity Analysis + Extended Metrics -----------------
    circ = results.get('circularity_analysis', {"Circularity Rate": 48, "Recyclability Rate": 88, "Recovery Efficiency": 90, "Secondary Material Content": 12})
    st.markdown("<div class='neon-card'><div class='section-title'>Circularity Analysis</div><div class='small-muted'>Key circularity metrics and progress indicators</div>", unsafe_allow_html=True)
    # Circularity gauge
    gauge = go.Figure(go.Indicator(mode="gauge+number", value=circ.get("Circularity Rate",50), number={"suffix":"%"}, gauge={"axis":{"range":[0,100]},"bar":{"color":"#00E6C8"}}))
    plotly_style(gauge, title="Circularity Rate", height=300)
    ca, cb = st.columns([0.45, 0.55])
    with ca:
        st.plotly_chart(gauge, use_container_width=True)
    with cb:
        st.markdown(f"<div style='font-weight:800;color:#00E6C8;'>Recyclability Rate: {circ.get('Recyclability Rate')}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='height:8px;'></div><div style='background:#f0fffb;border-radius:8px;height:10px;'><div style='background:#00a68a;width:{circ.get('Recyclability Rate',0)}%;height:10px;border-radius:8px;'></div></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='height:12px;'></div><div style='font-weight:800;color:#00E6C8;'>Recovery Efficiency: {circ.get('Recovery Efficiency')}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='height:8px;'></div><div style='background:#f0fffb;border-radius:8px;height:10px;'><div style='background:#018f80;width:{circ.get('Recovery Efficiency',0)}%;height:10px;border-radius:8px;'></div></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='height:12px;'></div><div style='font-weight:800;color:#00E6C8;'>Secondary Material Content: {circ.get('Secondary Material Content')}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='height:8px;'></div><div style='background:linear-gradient(90deg,#e9f4f3,#cfe9e6);border-radius:8px;height:10px;'><div style='background:#00a68a;width:{circ.get('Secondary Material Content',0)}%;height:10px;border-radius:8px;'></div></div>", unsafe_allow_html=True)
    # Extended circularity metrics table/cards
    ext = results.get('extended_circularity_metrics', {
        "Resource Efficiency":"92%","Extended Product Life":"110%","Reuse Potential":"40/50",
        "Material Recovery":"90%","Closed–Loop Potential":"75%","Recycling Content":"10%",
        "Landfill Rate":"8%","Energy Recovery":"2%"
    })
    st.markdown("<div style='height:10px;'></div><div style='display:flex;gap:10px;flex-wrap:wrap;'>", unsafe_allow_html=True)
    for k, v in ext.items():
        st.markdown(f"<div style='min-width:220px;background:rgba(255,255,255,0.95);padding:10px;border-radius:10px;box-shadow:0 8px 18px rgba(6,40,40,0.03);margin-bottom:8px;'><div style='font-weight:700;color:#0b4f4c;'>{k}</div><div style='font-weight:800;font-size:1.1rem;color:#083b3a;margin-top:6px;'>{v}</div></div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ----------------- 9) Material Flow (Sankey) -----------------
    mf = results.get('material_flow_analysis', results.get('material_flow', None))
    st.markdown("<div class='neon-card'><div class='section-title'>Material Flow Analysis (Sankey)</div><div class='small-muted'>Material mass and flow between stages</div></div>", unsafe_allow_html=True)
    if mf and isinstance(mf, dict) and mf.get('labels'):
        try:
            sankey_fig = go.Figure(go.Sankey(node=dict(label=mf['labels'], pad=15, thickness=15, line=dict(color="rgba(0,0,0,0.06)", width=0.5)), link=dict(source=mf['source'], target=mf['target'], value=mf['value'])))
            plotly_style(sankey_fig, title="Material Flow", height=420)
            st.plotly_chart(sankey_fig, use_container_width=True)
        except Exception as e:
            st.error("Failed to draw Sankey diagram.")
            st.exception(e)
    else:
        st.markdown("<div class='small-muted'>No material flow data available.</div>", unsafe_allow_html=True)

    # ----------------- 10) Key Impact Profiles (GWP, Energy, Water, Eutrophication, Acidification) -----------------
    kip = results.get('key_impact_profiles', {
        "GWP": 2293, "Energy": 26454, "Water": 4.7, "Eutrophication": 1.15, "Acidification": 4.1
    })
    st.markdown("<div class='neon-card'><div class='section-title'>Key Impact Profiles</div><div class='small-muted'>High-level impact metrics</div></div>", unsafe_allow_html=True)
    df_kip = pd.DataFrame(list(kip.items()), columns=["Metric","Value"])
    # bar chart
    fig_kip = px.bar(df_kip, x="Metric", y="Value", text="Value", title="Key Impact Profiles")
    plotly_style(fig_kip, title="Key Impact Profiles", x_title="Metric", y_title="Value")
    st.plotly_chart(fig_kip, use_container_width=True)

    # ----------------- 11) GWP Contribution Analysis (pie) -----------------
    st.markdown("<div class='neon-card'><div class='section-title'>GWP Contribution Analysis</div></div>", unsafe_allow_html=True)
    gwp_contrib = results.get('gwp_contribution_analysis', {"Production":60,"Processing":30,"Transport":10})
    df_gwp = pd.DataFrame(list(gwp_contrib.items()), columns=["Category","Value"])
    pie = px.pie(df_gwp, names='Category', values='Value', hole=0.33, title="GWP Contribution")
    plotly_style(pie, title="GWP Contribution Analysis")
    st.plotly_chart(pie, use_container_width=True)

    # ----------------- 12) Energy Source Breakdown -----------------
    st.markdown("<div class='neon-card'><div class='section-title'>Energy Source Breakdown</div></div>", unsafe_allow_html=True)
    energy = results.get('energy_source_breakdown', {"Coal":18000,"Grid":5000,"Renewables":3400})
    df_energy = pd.DataFrame(list(energy.items()), columns=["Energy Source","Value"])
    bar_energy = px.bar(df_energy, x="Energy Source", y="Value", text="Value", title="Energy Source Breakdown")
    plotly_style(bar_energy, title="Energy Source Breakdown", x_title="Energy Source", y_title="Value")
    st.plotly_chart(bar_energy, use_container_width=True)

    # ----------------- 13) Detailed Impact Assessment (chart + table) -----------------
    st.markdown("<div class='neon-card'><div class='section-title'>Detailed Impact Assessment</div><div class='small-muted'>Chart view & Table view of impact metrics</div></div>", unsafe_allow_html=True)
    impact_data = results.get('impact_data', [
        ("Global Warming Potential", 2293, "kg CO₂-eq"),
        ("Acidification Potential", 4.1, "kg SO₂-eq"),
        ("Photochemical Ozone Creation", 2.29, "kg NMVOC-eq"),
        ("Abiotic Depletion (Fossil)", 29100, "MJ"),
        ("Fresh Water Ecotoxicity", 22.88, "CTUe"),
        ("Energy Demand", 26454, "MJ"),
        ("Eutrophication Potential", 1.15, "kg PO₄-eq"),
        ("Particulate Matter Formation", 0.76, "kg PM2.5-eq"),
        ("Human Toxicity (Cancer)", 0.23, "CTUh"),
        ("Ionizing Radiation", 0.00458, "kBq U235-eq"),
        ("Water Consumption", 4.7, "m³"),
        ("Ozone Depletion Potential", 0.00229, "kg CFC-11 eq"),
        ("Abiotic Depletion (Elements)", 0.01, "kg Sb-eq"),
        ("Human Toxicity (Non-Cancer)", 2.29, "CTUh"),
        ("Land Use", 228.77, "m²·year")
    ])
    df_imp = pd.DataFrame(impact_data, columns=["Impact Metric","Value","Unit"])
    # Chart: select top N for visualization (avoid clutter)
    df_chart = df_imp.head(8).copy()
    fig_imp = px.bar(df_chart, x="Impact Metric", y="Value", text="Value", title="Selected Impact Metrics")
    plotly_style(fig_imp, title="Impact Metrics (selection)", x_title="Impact Metric", y_title="Value")
    st.plotly_chart(fig_imp, use_container_width=True)
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.dataframe(df_imp, hide_index=True, use_container_width=True)

    # ----------------- 14) Uncertainty Dashboard -----------------
    st.markdown("<div class='neon-card'><div class='section-title'>Uncertainty Dashboard</div><div class='small-muted'>Monte Carlo distributions and 95% confidence intervals</div></div>", unsafe_allow_html=True)
    gwp_arr = np.array(results.get('gwp_distribution')) if results.get('gwp_distribution') is not None else np.random.normal(loc=es.get('Global Warming Potential',2293), scale=98.7, size=1000)
    energy_arr = np.array(results.get('energy_distribution')) if results.get('energy_distribution') is not None else np.random.normal(loc=results.get('Overall Energy Demand',26454), scale=1387.8, size=1000)
    water_arr = np.array(results.get('water_distribution')) if results.get('water_distribution') is not None else np.random.normal(loc=es.get('Water Consumption',4.7), scale=0.3, size=1000)
    cols_u = st.columns(3)
    for idx, (arr, label, unit) in enumerate([(gwp_arr,"GWP","kg CO₂-eq"),(energy_arr,"Energy","MJ"),(water_arr,"Water","m³")]):
        mean = float(np.mean(arr)); std = float(np.std(arr)); ci_low, ci_high = np.percentile(arr,[2.5,97.5])
        hist = go.Figure()
        hist.add_trace(go.Histogram(x=arr, nbinsx=25, marker=dict(color="#00E6C8"), showlegend=False))
        hist.add_vline(x=mean, line_width=3, line_color='#013a36')
        hist.add_vline(x=ci_low, line_width=2, line_dash='dash', line_color='#013a36')
        hist.add_vline(x=ci_high, line_width=2, line_dash='dash', line_color='#013a36')
        hist.update_layout(margin=dict(l=12,r=12,t=48,b=36), height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        hist.update_layout(title=dict(text=f"<b>{label}</b><br><span style='font-size:0.9em;color:#2f6a66'>Mean: {mean:.1f} | σ: {std:.1f} | 95% CI</span>", y=0.92, x=0.5))
        cols_u[idx].plotly_chart(hist, use_container_width=True)

    # ----------------- 15) AI-Powered Insights & Recommendations (NLP-like) -----------------
    st.markdown("<div class='neon-card'><div class='section-title'>AI-Powered Insights & Recommendations</div><div class='small-muted'>NLP-based analysis identifying hotspots and suggested actions</div></div>", unsafe_allow_html=True)
    # Use the ai_recommendation.display_ai_recommendations function to render the detailed AI panel (it already formats summary, findings, evidence, root cause, action plan)
    try:
        ai_recommendation.display_ai_recommendations(ai_data, extra_context={
            "ore_conc": results.get("ore_conc"),
            "transports": results.get("transports", []),
            "selected_stage": st.session_state.get("selected_stage")
        })
    except Exception as e:
        st.error("AI rendering failed: " + str(e))
        if isinstance(ai_data, dict) and ai_data.get("summary"):
            st.info(ai_data.get("summary"))

    # Additionally include ore-grade warning and EV charging recommendations as explicit cards
    ore_conc = results.get("ore_conc")
    if ore_conc is not None:
        if ore_conc < 45:
            st.warning(f"⚠️ Low ore grade detected: {ore_conc}%. Low-grade ore increases energy use and waste. Consider higher-grade blending, alternative sourcing, or beneficiation improvements.")
        else:
            st.success(f"Ore grade: {ore_conc}% — within expected range for this analysis.")

    # EV charging suggestions (if any transport entries indicate EV or user flag)
    transports = results.get("transports", [])
    ev_flag = any((t.get("mode","").lower() in ["ev","electric","electric vehicle"] or t.get("fuel","").lower() == "electric") for t in transports)
    if ev_flag:
        st.markdown("<div style='background:linear-gradient(90deg,#f0fffb,#e8fff7);padding:10px;border-radius:10px;margin-bottom:8px;'><b>EV Charging Recommendations</b><ul style='margin-top:6px;'><li>Prefer on-site solar + battery for EV chargers to offset grid carbon.</li><li>Use smart charging and schedule charging during renewables-rich hours.</li><li>Implement demand-response to reduce peak loads and costs.</li></ul></div>", unsafe_allow_html=True)

    # ----------------- 16) Primary vs Recycled Scenario Comparison -----------------
    pvrs = results.get('primary_vs_recycled', {})
    if pvrs and 'comparison_table' in pvrs:
        st.markdown("<div class='neon-card'><div class='section-title'>Primary vs Recycled - Scenario Comparison</div><div class='small-muted'>Detailed comparison table + chart</div></div>", unsafe_allow_html=True)
        df_comp = pd.DataFrame(pvrs['comparison_table'])
        st.dataframe(df_comp, use_container_width=True)
        if "Metric" in df_comp.columns:
            df_long = df_comp.melt(id_vars=['Metric'], var_name='Scenario', value_name='Value')
            fig_comp = px.bar(df_long, x='Metric', y='Value', color='Scenario', barmode='group', text='Value', title="Primary vs Recycled Comparison")
            plotly_style(fig_comp, title="Primary vs Recycled Comparison", x_title="Metric", y_title="Value")
            st.plotly_chart(fig_comp, use_container_width=True)

    # ----------------- Footer tip -----------------
    st.markdown("<div style='height:10px;'></div><div class='small-muted'>Tip: Use platform export tools to download CSV / PDF versions of this report.</div>", unsafe_allow_html=True)


# -------------------------
# Local preview (if run directly)
# -------------------------
if __name__ == "__main__":
    demo_results = {
        "executive_summary": {
            "Global Warming Potential": 2293,
            "Circularity Score": 50,
            "Particulate Matter": 0.763,
            "Water Consumption": 4.7,
            "Supply Chain Hotspots": [
                {"title":"Production Phase GWP","description":"Dominant contributor","impact":66},
                {"title":"Processing Energy","description":"Secondary contributor","impact":24},
                {"title":"Transport","description":"Minor contributor","impact":10}
            ]
        },
        "Production Phase GWP": 2200,
        "Overall Energy Demand": 26454,
        "Circular Score": 50,
        "stage_metrics": {
            "Metal Ore Extraction": {"GWP":700,"Energy":5000,"Water":1.2},
            "Processing": {"GWP":900,"Energy":8000,"Water":2.0},
            "Manufacturing": {"GWP":350,"Energy":6000,"Water":0.8},
            "Transportation": {"GWP":150,"Energy":2000,"Water":0.2},
            "Use Phase": {"GWP":50,"Energy":2000,"Water":0.3},
            "End of Lifecycle": {"GWP":43,"Energy":1500,"Water":0.1}
        },
        "ore_conc": 52,
        "material_flow_analysis": {"labels":["Ore","Processing","Manufacture","Use","EoL"], "source":[0,1,2,2], "target":[1,2,3,4], "value":[100,85,80,20]},
        "circularity_analysis": {"Circularity Rate":48,"Recyclability Rate":88,"Recovery Efficiency":90,"Secondary Material Content":12},
        "extended_circularity_metrics": {"Resource Efficiency":"92%","Extended Product Life":"110%","Reuse Potential":"40/50","Material Recovery":"90%","Closed–Loop Potential":"75%","Recycling Content":"10%","Landfill Rate":"8%","Energy Recovery":"2%"},
        "gwp_contribution_analysis": {"Production":60,"Processing":30,"Transport":10},
        "energy_source_breakdown": {"Coal":18000,"Grid":5000,"Renewables":3400},
        "impact_data": [
            ("Global Warming Potential",2293,"kg CO₂-eq"),
            ("Acidification Potential",4.1,"kg SO₂-eq"),
            ("Photochemical Ozone Creation",2.29,"kg NMVOC-eq"),
            ("Abiotic Depletion (Fossil)",29100,"MJ"),
            ("Fresh Water Ecotoxicity",22.88,"CTUe"),
            ("Energy Demand",26454,"MJ"),
            ("Eutrophication Potential",1.15,"kg PO₄-eq"),
            ("Particulate Matter Formation",0.76,"kg PM2.5-eq"),
            ("Human Toxicity (Cancer)",0.23,"CTUh"),
            ("Ionizing Radiation",0.00458,"kBq U235-eq"),
            ("Water Consumption",4.7,"m³"),
            ("Ozone Depletion Potential",0.00229,"kg CFC-11 eq"),
            ("Abiotic Depletion (Elements)",0.01,"kg Sb-eq"),
            ("Human Toxicity (Non-Cancer)",2.29,"CTUh"),
            ("Land Use",228.77,"m²·year")
        ],
        "primary_vs_recycled": {"comparison_table":[{"Metric":"GWP","Primary":2200,"Recycled":600},{"Metric":"Energy","Primary":27000,"Recycled":9800}]},
        "transports": [{"mode":"Truck","fuel":"Diesel","distance_km":75},{"mode":"Truck","fuel":"Electric","distance_km":120}]
    }
    results_page(demo_results, ai_recommendation.ai_data_example)
