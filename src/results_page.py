# results_page.py
"""
Final results page for MetalliQ LCA platform (Workspace-themed)
- Preserves all original sections & logic from your file
- Multi-tone futuristic palette: #00EFFF -> #00B8CC -> #02C39A -> #7CF4E3
- Glassy white card style, readable fonts
- Always displays AI ore grade warning and EV charging suggestions
- No actual PDF/CSV download via st.download_button (CSV link provided via data URI)
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

# Prefer local ai_recommendation module if available
try:
    import ai_recommendation
    from ai_recommendation import ai_data_example
except Exception:
    ai_recommendation = None
    ai_data_example = None

# ---------------- Theme colors (multi-tone futuristic workspace) ----------------
ACCENT_1 = "#00EFFF"   # bright cyan
ACCENT_2 = "#00B8CC"   # teal
ACCENT_3 = "#02C39A"   # green-teal
ACCENT_4 = "#7CF4E3"   # pale aqua
TEXT = "#083a38"       # dark teal text for readability on glass
HEADER = "#0b6b66"     # header color
CARD_GLASS = "rgba(255,255,255,0.85)"  # glassy card background (light)
CARD_BORDER = "rgba(3,120,115,0.08)"

# ---------------- Helpers ----------------
def csv_download_link(df: pd.DataFrame, filename: str = "table.csv", label: str = "📥 Download CSV"):
    """
    Create a base64 download link for a pandas DataFrame (no st.download_button used).
    """
    try:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:text/csv;base64,{b64}" download="{filename}" style="text-decoration:none;color:{ACCENT_2};font-weight:600">{label}</a>'
        st.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        st.write("CSV export failed:", e)

def plot_style(fig: go.Figure, title: Optional[str] = None, height: Optional[int] = None):
    """
    Unified plot styling for Plotly figures to match workspace theme.
    """
    layout = dict(
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',
        margin=dict(l=40, r=24, t=48 if title else 12, b=40),
        font=dict(color=TEXT, family="Poppins, sans-serif", size=12),
        title=dict(text=title or "", x=0.5, xanchor="center", font=dict(color=HEADER, family="Orbitron, sans-serif")),
        legend=dict(bgcolor='rgba(255,255,255,0.6)', bordercolor='rgba(0,0,0,0.05)', font=dict(color=TEXT)),
        xaxis=dict(color=TEXT, gridcolor="rgba(0,0,0,0.06)", title_font=dict(color=HEADER)),
        yaxis=dict(color=TEXT, gridcolor="rgba(0,0,0,0.06)", title_font=dict(color=HEADER))
    )
    fig.update_layout(layout)
    if height:
        fig.update_layout(height=height)

    # Tune traces colors if possible
    for trace in fig.data:
        try:
            # Bars: use gradient-like hues by specifying the base color
            if isinstance(trace, go.Bar):
                trace.marker.line = dict(color="rgba(0,0,0,0.04)", width=0.5)
            # Pie: ensure marker colors cycle through our palette
            if isinstance(trace, go.Pie):
                trace.marker = dict(colors=[ACCENT_1, ACCENT_2, ACCENT_3, ACCENT_4], line=dict(color="rgba(0,0,0,0.04)", width=0.5))
                trace.textfont = dict(color="#063735")
        except Exception:
            pass
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
    r.setdefault("generated_on", datetime.date.today().strftime("%d %b %Y"))
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
        "labels": ["Metal Ore Extraction", "Manufacturing", "Transportation", "Use Phase", "End of Lifecycle", "Recycling Process", "Landfill"],
        "source": [0, 1, 1, 2, 3, 5],
        "target": [1, 2, 3, 4, 5, 6],
        "value": [100, 80, 50, 40, 30, 15]
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
    # ensure primary_vs_recycled is present in a shape we expect
    if "primary_vs_recycled" not in r or not isinstance(r["primary_vs_recycled"], list):
        r["primary_vs_recycled"] = [
            {"Metric": "GWP (kg CO2-eq)", "Primary": 2485, "Recycled": 597},
            {"Metric": "Energy (GJ)", "Primary": 28.77, "Recycled": 6.17},
            {"Metric": "Water (m³)", "Primary": 5.0, "Recycled": 2.0},
        ]
    return r

# ---------------- Main rendering function ----------------
def results_page(results: Optional[dict] = None, ai_text: Optional[Any] = None):
    st.set_page_config(layout="wide", page_title="MetalliQ — Final LCA Report")
    # Accent header progress bar (faint, static as requested)
    st.markdown(f"""
    <style>
    .top-accent {{
        height: 6px;
        width: 100%;
        background: linear-gradient(90deg, rgba(0,231,255,0.12) 0%, rgba(0,184,204,0.12) 40%, rgba(2,195,154,0.12) 70%);
        border-radius: 4px;
        margin-bottom: 12px;
        box-shadow: 0 2px 12px rgba(2,195,154,0.04) inset;
    }}
    </style>
    <div class="top-accent"></div>
    """, unsafe_allow_html=True)

    # Page CSS for glass cards and fonts
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@300;400;600&display=swap');
    body, .stApp {{
        background: linear-gradient(180deg, #F7FEFF 0%, #FFFFFF 100%) !important;
        color: {TEXT} !important;
        font-family: 'Poppins', sans-serif;
    }}
    h1,h2,h3,h4 {{
        font-family: 'Orbitron', sans-serif;
        color: {HEADER} !important;
    }}
    .card-override {{
        background: {CARD_GLASS} !important;
        border-radius: 12px !important;
        border: 1px solid {CARD_BORDER} !important;
        padding: 12px !important;
        box-shadow: 0 6px 20px rgba(2,195,154,0.06) !important;
    }}
    .metric-number {{
        color: {ACCENT_2} !important;
        font-weight:700;
        font-size:20px;
    }}
    .plotly .main-svg text {{
        fill: {TEXT} !important;
    }}
    /* Make table headers readable */
    .stDataFrame table th {{
        background: rgba(2,195,154,0.06) !important;
        color: {TEXT} !important;
        font-weight:600;
    }}
    </style>
    """, unsafe_allow_html=True)

    # prepare results safely
    r = safe_results(results)
    ai_data = ensure_ai_dict(ai_text)
    # if no ai_data passed, fallback to imported example or default
    if not ai_data:
        if ai_data_example:
            ai_data = ai_data_example
        else:
            ai_data = {"summary": "Production phase dominates GWP; consider recycled content and supplier energy mix.",
                       "findings": [], "ore_warning": {"text": "Ore grade variability detected: low-grade ores may increase processing emissions.", "severity": "Warning"},
                       "ev_charging": {"text": "Recommend off-peak charging during renewable supply windows.", "priority": "Advisory"}}

    # ---------- Header ----------
    st.markdown(f"""
        <div class="card-override" style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <h1 style="margin:0">{r.get('title','LCA Final Report')}</h1>
                <div style="color:rgba(3,60,57,0.8);font-size:13px;margin-top:6px">Generated on {r.get('generated_on')} by {r.get('generated_by')}</div>
            </div>
            <div style="display:flex;gap:10px;align-items:center;">
                <button style="background:linear-gradient(90deg,{ACCENT_1},{ACCENT_2});border:none;color:white;padding:8px 12px;border-radius:8px;font-weight:700;">Export PDF (dummy)</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------- ISO Conformance ----------
    st.markdown(f"""
        <div class="card-override" style="padding:14px;">
            <strong style="color:{ACCENT_3}">ISO 14044 Conformance</strong>
            <div style="color:rgba(3,60,57,0.8);margin-top:8px">
                This is a screening-level LCA broadly consistent with ISO 14044 principles for internal decision-making. For public comparative statements, a formal critical review is required.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # ---------- Executive Summary cards ----------
    exec_vals = r.get("executive_summary", {})
    c1, c2, c3, c4 = st.columns([1.6, 1, 1, 1])
    c1.markdown(f"<div class='card-override'><div style='font-size:13px;color:rgba(3,60,57,0.75)'>Global Warming Potential</div><div class='metric-number'>{exec_vals.get('Global Warming Potential',0):.0f} <span style='font-size:12px;color:rgba(3,60,57,0.6)'>kg CO₂-eq</span></div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card-override'><div style='font-size:13px;color:rgba(3,60,57,0.75)'>Circularity Score</div><div class='metric-number'>{exec_vals.get('Circularity Score',0)} <span style='font-size:12px;color:rgba(3,60,57,0.6)'>%</span></div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card-override'><div style='font-size:13px;color:rgba(3,60,57,0.75)'>Particulate Matter</div><div class='metric-number'>{exec_vals.get('Particulate Matter',0):.3g} <span style='font-size:12px;color:rgba(3,60,57,0.6)'>kg PM2.5-eq</span></div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='card-override'><div style='font-size:13px;color:rgba(3,60,57,0.75)'>Water Consumption</div><div class='metric-number'>{exec_vals.get('Water Consumption',0)} <span style='font-size:12px;color:rgba(3,60,57,0.6)'>m³</span></div></div>", unsafe_allow_html=True)

    st.markdown("")

    # ---------- Goal & Scope ----------
    st.markdown("<h3 style='margin:6px 0'>Goal & Scope (ISO 14044)</h3>", unsafe_allow_html=True)
    gs = r.get("goal_scope", {})
    left, right = st.columns(2)
    with left:
        intended_app_text = gs.get("Intended Application", "Screening assessment for internal R&D")
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
    st.markdown("<h3 style='margin:6px 0'>Data Quality & Uncertainty</h3>", unsafe_allow_html=True)
    dq = r.get("data_quality", {})
    # read values with defaults if missing
    rel = dq.get("Reliability", dq.get("reliability", "4/5"))
    comp = dq.get("Completeness", dq.get("completeness", "4/5"))
    temp = dq.get("Temporal", dq.get("temporal", "4/5"))
    geo = dq.get("Geographical", dq.get("geographical", "4/5"))
    tech = dq.get("Technological", dq.get("technological", "4/5"))

    agg_adqi = dq.get("Aggregated ADQI", dq.get("aggregated_adqi", None))
    if agg_adqi is None:
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
        st.markdown(f"**Reliability Score:** {rel}  \n**Completeness Score:** {comp}  \n**Temporal Score:** {temp}  \n**Geographical Score:** {geo}  \n**Technological Score:** {tech}")
    with b:
        st.markdown(
            f"<div class='card-override' style='text-align:center'>"
            f"<div style='color:rgba(3,60,57,0.75)'>Aggregated Data Quality</div>"
            f"<div style='font-size:28px;color:{ACCENT_2};font-weight:700'>{agg_adqi}</div>"
            f"<div style='color:rgba(3,60,57,0.6);margin-top:6px'>Result Uncertainty<br><strong>±{uncertainty_pct}%</strong></div>"
            f"</div>", unsafe_allow_html=True
        )

    st.markdown("---")

    # ---------- Supply Chain Hotspots ----------
    st.markdown("<h3 style='margin:6px 0'>Supply Chain Hotspots</h3>", unsafe_allow_html=True)
    for i, item in enumerate(r.get("supply_chain_hotspots", [])):
        border = f"border:2px solid rgba(3,120,115,0.12);background:linear-gradient(90deg, rgba(255,255,255,0.95), rgba(255,255,255,0.90));" if i == 0 else f"background:transparent;border:1px solid {CARD_BORDER};"
        st.markdown(f"<div class='card-override' style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;{border}'>"
                    f"<div><strong>{item['title']}</strong><div style='color:rgba(3,60,57,0.75);font-size:13px'>{item['desc']}</div></div>"
                    f"<div style='font-weight:800;color:{ACCENT_2}'>{item['share_pct']}%<div style='color:rgba(3,60,57,0.6);font-size:12px'>of GWP Impact</div></div></div>",
                    unsafe_allow_html=True)

    st.markdown("---")

    # ---------- Interactive Process Lifecycle ----------
    st.markdown("<h3 style='margin:6px 0'>Interactive Process Lifecycle</h3>", unsafe_allow_html=True)
    mf_labels = r["material_flow"]["labels"]
    st.markdown(f"<div class='card-override' style='padding:12px;margin-bottom:8px'></div>", unsafe_allow_html=True)
    cols = st.columns(len(mf_labels))
    for idx, lbl in enumerate(mf_labels):
        with cols[idx]:
            st.write(f"<div style='text-align:center'><div style='width:64px;height:64px;border-radius:40px;border:2px solid {ACCENT_1};display:flex;align-items:center;justify-content:center;margin:auto;background:linear-gradient(180deg, rgba(255,255,255,0.95), rgba(255,255,255,0.9))'>🔵</div><div style='font-size:13px;margin-top:6px;color:rgba(3,60,57,0.8)'>{lbl}</div></div>", unsafe_allow_html=True)
    sel = st.selectbox("Select stage to view stage-specific metrics", mf_labels, index=0)
    total_gwp = r["executive_summary"]["Global Warming Potential"]
    stage_share = 0.2 if sel == mf_labels[0] else (0.15 if sel == mf_labels[1] else 0.2 if sel == mf_labels[2] else 0.25 if sel == mf_labels[3] else 0.2)
    stage_metrics = {"GWP": round(total_gwp * stage_share, 1), "Energy": round(r["executive_summary"]["Overall Energy Demand"] * stage_share, 1), "Water": round(r["executive_summary"]["Water Consumption"] * stage_share, 3)}
    st.markdown(f"<div class='card-override'><strong>{sel}</strong> — GWP: <strong>{stage_metrics['GWP']}</strong> kg CO₂-eq • Energy: <strong>{stage_metrics['Energy']}</strong> MJ • Water: <strong>{stage_metrics['Water']}</strong> m³</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- AI-Generated Life Cycle Interpretation ----------
    st.markdown("<h3 style='margin:6px 0'>AI-Generated Life Cycle Interpretation</h3>", unsafe_allow_html=True)
    ai_lifecycle_text = ai_data.get("lifecycle_interpretation", None) or ai_data.get("summary", "")
    if not ai_lifecycle_text or len(ai_lifecycle_text.strip()) < 20:
        ai_lifecycle_text = (
            "The analysis clearly identifies the Global Warming Potential (GWP) from the production phase as the most significant environmental impact. "
            "Mean GWP is approx 2288 kg CO₂-eq, with production contributing the majority of the impact. The Circularity Score of 50% indicates room for improvement in material recovery. "
            "A Monte Carlo simulation estimates result uncertainty at approx ±14% for GWP (95% CI 2105–2472 kg CO₂-eq)."
        )
    st.markdown(f"<div class='card-override' style='padding:16px;color:rgba(3,60,57,0.9)'>{ai_lifecycle_text}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- Circularity Analysis + Sankey ----------
    st.markdown("<h3 style='margin:6px 0'>Circularity Analysis & Material Flow</h3>", unsafe_allow_html=True)
    left, right = st.columns([1,1.4])
    with left:
        circ = r["circularity"]
        fig_gauge = go.Figure(data=[go.Pie(labels=["Circular", "Remaining"], values=[circ["Circularity Rate"], 100-circ["Circularity Rate"]], hole=0.66, marker=dict(colors=[ACCENT_2, "rgba(200,200,200,0.25)"]), textinfo='none')])
        fig_gauge.add_annotation(dict(text=f"<b>{circ['Circularity Rate']}%</b><br><span style='font-size:12px;color:rgba(3,60,57,0.8)'>Circularity</span>", x=0.5, y=0.5, showarrow=False))
        plot_style(fig_gauge, height=320)
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown(f"<div class='card-override' style='padding:10px'>"
                    f"<div>Recyclability Rate: <strong>{circ['Recyclability Rate']}%</strong></div>"
                    f"<div>Recovery Efficiency: <strong>{circ['Recovery Efficiency']}%</strong></div>"
                    f"<div>Secondary Material Content: <strong>{circ['Secondary Material Content']}%</strong></div>"
                    f"</div>", unsafe_allow_html=True)

    with right:
        mf = r["material_flow"]
        try:
            node = dict(label=mf["labels"], pad=15, thickness=14, color=[ACCENT_4]*len(mf["labels"]))
            link = dict(source=mf["source"], target=mf["target"], value=mf["value"], color="rgba(7,170,170,0.25)")
            sankey = go.Figure(go.Sankey(node=node, link=link))
            plot_style(sankey, title="Material Flow Sankey", height=380)
            st.plotly_chart(sankey, use_container_width=True)
        except Exception as e:
            st.error("Sankey failed to render")
            st.write(e)

    st.markdown("---")

    # ---------- Extended Circularity Metrics ----------
    st.markdown("<h3 style='margin:6px 0'>Extended Circularity Metrics</h3>", unsafe_allow_html=True)
    metrics = r["extended_metrics"]
    cols = st.columns(4)
    keys = list(metrics.keys())
    for i, k in enumerate(keys):
        cols[i % 4].markdown(f"<div class='card-override' style='text-align:center'><div style='color:rgba(3,60,57,0.8)'>{k}</div><div style='font-size:20px;color:{ACCENT_2};font-weight:700'>{metrics[k]}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- Key Impact Profiles ----------
    st.markdown("<h3 style='margin:6px 0'>Key Impact Profiles</h3>", unsafe_allow_html=True)
    impact_df = pd.DataFrame(r["impact_list"], columns=["Impact Metric", "Value", "Unit"])
    top_keys = ["Global Warming Potential", "Energy Demand", "Water Consumption", "Eutrophication", "Acidification"]
    df_bar = impact_df[impact_df["Impact Metric"].isin(top_keys)]
    if df_bar.empty:
        df_bar = impact_df.head(5)
    fig_bar = px.bar(df_bar, x="Impact Metric", y="Value", text="Value", color="Impact Metric",
                     color_discrete_sequence=[ACCENT_1, ACCENT_2, ACCENT_3, ACCENT_4, ACCENT_2])
    plot_style(fig_bar, height=360)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # ---------- GWP Contribution & Energy Source ----------
    st.markdown("<div style='display:flex;gap:12px'>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1,1])
    with col_a:
        df_gwp = pd.DataFrame(list(r["gwp_breakdown"].items()), columns=["Category", "Share"])
        pie = px.pie(df_gwp, names="Category", values="Share", hole=0.4, color_discrete_sequence=[ACCENT_1, ACCENT_2, ACCENT_3])
        plot_style(pie, "GWP Contribution Analysis", height=300)
        st.plotly_chart(pie, use_container_width=True)
    with col_b:
        df_energy = pd.DataFrame(list(r["energy_breakdown"].items()), columns=["Source", "Value"])
        bar = px.bar(df_energy, x="Value", y="Source", orientation="h", text="Value", color="Source", color_discrete_sequence=[ACCENT_3, ACCENT_2])
        plot_style(bar, "Energy Source Breakdown (MJ)", height=300)
        st.plotly_chart(bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- Detailed Impact Assessment (chart + table) ----------
    st.markdown("<h3 style='margin:6px 0'>Detailed Impact Assessment</h3>", unsafe_allow_html=True)
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
    mock_values = {
        "Global Warming Potential": 2288.0,
        "Acidification Potential": 4.11,
        "Photochemical Ozone Creation": 2.29,
        "Abiotic Depletion (Fossil)": 29288.0,
        "Fresh Water Ecotoxicity": 22.88,
        "Energy Demand": 26626.0,
        "Eutrophication Demand": 1.14,
        "Particulate Matter Formation": 0.763,
        "Human Toxicity (Cancer)": 0.012,
        "Ionizing Radiation": 0.00035,
        "Water Consumption": 4.7,
        "Ozone Depletion Potential": 0.00005,
        "Abiotic Depletion (Elements)": 0.0012,
        "Human Toxicity (Non-Cancer)": 2.29,
        "Land Use": 228.77
    }
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
    impact_rows = []
    for name in impact_names:
        val = mock_values.get(name, 0.0)
        unit = units.get(name, "")
        impact_rows.append({"Impact Metric": name, "Value": val, "Unit": unit})
    impact_df = pd.DataFrame(impact_rows)
    impact_df["ValueNum"] = pd.to_numeric(impact_df["Value"], errors="coerce")
    impact_df_sorted = impact_df.sort_values("ValueNum", ascending=True)
    fig_imp = px.bar(impact_df_sorted, x="ValueNum", y="Impact Metric", orientation="h", text="ValueNum", color="Impact Metric",
                     color_discrete_sequence=[ACCENT_1, ACCENT_2, ACCENT_3, ACCENT_4, ACCENT_2, ACCENT_3, ACCENT_1, ACCENT_4, ACCENT_2, ACCENT_3, ACCENT_1, ACCENT_4, ACCENT_2, ACCENT_3, ACCENT_1])
    plot_style(fig_imp, height=480)
    st.plotly_chart(fig_imp, use_container_width=True)
    st.dataframe(impact_df.drop(columns=["ValueNum"]), use_container_width=True, height=260)
    csv_download_link(impact_df.drop(columns=["ValueNum"]), filename="detailed_impacts_mock.csv", label="📥 Download Detailed Impacts CSV")

    st.markdown("---")

    # ---------- Uncertainty Dashboard ----------
    st.markdown("<h3 style='margin:6px 0'>Uncertainty Dashboard</h3>", unsafe_allow_html=True)
    unc = r["uncertainty"]
    col_g, col_e, col_w = st.columns(3)
    def hist_col(col, arr, label, unit):
        arr = np.array(arr)
        mean = np.mean(arr)
        ci = np.percentile(arr, [2.5, 97.5])
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=arr, nbinsx=30, marker=dict(color=ACCENT_1)))
        fig.add_vline(x=mean, line_color=ACCENT_2, line_width=2)
        fig.add_vline(x=ci[0], line_dash="dash", line_color=ACCENT_2)
        fig.add_vline(x=ci[1], line_dash="dash", line_color=ACCENT_2)
        plot_style(fig, title=f"{label} distribution", height=300)
        col.plotly_chart(fig, use_container_width=True)
        col.markdown(f"**Mean:** {mean:.2f} {unit}  •  **95% CI:** [{ci[0]:.2f}, {ci[1]:.2f}]")
    hist_col(col_g, unc.get("GWP", []), "Global Warming Potential", "kg CO₂-eq")
    hist_col(col_e, unc.get("Energy", []), "Energy Demand", "MJ")
    hist_col(col_w, unc.get("Water", []), "Water Consumption", "m³")

    st.markdown("---")

    # ---------- AI-Powered Insights & Recommendations ----------
    st.markdown("<h3 style='margin:6px 0'>AI-Powered Insights & Recommendations</h3>", unsafe_allow_html=True)
    try:
        extra_ctx = {"executive_summary": r["executive_summary"], "supply_chain_hotspots": r["supply_chain_hotspots"]}
        # ensure ore_warning and ev_charging always present
        if "ore_warning" not in ai_data:
            ai_data["ore_warning"] = {"text": "Ore grade variability: potential emissions increase.", "severity": "Warning"}
        if "ev_charging" not in ai_data:
            ai_data["ev_charging"] = {"text": "Recommend off-peak charging during high renewable generation.", "priority": "Advisory"}

        if ai_recommendation and hasattr(ai_recommendation, "display_ai_recommendations"):
            ai_recommendation.display_ai_recommendations(ai_data, extra_context=extra_ctx)
        else:
            # Built-in rendering
            st.markdown("<div class='card-override'>", unsafe_allow_html=True)
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
                st.markdown(f"### {f.get('title','-')}  \n**Priority:** {f.get('priority','Medium')}")
                st.markdown(f"**Evidence:** {f.get('evidence','-')}")
                st.markdown(f"**Root Cause:** {f.get('root_cause','-')}")
                st.markdown("**Action Plan:**")
                for ap in f.get("action_plan", []):
                    st.markdown(f"- {ap.get('title')}  • Effort: {ap.get('effort','N/A')}  • Confidence: {ap.get('confidence','N/A')}%")
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

    # ---------- Primary vs. Recycled Scenario Comparison ----------
    st.markdown("<h3 style='margin:6px 0'>Primary vs. Recycled Route Comparison</h3>", unsafe_allow_html=True)
    df_pvr = pd.DataFrame(r.get("primary_vs_recycled", []))
    # normalize columns gracefully
    if not df_pvr.empty:
        df_pvr.columns = [str(c).strip().capitalize() for c in df_pvr.columns]
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

    if df_pvr.empty or not all(c in df_pvr.columns for c in ["Metric", "Primary", "Recycled"]):
        df_pvr = pd.DataFrame([
            {"Metric": "GWP (kg CO2-eq)", "Primary": 2485, "Recycled": 597},
            {"Metric": "Energy (GJ)", "Primary": 28.77, "Recycled": 6.17},
            {"Metric": "Water (m³)", "Primary": 5.0, "Recycled": 2.0},
        ])

    def compute_savings(p, r):
        try:
            if p == 0:
                return "—"
            pct = (p - r) / float(p) * 100.0
            return f"▼ {pct:.1f}%"
        except Exception:
            return "—"

    df_pvr["Savings"] = df_pvr.apply(lambda row: compute_savings(row.get("Primary", 0), row.get("Recycled", 0)), axis=1)

    display_df = df_pvr.copy()
    for col in ["Primary", "Recycled"]:
        if col in display_df.columns and pd.api.types.is_numeric_dtype(display_df[col]):
            display_df[col] = display_df[col].apply(lambda v: f"{v:,.2f}")

    st.markdown("<div class='card-override'>", unsafe_allow_html=True)
    st.table(display_df)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("")  # spacing

    # Chart group
    try:
        df_melt = df_pvr.melt(id_vars=["Metric", "Savings"], value_vars=["Primary", "Recycled"], var_name="Scenario", value_name="Value")
        fig_cmp = px.bar(df_melt, x="Metric", y="Value", color="Scenario", barmode="group", text="Value",
                         color_discrete_map={"Primary": ACCENT_3, "Recycled": ACCENT_1})
        fig_cmp.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        fig_cmp.update_layout(height=380, legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), xaxis_tickangle=-20, margin=dict(l=40, r=30, t=40, b=80))
        plot_style(fig_cmp, height=380)
        st.plotly_chart(fig_cmp, use_container_width=True)

        df_vis = df_pvr.sort_values("Primary", ascending=False)
        fig_vis = go.Figure()
        fig_vis.add_trace(go.Bar(y=df_vis["Metric"], x=df_vis["Primary"], orientation='h', name='Primary Route', marker=dict(color=ACCENT_3), hovertemplate='%{y}<br>Primary: %{x}<extra></extra>'))
        fig_vis.add_trace(go.Bar(y=df_vis["Metric"], x=df_vis["Recycled"], orientation='h', name='Recycled Route', marker=dict(color=ACCENT_1), hovertemplate='%{y}<br>Recycled: %{x}<extra></extra>'))
        fig_vis.update_layout(barmode='group', height=360, margin=dict(l=150, r=40, t=30, b=30))
        plot_style(fig_vis, height=360)
        st.plotly_chart(fig_vis, use_container_width=True)
    except Exception as e:
        st.error("Comparison chart failed to render")
        st.write(str(e))

    st.markdown("---")
    st.markdown("<div style='color:rgba(3,60,57,0.6);font-size:12px'>Generated by MetalliQ · Screening-level LCA. For formal comparative reporting follow ISO 14044 critical review processes.</div>", unsafe_allow_html=True)

# If executed directly, show demo
if __name__ == "__main__":
    results_page(None, None)
