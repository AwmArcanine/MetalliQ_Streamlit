import streamlit as st
import time
import traceback
from lca_simulation import run_simulation
from results_page import results_page


# ------------------------------- CONSTANTS -------------------------------
MATERIALS = [
    "Steel", "Stainless Steel", "Aluminum", "Copper", "Zinc", "Lead",
    "Chromium", "Nickel", "Magnesium", "Tin", "Titanium"
]

CATEGORY_APPS = [
    "Construction", "Automotive", "Aerospace", "Electrical & Electronics",
    "Packaging", "Railways", "Defence", "Consumer Goods", "Power Transmission"
]

INDIA_REGIONS = [
    "North India", "South India", "East India", "West India", "Central India", "North-East India",
    "Maharashtra", "Odisha", "Gujarat", "Jharkhand", "Tamil Nadu", "Chhattisgarh",
    "Karnataka", "West Bengal", "Andhra Pradesh", "Rajasthan", "Punjab", "Uttar Pradesh", "Telangana"
]

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


# ------------------------------- PAGE FUNCTION -------------------------------
def full_lca_study_form():
    st.set_page_config(layout="wide")

    # ------------------------------- THEME -------------------------------
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

        body, .stApp {
            background: #F6FAFB !important;
            font-family: 'Poppins', sans-serif !important;
            color: #1E1E1E;
        }

        h1, h2, h3 {
            color: #00494D !important;
            font-weight: 700 !important;
        }

        .section-card {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 16px;
            padding: 24px 28px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin-bottom: 25px;
            border: 1px solid rgba(0,109,119,0.15);
        }

        label, .stMarkdown, p, span, div {
            color: #003638 !important;
        }

        input, textarea, select {
            background: rgba(255,255,255,0.9) !important;
            color: #00494D !important;
            border-radius: 8px !important;
            border: 1px solid rgba(0,109,119,0.2) !important;
        }

        div[data-baseweb="select"] > div {
            background-color: rgba(255,255,255,0.9) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(0,109,119,0.2) !important;
        }

        /* Run Button */
        div.stButton > button {
            background: linear-gradient(90deg,#00A896,#02C39A);
            color: white !important;
            border-radius: 10px !important;
            border: none;
            padding: 0.6em 2em;
            font-weight: 600;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            box-shadow: 0 0 12px rgba(0, 168, 150, 0.6);
            transform: scale(1.03);
        }

        /* Inline Progress Bar */
        #progressbar {
            height: 5px;
            border-radius: 5px;
            background: rgba(0,168,150,0.15);
            overflow: hidden;
            margin-bottom: 20px;
        }
        #progressbar > div {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg,#00A896,#02C39A);
            transition: width 0.4s ease;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>AI-Powered Metals Sustainability Study 🌿</h1>", unsafe_allow_html=True)
    st.markdown("<div id='progressbar'><div></div></div>", unsafe_allow_html=True)

    # ------------------------------- FORM START -------------------------------
    with st.form("lca_study"):
        st.markdown("<div class='section-card'><h3>🎯 Goal & Scope Definition (ISO 14044)</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            intended_app = st.text_input("Intended Application", "Screening assessment for internal R&D.")
            system_boundary = st.selectbox("System Boundary", ["Cradle-to-Gate", "Cradle-to-Grave", "Gate-to-Gate", "Cradle-to-Cradle"], 0)
        with col2:
            intended_audience = st.text_input("Intended Audience", "Internal sustainability team.")
            comparative_assertion = st.radio("Comparative Assertion for Public Disclosure?", ["No", "Yes"], horizontal=True)
        study_limitations = st.text_area("Study Limitations", "Results are for design guidance only.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'><h3>🏗️ Project & Material</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("Project Name", "Building Frame Study")
            category = st.selectbox("Category / Application", CATEGORY_APPS, 0)
        with col2:
            material = st.selectbox("Material", MATERIALS, 0)
            region = st.selectbox("Analysis Region", list(ORE_AUTOFILLS.keys()) + ["Global Average"], 0)

            if region in ORE_AUTOFILLS:
                st.session_state["ore_conc"] = ORE_AUTOFILLS[region]["concentration"]
                st.session_state["ore_type"] = ORE_AUTOFILLS[region]["type"]
            ore_conc = st.number_input("Metal Ore Concentration (%)", 0.0, 100.0, float(st.session_state.get("ore_conc", 50)))
            ore_type = st.text_input("Type of Ore", st.session_state.get("ore_type", "Hematite"))
            coatings = st.selectbox("Coatings / Additives", ["None", "Anodized", "Painted/Epoxy", "Chromium plated", "Nickel plated", "Powder coated", "Galvanized Zinc"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'><h3>♻️ Lifecycle Stages</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            functional_unit = st.text_input("Functional Unit", "1 ton of product")
            sec_material_content = st.number_input("Secondary Material Content (%)", 0.0, 100.0, 10.0)
        with col2:
            production_process = st.selectbox("Production Process", ["Primary Route (BF-BOF)", "Secondary Route (EAF)", "Smelting", "Casting"], 1)
            use_duration = st.text_input("Use Phase Duration (years)", "30")
            end_life_scenario = st.selectbox("End-of-Life Scenario", ["90% Recycled", "50/50 Landfill", "100% Landfill"], 0)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'><h3>🚚 Transportation Stages</h3>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            transport1_stage = st.text_input("Stage 1 Name", "Mine to Plant")
        with col2:
            transport1_mode = st.selectbox("Mode", ["Truck", "Train", "Ship"], 0)
        with col3:
            transport1_fuel = st.selectbox("Fuel Type", ["Diesel", "Electric"], 0)
        with col4:
            transport1_dist = st.number_input("Distance (km)", 0.0, 10000.0, 75.0)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'><h3>⚙️ Advanced Parameters</h3>", unsafe_allow_html=True)
        grid_elec_mix = st.selectbox("Grid Electricity Mix", ["India - Grid Average", "India - Southern", "India - Western"], 0)
        water_source = st.selectbox("Water Source", ["Surface", "Groundwater", "Municipal"], 0)
        proceff = st.number_input("Process Energy Efficiency (%)", 0.0, 100.0, 85.0)
        lifetime_ext = st.number_input("Product Lifetime Extension (Years)", 0, 200, 5)
        waste_method = st.selectbox("Waste Treatment Method", ["Recycling", "Landfill", "Incineration"], 0)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'><h3>📊 Data Quality Assessment</h3>", unsafe_allow_html=True)
        reliability = st.slider("Reliability", 1, 5, 4)
        completeness = st.slider("Completeness", 1, 5, 4)
        temporal = st.slider("Temporal Correlation", 1, 5, 4)
        geographical = st.slider("Geographical Correlation", 1, 5, 4)
        technological = st.slider("Technological Correlation", 1, 5, 4)
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("Run Analysis")

    # ------------------------------- SIMULATION -------------------------------
    if submitted:
        form_data = locals().copy()

        js_fill_script = """
        <script>
        let bar = document.querySelector("#progressbar > div");
        if(bar){
            bar.style.width = "0%";
            let width = 0;
            let fill = setInterval(()=>{
                width += 2;
                if(width > 100) clearInterval(fill);
                bar.style.width = width + "%";
            }, 50);
        }
        </script>
        """
        st.markdown(js_fill_script, unsafe_allow_html=True)

        try:
            with st.spinner("Running LCA simulation..."):
                results = run_simulation(form_data)
                time.sleep(2)
            st.success("✅ Simulation complete!")
            st.markdown("<script>document.querySelector('#progressbar > div').style.width='100%';</script>", unsafe_allow_html=True)
            ai_text = results.get("ai_lifecycle_interpretation", "")
            results_page(results, ai_text)
        except Exception as e:
            st.error(f"❌ Simulation failed: {e}")
            st.text(traceback.format_exc())
