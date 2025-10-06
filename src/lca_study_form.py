import streamlit as st
import time
from lca_simulation import run_simulation
from results_page import results_page
from ai_recommendation import ai_data_example
# --- MetalliQ Neon-Teal Theme for LCA Study Form ---
def full_lca_study_form():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;500;600&display=swap');

        body, .stApp {
            background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #83C5BE 100%) !important;
            color: #E0FFFF;
            font-family: 'Poppins', sans-serif;
        }

        /* --- Form Container --- */
        .stForm {
            border: 1.8px solid rgba(0, 239, 255, 0.6);
            border-radius: 16px !important;
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 0 0 25px rgba(0, 239, 255, 0.2);
            padding: 20px !important;
        }

        /* --- Headings --- */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            color: #00EFFF !important;
            text-shadow: 0 0 18px rgba(0,239,255,0.8);
        }
        h3 {
            margin-top: 35px !important;
        }

        /* --- Labels and Field Text --- */
        label, p, span, div, .stMarkdown {
            color: #E0FFFF !important;
        }

        /* --- Input Fields --- */
        input, textarea {
            background: rgba(255,255,255,0.1) !important;
            color: #033E3E !important;
            border: 1px solid rgba(0,239,255,0.3) !important;
            border-radius: 10px !important;
            font-size: 0.95rem !important;
        }
        input:focus, textarea:focus {
            outline: none !important;
            border-color: #00EFFF !important;
            box-shadow: 0 0 10px rgba(0,239,255,0.4);
        }
        /* --- FIX for SELECTBOX TEXT COLOR --- */
        div[data-baseweb="select"] > div {
            background-color: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(0,239,255,0.3) !important;
            border-radius: 10px !important;
            color: #033E3E !important;
        }
        div[data-baseweb="select"] > div:hover {
            border-color: #00EFFF !important;
        }
        div[data-baseweb="select"] > div > div {
            color: #033E3E !important; /* selected text color */
        }
        div[data-baseweb="popover"] li {
            background-color: rgba(0,73,77,0.9) !important;
            color: #033E3E !important; /* dropdown option text color */
        }
        div[data-baseweb="popover"] li:hover {
            background-color: rgba(0,239,255,0.2) !important;
            color: #033E3E !important;
        }
        /* --- Neon Button (Run Analysis) --- */
        div.stButton > button, div[data-testid="baseButton-secondary"] button {
            background: linear-gradient(90deg, #00EFFF 0%, #00B8CC 100%) !important;
            color: #033E3E !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            border: none !important;
            padding: 0.7em 2.6em !important;
            font-size: 1.05rem !important;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 0 15px rgba(0,239,255,0.3);
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg, #00B8CC 0%, #00EFFF 100%) !important;
            box-shadow: 0 0 30px rgba(0,239,255,0.6);
            transform: scale(1.04);

        /* --- Radio, Slider, etc --- */
        .stRadio > label, .stSlider, .stSelectbox {
            color: #E0FFFF !important;
        }
        .stSlider > div > div {
            background: linear-gradient(90deg, #00EFFF, #00B8CC) !important;
        }

        /* --- Section Captions --- */
        caption, .stCaption {
            color: #A7FAFF !important;
            font-size: 0.85rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("AI-Powered Metals Sustainability")

    with st.form("lca_full_study"):
        # -------- SECTION 1 --------
        st.markdown("### 🎯 Goal & Scope Definition (ISO 14044)")
        col1, col2 = st.columns(2)
        with col1:
            intended_app = st.text_input(
                "Intended Application",
                value="Screening assessment for internal R&D purposes to compare material choices."
            )
            system_boundary = st.selectbox(
                "System Boundary",
                ["Cradle-to-Gate", "Cradle-to-Grave", "Gate-to-Gate", "Cradle-to-Cradle"],
                index=0
            )
        with col2:
            intended_audience = st.text_input(
                "Intended Audience", value="Internal engineering and sustainability departments.")
            comparative_assertion = st.radio(
                "Comparative Assertion for Public Disclosure?",
                ["No", "Yes"], horizontal=True, index=0
            )
        study_limitations = st.text_area(
            "Study Limitations",
            value="This analysis relies on industry-average data from recent Indian/International LCA datasets. Results are for design guidance; site-specific emissions are not included."
        )

        # -------- SECTION 2 --------
        st.markdown("### 🏗️ Project & Material")
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("Project Name", value="New Building Frame")
            category = st.selectbox(
                "Category / Application",
                ["Packaging", "Structural", "Automotive", "Construction", "Aerospace", "Railways", "Defence", "Electronics", "Power Transmission", "Other"],
                index=0
            )
            ore_conc = st.number_input("Metal Ore Concentration (%)", min_value=0.0, max_value=100.0, value=45.0, step=0.1)
            alloy_complexity = st.selectbox(
                "Alloy Complexity",
                ["Simple Alloy (High Purity)", "Ferritic", "Austenitic", "Martensitic", "High Carbon", "Low Alloy", "Medium Alloy", "High Alloy"],
                index=0
            )
        with col2:
            material = st.selectbox(
                "Material",
                ["Aluminum", "Steel", "Copper", "Zinc", "Lead", "Nickel", "Magnesium", "Titanium", "Stainless Steel", "Other"],
                index=0
            )
            analysis_region = st.selectbox(
                "Analysis Region",
                ["India - Odisha (Barbil)", "India - Gujarat", "India - Jharkhand (Singhbhum)", "India - Chhattisgarh", "India - Maharashtra", "India - West Bengal", "China", "EU", "USA", "Other Asia", "Global - Average", "Other"],
                index=0
            )
            ore_type = st.text_input("Type of Ore (Optional)", value="Bauxite")
            coatings = st.selectbox(
                "Coatings / Additives",
                ["None", "Anodized", "Painted/Epoxy", "Chromium plated", "Nickel plated", "Powder coated", "Galvanized Zinc", "Other"],
                index=0
            )

        # -------- SECTION 3 --------
        st.markdown("### ♻️ Lifecycle Stages")
        col1, col2 = st.columns(2)
        with col1:
            functional_unit = st.text_input("Functional Unit", value="1 ton of product")
            sec_material_content = st.number_input("Secondary Material Content (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
        with col2:
            production_process = st.selectbox(
                "Production Process",
                ["Primary Route (BF-BOF)", "Secondary Route (EAF)", "Bauxite Refining", "DRI - Coal", "DRI - Gas", "Smelting", "Casting", "Forging", "Powder Metallurgy", "Other"],
                index=2
            )
            use_duration = st.text_input("Use Phase Duration (years)", value="35")
            end_life_scenario = st.selectbox(
                "End of Life Cycle Scenario",
                ["90% Recycled", "50% Recycled / 50% Landfill", "100% Landfill", "Other"],
                index=0
            )

        # -------- SECTION 4 --------
        st.markdown("### 🚚 Transportation Stages")
        st.caption("*Example: mine → concentrator → plant*")

        st.markdown("#### Stage 1")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            transport1_stage = st.text_input("Stage Name", value="Mine to Concentrator")
        with col2:
            transport1_mode = st.selectbox("Mode", ["Truck", "Train", "Ship", "Other"], index=0, key="mode1")
        with col3:
            transport1_fuel = st.selectbox("Fuel Type", ["Diesel", "Electric", "Petrol", "Other"], index=0, key="fuel1")
        with col4:
            transport1_dist = st.number_input("Distance (km)", min_value=0.0, value=75.0, step=1.0, key="dist1")

        st.markdown("#### Stage 2")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            transport2_stage = st.text_input("Stage Name", value="Concentrator to Plant")
        with col2:
            transport2_mode = st.selectbox("Mode", ["Train", "Truck", "Ship", "Other"], index=0, key="mode2")
        with col3:
            transport2_fuel = st.selectbox("Fuel Type", ["Diesel", "Electric", "Other"], index=1, key="fuel2")
        with col4:
            transport2_dist = st.number_input("Distance (km)", min_value=0.0, value=250.0, step=1.0, key="dist2")

        # -------- SECTION 5 --------
        st.markdown("### ⚙️ Advanced Parameters")
        grid_elec_mix = st.selectbox(
            "Grid Electricity Mix",
            ["India - Grid Average", "India - Eastern Region (Coal Heavy)", "India - Western Region", "India - Southern Region", "India - Northern Region", "International Best", "Other"],
            index=0
        )
        water_source = st.selectbox("Water Source", ["Surface", "Groundwater", "Municipal", "Rainwater", "Other"], index=0)
        proceff = st.number_input("Process Energy Efficiency (%)", min_value=0.0, max_value=100.0, value=85.0, step=0.1)
        lifetime_ext = st.number_input("Product Lifetime Extension (Years)", min_value=0, max_value=200, value=5, step=1)
        waste_method = st.selectbox(
            "Waste Treatment Method",
            ["Recycling", "Controlled Landfill", "Open Landfill", "Incineration", "Composting", "Other"], index=0
        )

        # -------- SECTION 6 --------
        st.markdown("### 📊 Data Quality Assessment & Uncertainty (Pedigree Matrix)")
        reliability = st.slider("Reliability", 1, 5, 4)
        completeness = st.slider("Completeness", 1, 5, 4)
        temporal = st.slider("Temporal Correlation", 1, 5, 4)
        geographical = st.slider("Geographical Correlation", 1, 5, 4)
        technological = st.slider("Technological Correlation", 1, 5, 4)

        submitted = st.form_submit_button("Run Analysis")

        if submitted:
            # Collect form data
            form_data = {
                "intended_app": intended_app,
                "intended_audience": intended_audience,
                "system_boundary": system_boundary,
                "study_limitations": study_limitations,
                "comparative_assertion": comparative_assertion,
                "project_name": project_name,
                "category": category,
                "material": material,
                "region": analysis_region,
                "ore_type": ore_type,
                "ore_conc": ore_conc,
                "reliability": reliability,
                "completeness": completeness,
                "temporal": temporal,
                "geographical": geographical,
                "technological": technological
            }

            # Save to session
            st.session_state["lca_form_data"] = form_data

            try:
                # ✅ Run your simulation function directly
                st.info("Running LCA simulation... Please wait ⏳")
                results = run_simulation(form_data)
                st.session_state["lca_results"] = results
                progress_bar = st.progress(0)
                st.success("✅ LCA Simulation completed successfully!")
                for i in range(101):
                    time.sleep(0.05)
                    progress_bar.progress(i)
                ai_text = results.get("ai_lifecycle_interpretation","")
                st.markdown("<hr>",unsafe_allow_html=True)
                results_page(results,ai_text)

                
            except Exception as e:
                st.error(f"❌ Simulation failed: {e}")
