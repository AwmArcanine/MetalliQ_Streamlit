import streamlit as st

# --- MetalliQ Neon-Teal Theme for LCA Study Form ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;500;600&display=swap');

body, .stApp {
    background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #83C5BE 100%) !important;
    color: #E0FFFF !important;
    font-family: 'Poppins', sans-serif !important;
}

/* Headings */
h1 {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2.1rem !important;
    color: #00EFFF !important;
    text-shadow: 0 0 15px rgba(0,239,255,0.8);
    margin-bottom: 10px !important;
}

h2, h3, h4, h5, h6 {
    color: #C8FAF8 !important;
    font-weight: 600 !important;
}

/* Labels & Inputs */
label, .stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label {
    color: #E6FFFF !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}

.stTextInput, .stSelectbox, .stNumberInput, .stTextArea {
    color: #E6FFFF !important;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #00A896 0%, #02C39A 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    box-shadow: 0 0 15px rgba(0,168,150,0.4);
    transition: all 0.25s ease-in-out;
}
div.stButton > button:hover {
    box-shadow: 0 0 20px rgba(0,239,255,0.8);
    transform: scale(1.04);
}

/* Form fields */
.stTextInput input, .stNumberInput input, textarea {
    background: rgba(255,255,255,0.1) !important;
    color: #E6FFFF !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
}

/* Radio buttons and sliders */
.stRadio label {
    color: #E0FFFF !important;
}
.stSlider label {
    color: #C8FAF8 !important;
}

/* Section Titles */
.stMarkdown h3 {
    color: #7CF4E3 !important;
    text-shadow: 0 0 10px rgba(124,244,227,0.6);
}

/* Captions */
.stCaption, .stMarkdown small {
    color: #B5EDE9 !important;
}

/* Success message */
.stSuccess {
    background: rgba(0,239,255,0.1) !important;
    color: #00EFFF !important;
    border: 1px solid rgba(0,239,255,0.4) !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)


def full_lca_study_form():
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
            st.success("Inputs saved and sent for LCA simulation.", icon="✅")
