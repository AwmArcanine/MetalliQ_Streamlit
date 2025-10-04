import streamlit as st
import pandas as pd
import plotly.express as px

def compare_scenarios_page():
    st.title("Compare Scenarios & Reports")

    # ---- INPUT PANE ----
    st.markdown("#### 1. Define New Scenario for Comparison")
    c1, c2, c3 = st.columns([2,2,2])
    with c1:
        application = st.selectbox("Application", ["Automotive", "Building", "Aerospace"])
    with c2:
        scenario = st.selectbox("Route / Scenario", ["Primary Route", "Recycled Route", "Alternative Route"])
    with c3:
        funit = st.text_input("Functional Unit", "1 unit of product")
    
    metal_options = ["Steel", "Aluminium", "Copper", "Cement", "Polymers (PET)", "Composites (CFRP)", "Solar PV Panel", "Wind Turbine Blade"]
    metals = st.multiselect("Metals to Compare", metal_options, default=["Steel", "Aluminium"])
    
    st.markdown("")
    if st.button(f"Run Comparison ({len(metals)} materials)"):
        st.markdown("---")

        # ---- AI SUGGESTION (Static Example) ----
        st.markdown(
            """
            <div style='background:#f6fafd;border-radius:14px;padding:19px 18px 14px 26px;margin-bottom:16px;box-shadow:0 3px 11px #dfeeff80;'>
              <b>AI Suggestion: Best Fit Material</b>
              <div style='color:#646a70;margin-top:.2em;'>
                 For an <b>Automotive</b> application, <b>Steel</b> appears to be the best choice from a climate perspective due to its lower Global Warming Potential.
                 However, consider other factors like cost, durability, and other environmental impacts before making a final decision.
              </div>
            </div>
            """, unsafe_allow_html=True
        )

        # ---- IMPACT BREAKDOWN CHART ----
        st.markdown("#### Impact Breakdown")
        # Demo data for two metals and main impacts
        impact_names = [
            "Global Warming Potential",
            "Energy Demand",
            "Water Consumption",
            "Acidification Potential",
            "Eutrophication Potential",
            "Ozone Depletion Potential",
            "Circularity Score"
        ]
        # Example impact values: {metal: [GWP, Energy, ...]}
        metal_impact = {
            "Aluminium": [2300, 28000, 5, 4.4, 1.2, 0.0029, 27],
            "Steel":     [1900, 26500, 4, 4.1, 1.1, 0.00175, 50]
        }
        chart_data = []
        for m in metals:
            for i, name in enumerate(impact_names):
                chart_data.append({"Impact": name, "Material": m, "Value": metal_impact.get(m, [None]*7)[i]})
        df_chart = pd.DataFrame(chart_data)
        fig = px.bar(
            df_chart, 
            x="Impact", 
            y="Value", 
            color="Material", 
            barmode="group",
            height=380,
            template="simple_white",
            text_auto=True
        )
        fig.update_layout(legend_title_text="", xaxis_title="", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")

        # ---- DETAILED COMPARISON TABLE ----
        st.markdown("#### Detailed Impact Table")
        display_table = []
        for i, name in enumerate(impact_names):
            row = {"Impact Metric": name}
            for m in metals:
                val = metal_impact.get(m, [None]*7)[i]
                row[m] = val
            display_table.append(row)
        st.dataframe(pd.DataFrame(display_table))

        st.markdown("---")
        
# Usage
if __name__ == "__main__":
    compare_scenarios_page()
