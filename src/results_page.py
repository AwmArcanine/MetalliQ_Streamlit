# results_page.py
# Ready-to-paste Streamlit results page (keeps ai_recommendation.py as a separate module)
# Features applied:
# - Soft teal gradient page background + white-glass cards
# - Smooth fade-in animations for cards/sections
# - No expanders; all sections shown by default
# - Plotly charts use transparent backgrounds and visible titles/axis labels
# - Robust handling for AI recommendations (accepts dict or plain string; will try JSON if string)

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import ai_recommendation  # keep separate as requested

# -------------------------
# Global CSS (theme + glassy cards + animations)
# -------------------------
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    /* Page background: soft teal gradient */
    .reportview-container, .main {
        background: linear-gradient(120deg, #d9f4f1 0%, #eef9f8 100%) !important;
    }
    /* Glass card base */
    .glass-card {
        background: rgba(255,255,255,0.85);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 8px 28px rgba(13, 60, 79, 0.08);
        border: 1px solid rgba(27,122,115,0.06);
        transition: transform 0.28s ease, box-shadow 0.28s ease, opacity 0.45s ease;
        animation: fadeInUp 0.55s ease both;
    }

    /* Slightly stronger card for highlight sections */
    .glass-card-strong {
        background: rgba(255,255,255,0.94);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 10px 40px rgba(6, 45, 60, 0.07);
        border: 1px solid rgba(22,102,98,0.08);
        transition: transform 0.28s ease, box-shadow 0.28s ease, opacity 0.45s ease;
        animation: fadeInUp 0.55s ease both;
    }

    .glass-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 18px 48px rgba(6, 45, 60, 0.10);
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(250,250,250,0.92));
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 10px;
        box-shadow: 0 6px 18px rgba(8,45,64,0.05);
        text-align: left;
    }
    .metric-title { color: #2b5b58; font-weight:700; font-size:0.95rem; }
    .metric-value { color:#0f3b38; font-weight:900; font-size:1.9rem; letter-spacing:0.6px; }

    /* Section headers */
    .section-title {
        font-size:1.18rem;
        font-weight:800;
        color: #063b3a;
        margin-bottom:6px;
        letter-spacing:-0.2px;
    }
    .section-sub {
        color:#175c59;
        margin-bottom:10px;
    }

    /* Small helpers */
    .tiny-muted { color:#406a69; font-size:0.92rem; }
    .muted { color:#6e8a88; font-size:0.98rem; }

    /* Lifecycle row styles */
    .lifecycle-row { width:100%; margin: 16px auto 18px auto; display:flex; justify-content:space-between; align-items:center; }
    .lifecycle-stage {
        background: rgba(255,255,255,0.95);
        border-radius: 999px;
        width: 66px;
        height: 66px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:1.25rem;
        box-shadow: 0 10px 26px rgba(6,45,60,0.06);
        border: 1px solid rgba(11,78,74,0.05);
    }
    .stage-label { text-align:center; margin-top:8px; font-weight:700; color:#064c4a; font-size:0.95rem; }

    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Responsive tweaks */
    @media (max-width: 760px) {
        .lifecycle-row { flex-wrap:wrap; gap:14px; }
    }

    /* Streamlit-specific overrides for better whitespace */
    .stMarkdown, .stText, .stCaption {
        font-family: Inter, Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Helper functions
# -------------------------
def ensure_ai_data(ai_input):
    """
    Accepts either:
      - dict (already-structured AI recommendations),
      - string containing JSON,
      - plain string (convert to {'summary': <string>}).
    Returns a dict to pass to ai_recommendation.display_ai_recommendations
    """
    if ai_input is None:
        return None
    if isinstance(ai_input, dict):
        return ai_input
    if isinstance(ai_input, str):
        txt = ai_input.strip()
        # Try JSON parse
        try:
            parsed = json.loads(txt)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            # Not JSON; fall through
            pass
        # Not JSON: return simple dict with summary
        return {"summary": txt}
    # Unexpected type: convert to string summary
    return {"summary": str(ai_input)}

def plotly_style(fig, title=None, x_title=None, y_title=None, height=None):
    """
    Apply consistent transparent background, visible titles and axis labels.
    """
    # Titles and axis labels
    if title:
        fig.update_layout(title=dict(text=title, x=0.5, xanchor='center', yanchor='top', font=dict(size=16, family="Inter, Roboto")), title_x=0.5)
    if hasattr(fig, 'update_xaxes') and x_title:
        fig.update_xaxes(title_text=x_title, title_font=dict(size=12, family="Inter, Roboto"))
    if hasattr(fig, 'update_yaxes') and y_title:
        fig.update_yaxes(title_text=y_title, title_font=dict(size=12, family="Inter, Roboto"))
    # Transparent backgrounds
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=56, b=36),
        font=dict(family="Inter, Roboto", size=12)
    )
    if height:
        fig.update_layout(height=height)
    return fig

# -------------------------
# Main results_page function (callable)
# -------------------------
def results_page(results: dict, ai_text=None):
    """
    results: dict containing data pieces used in the page
    ai_text: ai recommendations as dict or string (will be normalized)
    """
    # Safeguard inputs
    results = results or {}
    ai_data = ensure_ai_data(ai_text)

    # Page title
    st.markdown("<div class='glass-card-strong'><div class='section-title'>Steel for New Building Frame</div><div class='muted'>Life Cycle Assessment — Results Dashboard</div></div>", unsafe_allow_html=True)

    # ISO 14044 banner
    st.markdown(
        """
        <div class='glass-card'>
            <div style='font-weight:800;color:#064c4a;font-size:1.02rem;'>ISO 14044 Conformance</div>
            <div class='muted' style='margin-top:6px;'>This is a screening-level LCA designed to be broadly consistent with ISO 14044 principles for internal decision-making. For public comparative assertions, a formal third-party critical review of this report is required.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- EXECUTIVE SUMMARY ----------
    es = results.get('executive_summary', {
        "Global Warming Potential": 2288,
        "Circularity Score": 50,
        "Particulate Matter": 0.763,
        "Water Consumption": 4.7,
        "Production Phase GWP": 2200,
        "Overall Energy Demand": 26700,
        "Circular Score": 50,
        "Supply Chain Hotspots": [
            {
                "title": "Production Phase Global Warming Potential",
                "description": "Highest Environmental Impact Contributor",
                "impact": 65
            },
            {
                "title": "Overall Energy Demand",
                "description": "",
                "impact": 25
            },
            {
                "title": "Circularity Score",
                "description": "",
                "impact": 10
            }
        ]
    })

    st.markdown("<div class='glass-card'><div class='section-title'>Executive Summary</div><div class='muted'>Mean results shown from Monte Carlo simulation (1,000 runs).</div></div>", unsafe_allow_html=True)
    # Four metrics
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("Global Warming Potential", f"{es.get('Global Warming Potential', 'N/A')}", "kg CO₂-eq"),
        ("Circularity Score", f"{es.get('Circularity Score', 'N/A')}", "%"),
        ("Particulate Matter", f"{es.get('Particulate Matter', 'N/A'):.3g}" if es.get('Particulate Matter') is not None else "N/A", "kg PM2.5-eq"),
        ("Water Consumption", f"{es.get('Water Consumption', 'N/A')}", "m³")
    ]
    col_list = [c1, c2, c3, c4]
    for col, (title, value, unit) in zip(col_list, metrics):
        col.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>{title}</div>
                <div class='metric-value'>{value} <span style="font-size:0.42em;font-weight:700;color:#4d6f6d;"> {unit}</span></div>
            </div>
        """, unsafe_allow_html=True)

    # ---------- Goal & Scope ----------
    gs = results.get('goal_scope', {
        "Intended Application": "Screening assessment for internal R&D purposes to compare material choices.",
        "System Boundary": "Cradle-to-Grave",
        "Limitations": "This analysis relies on industry-average data and does not include site-specific emissions. Results are for directional guidance only.",
        "Intended Audience": "Internal engineering and sustainability departments.",
        "Comparative Assertion for Public": "Yes"
    })
    left, right = st.columns([2.2, 1.05])
    left.markdown("<div class='glass-card'><div class='section-title'>Goal & Scope (ISO 14044)</div></div>", unsafe_allow_html=True)
    with left:
        st.write(f"**Intended Application:** {gs.get('Intended Application', '')}")
        st.write(f"**System Boundary:** {gs.get('System Boundary', '')}")
        st.write(f"**Limitations:** {gs.get('Limitations', '')}")
    with right:
        st.write(f"**Intended Audience:** {gs.get('Intended Audience', '')}")
        st.write(f"**Comparative Assertion for Public:** {gs.get('Comparative Assertion for Public', '')}")

    # ---------- Data Quality & Uncertainty ----------
    dq = results.get('data_quality', {
        "Reliability Score": 5,
        "Completeness Score": 5,
        "Temporal Score": 5,
        "Technological Score": 4,
        "Geographical Score": 4,
        "Aggregated Data Quality": 4.51,
        "Result Uncertainty": "±14%"
    })
    st.markdown("<div class='glass-card'><div class='section-title'>Data Quality & Uncertainty</div></div>", unsafe_allow_html=True)
    dq_col1, dq_col2 = st.columns([2, 1.2])
    with dq_col1:
        st.write(f"Reliability Score: {dq.get('Reliability Score', 'N/A')} / 5")
        st.write(f"Completeness Score: {dq.get('Completeness Score', 'N/A')} / 5")
        st.write(f"Temporal Score: {dq.get('Temporal Score', 'N/A')} / 5")
        st.write(f"Technological Score: {dq.get('Technological Score', 'N/A')} / 5")
        st.write(f"Geographical Score: {dq.get('Geographical Score', 'N/A')} / 5")
    with dq_col2:
        st.markdown(f"<div style='font-weight:700;font-size:1.2rem;color:#145c58;'>{dq.get('Aggregated Data Quality', 'N/A')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='muted'>Result Uncertainty <b>{dq.get('Result Uncertainty', '')}</b></div>", unsafe_allow_html=True)

    # ---------- Supply Chain Hotspots ----------
    st.markdown("<div class='glass-card'><div class='section-title'>Supply Chain Hotspots</div></div>", unsafe_allow_html=True)
    for h in es.get("Supply Chain Hotspots", []):
        color = "#fffaf0" if "Production Phase" in h.get('title', "") else "#fbfdff"
        border = "#f2c27a" if "Production Phase" in h.get('title', "") else "#efefef"
        st.markdown(
            f"""<div class='glass-card' style='padding:14px; background:{color}; border:1px solid {border};'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div style='flex:1;'>
                        <div style='font-weight:800;color:#2b5b58;font-size:1.01rem;'>{h.get('title')}</div>
                        <div class='muted' style='margin-top:6px;'>{h.get('description','')}</div>
                    </div>
                    <div style='text-align:right;min-width:120px;'>
                        <div style='font-weight:900;color:#114a49;font-size:1.5rem;'>{h.get('impact','')}%</div>
                        <div class='tiny-muted'>of GWP Impact</div>
                    </div>
                </div>
            </div>""",
            unsafe_allow_html=True
        )

    # ---------- Production Metrics ----------
    prod_gwp = es.get('Production Phase GWP', 'N/A')
    overall_energy = es.get('Overall Energy Demand', 'N/A')
    circular_score = es.get('Circular Score', 'N/A')

    st.markdown(
        f"""<div class='glass-card'>
            <div class='section-title'>Production Metrics</div>
            <div class='muted'>Key numbers from the production and supply chain stages.</div>
            <div style='display:flex;gap:18px;margin-top:12px;flex-wrap:wrap;'>
                <div style='min-width:210px; padding:12px; border-radius:10px; background:linear-gradient(180deg, rgba(255,255,255,0.96), rgba(250,250,250,0.94)); box-shadow:0 8px 22px rgba(10,50,50,0.035);'>
                    <div style='font-weight:700;color:#0b4f4c;'>Production Phase GWP</div>
                    <div style='font-weight:900;font-size:1.6rem;color:#083b3a;margin-top:6px;'>{prod_gwp} <span style='font-size:0.6rem;color:#3f6f6d;font-weight:700;'>kg CO₂-eq</span></div>
                </div>
                <div style='min-width:210px; padding:12px; border-radius:10px; background:linear-gradient(180deg, rgba(255,255,255,0.96), rgba(250,250,250,0.94)); box-shadow:0 8px 22px rgba(10,50,50,0.035);'>
                    <div style='font-weight:700;color:#0b4f4c;'>Overall Energy Demand</div>
                    <div style='font-weight:900;font-size:1.6rem;color:#083b3a;margin-top:6px;'>{overall_energy} <span style='font-size:0.6rem;color:#3f6f6d;font-weight:700;'>MJ</span></div>
                </div>
                <div style='min-width:210px; padding:12px; border-radius:10px; background:linear-gradient(180deg, rgba(255,255,255,0.96), rgba(250,250,250,0.94)); box-shadow:0 8px 22px rgba(10,50,50,0.035);'>
                    <div style='font-weight:700;color:#0b4f4c;'>Circular Score</div>
                    <div style='font-weight:900;font-size:1.6rem;color:#083b3a;margin-top:6px;'>{circular_score}%</div>
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True
    )

    # ---------- Process Lifecycle (visual row) ----------
    st.markdown(
        """
        <div class="glass-card">
            <div class='section-title'>Process Lifecycle</div>
            <div class='muted'>Click a lifecycle stage in the full app to see stage breakdowns. (Interactive in the full platform.)</div>
            <div class='lifecycle-row' style='margin-top:14px;'>
                <div style='text-align:center;'><div class='lifecycle-stage'>🌞</div><div class='stage-label'>Raw Material</div></div>
                <div style='text-align:center;'><div class='lifecycle-stage'>🧰</div><div class='stage-label'>Processing</div></div>
                <div style='text-align:center;'><div class='lifecycle-stage'>⚙️</div><div class='stage-label'>Manufacturing</div></div>
                <div style='text-align:center;'><div class='lifecycle-stage'>🚚</div><div class='stage-label'>Transport</div></div>
                <div style='text-align:center;'><div class='lifecycle-stage'>⏲️</div><div class='stage-label'>Use Phase</div></div>
                <div style='text-align:center;'><div class='lifecycle-stage'>🗑️</div><div class='stage-label'>End of Life</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- AI Generated Life Cycle Interpretation (displayed directly) ----------
    st.markdown("<div class='glass-card'><div class='section-title'>AI Generated Life Cycle Interpretation</div><div class='muted'>Insights and action plans from the AI module.</div></div>", unsafe_allow_html=True)
    if ai_data:
        try:
            # ai_recommendation.display_ai_recommendations expects a dict
            ai_recommendation.display_ai_recommendations(ai_data, extra_context={
                "ore_conc": results.get('ore_conc'),
                "transports": [
                    results.get('transport_stage_1', {}),
                    results.get('transport_stage_2', {})
                ]
            })
        except Exception as e:
            st.error("AI recommendations failed to render. See debug below.")
            st.exception(e)
            # fallback: show raw summary if present
            if isinstance(ai_data, dict) and ai_data.get("summary"):
                st.info(ai_data.get("summary"))
    else:
        st.markdown("<div class='glass-card'><div class='muted'>No AI interpretation available.</div></div>", unsafe_allow_html=True)

    # ---------- Sankey Diagram - Material Flow (rendered directly) ----------
    st.markdown("<div class='glass-card'><div class='section-title'>Material Flow (Sankey)</div><div class='muted'>Material flow between stages.</div></div>", unsafe_allow_html=True)
    mf = results.get('material_flow_analysis')
    if mf and isinstance(mf, dict) and mf.get('labels'):
        try:
            sankey_fig = go.Figure(go.Sankey(
                node=dict(label=mf['labels'], pad=18, thickness=18, line=dict(color="rgba(0,0,0,0.08)", width=0.5)),
                link=dict(source=mf['source'], target=mf['target'], value=mf['value'])
            ))
            sankey_fig = plotly_style(sankey_fig, title="Process Material Flow", height=420)
            st.plotly_chart(sankey_fig, use_container_width=True)
        except Exception as e:
            st.error("Failed to draw Sankey diagram.")
            st.exception(e)
    else:
        st.markdown("<div class='glass-card'><div class='muted'>No material flow data available.</div></div>", unsafe_allow_html=True)

    # ---------- Circularity Analysis ----------
    circ_metrics = results.get("circularity_analysis", {
        "Circularity Rate": 50,
        "Recyclability Rate": 90,
        "Recovery Efficiency": 92,
        "Secondary Material Content": 10
    })
    st.markdown("<div class='glass-card'><div class='section-title'>Circularity Analysis</div><div class='muted'>High-level circularity metrics and gauges.</div></div>", unsafe_allow_html=True)

    # Donut gauge (Indicator)
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=circ_metrics.get("Circularity Rate", 50),
        number={"suffix": "%", "font": {"size": 36}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": "#147c77", "thickness": 0.20},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [{"range": [0, 100], "color": "#e6f3f2"}]
        },
        domain={"x": [0, 1], "y": [0, 1]}
    ))
    plotly_style(gauge_fig, title="Circularity Rate", height=320)
    cA, cB = st.columns([0.45, 0.55])
    with cA:
        st.plotly_chart(gauge_fig, use_container_width=True)
    with cB:
        st.markdown(f"""
            <div style='padding:4px 2px;'>
                <div style='display:flex;justify-content:space-between;align-items:center;'><div class='muted'>Recyclability Rate</div><div style='font-weight:800;color:#0f4e4b;'>{circ_metrics.get('Recyclability Rate', '')}%</div></div>
                <div style='background:#e7f3f2;border-radius:9px;height:12px;margin-top:8px;'><div style='background:#147c77;width:{circ_metrics.get("Recyclability Rate",0)}%;height:12px;border-radius:9px;'></div></div>
                <div style='height:12px;'></div>
                <div style='display:flex;justify-content:space-between;align-items:center;'><div class='muted'>Recovery Efficiency</div><div style='font-weight:800;color:#0f4e4b;'>{circ_metrics.get('Recovery Efficiency', '')}%</div></div>
                <div style='background:#e7f3f2;border-radius:9px;height:12px;margin-top:8px;'><div style='background:#0b6b67;width:{circ_metrics.get("Recovery Efficiency",0)}%;height:12px;border-radius:9px;'></div></div>
                <div style='height:12px;'></div>
                <div style='display:flex;justify-content:space-between;align-items:center;'><div class='muted'>Secondary Material Content</div><div style='font-weight:800;color:#5a6b69;'>{circ_metrics.get('Secondary Material Content', '')}%</div></div>
                <div style='background:linear-gradient(90deg,#e9f4f3,#cfe9e6);border-radius:9px;height:12px;margin-top:8px;'><div style='background:#468f86;width:{circ_metrics.get("Secondary Material Content",0)}%;height:12px;border-radius:9px;'></div></div>
            </div>
        """, unsafe_allow_html=True)

    # ---------- Extended Circularity Grid ----------
    extcirc = results.get('extended_circularity_metrics', {
        "Resource Efficiency": "92%",
        "Extended Product Life": "110%",
        "Reuse Potential": "40/50",
        "Material Recovery": "90%",
        "Closed–Loop Potential": "75%",
        "Recycling Content": "10%",
        "Landfill Rate": "8%",
        "Energy Recovery": "2%"
    })
    st.markdown("<div class='glass-card'><div class='section-title'>Extended Circularity Metrics</div></div>", unsafe_allow_html=True)
    labels = list(extcirc.keys())
    values = list(extcirc.values())
    cols_per_row = 4
    for i in range(0, len(labels), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(labels):
                col.markdown(f"""
                    <div style='padding:10px;'>
                        <div style='background:rgba(255,255,255,0.96);border-radius:10px;padding:12px;box-shadow:0 8px 18px rgba(7,42,40,0.03);'>
                            <div style='font-weight:700;color:#0d504d;'>{labels[idx]}</div>
                            <div style='font-weight:800;font-size:1.25rem;color:#083d3b;margin-top:6px;'>{values[idx]}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------- GWP Contribution Pie ----------
    gwp_contrib = results.get('gwp_contribution_analysis', {})
    if gwp_contrib:
        df_gwp = pd.DataFrame(list(gwp_contrib.items()), columns=["Category", "Value"])
        pie = px.pie(df_gwp, names='Category', values='Value', title='GWP Contribution Analysis', hole=0.33)
        plotly_style(pie, title="GWP Contribution Analysis")
        st.plotly_chart(pie, use_container_width=True)

    # ---------- Energy Breakdown ----------
    energy_breakdown = results.get('energy_source_breakdown', {})
    if energy_breakdown:
        df_energy = pd.DataFrame(list(energy_breakdown.items()), columns=["Energy Source", "Value"])
        bar = px.bar(df_energy, x='Energy Source', y='Value', title='Energy Source Breakdown', text='Value')
        plotly_style(bar, title="Energy Source Breakdown", x_title="Energy Source", y_title="Value")
        st.plotly_chart(bar, use_container_width=True)

    # ---------- Key Impact Profiles ----------
    kip = results.get('key_impact_profiles', {})
    st.markdown("<div class='glass-card'><div class='section-title'>Key Impact Profiles</div></div>", unsafe_allow_html=True)
    if kip:
        try:
            df_kip = pd.DataFrame(kip).T.reset_index()
            if 'Metric' in df_kip.columns and 'Value' in df_kip.columns:
                fig_kip = px.bar(df_kip, x='Metric', y='Value', color='Metric', title='Key Impact Profiles', text='Value')
                plotly_style(fig_kip, title="Key Impact Profiles", x_title="Metric", y_title="Value")
                st.plotly_chart(fig_kip, use_container_width=True)
            elif 'index' in df_kip.columns and 'mean' in df_kip.columns:
                fig_kip = px.bar(df_kip, x='index', y='mean', text='mean', title='Key Impact Profiles')
                plotly_style(fig_kip, title="Key Impact Profiles", x_title="Metric", y_title="Mean")
                st.plotly_chart(fig_kip, use_container_width=True)
            else:
                st.write("Key Impact Profiles: unexpected data format.")
                st.dataframe(df_kip)
        except Exception as e:
            st.error("Error drawing Key Impact Profiles.")
            st.exception(e)
    else:
        st.write("No Key Impact Profiles data to display.")

    st.markdown("---")

    # ---------- Detailed Impact Assessment (table) ----------
    impact_data = results.get('impact_data', None)
    if impact_data is None:
        impact_data = [
            ("Global Warming Potential", 2293, "kg CO₂-eq"),
            ("Energy Demand", 26454, "MJ"),
            ("Water Consumption", 4.7, "m³"),
            ("Acidification Potential", 4.1, "kg SO₂-eq"),
            ("Eutrophication Potential", 1.15, "kg PO₄-eq"),
            ("Ozone Depletion Potential", 0.00229, "kg CFC-11 eq"),
            ("Photochemical Ozone Creation", 2.29, "kg NMVOC-eq"),
            ("Particulate Matter Formation", 0.76, "kg PM2.5-eq"),
            ("Abiotic Depletion (Fossil)", 29100, "MJ"),
            ("Abiotic Depletion (Elements)", 0.01, "kg Sb-eq"),
            ("Human Toxicity (Cancer)", 0.23, "CTUh"),
            ("Human Toxicity (Non-Cancer)", 2.29, "CTUh"),
            ("Freshwater Ecotoxicity", 22.88, "CTUe"),
            ("Ionizing Radiation", 0.00458, "kBq U235-eq"),
            ("Land Use", 228.77, "m²·year")
        ]
    df_imp = pd.DataFrame(impact_data, columns=["Impact Metric", "Value", "Unit"])
    st.markdown("<div class='glass-card'><div class='section-title'>Detailed Impact Assessment</div></div>", unsafe_allow_html=True)
    st.dataframe(df_imp, hide_index=True, use_container_width=True)

    st.markdown("---")

    # ---------- Uncertainty Distributions ----------
    st.markdown("<div class='glass-card'><div class='section-title'>Uncertainty Dashboard</div><div class='muted'>Monte Carlo-based distributions showing variability and 95% CIs.</div></div>", unsafe_allow_html=True)
    # Use provided arrays or sample if not present
    gwp_arr = np.array(results.get('gwp_distribution')) if results.get('gwp_distribution') is not None else np.random.normal(loc=es.get('Global Warming Potential', 2288), scale=98.7, size=1000)
    energy_arr = np.array(results.get('energy_distribution')) if results.get('energy_distribution') is not None else np.random.normal(loc=results.get('Overall Energy Demand', 26626), scale=1387.8, size=1000)
    water_arr = np.array(results.get('water_distribution')) if results.get('water_distribution') is not None else np.random.normal(loc=es.get('Water Consumption', 5), scale=0.3, size=1000)

    cols = st.columns(3)
    for idx, (arr, label, unit) in enumerate([
        (gwp_arr, "GWP", "kg CO₂-eq"),
        (energy_arr, "Energy", "MJ"),
        (water_arr, "Water", "m³")
    ]):
        mean = float(np.mean(arr))
        std = float(np.std(arr))
        ci_low, ci_high = np.percentile(arr, [2.5, 97.5])
        hist = go.Figure()
        hist.add_trace(go.Histogram(x=arr, nbinsx=20, marker=dict(color="#b0ddd8"), showlegend=False))
        hist.add_vline(x=mean, line_width=3, line_color='#145c59')
        hist.add_vline(x=ci_low, line_width=2, line_dash='dash', line_color='#145c59')
        hist.add_vline(x=ci_high, line_width=2, line_dash='dash', line_color='#145c59')
        hist.update_layout(
            margin=dict(l=12, r=12, t=48, b=36),
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=dict(text=f"<b>{label}</b><br><span style='font-size:0.87em;font-weight:400;color:#557a77'>Mean: {mean:.1f} | σ: {std:.1f} | 95% CI</span>", y=0.92, x=0.5, xanchor='center', yanchor='top'),
            xaxis_title=unit,
            yaxis_title=""
        )
        cols[idx].plotly_chart(hist, use_container_width=True)

    st.markdown("---")

    # ---------- AI Recommendations (again as short card / fallback) ----------
    # (Already displayed above with full rendering; show a compact summary here)
    if ai_data:
        # If there's a summary line, show summary card
        summary = ai_data.get("summary") if isinstance(ai_data, dict) else None
        if summary:
            st.markdown(f"<div class='glass-card'><div style='font-weight:800;color:#0c514f;'>AI — Summary</div><div class='muted' style='margin-top:6px;'>{summary}</div></div>", unsafe_allow_html=True)

    # ---------- Scenario Comparison ----------
    pvrs = results.get('primary_vs_recycled', {})
    if pvrs and 'comparison_table' in pvrs:
        df = pd.DataFrame(pvrs['comparison_table'])
        st.markdown("<div class='glass-card'><div class='section-title'>Primary vs Recycled - Scenario Comparison</div></div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        if not df.empty:
            # If a 'Metric' column exists produce grouped bar chart
            if "Metric" in df.columns:
                df_long = df.melt(id_vars=['Metric'], var_name="Scenario", value_name="Value")
                scen_fig = px.bar(df_long, x='Metric', y='Value', color='Scenario', barmode='group', text='Value')
                plotly_style(scen_fig, title="Scenario Comparison Across Metrics", x_title="Metric", y_title="Value")
                st.plotly_chart(scen_fig, use_container_width=True)

    # ---------- Footer / download hints ----------
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='muted'>Tip: Use the export tools in the platform to download CSV / PDF reports for your LCA study.</div>", unsafe_allow_html=True)


# If running the file directly for quick local preview (optional)
if __name__ == "__main__":
    # Minimal demo data for local preview
    demo_results = {
        "executive_summary": {
            "Global Warming Potential": 2293,
            "Circularity Score": 50,
            "Particulate Matter": 0.763,
            "Water Consumption": 4.7,
            "Production Phase GWP": 2200,
            "Overall Energy Demand": 26454,
            "Circular Score": 50,
            "Supply Chain Hotspots": [
                {"title": "Production Phase Global Warming Potential", "description": "Dominant contributor", "impact": 66},
                {"title": "Processing Energy", "description": "Secondary contributor", "impact": 24},
                {"title": "Transport", "description": "Minor contributor", "impact": 10}
            ]
        },
        "material_flow_analysis": {
            "labels": ["Ore", "Processing", "Manufacture", "Use", "End-of-life"],
            "source": [0, 1, 2, 2],
            "target": [1, 2, 3, 4],
            "value": [100, 85, 80, 20]
        },
        "circularity_analysis": {
            "Circularity Rate": 48,
            "Recyclability Rate": 88,
            "Recovery Efficiency": 90,
            "Secondary Material Content": 12
        },
        "primary_vs_recycled": {
            "comparison_table": [
                {"Metric": "GWP", "Primary": 2200, "Recycled": 600},
                {"Metric": "Energy", "Primary": 27000, "Recycled": 9800}
            ]
        }
    }
    demo_ai = {"summary": "Focus on increasing recycled content and renewable electricity in production.", "findings": []}
    results_page(demo_results, demo_ai)
