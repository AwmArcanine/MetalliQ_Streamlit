# results_page.py
# Final ready-to-paste module for MetalliQ LCA Results
# Features:
# - Neon/glossy card layout for each required section
# - Interactive lifecycle stage selection (buttons)
# - AI lifecycle interpretation integrated (uses ai_recommendation.display_ai_recommendations)
# - Sankey material flow, gauge, histograms, many Plotly charts (transparent backgrounds)
# - Primary vs Recycled comparison table + grouped chart
# - All sections present and shown by default (no expanders)
# - Defensive handling of missing input data (uses reasonable mock defaults)
# - No st.set_page_config() here (avoid conflicts with app.py)
# - Ready for integration with your app.py import results_page.results_page

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import ai_recommendation  # external module (must exist in project)

# -------------------------
# SAFE NOTE:
# Don't call st.set_page_config here to avoid reconfiguration when module is imported.
# -------------------------

# -------------------------
# Inline CSS: neon + glossy styles for this page only
# -------------------------
st.markdown(
    """
    <style>
    /* Page background subtle teal gradient (keeps global theme compatibility) */
    .reportview-container .main, .main {
        background: linear-gradient(120deg, #033231 0%, #0B5B58 40%, #1EAFA0 100%) !important;
    }

    /* Neon container */
    .neon-card {
        border-radius: 14px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,255,240,0.14);
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 12px 36px rgba(0,0,0,0.28), 0 0 20px rgba(0,255,240,0.03) inset;
        backdrop-filter: blur(4px);
    }

    /* Glossy sub-metrics */
    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        border: 1px solid rgba(255,255,255,0.04);
        box-shadow: 0 6px 18px rgba(3,40,39,0.35);
    }
    .metric-title { color:#CFF6F0; font-weight:700; font-size:0.95rem; }
    .metric-value { color:#E7FFFB; font-weight:900; font-size:1.6rem; }

    /* Section headings */
    .section-title { font-size:1.35rem; font-weight:900; color:#BFFDF5; margin-bottom:6px; }
    .section-sub { color:#DFFAF5; margin-bottom:12px; }

    /* Lifecycle stage buttons */
    .lifecycle-stage {
      width:78px; height:78px; border-radius:50%; display:flex; align-items:center; justify-content:center;
      margin:6px; border:2px solid rgba(0,255,240,0.12); color:#E9FFFB; font-size:1.6rem;
      background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      box-shadow: 0 6px 20px rgba(0,0,0,0.35);
    }
    .stage-label { color:#DFFAF5; font-weight:700; margin-top:6px; text-align:center; font-size:0.95rem; }

    /* AI card */
    .ai-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        border-radius: 12px;
        padding: 14px;
        margin-top: 10px;
        border: 1px solid rgba(0,255,240,0.06);
        box-shadow: 0 10px 30px rgba(0,0,0,0.28);
    }

    /* small helpers */
    .muted { color:#D6FFFB; opacity:0.95; }
    .tiny-muted { color:#CFF6F0; font-size:0.92rem; }

    /* make plotly toolbar icons visible */
    .modebar { filter: drop-shadow(0 1px 2px rgba(0,0,0,0.3)); }

    @media (max-width: 760px) {
        .lifecycle-stage { width:66px; height:66px; font-size:1.2rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Helper functions
# -------------------------
def plotly_style(fig, title=None, x_title=None, y_title=None, height=None):
    """Apply consistent styling to Plotly figures for this page."""
    if title:
        fig.update_layout(title=dict(text=title, x=0.5, font=dict(size=16, color="#E6FFFB"), xanchor='center'))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E6FFFB', family="Inter, Roboto"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=24, r=24, t=60, b=36)
    )
    if x_title:
        fig.update_xaxes(title_text=x_title, title_font=dict(color="#CFF6F0"))
    if y_title:
        fig.update_yaxes(title_text=y_title, title_font=dict(color="#CFF6F0"))
    if height:
        fig.update_layout(height=height)
    return fig

def render_metric_card(title, value, unit=""):
    """Render a single glossy metric card (HTML)."""
    display_val = value if value is not None else "N/A"
    unit_html = f" <span style='font-size:0.55em;color:#BFFDF5;font-weight:700;'>{unit}</span>" if unit else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{display_val}{unit_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def ensure_ai_data(ai_input):
    """Normalize ai_input into a dict for ai_recommendation.display_ai_recommendations."""
    if ai_input is None:
        return getattr(ai_recommendation, "ai_data_example", {"summary": "No AI data available."})
    if isinstance(ai_input, dict):
        return ai_input
    if isinstance(ai_input, str):
        txt = ai_input.strip()
        try:
            parsed = json.loads(txt)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass
        return {"summary": txt}
    # fallback
    return {"summary": str(ai_input)}

# -------------------------
# Interactive lifecycle setup
# -------------------------
LIFECYCLE_STAGES = [
    {"key": "ore", "label": "Metal Ore Extraction", "emoji": "⛏️"},
    {"key": "processing", "label": "Processing", "emoji": "🧰"},
    {"key": "manufacturing", "label": "Manufacturing", "emoji": "⚙️"},
    {"key": "transport", "label": "Transportation", "emoji": "🚚"},
    {"key": "use", "label": "Use Phase", "emoji": "🏗️"},
    {"key": "end", "label": "End of Life", "emoji": "♻️"},
]

if "results_lifecycle_selected" not in st.session_state:
    st.session_state["results_lifecycle_selected"] = "ore"

def select_lifecycle_stage(stage_key):
    st.session_state["results_lifecycle_selected"] = stage_key

# -------------------------
# Main page: results_page
# -------------------------
def results_page(results: dict = None, ai_text=None):
    """
    Render the full results page.
    - results: dict with expected keys for each section (safely handled)
    - ai_text: ai recommendations (dict or string). Will be normalized.
    """
    results = results or {}
    ai_data = ensure_ai_data(ai_text)

    # top title and caption
    st.markdown("<div style='margin-bottom:10px;'><h1 style='color:#E6FFFB;'>MetalliQ - Final LCA Report</h1></div>", unsafe_allow_html=True)
    st.caption("ISO 14044 aligned LCA output — interactive, with AI-powered lifecycle interpretation and scenario comparison.")

    # -------------------------
    # 1️⃣ ISO 14044 compliance
    # -------------------------
    st.markdown(
        """
        <div class="neon-card">
            <div class="section-title">ISO 14044 Compliance</div>
            <div class="section-sub">This screening-level assessment follows ISO 14044 principles for internal decision-making. Public comparative assertions require third-party critical review.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------
    # 2️⃣ Executive Summary (metrics cards)
    # -------------------------
    executive = results.get("executive_summary", {
        "Global Warming Potential": 2293,
        "Circularity Score": 50,
        "Particulate Matter": 0.763,
        "Water Consumption": 4.7
    })
    st.markdown("<div class='neon-card'><div class='section-title'>Executive Summary</div><div class='section-sub'>Averages from Monte Carlo simulation (if provided).</div></div>", unsafe_allow_html=True)
    # render 4 metrics
    e_cols = st.columns(4)
    metric_list = [
        ("Global Warming Potential", executive.get("Global Warming Potential", "N/A"), "kg CO₂-eq"),
        ("Circularity Score", executive.get("Circularity Score", "N/A"), "%"),
        ("Particulate Matter", executive.get("Particulate Matter", "N/A"), "kg PM2.5-eq"),
        ("Water Consumption", executive.get("Water Consumption", "N/A"), "m³"),
    ]
    for col, (t, v, u) in zip(e_cols, metric_list):
        with col:
            render_metric_card(t, v, u)

    # -------------------------
    # 3️⃣ Goal & Scope
    # -------------------------
    gs = results.get("goal_scope", {
        "Intended Application": "Screening assessment for internal R&D purposes to compare material choices.",
        "System Boundary": "Cradle-to-Grave",
        "Limitations": "Industry-average data used, site-specific emissions excluded.",
        "Intended Audience": "Internal engineering and sustainability departments",
        "Comparative Assertion for Public": "No"
    })
    st.markdown("<div class='neon-card'><div class='section-title'>Goal & Scope (ISO 14044)</div></div>", unsafe_allow_html=True)
    left_col, right_col = st.columns([2.2, 1.0])
    with left_col:
        st.write(f"**Intended Application:** {gs.get('Intended Application')}")
        st.write(f"**System Boundary:** {gs.get('System Boundary')}")
        st.write(f"**Study Limitations:** {gs.get('Limitations')}")
    with right_col:
        st.write(f"**Intended Audience:** {gs.get('Intended Audience')}")
        st.write(f"**Comparative Assertion (Public):** {gs.get('Comparative Assertion for Public')}")

    # -------------------------
    # 4️⃣ Data Quality & Uncertainty (pedigree)
    # -------------------------
    dq = results.get("data_quality", {
        "Reliability": 4,
        "Completeness": 4,
        "Temporal": 4,
        "Technological": 4,
        "Geographical": 4,
        "Aggregate Data Quality": 4.2,
        "Result Uncertainty": "±12%"
    })
    st.markdown("<div class='neon-card'><div class='section-title'>Data Quality & Uncertainty</div><div class='section-sub'>Pedigree matrix style scores and aggregated uncertainty.</div></div>", unsafe_allow_html=True)
    dq_cols = st.columns(6)
    dq_items = [("Reliability", dq.get("Reliability")), ("Completeness", dq.get("Completeness")),
                ("Temporal", dq.get("Temporal")), ("Technological", dq.get("Technological")),
                ("Geographical", dq.get("Geographical")), ("Aggregate Quality", dq.get("Aggregate Data Quality"))]
    for c, (name, val) in zip(dq_cols, dq_items):
        with c:
            render_metric_card(name, f"{val} / 5" if val is not None else "N/A")

    # show uncertainty
    st.markdown(f"<div class='neon-card'><div class='tiny-muted'>Result Uncertainty: <b>{dq.get('Result Uncertainty','N/A')}</b></div></div>", unsafe_allow_html=True)

    # -------------------------
    # 5️⃣ Supply Chain Hotspots
    # -------------------------
    st.markdown("<div class='neon-card'><div class='section-title'>Supply Chain Hotspots</div><div class='section-sub'>Top contributors identified by impact share.</div></div>", unsafe_allow_html=True)
    hotspots = results.get("supply_chain_hotspots", [
        {"title": "Production Phase GWP", "description": "Highest contributor (material extraction & primary production)", "impact": 66},
        {"title": "Overall Energy Demand", "description": "High energy intensity in smelting and refining", "impact": 24},
        {"title": "Transport", "description": "Freight/distance-related emissions", "impact": 10},
    ])
    for h in hotspots:
        color_block = "#fffaf0" if "Production" in h.get("title","") else "#f7fffe"
        border_color = "#f2c27a" if "Production" in h.get("title","") else "#dfeff0"
        st.markdown(
            f"""
            <div class="metric-card" style="padding:12px;background:{color_block};border:1px solid {border_color};">
                <div style="font-weight:800;color:#E6FFF9;">{h.get('title')}</div>
                <div style="margin-top:6px;color:#D9FFF8;">{h.get('description','')}</div>
                <div style="margin-top:8px;font-weight:900;color:#CFFDF4;font-size:1.2rem;">{h.get('impact','')}% <span style="font-size:0.8rem;color:#BFFDF0;">of GWP</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------
    # 6️⃣ Production Metrics
    # -------------------------
    production = results.get("production_metrics", {
        "Production Phase GWP": executive.get("Production Phase GWP", results.get("production_phase_gwp", 2200)),
        "Overall Energy Demand": executive.get("Overall Energy Demand", results.get("overall_energy", 26454)),
        "Circular Score": executive.get("Circularity Score", 50)
    })
    st.markdown("<div class='neon-card'><div class='section-title'>Production Metrics</div><div class='section-sub'>Key numbers from production & supply chain stages.</div></div>", unsafe_allow_html=True)
    prod_cols = st.columns(3)
    with prod_cols[0]:
        render_metric_card("Production Phase GWP", production.get("Production Phase GWP", "N/A"), "kg CO₂-eq")
    with prod_cols[1]:
        render_metric_card("Overall Energy Demand", production.get("Overall Energy Demand", "N/A"), "MJ")
    with prod_cols[2]:
        render_metric_card("Circular Score", production.get("Circular Score", "N/A"), "%")

    # -------------------------
    # 7️⃣ Interactive Process Lifecycle
    # -------------------------
    st.markdown("<div class='neon-card'><div class='section-title'>Interactive Process Lifecycle</div><div class='section-sub'>Click a lifecycle stage below to view stage-specific metrics and AI interpretation.</div></div>", unsafe_allow_html=True)

    # Render lifecycle icons / buttons horizontally
    cols = st.columns(len(LIFECYCLE_STAGES))
    for col, stage in zip(cols, LIFECYCLE_STAGES):
        with col:
            # Use st.button — OK since not inside a st.form
            clicked = st.button(stage["emoji"], key=f"lifecycle_btn_{stage['key']}")
            st.markdown(f"<div class='stage-label'>{stage['label']}</div>", unsafe_allow_html=True)
            if clicked:
                select_lifecycle_stage(stage["key"])

    selected_key = st.session_state.get("results_lifecycle_selected", "ore")
    st.markdown(f"<div class='neon-card'><div class='section-title'>Lifecycle Stage — {selected_key.capitalize()}</div></div>", unsafe_allow_html=True)

    # stage-specific metrics (safe defaults)
    default_stage_metrics = {
        "ore": {"GWP": 500, "Energy": 6000, "Water": 0.7, "notes": "Ore extraction & beneficiation"},
        "processing": {"GWP": 700, "Energy": 8000, "Water": 1.1, "notes": "Crushing, milling, concentration"},
        "manufacturing": {"GWP": 1200, "Energy": 15000, "Water": 2.3, "notes": "Smelting, refining, rolling"},
        "transport": {"GWP": 150, "Energy": 1200, "Water": 0.2, "notes": "Freight between facilities"},
        "use": {"GWP": 80, "Energy": 900, "Water": 1.0, "notes": "Product use-phase impacts"},
        "end": {"GWP": 40, "Energy": 400, "Water": 0.4, "notes": "End-of-life processing & recovery"}
    }
    stage_metrics = results.get("stage_metrics", default_stage_metrics)
    s_metrics = stage_metrics.get(selected_key, default_stage_metrics.get(selected_key, {}))

    # Show sub-metric cards for selected stage
    s_cols = st.columns(3)
    with s_cols[0]:
        render_metric_card("Stage GWP", s_metrics.get("GWP", "N/A"), "kg CO₂-eq")
    with s_cols[1]:
        render_metric_card("Stage Energy", s_metrics.get("Energy", "N/A"), "MJ")
    with s_cols[2]:
        render_metric_card("Stage Water", s_metrics.get("Water", "N/A"), "m³")

    # textual stage notes
    st.markdown(f"<div class='neon-card'><div class='tiny-muted'>Stage Notes: {s_metrics.get('notes','')}</div></div>", unsafe_allow_html=True)

    # AI lifecycle interpretation for selected stage (use ai_recommendation)
    st.markdown("<div class='neon-card'><div class='section-title'>AI Generated Life Cycle Interpretation</div><div class='section-sub'>AI insights for the selected lifecycle stage and action suggestions.</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='ai-card'>", unsafe_allow_html=True)
    try:
        # display_ai_recommendations expects dict + optional extra_context
        ai_recommendation.display_ai_recommendations(ai_data, extra_context={
            "selected_stage": selected_key,
            "stage_metrics": s_metrics,
            "ore_conc": results.get("ore_conc", None),
            "transport_type": results.get("transport_type", None)
        })
    except Exception as e:
        st.error("AI recommendations failed to render. See debug below:")
        st.exception(e)
        # fallback: print summary if available
        if isinstance(ai_data, dict) and ai_data.get("summary"):
            st.info(ai_data.get("summary"))
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # 8️⃣ Circularity Analysis & Donut Gauge
    # -------------------------
    circ = results.get("circularity_analysis", {
        "Circularity Rate": 48,
        "Recyclability Rate": 88,
        "Recovery Efficiency": 90,
        "Secondary Material Content": 12
    })
    st.markdown("<div class='neon-card'><div class='section-title'>Circularity Analysis</div><div class='section-sub'>High-level circularity metrics and visual gauge.</div></div>", unsafe_allow_html=True)
    cc0, cc1 = st.columns([0.4, 0.6])
    with cc0:
        # donut gauge via go.Indicator
        gauge_val = circ.get("Circularity Rate", 50)
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gauge_val,
            number={"suffix": "%", "font": {"size": 32, "color": "#E6FFFB"}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00FFC2", "thickness": 0.22},
                "bgcolor": "rgba(0,0,0,0)",
                "steps": [{"range": [0, 100], "color": "rgba(255,255,255,0.03)"}]
            },
            domain={"x": [0, 1], "y": [0, 1]}
        ))
        plotly_style(gauge, title="Circularity Rate", height=320)
        st.plotly_chart(gauge, use_container_width=True)
    with cc1:
        # Submetrics as progress bars and cards
        st.markdown("<div style='padding:6px 2px;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='tiny-muted'>Recyclability Rate <b style='color:#E8FFFB'>{circ.get('Recyclability Rate','N/A')}%</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#0f3f3a;border-radius:10px;height:12px;margin-top:6px;'><div style='background:#00FFC2;width:{circ.get('Recyclability Rate',0)}%;height:12px;border-radius:10px;'></div></div>", unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='tiny-muted'>Recovery Efficiency <b style='color:#E8FFFB'>{circ.get('Recovery Efficiency','N/A')}%</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#0f3f3a;border-radius:10px;height:12px;margin-top:6px;'><div style='background:#00A88F;width:{circ.get('Recovery Efficiency',0)}%;height:12px;border-radius:10px;'></div></div>", unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='tiny-muted'>Secondary Material Content <b style='color:#E8FFFB'>{circ.get('Secondary Material Content','N/A')}%</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:linear-gradient(90deg,#073a38,#0f4f4d);border-radius:10px;height:12px;margin-top:6px;'><div style='background:#00C9A7;width:{circ.get('Secondary Material Content',0)}%;height:12px;border-radius:10px;'></div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Extended circularity metrics grid (each metric glossy card)
    ext_circ = results.get("extended_circularity_metrics", {
        "Resource Efficiency": "92%",
        "Extended Product Life": "110%",
        "Reuse Potential": "40/50",
        "Material Recovery": "90%",
        "Closed–Loop Potential": "75%",
        "Recycling Content": "10%",
        "Landfill Rate": "8%",
        "Energy Recovery": "2%"
    })
    st.markdown("<div class='neon-card'><div class='section-title'>Extended Circularity Metrics</div><div class='section-sub'>Detailed circularity indicators.</div></div>", unsafe_allow_html=True)
    ext_labels = list(ext_circ.keys())
    # display 4 per row
    for i in range(0, len(ext_labels), 4):
        row_cols = st.columns(4)
        for j, col in enumerate(row_cols):
            idx = i + j
            if idx < len(ext_labels):
                key = ext_labels[idx]
                val = ext_circ[key]
                with col:
                    render_metric_card(key, val)

    # -------------------------
    # 9️⃣ Material Flow (Sankey)
    # -------------------------
    st.markdown("<div class='neon-card'><div class='section-title'>Material Flow (Sankey)</div><div class='section-sub'>Visualization of flows between lifecycle nodes.</div></div>", unsafe_allow_html=True)
    mf = results.get("material_flow_analysis", {
        "labels": ["Ore", "Processing", "Manufacture", "Use", "End-of-Life"],
        "source": [0, 1, 2, 2],
        "target": [1, 2, 3, 4],
        "value": [100, 85, 80, 20]
    })
    try:
        sankey_fig = go.Figure(go.Sankey(
            node=dict(label=mf["labels"], pad=18, thickness=18, line=dict(color="rgba(0,0,0,0.08)", width=0.5)),
            link=dict(source=mf["source"], target=mf["target"], value=mf["value"])
        ))
        plotly_style(sankey_fig, title="Material Flow", height=420)
        st.plotly_chart(sankey_fig, use_container_width=True)
    except Exception as e:
        st.error("Could not render Sankey diagram.")
        st.exception(e)

    # -------------------------
    # 10️⃣ Charts (GWP Contribution, Energy Breakdown, Key Impact Profiles)
    # -------------------------
    st.markdown("<div class='neon-card'><div class='section-title'>Charts: GWP Contribution, Energy Breakdown, Key Impact Profiles</div></div>", unsafe_allow_html=True)

    # GWP contribution pie (mock fallback)
    gwp_contrib = results.get("gwp_contribution_analysis", {"Production": 66, "Processing": 24, "Transport": 10})
    try:
        df_gwp = pd.DataFrame(list(gwp_contrib.items()), columns=["Category", "Value"])
        pie = px.pie(df_gwp, names="Category", values="Value", hole=0.34)
        plotly_style(pie, title="GWP Contribution Analysis", height=360)
        st.plotly_chart(pie, use_container_width=True)
    except Exception as e:
        st.error("GWP contribution chart failed.")
        st.exception(e)

    # Energy breakdown
    energy_breakdown = results.get("energy_source_breakdown", {"Grid Electricity": 18000, "Coal": 7000, "Renewables": 1454})
    try:
        df_energy = pd.DataFrame(list(energy_breakdown.items()), columns=["Source", "Value"])
        bar_energy = px.bar(df_energy, x="Source", y="Value", text="Value")
        plotly_style(bar_energy, title="Energy Source Breakdown", x_title="Energy Source", y_title="Value", height=360)
        st.plotly_chart(bar_energy, use_container_width=True)
    except Exception as e:
        st.error("Energy breakdown chart failed.")
        st.exception(e)

    # Key Impact Profiles (bar)
    kip = results.get("key_impact_profiles", {"GWP": 2293, "Energy": 26454, "Water": 4.7, "Eutrophication": 1.15, "Acidification": 4.1})
    try:
        df_kip = pd.DataFrame(list(kip.items()), columns=["Metric", "Value"])
        kip_fig = px.bar(df_kip, x="Metric", y="Value", text="Value")
        plotly_style(kip_fig, title="Key Impact Profiles", x_title="Metric", y_title="Value", height=360)
        st.plotly_chart(kip_fig, use_container_width=True)
    except Exception as e:
        st.error("Key Impact Profiles chart failed.")
        st.exception(e)

    # -------------------------
    # 11️⃣ Detailed Impact Assessment (chart + table)
    # -------------------------
    st.markdown("<div class='neon-card'><div class='section-title'>Detailed Impact Assessment</div><div class='section-sub'>Table and chart view of detailed impact metrics.</div></div>", unsafe_allow_html=True)
    impact_data = results.get("impact_data", [
        ("Global Warming Potential", 2293, "kg CO₂-eq"),
        ("Energy Demand", 26454, "MJ"),
        ("Water Consumption", 4.7, "m³"),
        ("Acidification Potential", 4.1, "kg SO₂-eq"),
        ("Eutrophication Potential", 1.15, "kg PO₄-eq"),
        ("Ozone Depletion Potential", 0.00229, "kg CFC-11 eq"),
        ("Particulate Matter Formation", 0.76, "kg PM2.5-eq"),
        ("Abiotic Depletion (Fossil)", 29100, "MJ"),
        ("Human Toxicity (Cancer)", 0.23, "CTUh"),
        ("Land Use", 228.77, "m²·year"),
    ])
    try:
        df_imp = pd.DataFrame(impact_data, columns=["Impact Metric", "Value", "Unit"])
        # Chart of numeric values (filter out those non-numeric for plotting)
        df_plot = df_imp.copy()
        df_plot["ValueNumeric"] = pd.to_numeric(df_plot["Value"], errors="coerce")
        df_plot = df_plot.dropna(subset=["ValueNumeric"])
        chart = px.bar(df_plot, x="Impact Metric", y="ValueNumeric", text="ValueNumeric")
        plotly_style(chart, title="Detailed Impact - Chart View", x_title="Metric", y_title="Value", height=420)
        st.plotly_chart(chart, use_container_width=True)
        st.dataframe(df_imp, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error("Failed to render detailed impact assessment.")
        st.exception(e)

    # -------------------------
    # 12️⃣ Uncertainty Dashboard (histograms)
    # -------------------------
    st.markdown("<div class='neon-card'><div class='section-title'>Uncertainty Dashboard</div><div class='section-sub'>Monte Carlo distributions and 95% CIs for major indicators.</div></div>", unsafe_allow_html=True)
    # sample arrays if not provided
    gwp_dist = np.array(results.get("gwp_distribution")) if results.get("gwp_distribution") is not None else np.random.normal(loc=executive.get("Global Warming Potential", 2293), scale=110, size=1000)
    energy_dist = np.array(results.get("energy_distribution")) if results.get("energy_distribution") is not None else np.random.normal(loc=production.get("Overall Energy Demand", 26454), scale=1200, size=1000)
    water_dist = np.array(results.get("water_distribution")) if results.get("water_distribution") is not None else np.random.normal(loc=executive.get("Water Consumption", 4.7), scale=0.3, size=1000)

    u_cols = st.columns(3)
    for (arr, label, unit), col in zip(
            [(gwp_dist, "GWP", "kg CO₂-eq"), (energy_dist, "Energy", "MJ"), (water_dist, "Water", "m³")],
            u_cols):
        mean = float(np.mean(arr))
        std = float(np.std(arr))
        ci_low, ci_high = np.percentile(arr, [2.5, 97.5])
        hist = go.Figure()
        hist.add_trace(go.Histogram(x=arr, nbinsx=30, marker=dict(color="#00FFC2"), showlegend=False, opacity=0.75))
        hist.add_vline(x=mean, line_width=3, line_color='#FFFFFF')
        hist.add_vline(x=ci_low, line_width=2, line_dash='dash', line_color='#A8FFF1')
        hist.add_vline(x=ci_high, line_width=2, line_dash='dash', line_color='#A8FFF1')
        hist.update_layout(
            margin=dict(l=12, r=12, t=56, b=36),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=dict(text=f"<b>{label}</b><br><span style='font-size:0.9rem;color:#CFF6F0'>Mean: {mean:.1f} | σ: {std:.1f} | 95% CI: [{ci_low:.1f}, {ci_high:.1f}]</span>", y=0.92, x=0.5),
            xaxis_title=unit, yaxis_title=""
        )
        plotly_style(hist, height=320)
        col.plotly_chart(hist, use_container_width=True)

    # -------------------------
    # 13️⃣ Primary vs Recycled Scenario Comparison (table + chart)
    # -------------------------
    st.markdown("<div class='neon-card'><div class='section-title'>Primary vs Recycled — Scenario Comparison</div><div class='section-sub'>Side-by-side environmental comparison between production routes.</div></div>", unsafe_allow_html=True)
    pvrs = results.get("primary_vs_recycled", {
        "comparison_table": [
            {"Metric": "Global Warming Potential (kg CO₂-eq)", "Primary": 2200, "Recycled": 620},
            {"Metric": "Energy Demand (MJ)", "Primary": 27000, "Recycled": 9800},
            {"Metric": "Water Consumption (m³)", "Primary": 5.1, "Recycled": 2.2},
            {"Metric": "Circularity Score (%)", "Primary": 48, "Recycled": 82},
        ]
    })
    df_comp = pd.DataFrame(pvrs["comparison_table"])
    st.dataframe(df_comp, use_container_width=True, hide_index=True)
    try:
        df_long = df_comp.melt(id_vars=["Metric"], var_name="Scenario", value_name="Value")
        comp_fig = px.bar(df_long, x="Metric", y="Value", color="Scenario", barmode="group", text="Value")
        plotly_style(comp_fig, title="Primary vs Recycled: Comparison", height=420)
        st.plotly_chart(comp_fig, use_container_width=True)
    except Exception as e:
        st.error("Scenario comparison chart failed.")
        st.exception(e)

    # -------------------------
    # 14️⃣ AI-Powered Insights & Recommendations (final summary)
    # -------------------------
    st.markdown("<div class='neon-card'><div class='section-title'>AI-Powered Insights & Recommendations</div><div class='section-sub'>NLP-based evidence, root causes, and action plans derived from lifecycle data.</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='ai-card'>", unsafe_allow_html=True)
    try:
        ai_recommendation.display_ai_recommendations(ai_data, extra_context={
            "ore_conc": results.get("ore_conc"),
            "transports": results.get("transports", []),
            "selected_stage": selected_key
        })
    except Exception as e:
        st.error("AI rendering failed. See details:")
        st.exception(e)
        if isinstance(ai_data, dict) and ai_data.get("summary"):
            st.info(ai_data.get("summary"))
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # Footer & download hint
    # -------------------------
    st.markdown(
        """
        <div style='margin-top:18px; padding:10px;'>
            <div style='color:#DFFAF5; text-align:center; font-size:0.95rem;'>
                Tip: Use the platform's export functionality to download CSV / PDF reports for documentation. For public claims, perform third-party critical review (ISO 14044).
            </div>
            <div style='height:8px;'></div>
            <div style='text-align:center;color:#A8FFF1;font-size:0.85rem;'>© 2025 MetalliQ Sustainability Platform</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------------------------
# Local preview: run a demo when file executed directly.
# -------------------------
if __name__ == "__main__":
    # Build demo results (comprehensive mock)
    demo_results = {
        "executive_summary": {
            "Global Warming Potential": 2293,
            "Circularity Score": 50,
            "Particulate Matter": 0.763,
            "Water Consumption": 4.7,
            "Production Phase GWP": 2200,
            "Overall Energy Demand": 26454
        },
        "goal_scope": {
            "Intended Application": "Screening-level LCA comparison",
            "System Boundary": "Cradle-to-Grave",
            "Limitations": "Industry-average data; site-specific emissions excluded",
            "Intended Audience": "Internal R&D",
            "Comparative Assertion for Public": "No"
        },
        "data_quality": {
            "Reliability": 5, "Completeness": 4, "Temporal": 4, "Technological": 4, "Geographical": 4,
            "Aggregate Data Quality": 4.4, "Result Uncertainty": "±10%"
        },
        "supply_chain_hotspots": [
            {"title": "Production Phase GWP", "description": "Primary production dominates GWP", "impact": 66},
            {"title": "Overall Energy Demand", "description": "High electricity use in smelting", "impact": 24},
            {"title": "Transport", "description": "Logistics emissions", "impact": 10}
        ],
        "production_metrics": {
            "Production Phase GWP": 2200,
            "Overall Energy Demand": 26454,
            "Circular Score": 50
        },
        "stage_metrics": {
            "ore": {"GWP": 520, "Energy": 6200, "Water": 0.8, "notes": "Open cast mining & beneficiation"},
            "processing": {"GWP": 720, "Energy": 7900, "Water": 1.2, "notes": "Concentration & refining"},
            "manufacturing": {"GWP": 1250, "Energy": 15000, "Water": 2.5, "notes": "Smelting & product fabrication"},
            "transport": {"GWP": 140, "Energy": 1100, "Water": 0.18, "notes": "Inter-site logistics"},
            "use": {"GWP": 90, "Energy": 950, "Water": 1.0, "notes": "Service life impacts"},
            "end": {"GWP": 45, "Energy": 420, "Water": 0.35, "notes": "Recycling and disposal"}
        },
        "circularity_analysis": {"Circularity Rate": 48, "Recyclability Rate": 88, "Recovery Efficiency": 90, "Secondary Material Content": 12},
        "extended_circularity_metrics": {
            "Resource Efficiency": "92%", "Extended Product Life": "110%", "Reuse Potential": "40/50",
            "Material Recovery": "90%", "Closed–Loop Potential": "75%", "Recycling Content": "10%", "Landfill Rate": "8%", "Energy Recovery": "2%"
        },
        "material_flow_analysis": {
            "labels": ["Ore", "Processing", "Manufacture", "Use", "End-of-Life"],
            "source": [0, 1, 2, 2],
            "target": [1, 2, 3, 4],
            "value": [100, 85, 80, 20]
        },
        "gwp_contribution_analysis": {"Production": 66, "Processing": 24, "Transport": 10},
        "energy_source_breakdown": {"Grid": 18000, "Coal": 7000, "Renewables": 1454},
        "key_impact_profiles": {"GWP": 2293, "Energy": 26454, "Water": 4.7, "Acidification": 4.1, "Eutrophication": 1.15},
        "impact_data": [
            ("Global Warming Potential", 2293, "kg CO₂-eq"),
            ("Energy Demand", 26454, "MJ"),
            ("Water Consumption", 4.7, "m³"),
            ("Acidification Potential", 4.1, "kg SO₂-eq"),
            ("Eutrophication Potential", 1.15, "kg PO₄-eq"),
            ("Particulate Matter Formation", 0.76, "kg PM2.5-eq")
        ],
        "primary_vs_recycled": {
            "comparison_table": [
                {"Metric": "Global Warming Potential (kg CO₂-eq)", "Primary": 2200, "Recycled": 620},
                {"Metric": "Energy Demand (MJ)", "Primary": 27000, "Recycled": 9800},
                {"Metric": "Water Consumption (m³)", "Primary": 5.1, "Recycled": 2.2},
                {"Metric": "Circularity Score (%)", "Primary": 48, "Recycled": 82}
            ]
        },
        "ore_conc": 45.6,
        "transports": [{"mode": "Truck", "dist": 250}, {"mode": "Ship", "dist": 800}]
    }

    # demo AI data uses ai_recommendation.ai_data_example if available
    demo_ai = ensure_ai_data(getattr(ai_recommendation, "ai_data_example", {"summary":"Use recycled content and renewables."}))
    results_page(demo_results, demo_ai)
