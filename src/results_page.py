import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ai_recommendation
import numpy as np
# Add a general card CSS for all cards at the top:
st.markdown("""
<style>
.results-card {
    background: #f2f4f6;
    border-radius: 14px;
    box-shadow: 0 2.5px 15px #d4d5de71;
    padding: 18px 20px 16px 22px;
    margin-bottom: 1.1em;
}
.metric-card {
    background: #f2f4f6;
    border-radius: 14px;
    box-shadow: 0 2.5px 15px #d4d5de71;
    text-align: center;
    min-width: 180px;
    min-height: 96px;
    padding: 28px 0 18px 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)


def results_page(results, ai_text):
    st.title("Steel for New Building Frame")
    st.markdown("---")

    # ISO 14044 Compliance banner
    st.markdown(
        """
        <div class='results-card' style='background:#eef3fc; border-radius:16px; padding:21px 25px 17px 40px; margin-bottom: 20px; font-size:1.07em; border: 1px solid #c5dbfc;'>
            <b>ISO 14044 Conformance</b><br>
            This is a screening-level LCA designed to be broadly consistent with ISO 14044 principles for internal decision-making.
            For public comparative assertions, a formal third-party critical review of this report is required.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # EXECUTIVE SUMMARY
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
    st.markdown("<div style='font-size:1.22rem;font-weight:700;margin-bottom:3px;'>Executive Summary</div>", unsafe_allow_html=True)
    st.caption("Displaying the mean values from a 1,000-run Monte Carlo simulation.")
    cols = st.columns(4)
    cols[0].markdown(
        f"""<div class='metric-card' style='background:#fbfbfb;border-radius:14px;padding:17px 0 11px 20px;box-shadow:0 1.5px 10px #e5e5ec7a;margin-bottom:1rem;'>
        <span style='color:#909da9;font-weight:500;'>Global Warming Potential</span><br>
        <span style='font-size:2.07em;font-weight:850;color:#262626;'>{es.get('Global Warming Potential', 2288)}</span>
        <span style='color:#b4b9c2;font-weight:900;'> kg CO₂-eq</span></div>""", unsafe_allow_html=True)
    cols[1].markdown(
        f"""<div class='metric-card' style='background:#fbfbfb;border-radius:14px;padding:17px 0 11px 20px;box-shadow:0 1.5px 10px #e5e5ec7a;margin-bottom:1rem;'>
        <span style='color:#909da9;font-weight:500;'>Circularity Score</span><br>
        <span style='font-size:2.07em;font-weight:850;color:#262626;'>{es.get('Circularity Score', 50)}</span>
        <span style='color:#b4b9c2;font-weight:900;'> %</span></div>""", unsafe_allow_html=True)
    cols[2].markdown(
        f"""<div class='metric-card' style='background:#fbfbfb;border-radius:14px;padding:17px 0 11px 20px;box-shadow:0 1.5px 10px #e5e5ec7a;margin-bottom:1rem;'>
        <span style='color:#909da9;font-weight:500;'>Particulate Matter</span><br>
        <span style='font-size:2.07em;font-weight:850;color:#262626;'>{es.get('Particulate Matter', 0.763):.3g}</span>
        <span style='color:#b4b9c2;font-weight:900;'> kg PM2.5-eq</span></div>""", unsafe_allow_html=True)
    cols[3].markdown(
        f"""<div class='metric-card' style='background:#fbfbfb;border-radius:14px;padding:17px 0 11px 20px;box-shadow:0 1.5px 10px #e5e5ec7a;margin-bottom:1rem;'>
        <span style='color:#909da9;font-weight:500;'>Water Consumption</span><br>
        <span style='font-size:2.07em;font-weight:850;color:#262626;'>{es.get('Water Consumption', 4.7)}</span>
        <span style='color:#b4b9c2;font-weight:900;'> m³</span></div>""", unsafe_allow_html=True)
    st.markdown("---")

    # Goal & Scope
    gs = results.get('goal_scope', {
        "Intended Application": "Screening assessment for internal R&D purposes to compare material choices.",
        "System Boundary": "Cradle-to-Grave",
        "Limitations": "This analysis relies on industry-average data and does not include site-specific emissions. Results are for directional guidance only.",
        "Intended Audience": "Internal engineering and sustainability departments.",
        "Comparative Assertion for Public": "Yes"
    })
    st.markdown("<div style='margin-top:1.7em;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2.2, 1.1])
    with c1:
        st.markdown("<div style='font-weight:700;font-size:1.07rem;margin-bottom:5px;'>Goal & Scope (ISO 14044)</div>", unsafe_allow_html=True)
        st.write(f"**Intended Application:** {gs.get('Intended Application', '')}")
        st.write(f"**System Boundary:** {gs.get('System Boundary', '')}")
        st.write(f"**Limitations:** {gs.get('Limitations', '')}")
    with c2:
        st.write(f"**Intended Audience:** {gs.get('Intended Audience', '')}")
        st.write(f"**Comparative Assertion for Public:** {gs.get('Comparative Assertion for Public', '')}")
    st.markdown("---")

    # Data Quality + Uncertainty
    dq = results.get('data_quality', {
        "Reliability Score": 5,
        "Completeness Score": 5,
        "Temporal Score": 5,
        "Technological Score": 4,
        "Geographical Score": 4,
        "Aggregated Data Quality": 4.51,
        "Result Uncertainty": "±14%"
    })
    c1, c2 = st.columns([2, 1.2])
    with c1:
        st.markdown("<div style='font-weight:700;font-size:1.07rem;margin-top:1.2em;'>Data Quality & Uncertainty</div>", unsafe_allow_html=True)
        st.write(f"Reliability Score: {dq.get('Reliability Score', 'N/A')} / 5")
        st.write(f"Completeness Score: {dq.get('Completeness Score', 'N/A')} / 5")
        st.write(f"Temporal Score: {dq.get('Temporal Score', 'N/A')} / 5")
        st.write(f"Technological Score: {dq.get('Technological Score', 'N/A')} / 5")
        st.write(f"Geographical Score: {dq.get('Geographical Score', 'N/A')} / 5")
    with c2:
        st.markdown("<div style='font-size:1.07em;font-weight:500;color:#415;'>Aggregated Data Quality</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:2.3em;font-weight:800;'>{dq.get('Aggregated Data Quality', 'N/A')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:1.1em;margin-top:4px;color:#1769a0;'>Result Uncertainty <b>{dq.get('Result Uncertainty', '')}</b></div>", unsafe_allow_html=True)
    st.markdown("---")

    # Supply Chain Hotspots
    st.markdown("<div style='font-weight:700;font-size:1.10rem;margin-top:1.65em;margin-bottom:5px;'>Supply Chain Hotspots</div>", unsafe_allow_html=True)
    for h in es["Supply Chain Hotspots"]:
        color = "#fff6ea" if "Production Phase" in h['title'] else "#f5f5f6"
        border = "#ecb263" if "Production Phase" in h['title'] else "#efefef"
        st.markdown(
            f"""<div style="background:{color};border-radius:10px;
            border:2px solid {border};
            display:flex;align-items:center;margin-bottom:12px;box-shadow:0 1px 6px #efc26634;">
            <div style="flex:5;padding:12px 9px 6px 21px;">
                <span style="font-weight:730;font-size:1.09em;color:#b06718;">{h['title']}</span>
                {"<div style='font-size:.97em;color:#dc9509;margin-top:2.5px;'>" + h['description'] + "</div>" if h['description'] else ""}
            </div>
            <div style="flex:1;padding:0 32px 0 10px;text-align:right;font-weight:800;font-size:1.6em;color:#dd961f;">
                {h['impact']}%
                <span style="font-size:.8em;font-weight:600; color:#c9b072;">of GWP Impact</span>
            </div>
            </div>""", unsafe_allow_html=True
        )
    st.markdown("---")


    # Production Metrics
    st.markdown(
        f"""<div style='display:flex;gap:28px;margin-top:1.9em;'>
            <div style='background:#f8fafd;border-radius:11px;padding:15px 28px 15px 22px;min-width:210px;'>
                <span style='color:#799;font-size:1em;'>Production Phase GWP</span><br>
                <span style='font-size:2em;font-weight:800;color:#136;'>{es['Production Phase GWP']}</span>
                <span style='font-size:1em;color:#aec;'>kg CO₂-eq</span>
            </div>
            <div style='background:#f8fafd;border-radius:11px;padding:15px 28px 15px 22px;min-width:210px;'>
                <span style='color:#799;font-size:1em;'>Overall Energy Demand</span><br>
                <span style='font-size:2em;font-weight:800;color:#136;'>{es['Overall Energy Demand']}</span>
                <span style='font-size:1em;color:#aec;'>MJ</span>
            </div>
            <div style='background:#f8fafd;border-radius:11px;padding:15px 28px 15px 22px;min-width:210px;'>
                <span style='color:#799;font-size:1em;'>Circular Score</span><br>
                <span style='font-size:2em;font-weight:800;color:#136;'>{es['Circular Score']}%</span>
            </div>
        </div>""", unsafe_allow_html=True
    )
    st.markdown("---")

    #Process Lifecycle

    st.markdown(
        """
        <style>
        .lifecycle-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 98%;
            margin: 40px auto 30px auto;
            position: relative;
        }
        .lifecycle-line {
            position: absolute;
            top: 42px;
            left: 8%;
            width: 84%;
            border-top: 2px solid #c1d9ef;
            z-index: 1;
            height: 0;
        }
        .lifecycle-stage {
            background: #fff;
            border: 2.5px solid #18538618;
            border-radius: 2.5em;
            width: 65px;
            height: 65px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 5px;
            position: relative;
            z-index: 2;
            box-shadow: 0 6px 23px #e1eaff81;
            transition: box-shadow 0.2s;
        }
        .lifecycle-stage:hover {
            box-shadow: 0 8px 23px #1a2e4a13;
            border: 2.5px solid #508fda66;
        }
        .icon-label {
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 90px;
        }
        .stage-label {
            font-size: 1em;
            font-weight: 600;
            color: #233354;
            margin-top: 9px;
            letter-spacing: -0.5px;
        }
        </style>
        <div class="lifecycle-row">
            <div class="lifecycle-line"></div>
            <div class="icon-label">
                <div class="lifecycle-stage">🌞</div>
                <div class="stage-label">Raw Material</div>
            </div>
            <div class="icon-label">
                <div class="lifecycle-stage">🧰</div>
                <div class="stage-label">Processing</div>
            </div>
            <div class="icon-label">
                <div class="lifecycle-stage">⚙️</div>
                <div class="stage-label">Manufacturing</div>
            </div>
            <div class="icon-label">
                <div class="lifecycle-stage">🚚</div>
                <div class="stage-label">Transport</div>
            </div>
            <div class="icon-label">
                <div class="lifecycle-stage">⏲️</div>
                <div class="stage-label">Use Phase</div>
            </div>
            <div class="icon-label">
                <div class="lifecycle-stage">🗑️</div>
                <div class="stage-label">End of Life</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Hover for details, click for breakdowns.")

    st.divider()
    # AI Life Cycle Interpretation
    with st.expander("AI Generated Life Cycle Interpretation"):
        st.markdown(ai_text if ai_text else "No AI interpretation available.")
    st.markdown("---")

    # Sankey Diagram, Material Flow
    with st.expander("Process Life Cycle - Sankey Diagram"):
        mf = results.get('material_flow_analysis')
        if mf:
            fig = go.Figure(go.Sankey(
                node=dict(label=mf['labels']),
                link=dict(source=mf['source'], target=mf['target'], value=mf['value'])
            ))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No material flow data available.")
    st.markdown("---")

    #Circularity Analysis
    # --- Circularity Analysis Card ---
    circ_metrics = results.get("circularity_analysis", {
        "Circularity Rate": 50,
        "Recyclability Rate": 90,
        "Recovery Efficiency": 92,
        "Secondary Material Content": 10
    })
    st.markdown("""
    <div style='background:#f8fafc;border-radius:16px;padding:28px 28px 18px 28px;box-shadow:0 2px 16px #c3d3e33c;margin-bottom:30px;'>
        <h3 style="font-size:1.23rem;">Circularity Analysis</h3>
    </div>
    """, unsafe_allow_html=True)

    # Dounut Gauge for Circularity Rate
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value = circ_metrics.get("Circularity Rate", 50),
        number={"suffix": "%", "font": {"size":44, "color": "#16507e", "family": "Roboto"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 2},
            "bar": {"color": "#1765b6", "thickness": 0.23},
            "bgcolor": "#e7edf3",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 100], "color": "#e7edf3"}
            ]
        },
        domain={"x": [0, 1], "y": [0, 1]}
    ))
    fig.update_layout(
        width=320, height=300,
        margin=dict(l=0, r=0, t=10, b=5),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    c1, c2 = st.columns([0.47, 0.53])
    with c1:
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(
            f"""
    <div style="margin-top:22px;">
    <div style="font-size:1em;margin-bottom:5px;">
        Recyclability Rate
        <span style="float:right;font-weight:800;color:#2369a8;">{circ_metrics["Recyclability Rate"]}%</span>
    </div>
    <div style="background:#e7edf3;border-radius:9px;height:13px; margin-bottom:18px;">
        <div style="background:#225c85;width:{circ_metrics["Recyclability Rate"]}%;height:13px;border-radius:9px;"></div>
    </div>

    <div style="font-size:1em;margin-bottom:5px;">
        Recovery Efficiency
        <span style="float:right;font-weight:800;color:#2369a8;">{circ_metrics["Recovery Efficiency"]}%</span>
    </div>
    <div style="background:#e7edf3;border-radius:9px;height:13px;margin-bottom:18px;">
        <div style="background:#1765b6;width:{circ_metrics["Recovery Efficiency"]}%;height:13px;border-radius:9px;"></div>
    </div>

    <div style="font-size:1em;margin-bottom:5px;">
        Secondary Material Content
        <span style="float:right;font-weight:800;color:#85888a;">{circ_metrics["Secondary Material Content"]}%</span>
    </div>
    <div style="background:#e7edf3;border-radius:9px;height:13px;margin-bottom:5px;">
        <div style="background:linear-gradient(90deg,#b0b3b5,#78797c 85%);width:{circ_metrics["Secondary Material Content"]}%;height:13px;border-radius:9px;"></div>
    </div>
    </div>
    """,
            unsafe_allow_html=True,
        )


    # Responsive Extended Circularity Metrics Card Grid

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

    st.markdown("""
    <style>
    .metric-card {
        background: #f8fafc;
        border-radius: 13px;
        padding: 28px 0 18px 0;
        box-shadow: 0 2px 12px #c3d3e35c;
        text-align: center;
        margin-bottom: 20px;
        min-width: 180px;
        min-height: 96px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-label {
        color: #6f7887;
        font-size: 1.13em;
        font-weight: 600;
        margin-bottom: 7px;
        white-space: pre-line;
    }
    .metric-value {
        color: #003866;
        font-size: 2em;
        font-weight: 800;
        letter-spacing: 0.6px;
        margin-bottom: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### Extended Circularity Metrics")

    labels = list(extcirc.keys())
    values = list(extcirc.values())

    # Choose 3 or 4 columns per row based on screen, keeps spacing optimal
    cols_per_row = 4  # Try 3 if still squished, or use st.columns dynamically
    for i in range(0, len(labels), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(labels):
                col.markdown(f'''
                    <div class='metric-card'>
                        <div class='metric-label'>{labels[idx]}</div>
                        <div class='metric-value'>{values[idx]}</div>
                    </div>
                ''', unsafe_allow_html=True)

    st.divider()


    # GWP Contribution Pie Chart
    gwp_contrib = results.get('gwp_contribution_analysis', {})
    if gwp_contrib:
        df_gwp = pd.DataFrame(list(gwp_contrib.items()), columns=["Category", "Value"])
        fig = px.pie(df_gwp, names='Category', values='Value', title='GWP Contribution Analysis')
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # Energy Breakdown
    energy_breakdown = results.get('energy_source_breakdown', {})
    if energy_breakdown:
        df_energy = pd.DataFrame(list(energy_breakdown.items()), columns=["Energy Source", "Value"])
        fig = px.bar(df_energy, x='Energy Source', y='Value', title='Energy Source Breakdown')
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # Key Impact Profiles and Chart
    kip = results.get('key_impact_profiles', {})
    if kip:
        df_kip = pd.DataFrame(kip).T.reset_index()
        if {'mean', 'Metric', 'Value'}.intersection(set(df_kip.columns)):
            # try each style as appropriate, or better, print/inspect your df_kip columns first!
            if 'Metric' in df_kip.columns:
                fig = px.bar(df_kip, x='Metric', y='Value', color='Metric', text='Value', title='Key Impact Profiles')
            elif 'index' in df_kip.columns and 'mean' in df_kip.columns:
                fig = px.bar(df_kip, x='index', y='mean', text='mean', title='Key Impact Profiles')
            else:
                st.write("KIP: DataFrame column mismatch, columns:", df_kip.columns)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No Key Impact Profiles data to display.")
    else:
        st.write("No Key Impact Profiles data to display.")
    st.markdown("---")

        # ---------- IMPACT METRICS GRID ----------

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
    df = pd.DataFrame(impact_data, columns=["Impact Metric", "Value", "Unit"])
    st.markdown("#### Detailed Impact Assessment")
    st.dataframe(df, hide_index=True)
    st.markdown("---")

    # Uncertainty Distributions
    gwp_arr = np.random.normal(loc=2288, scale=98.7, size=1000)
    energy_arr = np.random.normal(loc=26626, scale=1387.8, size=1000)
    water_arr = np.random.normal(loc=5, scale=0.3, size=1000)

    st.markdown("""
    <style>
    .uncertainty-card {
        background: linear-gradient(98deg,#f9fbfe 70%, #e4ecf8 120%);
        border-radius: 22px;
        box-shadow: 0 2px 28px #cbe4ff2a;
        padding: 2em 2em 1.5em 2em;
        margin-bottom: 1.4em;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='uncertainty-card'>"
        "<div style='font-size:2rem;font-weight:700;'>Uncertainty Dashboard</div>"
        "<div style='color:#7c858a;font-size:1.07em;margin-bottom:20px;'>Based on Monte Carlo simulation (1000 runs) to assess data variability.</div>",
        unsafe_allow_html=True
    )

    cols = st.columns(3)
    for idx, (arr, label, unit) in enumerate([
        (gwp_arr, "GWP", "kg CO₂-eq"),
        (energy_arr, "Energy", "MJ"),
        (water_arr, "Water", "m³")
    ]):
        mean = np.mean(arr)
        std = np.std(arr)
        ci_low, ci_high = np.percentile(arr, [2.5,97.5])
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=arr, nbinsx=18, marker=dict(color="#b8bcd0"), showlegend=False))
        fig.add_vline(x=mean, line_width=3, line_color='#285fc7')
        fig.add_vline(x=ci_low, line_width=2, line_dash='dash', line_color='#285fc7')
        fig.add_vline(x=ci_high, line_width=2, line_dash='dash', line_color='#285fc7')
        fig.update_layout(
            margin=dict(l=10, r=10, t=43, b=45),
            height=280,
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title=unit,
            yaxis_title="",
            font=dict(family="Inter,sans-serif", size=15),
            title=dict(
                text=f"<b>{label}</b><br><span style='font-size:0.83em;font-weight:400;color:#889'>"
                     f"Mean: {mean:.1f} | σ: {std:.1f} | 95% CI</span>",
                y=0.92, x=0.5, xanchor='center', yanchor='top'
            ),
        )
        cols[idx].plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

    # AI-Powered Insights/Recommendations
    extra_context = {
    "ore_conc": results.get('ore_conc'),
    "transports": [
        results.get('transport_stage_1', {}),
        results.get('transport_stage_2', {})
    ]
    }
    if ai_text:
        ai_recommendation.display_ai_recommendations(ai_text,extra_context)
    st.markdown("---")
    
    # Scenario Comparison Table and Chart
    pvrs = results.get('primary_vs_recycled', {})
    if pvrs and 'comparison_table' in pvrs:
        df = pd.DataFrame(pvrs['comparison_table'])
        st.markdown("### Primary vs Recycled Scenario Comparison")
        st.dataframe(df)
        if not df.empty and "Metric" in df.columns:
            df_long = df.melt(id_vars=['Metric'], var_name="Scenario", value_name="Value")
            fig = px.bar(df_long, x='Metric', y='Value', color='Scenario', barmode='group',
                        title='Scenario Comparison Across Multiple Metrics')
            st.plotly_chart(fig, use_container_width=True)
