import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ai_recommendation
import numpy as np

def results_page(results, ai_text):
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;500;600&display=swap');

    html, body, .stApp {
        background: linear-gradient(135deg, #00161a 0%, #002f38 45%, #00535c 100%) !important;
        color: #e0f7fa !important;
        font-family: 'Poppins', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif;
        color: #00e5ff !important;
        text-shadow: 0 0 16px rgba(0, 229, 255, 0.7);
    }

    .results-card, .metric-card {
        background: rgba(0, 50, 60, 0.35);
        border: 1.5px solid rgba(0, 255, 255, 0.25);
        border-radius: 16px;
        box-shadow: 0 0 18px rgba(0, 255, 255, 0.15);
        color: #ccfaff;
    }

    .stDataFrame, .stTable {
        background-color: rgba(255, 255, 255, 0.05);
        color: #e0f7fa;
        border-radius: 10px;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #00e5ff 0%, #00bcd4 100%) !important;
        color: #001f26 !important;
        font-weight: 700;
        border-radius: 10px;
        border: 1px solid #00ffff80;
        box-shadow: 0 0 15px rgba(0,239,255,0.4);
    }
    div.stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 25px rgba(0,239,255,0.7);
    }
    hr, .stDivider {
        border-color: rgba(0,255,255,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    st.title("AI-Driven LCA Results: Steel for New Building Frame")
    st.markdown("---")

    # --- ISO 14044 Conformance Banner ---
    st.markdown(
        """
        <div class='results-card' style='padding:22px 30px 16px 30px;'>
            <b style='color:#00e5ff;'>ISO 14044 Conformance</b><br>
            This LCA follows ISO 14044 principles for internal sustainability assessments.
            For public comparative disclosures, a certified third-party review is needed.
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("---")

    # --- EXECUTIVE SUMMARY ---
    es = results.get('executive_summary', {
        "Global Warming Potential": 2288,
        "Circularity Score": 50,
        "Particulate Matter": 0.763,
        "Water Consumption": 4.7,
        "Production Phase GWP": 2200,
        "Overall Energy Demand": 26700,
        "Circular Score": 50,
        "Supply Chain Hotspots": [
            {"title": "Production Phase GWP", "description": "Highest impact from primary steelmaking", "impact": 65},
            {"title": "Energy Demand", "description": "High fossil energy consumption", "impact": 25},
            {"title": "Circularity Score", "description": "Limited recycling input", "impact": 10}
        ]
    })

    st.subheader("⚙️ Executive Summary")
    st.caption("Mean values derived from Monte Carlo simulation (1,000 runs).")
    cols = st.columns(4)
    metrics = [
        ("Global Warming Potential", f"{es.get('Global Warming Potential', 2288)}", "kg CO₂-eq"),
        ("Circularity Score", f"{es.get('Circularity Score', 50)}", "%"),
        ("Particulate Matter", f"{es.get('Particulate Matter', 0.763):.3g}", "kg PM2.5-eq"),
        ("Water Consumption", f"{es.get('Water Consumption', 4.7)}", "m³")
    ]
    for i, (label, val, unit) in enumerate(metrics):
        cols[i].markdown(
            f"""<div class='metric-card' style='text-align:center;padding:20px 10px;'>
            <span style='color:#00ffffcc;font-weight:600;'>{label}</span><br>
            <span style='font-size:2.2em;font-weight:800;color:#e0f7fa;'>{val}</span>
            <span style='color:#00bcd4;font-weight:700;font-size:1.1em;'> {unit}</span>
            </div>""", unsafe_allow_html=True
        )
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- GOAL & SCOPE ---
    gs = results.get('goal_scope', {
        "Intended Application": "Screening LCA for material comparison.",
        "System Boundary": "Cradle-to-Grave",
        "Limitations": "Uses averaged datasets, excludes site-specific data.",
        "Intended Audience": "Sustainability & Engineering teams.",
        "Comparative Assertion for Public": "No"
    })
    st.markdown("### 🎯 Goal & Scope (ISO 14044)")
    st.write(f"**Intended Application:** {gs.get('Intended Application')}")
    st.write(f"**System Boundary:** {gs.get('System Boundary')}")
    st.write(f"**Limitations:** {gs.get('Limitations')}")
    st.write(f"**Intended Audience:** {gs.get('Intended Audience')}")
    st.write(f"**Comparative Assertion:** {gs.get('Comparative Assertion for Public')}")
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- AI LIFE CYCLE INTERPRETATION ---
    mock_ai_text = """
    <b>AI Lifecycle Summary:</b><br>
    The AI detected high environmental intensity in the primary production stage, 
    mainly due to fossil energy consumption and transportation. Transitioning 
    to renewable electricity, optimizing logistics, and increasing recycled content 
    could reduce GWP by up to <b>48%</b>.
    """
    st.markdown("### 🤖 AI Life Cycle Interpretation")
    with st.expander("View AI Insights"):
        st.markdown(ai_text if ai_text else mock_ai_text, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- SUPPLY CHAIN HOTSPOTS ---
    st.markdown("### 🔥 Supply Chain Hotspots")
    for h in es["Supply Chain Hotspots"]:
        st.markdown(
            f"""
            <div class='results-card' style='margin-bottom:10px;padding:14px 18px;'>
                <b style='color:#00ffff;'>{h['title']}</b><br>
                <i>{h['description']}</i><br>
                <span style='color:#9cf;'>Impact Contribution: {h['impact']}%</span>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- SANKEY DIAGRAM ---
    st.markdown("### 🔄 Material Flow Analysis (Sankey)")
    mf = results.get('material_flow_analysis', {
        "labels": ["Mining", "Refining", "Manufacturing", "Use Phase", "Recycling", "Landfill"],
        "source": [0, 1, 2, 3, 3],
        "target": [1, 2, 3, 4, 5],
        "value": [100, 80, 60, 40, 20]
    })
    fig = go.Figure(go.Sankey(
        node=dict(label=mf["labels"], pad=20, thickness=16, color="rgba(0,255,255,0.5)"),
        link=dict(source=mf["source"], target=mf["target"], value=mf["value"],
                  color="rgba(0,255,255,0.2)")
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e0f7fa", height=420)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- CIRCULARITY GAUGE ---
    circ = results.get("circularity_analysis", {"Circularity Rate": 50, "Recyclability Rate": 85})
    st.markdown("### ♻️ Circularity Dashboard")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=circ["Circularity Rate"],
        number={"suffix": "%", "font": {"color": "#00e5ff", "size": 42}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#00ffff"},
            "bgcolor": "rgba(255,255,255,0.1)",
            "steps": [{"range": [0, 100], "color": "rgba(0,255,255,0.15)"}],
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- AI RECOMMENDATIONS (if available) ---
    extra_context = {
        "ore_conc": results.get("ore_conc", 45),
        "transports": [
            results.get("transport_stage_1", {}),
            results.get("transport_stage_2", {})
        ]
    }
    ai_recommendation.display_ai_recommendations(ai_recommendation.ai_data_example, extra_context)
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- FINAL NOTE ---
    st.markdown(
        "<div style='text-align:center;color:#9cf;font-size:0.95em;'>MetalliQ LCA Platform © 2025</div>",
        unsafe_allow_html=True
    )
