# results_page.py
# Rewritten results page for MetalliQ LCA platform
# Expects: results (dict) and ai_text (dict or str)
# Uses ai_recommendation.display_ai_recommendations for AI cards.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import ai_recommendation
from typing import Optional, Dict, Any

# ---------- Scoped CSS (won't override global app.css) ----------
st.markdown(
    """
    <style>
    /* Scoped classes for results page */
    .mq-neon { border-radius:12px; padding:12px; margin-bottom:16px; border:1px solid rgba(0,150,130,0.12); background:rgba(255,255,255,0.02); }
    .mq-title { font-weight:800; color:#006d66; font-size:1.12rem; }
    .mq-sub { color:#2f6b66; font-size:0.95rem; margin-bottom:8px; }
    .mq-card { background:linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,255,255,0.92)); padding:10px; border-radius:8px; box-shadow:0 8px 20px rgba(4,60,60,0.03); }
    .mq-metric { font-weight:800; color:#073a38; font-size:1.4rem; }
    .mq-small { color:#6c9b97; font-size:0.9rem; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Helpers ----------
def ensure_ai_dict(ai_in: Optional[Any]) -> Optional[Dict]:
    if ai_in is None:
        return None
    if isinstance(ai_in, dict):
        return ai_in
    if isinstance(ai_in, str):
        s = ai_in.strip()
        try:
            parsed = json.loads(s)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            return {"summary": s}
    return {"summary": str(ai_in)}

def plot_style(fig: go.Figure, title: str = None, height: int = None):
    if title:
        fig.update_layout(title=dict(text=title, x=0.5, xanchor="center", font=dict(size=14)))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    if height:
        fig.update_layout(height=height)
    return fig

def df_to_csv_download_link(df: pd.DataFrame, filename: str = "export.csv"):
    csv = df.to_csv(index=False).encode('utf-8')
    return st.download_button(label="Download CSV", data=csv, file_name=filename, mime="text/csv")

# ---------- Main ----------
def results_page(results: Optional[dict] = None, ai_text: Optional[Any] = None):
    """
    Render final LCA report. Safe to call even if 'results' is None or partial.
    """
    st.set_option('deprecation.showPyplotGlobalUse', False)
    results = results or {}
    ai_data = ensure_ai_dict(ai_text)

    # Merge defaults (safe fallbacks)
    # Try to reuse common keys from lca_simulation output if present
    executive = results.get("executive_summary", {})
    if not executive:
        # sensible defaults if run_simulation wasn't executed
        executive = {
            "Global Warming Potential": 2293.0,
            "Circularity Score": 50,
            "Particulate Matter": 0.76,
            "Water Consumption": 4.7,
            "Production Phase GWP": 1490.0,
            "Overall Energy Demand": 26454,
            "Circular Score": 50,
            "Supply Chain Hotspots": []
        }

    # Impact list default
    impact_list = results.get("impact_data", [
        ("Global Warming Potential", executive.get("Global Warming Potential", 2293.0), "kg CO2-eq"),
        ("Energy Demand", executive.get("Overall Energy Demand", 26454), "MJ"),
        ("Water Consumption", executive.get("Water Consumption", 4.7), "m3"),
    ])

    # Sankey / Material flow defaults
    mf = results.get("material_flow_analysis", {
        "labels": ["Metal Ore Extraction", "Manufacturing", "Transportation", "Use Phase", "End of Life", "Recycling", "Landfill"],
        "source": [0, 0, 1, 2, 3, 4],
        "target": [1, 2, 2, 3, 4, 5],
        "value": [100, 70, 60, 50, 30, 12]
    })

    circularity = results.get("circularity_analysis", {
        "Circularity Rate": 48,
        "Recyclability Rate": 88,
        "Recovery Efficiency": 90,
        "Secondary Material Content": 12
    })

    extended_circ = results.get("extended_circularity_metrics", {
        "Resource Efficiency": "92%",
        "Extended Product Life": "110%",
        "Reuse Potential": "40%",
        "Material Recovery": "90%",
        "Closed-loop Potential": "75%",
        "Recycling Content": "10%",
        "Landfill Rate": "8%",
        "Energy Recovery": "2%"
    })

    gwp_breakdown = results.get("gwp_contribution_analysis", {"Production": 66, "Transport": 25, "Use Phase": 9})
    energy_breakdown = results.get("energy_source_breakdown", {"Grid Electricity": 70, "Direct Fuel": 20000, "Renewables": 1454})

    # Primary vs Recycled
    pvr = results.get("primary_vs_recycled", {}).get("comparison_table", [
        {"Metric": "Global Warming Potential (kg CO2-eq)", "Primary": 2200, "Recycled": 600},
        {"Metric": "Energy Demand (MJ)", "Primary": 27000, "Recycled": 9800},
        {"Metric": "Water Consumption (m3)", "Primary": 5.0, "Recycled": 1.4},
    ])
    df_pvr = pd.DataFrame(pvr)

    # Uncertainty distributions (MonteCarlo arrays) fallback
    gwp_arr = np.array(results.get("uncertainty_dashboard", {}).get("Global Warming Potential", []))
    energy_arr = np.array(results.get("uncertainty_dashboard", {}).get("Energy Demand", []))
    water_arr = np.array(results.get("uncertainty_dashboard", {}).get("Water Consumption", []))
    if gwp_arr.size == 0:
        gwp_arr = np.random.normal(loc=executive.get("Global Warming Potential", 2293.0), scale=100, size=1000)
    if energy_arr.size == 0:
        energy_arr = np.random.normal(loc=executive.get("Overall Energy Demand", 26454), scale=1500, size=1000)
    if water_arr.size == 0:
        water_arr = np.random.normal(loc=executive.get("Water Consumption", 4.7), scale=0.4, size=1000)

    # PAGE TITLE
    st.markdown(f"<div class='mq-neon'><div class='mq-title'>MetalliQ — Final LCA Report</div><div class='mq-sub'>ISO 14044-aligned interactive report, AI interpretation & scenario comparison</div></div>", unsafe_allow_html=True)

    # ---------------- ISO 14044 Compliance ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>ISO 14044 Compliance</div>", unsafe_allow_html=True)
        st.markdown("<div class='mq-card'><b>Conformance Level:</b> Screening-level alignment with ISO 14044 principles. For formal comparative assertions and public disclosure, follow the ISO critical review process and use site-specific primary data where required.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Executive Summary ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Executive Summary</div><div class='mq-sub'>Key aggregated indicators (Monte Carlo averages where available)</div>", unsafe_allow_html=True)
        cols = st.columns(4)
        try:
            cols[0].markdown(f"<div class='mq-card'><div class='mq-small'>Global Warming Potential</div><div class='mq-metric'>{executive.get('Global Warming Potential'):.1f} <span class='mq-small'>kg CO₂-eq</span></div></div>", unsafe_allow_html=True)
            cols[1].markdown(f"<div class='mq-card'><div class='mq-small'>Circularity Score</div><div class='mq-metric'>{executive.get('Circularity Score')} <span class='mq-small'>%</span></div></div>", unsafe_allow_html=True)
            cols[2].markdown(f"<div class='mq-card'><div class='mq-small'>Particulate Matter</div><div class='mq-metric'>{executive.get('Particulate Matter'):.3g} <span class='mq-small'>kg PM2.5-eq</span></div></div>", unsafe_allow_html=True)
            cols[3].markdown(f"<div class='mq-card'><div class='mq-small'>Water Consumption</div><div class='mq-metric'>{executive.get('Water Consumption')} <span class='mq-small'>m³</span></div></div>", unsafe_allow_html=True)
        except Exception:
            # defensive in case numeric conversions fail
            st.write(cols[0].markdown if False else "")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Goal & Scope ----------------
    gs = results.get("goal_scope", {})
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Goal & Scope (ISO 14044)</div><div class='mq-sub'>Study boundary, intended application & audience</div>", unsafe_allow_html=True)
        st.markdown("<div class='mq-card'>", unsafe_allow_html=True)
        st.write(gs or {"Intended Application": "Screening study", "System Boundary": "Cradle-to-Gate"})
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------- Data Quality & Uncertainty ----------------
    dq = results.get("data_quality", {})
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Data Quality & Uncertainty</div><div class='mq-sub'>Pedigree scores & aggregated uncertainty indicators</div>", unsafe_allow_html=True)
        st.markdown("<div class='mq-card'>", unsafe_allow_html=True)
        st.write(dq or {"Reliability": "N/A", "Completeness": "N/A"})
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------- Supply Chain Hotspots ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Supply Chain Hotspots</div><div class='mq-sub'>Top contributors by impact share</div>", unsafe_allow_html=True)
        sc = executive.get("Supply Chain Hotspots", [])
        if sc:
            for h in sc:
                st.markdown(f"<div class='mq-card'><b>{h.get('title')}</b><div class='mq-small'>{h.get('description')}</div><div style='margin-top:6px;font-weight:800;color:#095a55'>{h.get('impact','')}% of total impact</div></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='mq-card'><i>No hotspots identified in results.</i></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Interactive Process Lifecycle ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Interactive Process Lifecycle</div><div class='mq-sub'>Click a stage to view stage-specific metrics and AI notes</div>", unsafe_allow_html=True)
        # small interactive selector from material flow labels if available
        stages = mf.get("labels", ["Metal Ore Extraction", "Manufacturing", "Transportation", "Use Phase", "End of Life"])
        selected = st.selectbox("Select Lifecycle Stage", stages, index=0)
        # stage mock metrics: if results contain stage metrics, use them; otherwise compute proportional share
        stage_metrics = results.get("stage_metrics", {}).get(selected, {})
        if not stage_metrics:
            # derive approximate numbers by evenly splitting GWP
            total_gwp = executive.get("Global Warming Potential", 2293.0)
            approx = {"GWP": round(total_gwp * (0.2 if selected == stages[0] else 0.15), 1),
                      "Energy": round(executive.get("Overall Energy Demand", 26454) * 0.1, 1),
                      "Water": round(executive.get("Water Consumption", 4.7) * 0.2, 3)}
            stage_metrics = approx
        st.markdown(f"<div class='mq-card'><b>Stage:</b> {selected} <br><b>GWP:</b> {stage_metrics.get('GWP')} kg CO₂-eq  •  <b>Energy:</b> {stage_metrics.get('Energy')} MJ  •  <b>Water:</b> {stage_metrics.get('Water')} m³</div>", unsafe_allow_html=True)

        # Stage-level AI (reuse ai_recommendation)
        st.markdown("<div style='margin-top:8px;'>", unsafe_allow_html=True)
        stage_ai = {
            "summary": f"Stage-level interpretation for {selected}.",
            "findings": [
                {
                    "title": f"{selected} - GWP hotspot",
                    "priority": "High Priority" if stage_metrics.get("GWP", 0) > (executive.get("Global Warming Potential", 1) * 0.2) else "Medium Priority",
                    "evidence": f"{selected} contributes approx {stage_metrics.get('GWP')} kg CO₂-eq",
                    "root_cause": "Energy intensity and transport distances",
                    "action_plan": [
                        {"title": "Process optimization", "desc": "Implement heat recovery", "impact": "Lower energy/GWP", "effort": "Medium Effort", "confidence": 80}
                    ]
                }
            ]
        }
        try:
            ai_recommendation.display_ai_recommendations(stage_ai, extra_context={"stage": selected, "stage_metrics": stage_metrics})
        except Exception:
            st.write("AI stage interpretation unavailable.")
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------- AI Generated Life Cycle Interpretation (global) ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>AI Generated Life Cycle Interpretation</div><div class='mq-sub'>NLP-powered insights and recommended actions</div>", unsafe_allow_html=True)
        if ai_data:
            try:
                extra = {"executive_summary": executive, "material_flow": mf}
                ai_recommendation.display_ai_recommendations(ai_data, extra_context=extra)
            except Exception:
                st.error("Failed to render AI recommendations.")
                st.write(ai_data.get("summary", str(ai_data)))
        else:
            st.markdown("<div class='mq-card'><i>No AI interpretation provided for this study.</i></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Material Flow (Sankey) ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Material Flow (Sankey)</div><div class='mq-sub'>Process-level material transfers</div>", unsafe_allow_html=True)
        try:
            node = dict(label=mf["labels"], pad=18, thickness=18, line=dict(color="rgba(0,0,0,0.06)", width=0.5))
            link = dict(source=mf["source"], target=mf["target"], value=mf["value"])
            sankey_fig = go.Figure(go.Sankey(node=node, link=link))
            plot_style(sankey_fig, title="Material Flow Sankey", height=420)
            st.plotly_chart(sankey_fig, use_container_width=True)
        except Exception as e:
            st.error("Sankey diagram failed to render.")
            st.exception(e)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Circularity Analysis ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Circularity Analysis</div><div class='mq-sub'>High-level circularity metrics and progress bars</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([0.45, 0.55])
        with col1:
            circ_val = circularity.get("Circularity Rate", 50)
            gauge = go.Figure(go.Indicator(mode="gauge+number", value=circ_val, number={"suffix":"%"}, gauge={"axis": {"range":[0,100]}, "bar":{"color":"#00897b"}}))
            plot_style(gauge, title="Circularity Rate", height=300)
            st.plotly_chart(gauge, use_container_width=True)
        with col2:
            st.markdown("<div class='mq-card'>", unsafe_allow_html=True)
            st.markdown(f"**Recyclability Rate:** {circularity.get('Recyclability Rate', 'N/A')}%")
            st.progress(int(circularity.get('Recyclability Rate', 0)))
            st.markdown(f"**Recovery Efficiency:** {circularity.get('Recovery Efficiency', 'N/A')}%")
            st.progress(int(circularity.get('Recovery Efficiency', 0)))
            st.markdown(f"**Secondary Material Content:** {circularity.get('Secondary Material Content', 'N/A')}%")
            st.progress(int(circularity.get('Secondary Material Content', 0)))
            st.markdown("</div>", unsafe_allow_html=True)

        # Extended metrics grid
        st.markdown("<div style='margin-top:12px;'/>", unsafe_allow_html=True)
        cols = st.columns(4)
        items = list(extended_circ.items())
        for i, (k, v) in enumerate(items):
            cols[i % 4].markdown(f"<div class='mq-card'><b>{k}</b><div class='mq-small' style='margin-top:6px'>{v}</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Charts: GWP Contribution & Energy Breakdown ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Key Charts</div><div class='mq-sub'>GWP contribution and energy source breakdown</div>", unsafe_allow_html=True)
        # GWP pie
        try:
            df_gwp = pd.DataFrame(list(gwp_breakdown.items()), columns=["Category", "Share"])
            pie = px.pie(df_gwp, names="Category", values="Share", hole=0.35)
            plot_style(pie, title="GWP Contribution Analysis", height=340)
            st.plotly_chart(pie, use_container_width=True)
        except Exception:
            st.write("GWP contribution chart not available.")

        # Energy breakdown bar
        try:
            df_energy = pd.DataFrame(list(energy_breakdown.items()), columns=["Source", "Value"])
            bar = px.bar(df_energy, x="Source", y="Value", text="Value")
            plot_style(bar, title="Energy Source Breakdown", height=320)
            st.plotly_chart(bar, use_container_width=True)
        except Exception:
            st.write("Energy breakdown chart not available.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Detailed Impact Assessment ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Detailed Impact Assessment</div><div class='mq-sub'>Table & chart views for all reported impact metrics</div>", unsafe_allow_html=True)
        df_imp = pd.DataFrame(impact_list, columns=["Impact Metric", "Value", "Unit"])
        # Chart: numeric values only
        numeric = df_imp.copy()
        numeric["ValueNum"] = pd.to_numeric(numeric["Value"], errors='coerce')
        numeric_chart = numeric.dropna(subset=["ValueNum"])
        if not numeric_chart.empty:
            fig = px.bar(numeric_chart, x="Impact Metric", y="ValueNum", text="ValueNum")
            plot_style(fig, title="Impact Metrics Chart", height=380)
            st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_imp, use_container_width=True)
        df_to_csv_download_link(df_imp, filename="detailed_impact_assessment.csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Uncertainty Dashboard ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Uncertainty Dashboard</div><div class='mq-sub'>Monte Carlo distributions and 95% CI</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        def hist_col(col, arr, label, unit):
            mean = float(np.mean(arr))
            ci = np.percentile(arr, [2.5, 97.5])
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=arr, nbinsx=30, marker=dict(color="#aee6de"), showlegend=False))
            fig.add_vline(x=mean, line_color="#145c59", line_width=3)
            fig.add_vline(x=ci[0], line_dash="dash", line_color="#145c59")
            fig.add_vline(x=ci[1], line_dash="dash", line_color="#145c59")
            plot_style(fig, title=f"{label} distribution", height=300)
            col.plotly_chart(fig, use_container_width=True)
            col.markdown(f"**Mean:** {mean:.2f} {unit}  •  **95% CI:** [{ci[0]:.2f}, {ci[1]:.2f}]")
        hist_col(c1, gwp_arr, "Global Warming Potential", "kg CO₂-eq")
        hist_col(c2, energy_arr, "Energy Demand", "MJ")
        hist_col(c3, water_arr, "Water Consumption", "m³")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Primary vs Recycled Scenario Comparison ----------------
    with st.container():
        st.markdown("<div class='mq-neon'><div class='mq-title'>Primary vs Recycled Scenario Comparison</div><div class='mq-sub'>Detailed comparison table + charts</div>", unsafe_allow_html=True)
        st.dataframe(df_pvr, use_container_width=True)
        df_to_csv_download_link(df_pvr, filename="primary_vs_recycled_comparison.csv")
        # Comparison chart: show Primary vs Recycled for numeric columns
        numeric_cols = [c for c in df_pvr.columns if c != "Metric"]
        try:
            df_chart = df_pvr.melt(id_vars="Metric", value_vars=numeric_cols, var_name="Scenario", value_name="Value")
            fig_cmp = px.bar(df_chart, x="Metric", y="Value", color="Scenario", barmode="group", text="Value")
            plot_style(fig_cmp, title="Primary vs Recycled — Comparison", height=380)
            st.plotly_chart(fig_cmp, use_container_width=True)
        except Exception:
            st.write("Comparison chart unavailable.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Exports & Report Actions ----------------
    with st.container():
        st.markdown(
            "<div class='mq-neon'><div class='mq-title'>Export & Actions</div><div class='mq-sub'>Save or export report sections</div>", 
            unsafe_allow_html=True)
        # flattened CSV exports for core tables
        download_json = json.dumps(results, indent=2)
        st.download_button(
            label="📦 Download Full Report (JSON)",
            data=download_json,
            file_name="lca_report.json",
            mime="application/json",
        )
        st.markdown("</div>", unsafe_allow_html=True)
    # Footer note
    st.markdown("<div style='margin-top:14px;color:#5f7f7b;font-size:0.9rem;'>Generated by MetalliQ · Screening-level LCA. For regulatory/comparative reporting follow ISO 14044 critical review steps.</div>", unsafe_allow_html=True)

# If executed directly (for testing)
if __name__ == "__main__":
    # quick debug/demo when running this file directly
    demo_results = {}
    results_page(demo_results, ai_text=ai_recommendation.ai_data_example if hasattr(ai_recommendation, 'ai_data_example') else {"summary":"Demo AI"})
