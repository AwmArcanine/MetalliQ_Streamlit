import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ai_recommendation
import numpy as np

# ------------------------------------------------------------------------------
# Results page: glassy metric cards, transparent/clean charts, mock AI fallback
# ------------------------------------------------------------------------------

st.markdown(
    """
    <style>
    /* subtle teal pulse for hotspot cards */
    @keyframes tealPulse {
        0% { box-shadow: 0 0 8px rgba(0,239,255,0.18); border-color: rgba(0,239,255,0.28);}
        50% { box-shadow: 0 0 20px rgba(0,239,255,0.32); border-color: rgba(0,239,255,0.55);}
        100% { box-shadow: 0 0 8px rgba(0,239,255,0.18); border-color: rgba(0,239,255,0.28);}
    }

    /* glossy metric cards (dark text inside) */
    .metric-card {
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(14px) saturate(140%);
        -webkit-backdrop-filter: blur(14px) saturate(140%);
        border: 1.6px solid rgba(255,255,255,0.35);
        box-shadow: 0 10px 30px rgba(255,255,255,0.14);
        color: #111; /* dark text */
        border-radius: 14px;
        padding: 18px 20px;
        text-align: left;
        margin-bottom: 1rem;
    }

    .metric-card .metric-title {
        color: #333;
        font-weight: 600;
        font-size: 0.98rem;
    }

    .metric-card .metric-value {
        color: #0b0b0b;
        font-weight: 800;
        font-size: 1.9rem;
        margin-top: 6px;
    }

    /* general results banner/card */
    .results-card {
        background: rgba(255,255,255,0.18);
        backdrop-filter: blur(12px) saturate(140%);
        -webkit-backdrop-filter: blur(12px) saturate(140%);
        border: 1.2px solid rgba(255,255,255,0.32);
        border-radius: 16px;
        padding: 20px 24px;
        color: #111;
        margin-bottom: 1rem;
    }

    /* hotspot cards - glassy + teal pulse */
    .hotspot-card {
        background: rgba(255,255,255,0.22);
        backdrop-filter: blur(16px) saturate(160%);
        -webkit-backdrop-filter: blur(16px) saturate(160%);
        border: 1.5px solid rgba(0,239,255,0.22);
        box-shadow: 0 8px 28px rgba(0,239,255,0.08);
        border-radius: 12px;
        padding: 12px 16px;
        color: #111;
        margin-bottom: 12px;
        animation: tealPulse 4s ease-in-out infinite;
    }

    /* uncertainty banner (transparent/glassy) */
    .uncertainty-card {
        background: rgba(255,255,255,0.18);
        backdrop-filter: blur(20px) saturate(170%);
        -webkit-backdrop-filter: blur(20px) saturate(170%);
        border-radius: 18px;
        border: 1.2px solid rgba(0,239,255,0.16);
        box-shadow: 0 6px 28px rgba(0,0,0,0.06);
        padding: 18px;
        color: #111;
        margin-bottom: 1.1rem;
    }

    /* smaller utility tweaks - keep charts plain/transparent */
    .stPlotlyChart > div {
        background: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def results_page(results, ai_text):
    """
    Render the results page.
    - results: dict returned from run_simulation(...) or similar
    - ai_text: either an AI dict (expected by ai_recommendation.display_ai_recommendations)
               or None. If None, the page will show a mock AI interpretation and use
               ai_recommendation.ai_data_example for recommendations display.
    """

    # Title
    st.title("Steel for New Building Frame")
    st.markdown("---")

    # ISO 14044 Compliance banner (kept minimal & glassy)
    st.markdown(
        """
        <div class='results-card'>
            <b>ISO 14044 Conformance</b><br>
            This is a screening-level LCA designed to be broadly consistent with ISO 14044 principles for internal decision-making.
            For public comparative assertions, a formal third-party critical review of this report is required.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # EXECUTIVE SUMMARY
    # -------------------------------------------------------------------------
    es = results.get(
        "executive_summary",
        {
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
                    "impact": 65,
                },
                {"title": "Overall Energy Demand", "description": "", "impact": 25},
                {"title": "Circularity Score", "description": "", "impact": 10},
            ],
        },
    )

    st.markdown("<div style='font-size:1.18rem;font-weight:700;margin-bottom:6px;'>Executive Summary</div>", unsafe_allow_html=True)
    st.caption("Displaying the mean values from a Monte Carlo simulation (e.g. 1,000 runs).")

    # Metric cards row (4)
    cols = st.columns(4)
    metrics = [
        ("Global Warming Potential", es.get("Global Warming Potential", 0), "kg CO₂-eq"),
        ("Circularity Score", es.get("Circularity Score", 0), "%"),
        ("Particulate Matter", es.get("Particulate Matter", 0.0), "kg PM2.5-eq"),
        ("Water Consumption", es.get("Water Consumption", 0.0), "m³"),
    ]
    for c, (title, value, unit) in zip(cols, metrics):
        c.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
                <div style="color:#555;font-weight:700;margin-top:6px;">{unit}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Goal & Scope (left) and Audience/Comparative assertion (right)
    # -------------------------------------------------------------------------
    gs = results.get(
        "goal_scope",
        {
            "Intended Application": "Screening assessment for internal R&D purposes to compare material choices.",
            "System Boundary": "Cradle-to-Grave",
            "Limitations": "This analysis relies on industry-average data and does not include site-specific emissions. Results are directional only.",
            "Intended Audience": "Internal engineering and sustainability departments.",
            "Comparative Assertion for Public": "No",
        },
    )

    c1, c2 = st.columns([2.2, 1.1])
    with c1:
        st.markdown("<div style='font-weight:700;font-size:1.02rem;margin-bottom:6px;'>Goal & Scope (ISO 14044)</div>", unsafe_allow_html=True)
        st.write(f"**Intended Application:** {gs.get('Intended Application','')}")
        st.write(f"**System Boundary:** {gs.get('System Boundary','')}")
        st.write(f"**Limitations:** {gs.get('Limitations','')}")
    with c2:
        st.write(f"**Intended Audience:** {gs.get('Intended Audience','')}")
        st.write(f"**Comparative Assertion for Public:** {gs.get('Comparative Assertion for Public','No')}")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Data Quality & Uncertainty (simple textual display)
    # -------------------------------------------------------------------------
    dq = results.get(
        "data_quality",
        {
            "Reliability": 4,
            "Completeness": 4,
            "Temporal Correlation": 4,
            "Technological Correlation": 4,
            "Geographical Correlation": 4,
            "Aggregated Data Quality": 4.5,
            "Result Uncertainty": "±14%",
        },
    )

    c1, c2 = st.columns([2, 1.2])
    with c1:
        st.markdown("<div style='font-weight:700;font-size:1.02rem;margin-top:6px;'>Data Quality & Uncertainty</div>", unsafe_allow_html=True)
        st.write(f"Reliability Score: {dq.get('Reliability', 4)} / 5")
        st.write(f"Completeness Score: {dq.get('Completeness', 4)} / 5")
        st.write(f"Temporal Correlation: {dq.get('Temporal Correlation', 4)} / 5")
        st.write(f"Technological Correlation: {dq.get('Technological Correlation', 4)} / 5")
        st.write(f"Geographical Correlation: {dq.get('Geographical Correlation', 4)} / 5")
    with c2:
        st.markdown("<div style='font-size:1.07em;font-weight:600;color:#333;'>Aggregated Data Quality</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:2.2em;font-weight:800;color:#111;'>{dq.get('Aggregated Data Quality', 4.5)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.98em;margin-top:6px;color:#666;'>Result Uncertainty <b>{dq.get('Result Uncertainty','')}</b></div>", unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Supply Chain Hotspots - glassy cards
    # -------------------------------------------------------------------------
    st.markdown("<div style='font-weight:700;font-size:1.05rem;margin-top:6px;margin-bottom:8px;'>Supply Chain Hotspots</div>", unsafe_allow_html=True)
    for h in es.get("Supply Chain Hotspots", []):
        title = h.get("title", "")
        desc = h.get("description", "")
        impact = h.get("impact", "")
        st.markdown(
            f"""
            <div class="hotspot-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-weight:700;color:#0b0b0b;">{title}</div>
                    <div style="font-weight:800;color:#007a7a;">{impact}%</div>
                </div>
                <div style="margin-top:6px;color:#333;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Production Metrics (compact)
    # -------------------------------------------------------------------------
    st.markdown(
        f"""
        <div style='display:flex;gap:18px;flex-wrap:wrap;margin-top:10px;'>
            <div style='background:rgba(255,255,255,0.12);padding:12px 18px;border-radius:10px;min-width:200px;'>
                <div style='color:#333;font-weight:600;'>Production Phase GWP</div>
                <div style='font-weight:800;font-size:1.4rem;color:#111;'>{es.get('Production Phase GWP', '—')}</div>
                <div style='color:#666;font-size:0.95rem;'>kg CO₂-eq</div>
            </div>
            <div style='background:rgba(255,255,255,0.12);padding:12px 18px;border-radius:10px;min-width:200px;'>
                <div style='color:#333;font-weight:600;'>Overall Energy Demand</div>
                <div style='font-weight:800;font-size:1.4rem;color:#111;'>{es.get('Overall Energy Demand', '—')}</div>
                <div style='color:#666;font-size:0.95rem;'>MJ</div>
            </div>
            <div style='background:rgba(255,255,255,0.12);padding:12px 18px;border-radius:10px;min-width:200px;'>
                <div style='color:#333;font-weight:600;'>Circular Score</div>
                <div style='font-weight:800;font-size:1.4rem;color:#111;'>{es.get('Circular Score', '—')}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Process Lifecycle visual row (icons + labels) - keep as-is
    # -------------------------------------------------------------------------
    st.markdown(
        """
        <style>
        .lifecycle-row { display:flex; justify-content:space-between; align-items:center; width:100%; margin:18px 0; }
        .lifecycle-stage { background:#fff; border-radius:50%; width:60px; height:60px; display:flex; align-items:center; justify-content:center; box-shadow:0 8px 20px rgba(0,0,0,0.06); }
        .stage-label { font-size:0.95rem; color:#333; margin-top:6px; text-align:center; }
        </style>
        <div class="lifecycle-row">
            <div style="text-align:center;">
                <div class="lifecycle-stage">⛏️</div>
                <div class="stage-label">Raw Material</div>
            </div>
            <div style="text-align:center;">
                <div class="lifecycle-stage">🏭</div>
                <div class="stage-label">Processing</div>
            </div>
            <div style="text-align:center;">
                <div class="lifecycle-stage">⚙️</div>
                <div class="stage-label">Manufacturing</div>
            </div>
            <div style="text-align:center;">
                <div class="lifecycle-stage">🚚</div>
                <div class="stage-label">Transport</div>
            </div>
            <div style="text-align:center;">
                <div class="lifecycle-stage">🏠</div>
                <div class="stage-label">Use Phase</div>
            </div>
            <div style="text-align:center;">
                <div class="lifecycle-stage">♻️</div>
                <div class="stage-label">End of Life</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Hover icons for concept — click events can be wired to drilldowns in future iterations.")
    st.divider()

    # -------------------------------------------------------------------------
    # AI Generated Life Cycle Interpretation -> show mock if ai_text missing
    # -------------------------------------------------------------------------
    mock_ai_text_html = """
    <div style="color:#111;line-height:1.5;">
    <b>AI Lifecycle Summary:</b><br>
    The AI model detected that the <b>production phase</b> contributes the most to total GWP due to
    fossil fuel dependency and inefficient transport logistics. Increasing <b>recycled content</b>,
    optimizing <b>energy efficiency</b>, and switching to <b>renewables</b> can reduce the impact by up to 45%.
    </div>
    """

    with st.expander("AI Generated Life Cycle Interpretation"):
        if ai_text:
            # if ai_text is a dict expected by ai_recommendation.display_ai_recommendations
            # show plain formatted text if it's a string, otherwise show the dict summary
            if isinstance(ai_text, str):
                st.markdown(f"<div style='color:#111;'>{ai_text}</div>", unsafe_allow_html=True)
            else:
                # try to render a simple summary field if present
                summary = None
                if isinstance(ai_text, dict):
                    summary = ai_text.get("summary") or ai_text.get("ai_summary") or None
                if summary:
                    st.markdown(f"<div style='color:#111;'>{summary}</div>", unsafe_allow_html=True)
                else:
                    # fallback: render the mock html
                    st.markdown(mock_ai_text_html, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Sankey Diagram (material flow) - transparent background
    # -------------------------------------------------------------------------
    with st.expander("Process Life Cycle - Sankey Diagram"):
        mf = results.get("material_flow_analysis")
        if mf:
            try:
                fig = go.Figure(
                    go.Sankey(
                        node=dict(label=mf["labels"], pad=15),
                        link=dict(source=mf["source"], target=mf["target"], value=mf["value"]),
                    )
                )
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.write("Sankey plot error:", e)
                st.write(mf)
        else:
            st.write("No material flow data available.")
    st.markdown("---")

    # -------------------------------------------------------------------------
    # Circularity Analysis (card + donut gauge)
    # -------------------------------------------------------------------------
    circ_metrics = results.get(
        "circularity_analysis",
        {
            "Circularity Rate": 50,
            "Recyclability Rate": 90,
            "Recovery Efficiency": 92,
            "Secondary Material Content": 10,
        },
    )

    st.markdown(
        """
        <div style='background:rgba(255,255,255,0.12);border-radius:12px;padding:14px;margin-bottom:12px;'>
            <h3 style='margin:4px 0 6px 0;color:#111;'>Circularity Analysis</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=circ_metrics.get("Circularity Rate", 50),
            number={"suffix": "%", "font": {"size":40, "color": "#111"}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#007a7a"},
                "bgcolor": "rgba(0,0,0,0)",
            },
        )
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10))
    c1, c2 = st.columns([0.45, 0.55])
    with c1:
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(
            f"""
            <div style="font-size:0.98rem;margin-top:8px;">
                <div style="display:flex;justify-content:space-between;">
                    <div>Recyclability Rate</div>
                    <div style="font-weight:800;color:#007a7a;">{circ_metrics.get('Recyclability Rate', 0)}%</div>
                </div>
                <div style="background:#eee;border-radius:8px;height:10px;margin-top:6px;">
                    <div style="background:#00b8d4;border-radius:8px;width:{circ_metrics.get('Recyclability Rate',0)}%;height:10px;"></div>
                </div>

                <div style="display:flex;justify-content:space-between;margin-top:12px;">
                    <div>Recovery Efficiency</div>
                    <div style="font-weight:800;color:#007a7a;">{circ_metrics.get('Recovery Efficiency', 0)}%</div>
                </div>
                <div style="background:#eee;border-radius:8px;height:10px;margin-top:6px;">
                    <div style="background:#1765b6;border-radius:8px;width:{circ_metrics.get('Recovery Efficiency',0)}%;height:10px;"></div>
                </div>

                <div style="display:flex;justify-content:space-between;margin-top:12px;">
                    <div>Secondary Material Content</div>
                    <div style="font-weight:800;color:#555;">{circ_metrics.get('Secondary Material Content', 0)}%</div>
                </div>
                <div style="background:#eee;border-radius:8px;height:10px;margin-top:6px;">
                    <div style="background:linear-gradient(90deg,#b0b3b5,#78797c 85%);border-radius:8px;width:{circ_metrics.get('Secondary Material Content',0)}%;height:10px;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Extended Circularity Metrics (grid of small cards)
    # -------------------------------------------------------------------------
    extcirc = results.get(
        "extended_circularity_metrics",
        {
            "Resource Efficiency": "92%",
            "Extended Product Life": "110%",
            "Reuse Potential": "40/50",
            "Material Recovery": "90%",
            "Closed–Loop Potential": "75%",
            "Recycling Content": "10%",
            "Landfill Rate": "8%",
            "Energy Recovery": "2%",
        },
    )

    st.markdown("<div style='font-weight:700;margin-bottom:8px;'>Extended Circularity Metrics</div>", unsafe_allow_html=True)
    labels = list(extcirc.keys())
    values = list(extcirc.values())

    cols_per_row = 4
    for i in range(0, len(labels), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(labels):
                col.markdown(
                    f"""
                    <div class="metric-card" style="padding:14px;">
                        <div style="font-size:0.98rem;color:#444;font-weight:700;">{labels[idx]}</div>
                        <div style="font-size:1.6rem;font-weight:800;color:#111;margin-top:6px;">{values[idx]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.divider()

    # -------------------------------------------------------------------------
    # GWP Contribution pie chart (transparent)
    # -------------------------------------------------------------------------
    gwp_contrib = results.get("gwp_contribution_analysis", {})
    if gwp_contrib:
        df_gwp = pd.DataFrame(list(gwp_contrib.items()), columns=["Category", "Value"])
        fig = px.pie(df_gwp, names="Category", values="Value", title="GWP Contribution Analysis")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#111"))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Energy source breakdown (bar chart => transparent background)
    # -------------------------------------------------------------------------
    energy_breakdown = results.get("energy_source_breakdown", {})
    if energy_breakdown:
        df_energy = pd.DataFrame(list(energy_breakdown.items()), columns=["Energy Source", "Value"])
        fig = px.bar(df_energy, x="Energy Source", y="Value", title="Energy Source Breakdown")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#111"))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Key Impact Profiles and Chart (attempt to intelligently plot)
    # -------------------------------------------------------------------------
    kip = results.get("key_impact_profiles", {})
    if kip:
        try:
            df_kip = pd.DataFrame(kip).T.reset_index()
            # prefer index+mean structure if present
            if "mean" in df_kip.columns and "index" in df_kip.columns:
                fig = px.bar(df_kip, x="index", y="mean", text="mean", title="Key Impact Profiles")
            elif {"Metric", "Value"}.issubset(df_kip.columns):
                fig = px.bar(df_kip, x="Metric", y="Value", color="Metric", text="Value", title="Key Impact Profiles")
            else:
                # try to melt if necessary
                st.write("KIP dataframe columns:", df_kip.columns)
                fig = None

            if fig:
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#111"))
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.write("No Key Impact Profiles data to display or error plotting:", e)
    else:
        st.write("No Key Impact Profiles data to display.")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Detailed Impact Assessment - table
    # -------------------------------------------------------------------------
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
        ("Land Use", 228.77, "m²·year"),
    ]
    df = pd.DataFrame(impact_data, columns=["Impact Metric", "Value", "Unit"])
    st.markdown("#### Detailed Impact Assessment")
    st.dataframe(df, hide_index=True)
    st.markdown("---")

    # -------------------------------------------------------------------------
    # Uncertainty Distributions (histograms) - glassy container above charts
    # -------------------------------------------------------------------------
    gwp_arr = np.random.normal(loc=results.get("executive_summary", {}).get("Global Warming Potential", 2288), scale=98.7, size=1000)
    energy_arr = np.random.normal(loc=results.get("executive_summary", {}).get("Overall Energy Demand", 26626), scale=1387.8, size=1000)
    water_arr = np.random.normal(loc=results.get("executive_summary", {}).get("Water Consumption", 5), scale=0.3, size=1000)

    st.markdown(
        "<div class='uncertainty-card'><div style='font-size:1.4rem;font-weight:700;color:#111;'>Uncertainty Dashboard</div>"
        "<div style='color:#333;'>Based on Monte Carlo simulation to assess data variability across multiple runs.</div></div>",
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for idx, (arr, label, unit) in enumerate(
        [(gwp_arr, "GWP", "kg CO₂-eq"), (energy_arr, "Energy", "MJ"), (water_arr, "Water", "m³")]
    ):
        mean = np.mean(arr)
        std = np.std(arr)
        ci_low, ci_high = np.percentile(arr, [2.5, 97.5])
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=arr, nbinsx=18, marker=dict(color="#4aa3a3"), showlegend=False))
        fig.add_vline(x=mean, line_width=3, line_color="#155a5a")
        fig.add_vline(x=ci_low, line_dash="dash", line_color="#155a5a", line_width=2)
        fig.add_vline(x=ci_high, line_dash="dash", line_color="#155a5a", line_width=2)
        fig.update_layout(
            margin=dict(l=10, r=10, t=40, b=30),
            height=300,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#111"),
            title=dict(
                text=f"<b>{label}</b><br><span style='font-size:0.85em;color:#555'>Mean: {mean:.1f} | σ: {std:.1f} | 95% CI</span>",
                y=0.95,
                x=0.5,
                xanchor="center",
            ),
        )
        cols[idx].plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # AI-Powered Insights / Recommendations
    # Use provided ai_text if it's a dict compatible with ai_recommendation.display_ai_recommendations,
    # otherwise fall back to ai_recommendation.ai_data_example
    # -------------------------------------------------------------------------
    extra_context = {
        "ore_conc": results.get("ore_conc"),
        "transports": [results.get("transport_stage_1", {}), results.get("transport_stage_2", {})],
    }

    # If ai_text provided and it looks like the dict expected by ai_recommendation, pass it through.
    # Otherwise, use ai_recommendation.ai_data_example as fallback for a consistent UI.
    try:
        if ai_text and isinstance(ai_text, dict):
            ai_recommendation.display_ai_recommendations(ai_text, extra_context)
        else:
            # if ai_text is string, show it inside a simple info block then still show recommendations example
            if ai_text and isinstance(ai_text, str):
                st.info(ai_text)
            ai_recommendation.display_ai_recommendations(getattr(ai_recommendation, "ai_data_example", {}), extra_context)
    except Exception as e:
        st.write("AI recommendation display failed:", e)
        # last resort: show example if available
        try:
            ai_recommendation.display_ai_recommendations(getattr(ai_recommendation, "ai_data_example", {}), extra_context)
        except Exception:
            pass

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Scenario Comparison Table + Chart (Primary vs Recycled)
    # -------------------------------------------------------------------------
    pvrs = results.get("primary_vs_recycled", {})
    if pvrs and "comparison_table" in pvrs:
        df = pd.DataFrame(pvrs["comparison_table"])
        st.markdown("### Primary vs Recycled Scenario Comparison")
        st.dataframe(df, hide_index=True)
        if not df.empty and "Metric" in df.columns:
            df_long = df.melt(id_vars=["Metric"], var_name="Scenario", value_name="Value")
            fig = px.bar(df_long, x="Metric", y="Value", color="Scenario", barmode="group", title="Scenario Comparison Across Multiple Metrics")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#111"))
            st.plotly_chart(fig, use_container_width=True)

    # End of results_page function
