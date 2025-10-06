import streamlit as st
import time
import traceback
from lca_simulation import run_simulation
from results_page import results_page

# --- Material, Region & Autofill Data ---
ORE_AUTOFILLS = {
    "Odisha": {"concentration": 55, "type": "Hematite"},
    "Maharashtra": {"concentration": 46, "type": "Magnetite"},
    "Jharkhand": {"concentration": 60, "type": "Hematite"},
    "Chhattisgarh": {"concentration": 62, "type": "Hematite"},
    "Gujarat": {"concentration": 50, "type": "Magnetite"},
    "Tamil Nadu": {"concentration": 48, "type": "Hematite"},
    "Karnataka": {"concentration": 52, "type": "Magnetite"},
    "West Bengal": {"concentration": 54, "type": "Goethite"},
    "Andhra Pradesh": {"concentration": 49, "type": "Hematite"},
    "Rajasthan": {"concentration": 45, "type": "Magnetite"},
    "Punjab": {"concentration": 47, "type": "Hematite"},
    "Uttar Pradesh": {"concentration": 44, "type": "Goethite"},
    "Telangana": {"concentration": 53, "type": "Hematite"},
    "North India": {"concentration": 41, "type": "Magnetite"},
    "South India": {"concentration": 50, "type": "Hematite"},
    "East India": {"concentration": 55, "type": "Hematite"},
    "West India": {"concentration": 47, "type": "Magnetite"},
    "Central India": {"concentration": 53, "type": "Hematite"},
    "North-East India": {"concentration": 40, "type": "Goethite"},
}

# --- Themed Style ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;500;600&display=swap');

/* Background */
body, .stApp {
    background: linear-gradient(135deg, #003C43 0%, #006D77 40%, #83C5BE 100%) !important;
    color: #E0FBFC;
    font-family: 'Poppins', sans-serif;
    overflow-x: hidden;
}

/* Fade-in animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(15px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Card Style */
.card {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(124, 244, 227, 0.25);
    border-radius: 18px;
    padding: 20px 25px;
    box-shadow: 0 8px 25px rgba(0, 109, 119, 0.4);
    margin-bottom: 25px;
    animation: fadeIn 0.7s ease forwards;
}

/* Section Headers */
.card h3 {
    font-family: 'Orbitron', sans-serif;
    color: #02C39A !important;
    text-shadow: 0 0 15px rgba(124, 244, 227, 0.7);
    margin-bottom: 8px;
}
.card hr {
    border: 0;
    height: 2px;
    background: linear-gradient(90deg, rgba(124,244,227,0.7), rgba(255,255,255,0));
    margin-bottom: 18px;
}

/* Inputs */
input, textarea {
    background: rgba(255,255,255,0.1) !important;
    color: #E0FBFC !important;
    border: 1px solid rgba(124,244,227,0.3) !important;
    border-radius: 10px !important;
}
input:focus, textarea:focus {
    outline: none !important;
    border-color: #02C39A !important;
    box-shadow: 0 0 10px rgba(124,244,227,0.4);
}

/* Selectboxes */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.1) !important;
    color: #E0FBFC !important;
    border-radius: 10px !important;
}

/* Button */
div.stButton > button {
    background: linear-gradient(90deg, #00A896 0%, #02C39A 100%) !important;
    color: #033E3E !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 0.7em 2.6em !important;
    box-shadow: 0 0 15px rgba(124,244,227,0.4);
    transition: all 0.3s ease-in-out;
}
div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 25px rgba(124,244,227,0.7);
}

/* Progress Bar */
#progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 6px;
    width: 0%;
    background: linear-gradient(90deg, #02C39A, #00A896, #83C5BE);
    box-shadow: 0 0 15px rgba(124,244,227,0.7);
    transition: width 0.4s ease;
    z-index: 9999;
}
</style>
<div id="progress-bar"></div>
<script>
let bar = document.getElementById("progress-bar");
bar.style.width = "0%";
</script>
""", unsafe_allow_html=True)

st.title("AI-Powered Metals Sustainability Study ⚙️")

with st.container():
    st.markdown("<div class='card'><h3>🎯 Goal & Scope Definition (ISO 14044)</h3><hr>", unsafe_allow_html=True)
    intended_app = st.text_input("Intended Application", "Compare material choices for internal R&D")
    system_boundary = st.selectbox("System Boundary", ["Cradle-to-Gate", "Cradle-to-Grave", "Gate-to-Gate", "Cradle-to-Cradle"])
    intended_audience = st.text_input("Intended Audience", "Internal engineering and sustainability departments.")
    comparative_assertion = st.radio("Comparative Assertion for Public Disclosure?", ["No", "Yes"], horizontal=True)
    study_limitations = st.text_area("Study Limitations", "Uses industry-average datasets; site-specific data not included.")
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='card'><h3>🏗️ Project & Material</h3><hr>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name", "New Building Frame")
        category = st.selectbox("Category / Application", ["Construction", "Automotive", "Aerospace", "Packaging", "Other"])
    with col2:
        material = st.selectbox("Material", ["Steel", "Aluminum", "Copper", "Nickel", "Titanium"])
        region = st.selectbox("Analysis Region", list(ORE_AUTOFILLS.keys()) + ["China", "EU", "USA"], index=0)

    if region in ORE_AUTOFILLS:
        st.session_state["ore_conc"] = ORE_AUTOFILLS[region]["concentration"]
        st.session_state["ore_type"] = ORE_AUTOFILLS[region]["type"]
    else:
        st.session_state.setdefault("ore_conc", 50)
        st.session_state.setdefault("ore_type", "Bauxite")

    ore_conc = st.number_input("Metal Ore Concentration (%)", min_value=0.0, max_value=100.0,
                               value=float(st.session_state["ore_conc"]), step=0.5)
    ore_type = st.text_input("Type of Ore", st.session_state["ore_type"])
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='card'><h3>♻️ Lifecycle Stages</h3><hr>", unsafe_allow_html=True)
    functional_unit = st.text_input("Functional Unit", "1 ton of product")
    sec_material_content = st.number_input("Secondary Material Content (%)", 0.0, 100.0, 10.0)
    production_process = st.selectbox("Production Process", ["Primary Route", "Secondary Route", "Smelting", "Casting"])
    end_life_scenario = st.selectbox("End of Life Cycle Scenario", ["90% Recycled", "50% Recycled", "Landfill"])
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='card'><h3>📊 Data Quality & Uncertainty</h3><hr>", unsafe_allow_html=True)
    reliability = st.slider("Reliability", 1, 5, 4)
    completeness = st.slider("Completeness", 1, 5, 4)
    temporal = st.slider("Temporal Correlation", 1, 5, 4)
    geographical = st.slider("Geographical Correlation", 1, 5, 4)
    technological = st.slider("Technological Correlation", 1, 5, 4)
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("Run Analysis"):
    try:
        st.markdown("<script>document.getElementById('progress-bar').style.width='10%';</script>", unsafe_allow_html=True)
        with st.spinner("Running LCA simulation..."):
            results = run_simulation({
                "intended_app": intended_app,
                "intended_audience": intended_audience,
                "system_boundary": system_boundary,
                "study_limitations": study_limitations,
                "comparative_assertion": comparative_assertion,
                "project_name": project_name,
                "category": category,
                "material": material,
                "region": region,
                "ore_type": ore_type,
                "ore_conc": ore_conc,
                "functional_unit": functional_unit,
                "sec_material_content": sec_material_content,
                "production_process": production_process,
                "end_life_scenario": end_life_scenario,
                "reliability": reliability,
                "completeness": completeness,
                "temporal": temporal,
                "geographical": geographical,
                "technological": technological
            })
        for i in range(11, 101, 5):
            st.markdown(f"<script>document.getElementById('progress-bar').style.width='{i}%';</script>", unsafe_allow_html=True)
            time.sleep(0.05)
        st.success("✅ Simulation Complete!")
        results_page(results, results.get("ai_life_cycle_interpretation", ""))
    except Exception as e:
        st.error(f"❌ Simulation failed: {e}")
        st.text(traceback.format_exc())
