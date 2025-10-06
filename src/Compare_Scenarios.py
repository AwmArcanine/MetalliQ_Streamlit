import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


def load_theme():
    theme_path = Path("theme.css")
    if theme_path.exists():
        st.markdown(f"<style>{theme_path.read_text()}</style>", unsafe_allow_html=True)


def compare_scenarios_page():
    load_theme()

    st.markdown("<h2 style='color:#00FFFF;font-weight:800;letter-spacing:-0.5px;'>⚖️ Compare Scenarios & Reports</h2>", unsafe_allow_html=True)
    st.caption("Analyze and visualize environmental impacts across different production scenarios.")

    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        application = st.selectbox("Application", ["Automotive", "Building", "Aerospace"])
    with c2:
        scenario = st.selectbox("Route / Scenario", ["Primary Route", "Recycled Route", "Alternative Route"])
    with c3:
        funit = st.text_input("Functional Unit", "1 unit of product")

    metal_options = ["Steel", "Aluminium", "Copper", "Cement", "Polymers (PET)", "Composites (CFRP)"]
    metals = st.multiselect("Metals to Compare", metal_options, default=["Steel", "Aluminium"])

    if st.button(f"Run Comparison ({len(metals)} materials)"):
        st.markdown("<div class='ai-card fade-in'><b>🤖 AI Suggestion:</b> Steel appears to be the most sustainable for automotive use.</div>", unsafe_allow_html=True)

        impact_names = ["Global Warming Potential", "Energy Demand", "Water Consumption", "Acidification Potential"]
        metal_impact = {
            "Aluminium": [2300, 28000, 5, 4.4],
            "Steel": [1900, 26500, 4, 4.1]
        }
        chart_data = []
        for m in metals:
            for i, name in enumerate(impact_names):
                chart_data.append({"Impact": name, "Material": m, "Value": metal_impact.get(m, [None]*4)[i]})
        df_chart = pd.DataFrame(chart_data)
        fig = px.bar(df_chart, x="Impact", y="Value", color="Material", barmode="group", text_auto=True)
        fig.update_layout(
            legend_title_text="Material",
            font=dict(color="#FFFFFF"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df_chart.pivot(index="Impact", columns="Material", values="Value"), use_container_width=True)
