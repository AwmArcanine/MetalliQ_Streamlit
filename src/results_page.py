# results_page.py
"""
Final results page for MetalliQ LCA platform (Plotly-based)
- No st.download_button usage (data URIs used instead)
- Mock-data safe: nothing is left empty
- Integrates ai_recommendation display when available; otherwise renders built-in AI block
- Always shows Ore Grade warning and EV charging recommendations in AI Insights
- Contains a dummy "Export PDF" button (no actual PDF export)
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import datetime
import plotly.express as px
import plotly.graph_objects as go
import base64
from typing import Optional, Any, Dict

# try importing ai helpers if available
try:
    import ai_recommendation
    from ai_recommendation import ai_data_example
except Exception:
    ai_recommendation = None
    ai_data_example = None

# ---------------- Theme colors (soft teal + glass)
ACCENT = "#5bfff1"
ACCENT_DARK = "#16f3e0"
CARD_BG = "rgba(255,255,255,0.30)"
MUTED = "#fcfcfc"
TITLE = "#11ebe4"

# ---------------- Helpers ----------------
def csv_download_link(df, filename: str = "table.csv", label: str = "Download CSV"):
    """
    Create a base64 download link for a pandas DataFrame (no st.download_button used).
    Usage: csv_download_link(df, filename="my.csv", label="Download CSV")
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:text/csv;base64,{b64}" download="{filename}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)

def plot_style(fig: go.Figure, title: Optional[str] = None, height: Optional[int] = None):
    layout = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=24, r=24, t=40 if title else 8, b=24),
        font=dict(color=MUTED),
        title=dict(x=0.5, xanchor="center")
    )
    fig.update_layout(layout)
    if title:
        fig.update_layout(title_text=title)
    if height:
        fig.update_layout(height=height)
    return fig

def ensure_ai_dict(ai_in: Optional[Any]):
    if ai_in is None:
        return None
    if isinstance(ai_in, dict):
        return ai_in
    if isinstance(ai_in, str):
        try:
            parsed = json.loads(ai_in)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            return {"summary": ai_in}
    return {"summary": str(ai_in)}

def safe_results(results: Optional[dict]) -> dict:
    """Return a results dict with realistic mock defaults so nothing is empty."""
    r = results.copy() if results else {}
    r.setdefault("title", "Steel for New Building Frame")
    r.setdefault("generated_by", "John Doe")
    r.setdefault("generated_on", datetime.date.today().strftime("%d/%m/%Y"))
    r.setdefault("executive_summary", {
        "Global Warming Potential": 2288.0,
        "Circularity Score": 50,
        "Particulate Matter": 0.763,
        "Water Consumption": 4.7,
        "Overall Energy Demand": 26625.84
    })
    r.setdefault("goal_scope", {
        "Intended Application": "Screening assessment for internal R&D",
        "Intended Audience": "Engineering & sustainability teams",
        "System Boundary": "Cradle-to-Gate",
        "Comparative Assertion for Public": "No (screening-level)"
    })
    r.setdefault("data_quality", {
        "Reliability": "5/5", "Completeness": "5/5", "Temporal": "5/5", "Geographical": "4/5", "Technological": "4/5",
        "Aggregated ADQI": 4.51, "Result Uncertainty pct": 14
    })
    r.setdefault("supply_chain_hotspots", [
        {"title": "Production Phase Global Warming Potential", "desc": "Highest environmental impact contributor", "share_pct": 65},
        {"title": "Overall Energy Demand", "desc": "High energy intensity", "share_pct": 25},
        {"title": "Circularity Score", "desc": "Opportunities to increase recycled content", "share_pct": 10},
    ])
    r.setdefault("material_flow", {
        "labels": ["Raw Input", "Processing", "Manufacturing", "Product in Use", "End of Life", "Recycling", "Waste"],
        "source": [0, 1, 2, 2, 3, 4],
        "target": [1, 2, 3, 4, 5, 6],
        "value": [100, 80, 70, 60, 20, 15]
    })
    r.setdefault("circularity", {
        "Circularity Rate": 50,
        "Recyclability Rate": 90,
        "Recovery Efficiency": 92,
        "Secondary Material Content": 10
    })
    r.setdefault("extended_metrics", {
        "Resource Efficiency": "92%", "Extended Product Life": "110%", "Reuse Potential": "40/50",
        "Material Recovery": "90%", "Closed-loop Potential": "75%", "Recycling Content": "10%", "Landfill Rate": "8%", "Energy Recovery": "2%"
    })
    r.setdefault("impact_list", [
        ("Global Warming Potential", 2288.0, "kg CO₂-eq"),
        ("Energy Demand", 26626.0, "MJ"),
        ("Water Consumption", 4.7, "m³"),
        ("Acidification Potential", 4.11, "kg SO₂-eq"),
        ("Eutrophication", 1.14, "kg PO₄-eq"),
        ("Photochemical Ozone", 2.29, "kg NMVOC-eq"),
        ("Particulate Matter", 0.76, "kg PM2.5-eq"),
        ("Abiotic Depletion (Fossil)", 29288, "MJ"),
        ("Human Toxicity (Non-Cancer)", 2.29, "CTUh"),
        ("Freshwater Ecotoxicity", 22.88, "CTUe"),
        ("Land Use", 228.77, "m²·year")
    ])
    r.setdefault("gwp_breakdown", {"Production": 66, "Transport": 25, "Use Phase": 9})
    r.setdefault("energy_breakdown", {"Direct Fuel": 24794.84, "Grid Electricity": 1831.00})
    r.setdefault("primary_vs_recycled", [
        {"Metric": "GWP (kg CO2-eq)", "Primary": 2485, "Recycled": 597},
        {"Metric": "Energy (GJ)", "Primary": 28.77, "Recycled": 6.17},
        {"Metric": "Water (m³)", "Primary": 5.0, "Recycled": 2.0},
        {"Metric": "Acidification (kg SO2-eq)", "Primary": 4.40, "Recycled": 1.35},
        {"Metric": "Eutrophication (kg PO4-eq)", "Primary": 1.24, "Recycled": 0.30},
    ])
    # Monte Carlo arrays for uncertainty dashboard
    if "uncertainty" not in r:
        rng = np.random.default_rng(123)
        gwp_arr = rng.normal(loc=r["executive_summary"]["Global Warming Potential"], scale=100, size=1000)
        energy_arr = rng.normal(loc=r["executive_summary"]["Overall Energy Demand"], scale=1500, size=1000)
        water_arr = rng.normal(loc=r["executive_summary"]["Water Consumption"], scale=0.4, size=1000)
        r["uncertainty"] = {"GWP": gwp_arr.tolist(), "Energy": energy_arr.tolist(), "Water": water_arr.tolist()}
    return r

# ---------------- Main rendering function ----------------
def results_page(results: Optional[dict] = None, ai_text: Optional[Any] = None):
    st.set_page_config(layout="wide", page_title="MetalliQ — Final LCA Report")
    st.markdown(
    """
    <style>
      /* Page body / base text for results page */
      .stApp, body {
        color: #083a38 !important; /* dark teal for high contrast */
      }

      /* Improve contrast inside cards */
      .result-card, .stMarkdown, .stText, .stDataFrame {
        color: #083a38 !important;
      }

      /* Make headings clearly visible */
      h1, h2, h3, h4, h5, h6 {
        color: #063735 !important;
      }

      /* Table fonts and header */
      .stDataFrame table {
        color: #063735 !important;
        font-size: 14px;
      }
      .stDataFrame th {
        background: rgba(6, 55, 53, 0.06) !important;
        color: #022f2d !important;
        font-weight: 700;
      }

      /* Buttons and links (dummy export etc) */
      a, a:link, a:visited {
        color: #0f8f88 !important;
      }

      /* tooltips/plot text */
      .plotly .main-svg text {
        fill: #083a38 !important;
      }

      /* small card shading override for readability */
      .card-override {
        background: rgba(255, 255, 255, 0.18) !important; /* glassy transparency */
        backdrop-filter: blur(12px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(12px) saturate(160%) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: rgba(6, 55, 53, 0.92) !important;  /* slightly darker teal text */
        font-weight: 500 !important;  /* make text less faint */
        text-shadow: 0 0 6px rgba(255, 255, 255, 0.35); /* gentle glow for contrast */
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
        border-radius: 12px !important;
        padding: 14px !important;
        transition: all 0.3s ease-in-out;
        gap:8px;
    }
    .card-override:hover {
        background: rgba(255, 255, 255, 0.24) !important;
        transform: scale(1.02);
    }


    </style>
    """,
    unsafe_allow_html=True,
)
    r = safe_results(results)
    ai_data = ensure_ai_dict(ai_text)
    # If no ai_data passed, prefer imported ai_data_example, otherwise fallback to default
    if not ai_data:
        if ai_data_example:
            ai_data = ai_data_example
        else:
            ai_data = {
                "summary": "The analysis identifies the production phase as the primary GWP hotspot. Recommendations focus on recycled content and supplier energy mix.",
                "findings": [
                    {
                        "title": "Mitigate High Global Warming Potential from Primary Steel Production",
                        "priority": "High",
                        "evidence": f"Production stage accounts for approx {r['supply_chain_hotspots'][0]['share_pct']}% of GWP.",
                        "root_cause": "High fossil-fuel energy use in production and low recycled content.",
                        "action_plan": [
                            {"title": "Explore higher recycled-content steel", "effort": "Medium", "confidence": 90},
                            {"title": "Engage suppliers on energy efficiency", "effort": "Medium", "confidence": 80},
                        ],
                    }
                ],
                # Always include ore_warning and ev_recommendation placeholders (user requested always show these)
                "ore_warning": {"text": "Ore grade variability detected: low-grade ores may increase processing emissions.", "severity": "Warning"},
                "ev_charging": {"text": "If transport uses electric vehicles, recommend energy-efficient charging during off-peak renewable supply windows.", "priority": "Advisory"}
            }

    # ---- Top header and export links ----
    st.markdown(
        f"""
        <div style="background:{CARD_BG};padding:20px;border-radius:10px;border:1px solid rgba(0,0,0,0.03)">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <h1 style="margin:0;color:{TITLE};">{r['title']}</h1>
                    <div style="color:{MUTED};font-size:14px">Generated on {r['generated_on']} by {r['generated_by']}</div>
                </div>
                <div style="display:flex;gap:10px;align-items:center;">
                    <!-- Dummy PDF export button will be rendered below by Streamlit -->
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------- ISO Conformance ----------
    st.markdown(f"""
        <div style="background:{CARD_BG};padding:18px;border-radius:10px;border:1px solid rgba(0,120,115,0.06);">
            <strong style="color:{ACCENT_DARK}">ISO 14044 Conformance</strong>
            <div style="color:{MUTED};margin-top:6px">
                This is a screening-level LCA broadly consistent with ISO 14044 principles for internal decision-making. For public comparative statements, a formal critical review is required.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # ---------- Executive Summary cards ----------
    exec_vals = r["executive_summary"]
    c1, c2, c3, c4 = st.columns([1.5,1,1,1])
    c1.markdown(f"<div style='background:{CARD_BG};padding:18px;border-radius:10px'><div style='font-size:13px;color:{MUTED}'>Global Warming Potential</div><div style='font-size:22px;color:{TITLE};font-weight:700'>{exec_vals['Global Warming Potential']:.0f} <span style='font-size:12px;color:{MUTED}'>kg CO₂-eq</span></div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div style='background:{CARD_BG};padding:18px;border-radius:10px'><div style='font-size:13px;color:{MUTED}'>Circularity Score</div><div style='font-size:22px;color:{TITLE};font-weight:700'>{exec_vals['Circularity Score']} <span style='font-size:12px;color:{MUTED}'>%</span></div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div style='background:{CARD_BG};padding:18px;border-radius:10px'><div style='font-size:13px;color:{MUTED}'>Particulate Matter</div><div style='font-size:22px;color:{TITLE};font-weight:700'>{exec_vals['Particulate Matter']:.3g} <span style='font-size:12px;color:{MUTED}'>kg PM2.5-eq</span></div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div style='background:{CARD_BG};padding:18px;border-radius:10px'><div style='font-size:13px;color:{MUTED}'>Water Consumption</div><div style='font-size:22px;color:{TITLE};font-weight:700'>{exec_vals['Water Consumption']} <span style='font-size:12px;color:{MUTED}'>m³</span></div></div>", unsafe_allow_html=True)

    st.markdown("")

    # ---------- Goal & Scope ----------
    st.markdown("<div style='background:transparent;padding:6px'><h3 style='margin:6px 0;color:#0b6b66'>Goal & Scope (ISO 14044)</h3></div>", unsafe_allow_html=True)
    gs = r.get("goal_scope", {})  # <-- safe access, won't raise KeyError

    left, right = st.columns(2)
    with left:
        intended_app_text = gs.get("Intended Application", r.get("executive_summary", {}).get("Intended Application", "Screening assessment for internal R&D"))
        st.markdown(f"**Intended Application**  \n{intended_app_text}")
        system_boundary_text = gs.get("System Boundary", "Cradle-to-Gate")
        st.markdown(f"**System Boundary**  \n{system_boundary_text}")
    with right:
        intended_audience_text = gs.get("Intended Audience", "Internal engineering and sustainability departments")
        st.markdown(f"**Intended Audience**  \n{intended_audience_text}")
        comp_assertion = gs.get("Comparative Assertion for Public", gs.get("comparative_assertion", "No"))
        st.markdown(f"**Comparative Assertion for Public**  \n{comp_assertion}")
    st.markdown("---")

    # ---------- Data Quality & Uncertainty (ADQI) ----------
        # ---------- Data Quality & Uncertainty (ADQI) ----------
    st.markdown("<h3 style='color:#0b6b66'>Data Quality & Uncertainty</h3>", unsafe_allow_html=True)
    dq = r.get("data_quality", {})  # safe access

    # read values with defaults if missing
    rel = dq.get("Reliability", dq.get("reliability", "4/5"))
    comp = dq.get("Completeness", dq.get("completeness", "4/5"))
    temp = dq.get("Temporal", dq.get("temporal", "4/5"))
    geo = dq.get("Geographical", dq.get("geographical", "4/5"))
    tech = dq.get("Technological", dq.get("technological", "4/5"))

    # aggregated ADQI: try common keys, fall back to a computed average
    agg_adqi = dq.get("Aggregated ADQI", dq.get("aggregated_adqi", None))
    if agg_adqi is None:
        # try to compute numeric average when slider integers are available
        def parse_score(s):
            try:
                if isinstance(s, str) and "/" in s:
                    return float(s.split("/")[0])
                return float(s)
            except Exception:
                return None
        parts = [parse_score(x) for x in (rel, comp, temp, geo, tech)]
        nums = [p for p in parts if p is not None]
        if nums:
            agg_adqi = round(sum(nums) / len(nums), 2)
        else:
            agg_adqi = 4.0

    uncertainty_pct = dq.get("Result Uncertainty pct", dq.get("result_uncertainty_pct", dq.get("uncertainty_pct", 14)))

    a, b = st.columns([2,1])
    with a:
        # show the individual scores; they are strings like "4/5" in many cases
        st.markdown(f"**Reliability Score:** {rel}  \n**Completeness Score:** {comp}  \n**Temporal Score:** {temp}  \n**Geographical Score:** {geo}  \n**Technological Score:** {tech}")
    with b:
        st.markdown(
            f"<div style='background:{CARD_BG};padding:14px;border-radius:8px;text-align:center'>"
            f"<div style='color:{MUTED}'>Aggregated Data Quality</div>"
            f"<div style='font-size:28px;color:{ACCENT_DARK};font-weight:700'>{agg_adqi}</div>"
            f"<div style='color:{MUTED};margin-top:6px'>Result Uncertainty<br><strong>±{uncertainty_pct}%</strong></div>"
            f"</div>",
            unsafe_allow_html=True
        )


    st.markdown("---")

    # ---------- Supply Chain Hotspots ----------
    st.markdown("<h3 style='color:#0b6b66'>Supply Chain Hotspots</h3>", unsafe_allow_html=True)
    for i, item in enumerate(r["supply_chain_hotspots"]):
        # highlight first card
        border = f"border:4px solid rgba(255,150,20,0.22);background:linear-gradient(90deg, rgba(255,255,255,0.30), rgba(255,245,230,0.02));" if i == 0 else f"background:{CARD_BG};border:1px solid rgba(0,0,0,0.03);"
        st.markdown(f"<div style='padding:12px;border-radius:8px;{border}display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'><div><strong>{item['title']}</strong><div style='color:{MUTED};font-size:13px'>{item['desc']}</div></div><div style='font-weight:800;color:{ACCENT_DARK}'>{item['share_pct']}%<div style='color:{MUTED};font-size:12px'>of GWP Impact</div></div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- Interactive Process Lifecycle ----------
    st.markdown("<h3 style='color:#0b6b66'>Interactive Process Lifecycle</h3>", unsafe_allow_html=True)
    mf_labels = r["material_flow"]["labels"]
    st.markdown("<div style='background:{0};padding:12px;border-radius:12px'>{1}</div>".format(CARD_BG, ""), unsafe_allow_html=True)
    cols = st.columns(len(mf_labels))
    for idx, lbl in enumerate(mf_labels):
        with cols[idx]:
            st.write(f"<div style='text-align:center'><div style='width:64px;height:64px;border-radius:40px;border:2px solid {ACCENT};display:flex;align-items:center;justify-content:center;margin:auto;background:rgba(255,255,255,0.95)'>🔵</div><div style='font-size:13px;margin-top:6px;color:{MUTED}'>{lbl}</div></div>", unsafe_allow_html=True)
    # stage selector shows stage metrics
    sel = st.selectbox("Select stage to view stage-specific metrics", mf_labels, index=0)
    # create mock stage metrics
    total_gwp = r["executive_summary"]["Global Warming Potential"]
    stage_share = 0.2 if sel == mf_labels[0] else (0.15 if sel == mf_labels[1] else 0.2 if sel == mf_labels[2] else 0.25 if sel == mf_labels[3] else 0.2)
    stage_metrics = {"GWP": round(total_gwp * stage_share, 1), "Energy": round(r["executive_summary"]["Overall Energy Demand"] * stage_share, 1), "Water": round(r["executive_summary"]["Water Consumption"] * stage_share, 3)}
    st.markdown(f"<div style='background:{CARD_BG};padding:12px;border-radius:8px'><strong>{sel}</strong> — GWP: <strong>{stage_metrics['GWP']}</strong> kg CO₂-eq • Energy: <strong>{stage_metrics['Energy']}</strong> MJ • Water: <strong>{stage_metrics['Water']}</strong> m³</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- AI-Generated Life Cycle Interpretation ----------
    st.markdown("<h3 style='color:#0b6b66'>AI-Generated Life Cycle Interpretation</h3>", unsafe_allow_html=True)
    ai_lifecycle_text = ai_data.get("lifecycle_interpretation", None) or ai_data.get("summary", "")
    # if a long paragraph isn't available, use a default narrative (from your screenshot)
    if not ai_lifecycle_text or len(ai_lifecycle_text.strip()) < 20:
        ai_lifecycle_text = (
            "The analysis clearly identifies the Global Warming Potential (GWP) from the production phase as the most significant environmental impact. "
            "Mean GWP is approx 2288 kg CO₂-eq, with production contributing the majority of the impact. The Circularity Score of 50% indicates room for improvement in material recovery. "
            "A Monte Carlo simulation estimates result uncertainty at approx ±14% for GWP (95% CI 2105–2472 kg CO₂-eq). These findings are suitable for internal R&D comparisons and directional guidance."
        )
    st.markdown(f"<div style='background:{CARD_BG};padding:16px;border-radius:10px;color:{MUTED}'>{ai_lifecycle_text}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- Circularity Analysis + Sankey side-by-side ----------
    st.markdown("<h3 style='color:#0b6b66'>Circularity Analysis & Material Flow</h3>", unsafe_allow_html=True)
    left, right = st.columns([1,1.4])
    with left:
        circ = r["circularity"]
        # gauge as donut using pie with hole and one slice colored
        fig_gauge = go.Figure(data=[go.Pie(labels=["Circular", "Remaining"], values=[circ["Circularity Rate"], 100-circ["Circularity Rate"]], hole=0.7, marker=dict(colors=[ACCENT_DARK, "rgba(200,200,200,0.35)"]), textinfo='none')])
        fig_gauge.add_annotation(dict(text=f"<b>{circ['Circularity Rate']}%</b><br><span style='font-size:12px;color:{MUTED}'>Circularity</span>", x=0.5, y=0.5, showarrow=False))
        plot_style(fig_gauge, height=320)
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown(f"<div style='background:{CARD_BG};padding:10px;border-radius:8px'><div>Recyclability Rate: <strong>{circ['Recyclability Rate']}%</strong></div><div>Recovery Efficiency: <strong>{circ['Recovery Efficiency']}%</strong></div><div>Secondary Material Content: <strong>{circ['Secondary Material Content']}%</strong></div></div>", unsafe_allow_html=True)

    with right:
        # Sankey
        mf = r["material_flow"]
        try:
            node = dict(label=mf["labels"], pad=15, thickness=14)
            link = dict(source=mf["source"], target=mf["target"], value=mf["value"])
            sankey = go.Figure(go.Sankey(node=node, link=link))
            plot_style(sankey, title="Material Flow Sankey", height=380)
            st.plotly_chart(sankey, use_container_width=True)
        except Exception as e:
            st.error("Sankey failed to render")
            st.write(e)

    st.markdown("---")

    # ---------- Extended Circularity Metrics ----------
    st.markdown("<h3 style='color:#0b6b66'>Extended Circularity Metrics</h3>", unsafe_allow_html=True)
    metrics = r["extended_metrics"]
    # 4 columns grid
    cols = st.columns(4)
    keys = list(metrics.keys())
    for i, k in enumerate(keys):
        cols[i % 4].markdown(f"<div style='background:{CARD_BG};padding:14px;margin:10px;border-radius:8px;text-align:center'><div style='color:{MUTED}'>{k}</div><div style='font-size:20px;color:{ACCENT_DARK};font-weight:700'>{metrics[k]}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- Key Impact Profiles ----------
    st.markdown("<h3 style='color:#0b6b66'>Key Impact Profiles</h3>", unsafe_allow_html=True)
    impact_df = pd.DataFrame(r["impact_list"], columns=["Impact Metric", "Value", "Unit"])
    # pick subset of common categories for the big bar chart
    top_keys = ["Global Warming Potential", "Energy Demand", "Water Consumption", "Eutrophication", "Acidification"]
    df_bar = impact_df[impact_df["Impact Metric"].isin(top_keys)]
    if df_bar.empty:
        df_bar = impact_df.head(5)
    fig_bar = px.bar(df_bar, x="Impact Metric", y="Value", text="Value")
    plot_style(fig_bar, height=360)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # ---------- GWP Contribution & Energy Source ----------
    st.markdown("<div style='display:flex;gap:12px'>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1,1])
    with col_a:
        df_gwp = pd.DataFrame(list(r["gwp_breakdown"].items()), columns=["Category", "Share"])
        pie = px.pie(df_gwp, names="Category", values="Share", hole=0.4)
        plot_style(pie, "GWP Contribution Analysis", height=300)
        st.plotly_chart(pie, use_container_width=True)
    with col_b:
        df_energy = pd.DataFrame(list(r["energy_breakdown"].items()), columns=["Source", "Value"])
        bar = px.bar(df_energy, x="Value", y="Source", orientation="h", text="Value")
        plot_style(bar, "Energy Source Breakdown (MJ)", height=300)
        st.plotly_chart(bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

   # ---------- Detailed Impact Assessment (chart + table) ----------
    st.markdown("<h3 style='color:#0b6b66'>Detailed Impact Assessment</h3>", unsafe_allow_html=True)

    # -- Use mock direct data for the full list of requested impact metrics --
    impact_names = [
        "Global Warming Potential",
        "Acidification Potential",
        "Photochemical Ozone Creation",
        "Abiotic Depletion (Fossil)",
        "Fresh Water Ecotoxicity",
        "Energy Demand",
        "Eutrophication Demand",
        "Particulate Matter Formation",
        "Human Toxicity (Cancer)",
        "Ionizing Radiation",
        "Water Consumption",
        "Ozone Depletion Potential",
        "Abiotic Depletion (Elements)",
        "Human Toxicity (Non-Cancer)",
        "Land Use"
    ]

    # plausible mock values (adjust if you want different magnitudes)
    mock_values = {
        "Global Warming Potential": 2288.0,           # kg CO2-eq
        "Acidification Potential": 4.11,              # kg SO2-eq
        "Photochemical Ozone Creation": 2.29,         # kg NMVOC-eq
        "Abiotic Depletion (Fossil)": 29288.0,        # MJ
        "Fresh Water Ecotoxicity": 22.88,             # CTUe
        "Energy Demand": 26626.0,                     # MJ
        "Eutrophication Demand": 1.14,                # kg PO4-eq
        "Particulate Matter Formation": 0.763,        # kg PM2.5-eq
        "Human Toxicity (Cancer)": 0.012,             # CTUh
        "Ionizing Radiation": 0.00035,                # kBq U235-eq (example)
        "Water Consumption": 4.7,                     # m3
        "Ozone Depletion Potential": 0.00005,         # kg CFC-11-eq
        "Abiotic Depletion (Elements)": 0.0012,       # kg Sb-eq (example)
        "Human Toxicity (Non-Cancer)": 2.29,          # CTUh
        "Land Use": 228.77                             # m2·year
    }

    # units mapping
    units = {
        "Global Warming Potential": "kg CO₂-eq",
        "Acidification Potential": "kg SO₂-eq",
        "Photochemical Ozone Creation": "kg NMVOC-eq",
        "Abiotic Depletion (Fossil)": "MJ",
        "Fresh Water Ecotoxicity": "CTUe",
        "Energy Demand": "MJ",
        "Eutrophication Demand": "kg PO₄-eq",
        "Particulate Matter Formation": "kg PM2.5-eq",
        "Human Toxicity (Cancer)": "CTUh",
        "Ionizing Radiation": "kBq U235-eq",
        "Water Consumption": "m³",
        "Ozone Depletion Potential": "kg CFC-11-eq",
        "Abiotic Depletion (Elements)": "kg Sb-eq",
        "Human Toxicity (Non-Cancer)": "CTUh",
        "Land Use": "m²·year"
    }

    # Build DataFrame from the mock values
    impact_rows = []
    for name in impact_names:
        val = mock_values.get(name, 0.0)
        unit = units.get(name, "")
        impact_rows.append({"Impact Metric": name, "Value": val, "Unit": unit})
    impact_df = pd.DataFrame(impact_rows)

    # Chart: horizontal bar sorted by value (descending)
    impact_df["ValueNum"] = pd.to_numeric(impact_df["Value"], errors="coerce")
    impact_df_sorted = impact_df.sort_values("ValueNum", ascending=True)  # ascending True for horizontal bar bottom->top
    fig_imp = px.bar(
        impact_df_sorted,
        x="ValueNum",
        y="Impact Metric",
        orientation="h",
        text="ValueNum",
        labels={"ValueNum": "Value", "Impact Metric": "Impact Metric"}
    )
    plot_style(fig_imp, height=480)
    st.plotly_chart(fig_imp, use_container_width=True)

    # Show the table and provide a CSV download link (no external file required)
    st.dataframe(impact_df.drop(columns=["ValueNum"]), use_container_width=True, height=260)
    csv_download_link(impact_df.drop(columns=["ValueNum"]), filename="detailed_impacts_mock.csv", label="📥 Download Detailed Impacts CSV")

    st.markdown("---")

    # ---------- Uncertainty Dashboard ----------
    st.markdown("<h3 style='color:#0b6b66'>Uncertainty Dashboard</h3>", unsafe_allow_html=True)
    unc = r["uncertainty"]
    col_g, col_e, col_w = st.columns(3)
    def hist_col(col, arr, label, unit):
        arr = np.array(arr)
        mean = np.mean(arr)
        ci = np.percentile(arr, [2.5, 97.5])
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=arr, nbinsx=30, marker=dict(color=ACCENT)))
        fig.add_vline(x=mean, line_color=ACCENT_DARK, line_width=2)
        fig.add_vline(x=ci[0], line_dash="dash", line_color=ACCENT_DARK)
        fig.add_vline(x=ci[1], line_dash="dash", line_color=ACCENT_DARK)
        plot_style(fig, title=f"{label} distribution", height=300)
        col.plotly_chart(fig, use_container_width=True)
        col.markdown(f"**Mean:** {mean:.2f} {unit}  •  **95% CI:** [{ci[0]:.2f}, {ci[1]:.2f}]")
    hist_col(col_g, unc["GWP"], "Global Warming Potential", "kg CO₂-eq")
    hist_col(col_e, unc["Energy"], "Energy Demand", "MJ")
    hist_col(col_w, unc["Water"], "Water Consumption", "m³")

    st.markdown("---")

    # ---------- AI-Powered Insights & Recommendations (always show ore & ev warnings) ----------
    st.markdown("<h3 style='color:#0b6b66'>AI-Powered Insights & Recommendations</h3>", unsafe_allow_html=True)
    # If module provided a display function, prefer using it (keeps styling consistent)
    try:
        extra_ctx = {"executive_summary": r["executive_summary"], "supply_chain_hotspots": r["supply_chain_hotspots"]}
        if ai_recommendation and hasattr(ai_recommendation, "display_ai_recommendations"):
            # ensure ore_grade and ev recommendations exist in ai_data
            if "ore_warning" not in ai_data:
                ai_data["ore_warning"] = {"text": "Ore grade variability: potential emissions increase.", "severity": "Warning"}
            if "ev_charging" not in ai_data:
                ai_data["ev_charging"] = {"text": "Recommend off-peak charging during high renewable generation.", "priority": "Advisory"}
            ai_recommendation.display_ai_recommendations(ai_data, extra_context=extra_ctx)
        else:
            # Render built-in styled AI card list
            st.markdown(f"<div style='background:{CARD_BG};padding:14px;border-radius:10px'>", unsafe_allow_html=True)
            st.markdown(f"**AI Summary:**  \n{ai_data.get('summary','No summary available.')}")
            findings = ai_data.get("findings", [])
            if not findings:
                findings = [{
                    "title": "Mitigate High Global Warming Potential from Primary Steel Production",
                    "priority": "High",
                    "evidence": "Production stage is dominant contributor to GWP.",
                    "root_cause": "Energy-intensive primary steel production.",
                    "action_plan": [
                        {"title": "Increase recycled content", "effort": "Medium", "confidence": 90},
                        {"title": "Supplier energy engagement", "effort": "Medium", "confidence": 80},
                    ]
                }]
            for f in findings:
                st.markdown(f"### {f['title']}  \n**Priority:** {f.get('priority','Medium')}")
                st.markdown(f"**Evidence:** {f.get('evidence','-')}")
                st.markdown(f"**Root Cause:** {f.get('root_cause','-')}")
                st.markdown("**Action Plan:**")
                for ap in f.get("action_plan", []):
                    st.markdown(f"- {ap.get('title')}  • Effort: {ap.get('effort','N/A')}  • Confidence: {ap.get('confidence','N/A')}%")
            # Always show ore grade & EV advice
            ore = ai_data.get("ore_warning", {"text":"Ore grade warning not provided."})
            ev = ai_data.get("ev_charging", {"text":"EV charging recommendations not provided."})
            st.markdown("---")
            st.markdown(f"**Ore Grade Warning:** {ore.get('text')}")
            st.markdown(f"**EV Charging Recommendation:** {ev.get('text')}")
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error("Failed to render AI recommendations.")
        st.write(str(e))

    st.markdown("---")
    # ---------- Primary vs. Recycled Scenario Comparison (table + charts) ----------
    st.markdown("<h3 style='color:#0b6b66'>Primary vs. Recycled Route Comparison</h3>", unsafe_allow_html=True)

    # defensive: ensure results variable exists
    if results is None:
        results = {}

    # try to get data
    df_pvr = pd.DataFrame(results.get("primary_vs_recycled", []))

    # --- Auto-fix: if columns are lowercase or wrong ---
    if not df_pvr.empty:
        # normalize columns
        df_pvr.columns = [str(c).strip().capitalize() for c in df_pvr.columns]
        # check if we have needed columns, otherwise rename known variants
        rename_map = {}
        for col in df_pvr.columns:
            if col.lower() == "primary":
                rename_map[col] = "Primary"
            elif col.lower() == "recycled":
                rename_map[col] = "Recycled"
            elif col.lower() == "metric":
                rename_map[col] = "Metric"
        if rename_map:
            df_pvr.rename(columns=rename_map, inplace=True)

    # --- If still empty or missing columns, build mock fallback ---
    if df_pvr.empty or not all(c in df_pvr.columns for c in ["Metric", "Primary", "Recycled"]):
        df_pvr = pd.DataFrame([
            {"Metric": "GWP (kg CO2-eq)", "Primary": 2485, "Recycled": 597},
            {"Metric": "Energy (GJ)", "Primary": 28.77, "Recycled": 6.17},
            {"Metric": "Water (m³)", "Primary": 5.0, "Recycled": 2.0},
            {"Metric": "Acidification (kg SO2-eq)", "Primary": 4.40, "Recycled": 1.35},
            {"Metric": "Eutrophication (kg PO4-eq)", "Primary": 1.24, "Recycled": 0.30},
        ])

    # --- Compute savings ---
    def compute_savings(p, r):
        try:
            if p == 0:
                return "—"
            pct = (p - r) / float(p) * 100.0
            return f"▼ {pct:.1f}%"
        except Exception:
            return "—"

    df_pvr["Savings"] = df_pvr.apply(
        lambda row: compute_savings(row.get("Primary", 0), row.get("Recycled", 0)),
        axis=1,
    )

    # --- Format table display ---
    display_df = df_pvr.copy()
    for col in ["Primary", "Recycled"]:
        if pd.api.types.is_numeric_dtype(display_df[col]):
            display_df[col] = display_df[col].apply(lambda v: f"{v:,.2f}")

    st.markdown("<div class='card-override' style='padding:10px;border-radius:8px'>", unsafe_allow_html=True)
    st.table(display_df)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")  # spacing

    # --- Charts ---
    try:
        df_melt = df_pvr.melt(
            id_vars=["Metric", "Savings"],
            value_vars=["Primary", "Recycled"],
            var_name="Scenario",
            value_name="Value"
        )
        PRIMARY_COLOR = "#6c757d"
        RECYCLED_COLOR = "#0f8f88"
        color_map = {"Primary": PRIMARY_COLOR, "Recycled": RECYCLED_COLOR}

        # grouped bar chart
        fig_cmp = px.bar(
            df_melt,
            x="Metric",
            y="Value",
            color="Scenario",
            barmode="group",
            text="Value",
            color_discrete_map=color_map
        )
        fig_cmp.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        fig_cmp.update_layout(
            height=380,
            legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_tickangle=-20,
            margin=dict(l=40, r=30, t=40, b=80)
        )
        plot_style(fig_cmp, height=380)
        st.plotly_chart(fig_cmp, use_container_width=True)

        # horizontal bar chart
        df_vis = df_pvr.sort_values("Primary", ascending=False)
        fig_vis = go.Figure()
        fig_vis.add_trace(go.Bar(
            y=df_vis["Metric"],
            x=df_vis["Primary"],
            orientation='h',
            name='Primary Route',
            marker=dict(color=PRIMARY_COLOR),
            hovertemplate='%{y}<br>Primary: %{x}<extra></extra>'
        ))
        fig_vis.add_trace(go.Bar(
            y=df_vis["Metric"],
            x=df_vis["Recycled"],
            orientation='h',
            name='Recycled Route',
            marker=dict(color=RECYCLED_COLOR),
            hovertemplate='%{y}<br>Recycled: %{x}<extra></extra>'
        ))
        fig_vis.update_layout(
            barmode='group',
            height=360,
            margin=dict(l=150, r=40, t=30, b=30)
        )
        plot_style(fig_vis, height=360)
        st.plotly_chart(fig_vis, use_container_width=True)
    except Exception as e:
        st.error("Comparison chart failed to render")
        st.write(str(e))




    st.markdown("---")

    st.markdown("<div style='color:rgba(0,0,0,0.6);font-size:12px'>Generated by MetalliQ · Screening-level LCA. For formal comparative reporting follow ISO 14044 critical review processes.</div>", unsafe_allow_html=True)

# If executed directly, run a demo render
if __name__ == "__main__":
    results_page(None, None)
