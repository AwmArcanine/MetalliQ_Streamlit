import streamlit as st
import pandas as pd
import plotly.express as px

def compare_scenarios_page():
    # ---------- THEME STYLING ----------
    st.markdown("""
    <style>
    .compare-container {
        background: rgba(255,255,255,0.65);
        border-radius: 18px;
        box-shadow: 0 8px 28px rgba(0,109,119,0.15);
        padding: 28px 32px;
        backdrop-filter: blur(10px);
        width: 98%;
        margin: 25px auto;
        animation: fadeIn 0.5s ease-in-out;
    }
    .section-title {
        font-size: 1.35em;
        font-weight: 800;
        color: #00494D;
        border-left: 4px solid #00A896;
        padding-left: 8px;
        margin-top: 25px;
        margin-bottom: 10px;
        letter-spacing: -0.3px;
    }
    .ai-card {
        background: rgba(240,255,252,0.9);
        border: 1.5px solid rgba(0,168,150,0.25);
        border-radius: 14px;
        padding: 16px 20px;
        margin: 20px 0 15px 0;
        box-shadow: 0 4px 16px rgba(0,168,150,0.12);
        transition: all 0.25s ease;
    }
    .ai-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(0,168,150,0.2);
    }
    .ai-title {
        font-weight: 700;
        color: #006D77;
        font-size: 1.1em;
    }
    .ai-text {
        color: #0b2e2f;
        font-size: 1.02em;
        margin-top: 3px;
    }
    .stSelectbox, .stTextInput, .stMultiSelect {
        background: rgba(255,255,255,0.7) !important;
        border-radius: 10px !important;
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- PAGE CONTENT ----------
    st.markdown("<div class='compare-container'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#006D77;font-weight:800;letter-spacing:-0.5px;'>⚖️ Compare Scenarios & Reports</h2>", unsafe_allow_html=True)

    # ---- INPUT PANE ----
    st.markdown("<div class='section-title'>1️⃣ Define New Scenario for Comparison</div>", unsafe_allow_html=True)
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
        st.markdown("<hr style='margin:15px 0;border-color:rgba(0,168,150,0.3);'>", unsafe_allow_html=True)

        # ---- AI SUGGESTION (Static Example) ----
        st.markdown("""
        <div class='ai-card'>
            <div class='ai-title'>🤖 AI Suggestion: Best Fit Material</div>
            <div class='ai-text'>
                For an <b>Automotive</b> application, <b>Steel</b> appears to be the best choice from a climate perspective due to its lower Global Warming Potential.
                However, consider other factors like cost, durability, and other environmental impacts before making a final decision.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ---- IMPACT BREAKDOWN CHART ----
        st.markdown("<div class='section-title'>2️⃣ Impact Breakdown</div>", unsafe_allow_html=True)

        impact_names = [
            "Global Warming Potential",
            "Energy Demand",
            "Water Consumption",
            "Acidification Potential",
            "Eutrophication Potential",
            "Ozone Depletion Potential",
            "Circularity Score"
        ]
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
            height=420,
            template="simple_white",
            text_auto=True
        )
        fig.update_layout(
            legend_title_text="",
            xaxis_title="",
            yaxis_title="Impact Value",
            font=dict(color="#00494D", size=12),
            title=dict(text="", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<hr style='margin:15px 0;border-color:rgba(0,168,150,0.3);'>", unsafe_allow_html=True)

        # ---- DETAILED COMPARISON TABLE ----
        st.markdown("<div class='section-title'>3️⃣ Detailed Impact Table</div>", unsafe_allow_html=True)
        display_table = []
        for i, name in enumerate(impact_names):
            row = {"Impact Metric": name}
            for m in metals:
                val = metal_impact.get(m, [None]*7)[i]
                row[m] = val
            display_table.append(row)
        st.dataframe(pd.DataFrame(display_table), use_container_width=True)

        st.markdown("<hr style='margin:20px 0;border-color:rgba(0,168,150,0.3);'>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- Local Testing ----------
if __name__ == "__main__":
    compare_scenarios_page()
