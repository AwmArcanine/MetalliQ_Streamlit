# lca_study_form.py
# Fixed version with robust autofill (region -> ore concentration/type)
# - Uses st.session_state and selectbox on_change callback so autofill always works
# - Preserves all original input fields from your provided file
# - Keeps the subtle header progress placeholder (you can animate it during simulation)
# Note: this file expects lca_simulation.run_simulation and results_page.results_page to exist.

import streamlit as st
import time
import traceback
from lca_simulation import run_simulation
from results_page import results_page

# ---------------------------------------------------------------------
# Constants (copied from your original file)
# ---------------------------------------------------------------------
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

ALLOY_COMPLEXITY = [
    "Ferritic", "Austenitic", "Martensitic", "High Carbon", "Low Alloy", "Medium Alloy", "High Alloy"
]

COATINGS = [
    "Galvanized (Zinc)", "Anodized (Aluminum)", "Painted/Epoxy", "Chromium plated", "Nickel plated",
    "Phosphate", "Tin plating", "Powder coated", "None"
]

PRODUCTION_PROCESSES = [
    "Blast Furnace", "Electric Arc Furnace", "DRI (Direct Reduced Iron)", "Bauxite Refining",
    "Smelting", "Rolling Mill", "Casting", "Forging", "Extrusion"
]

FUEL_TYPES = [
    "Diesel", "Petrol", "LPG", "CNG", "Bio-Diesel", "Coal", "Natural Gas", "Electricity"
]

CHARGING_POWER = [
    "Grid Electricity", "Solar", "Wind", "Biomass", "Hydro", "Battery Swapping"
]

GRID_MIX = [
    "Western Grid", "Northern Grid", "Eastern Grid", "Southern Grid", "Central Grid",
    "North-Eastern Grid", "Maharashtra State Grid", "Tamil Nadu State Grid", "Gujarat State Grid"
]

WATER_SOURCES = [
    "Municipal Supply", "Groundwater", "Ganga River", "Yamuna River", "Godavari River", "Brahmaputra River",
    "Rainwater", "Recycled/Reuse"
]

WASTE_METHODS = [
    "Landfill", "Chemical Precipitation", "Incineration", "Recycling", "Pyrometallurgical Processing",
    "Biological Treatment", "Coagulation/Flocculation"
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


# ---------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------
def full_lca_study_form():
    st.set_page_config(layout="wide", page_title="LCA Study Form")
    # Basic theme (keeps visuals consistent with workspace)
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
      body, .stApp { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #83C5BE 100%) !important; color: #E0FFFF; }
      .section-card { background: rgba(255,255,255,0.06); padding:18px; border-radius:12px; border:1px solid rgba(255,255,255,0.06); margin-bottom:18px; }
      label, .stMarkdown, p, span, div { color: #E0FFFF !important; }
      div[data-baseweb="select"] > div { background-color: rgba(255,255,255,0.06) !important; color:#033E3E !important; border-radius:10px !important; border:1px solid rgba(0,239,255,0.12) !important; }
      input, textarea { background: rgba(255,255,255,0.9) !important; color: #033E3E !important; border-radius: 8px !important; }
      /* style progress (Streamlit progress) */
      div.stProgress > div > div { background: linear-gradient(90deg,#00EFFF,#00B8CC) !important; height: 6px !important; border-radius: 6px !important;}
    </style>
    """, unsafe_allow_html=True)

    st.title("AI-Powered Metals Sustainability Study")

    # Create a header progress widget (initially 0%)
    header_progress = st.progress(0)

    # -----------------------------
    # Ensure session_state defaults for autofill keys
    # -----------------------------
    # default region so selectbox has a stable key value at first render
    if "analysis_region" not in st.session_state:
        # choose first key from ORE_AUTOFILLS for initial autofill
        default_region = list(ORE_AUTOFILLS.keys())[0] if len(ORE_AUTOFILLS) > 0 else "Global - Average"
        st.session_state.analysis_region = default_region

    # initialize ore_conc_input and ore_type_input if absent (so fields have values)
    if "ore_conc_input" not in st.session_state:
        # if initial region is defined in ORE_AUTOFILLS, use it
        reg0 = st.session_state.get("analysis_region")
        if reg0 in ORE_AUTOFILLS:
            st.session_state.ore_conc_input = float(ORE_AUTOFILLS[reg0]["concentration"])
            st.session_state.ore_type_input = ORE_AUTOFILLS[reg0]["type"]
        else:
            st.session_state.ore_conc_input = 50.0
            st.session_state.ore_type_input = "Bauxite"

    # callback when analysis_region selectbox changes
    def _on_region_change():
        reg = st.session_state.get("analysis_region")
        if reg in ORE_AUTOFILLS:
            st.session_state.ore_conc_input = float(ORE_AUTOFILLS[reg]["concentration"])
            st.session_state.ore_type_input = ORE_AUTOFILLS[reg]["type"]
        else:
            # optional: set sensible defaults when region not in mapping
            st.session_state.ore_conc_input = st.session_state.get("ore_conc_input", 50.0)
            st.session_state.ore_type_input = st.session_state.get("ore_type_input", "Bauxite")


    # -----------------------------
    # The form (all original inputs preserved)
    # -----------------------------
    with st.form("lca_full_study"):
        # -------- SECTION 1 --------
        st.markdown("<div class='section-card'><h3 style='color:#00EFFF'>🎯 Goal & Scope Definition (ISO 14044)</h3>", unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)

        # -------- SECTION 2 --------
        st.markdown("<div class='section-card'><h3 style='color:#00EFFF'>🏗️ Project & Material</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("Project Name", value="New Building Frame")
            category = st.selectbox(
                "Category / Application",
                ["Packaging", "Structural", "Automotive", "Construction", "Aerospace", "Railways", "Defence", "Electronics", "Power Transmission", "Other"],
                index=0
            )
        with col2:
            material = st.selectbox(
                "Material",
                ["Aluminum", "Steel", "Copper", "Zinc", "Lead", "Nickel", "Magnesium", "Titanium", "Stainless Steel", "Other"],
                index=0
            )

            # Analysis region selectbox uses session_state key and on_change callback
            analysis_region = st.selectbox(
                "Analysis Region",
                list(ORE_AUTOFILLS.keys()) + ["China", "EU", "USA", "Other Asia", "Global - Average", "Other"],
                index=0,
                key="analysis_region",
                on_change=_on_region_change
            )

            # editable autofilled fields bound to session_state keys
            ore_conc = st.number_input(
                "Metal Ore Concentration (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(st.session_state.get("ore_conc_input", 50.0)),
                step=0.5,
                key="ore_conc_input",
            )
            ore_type = st.text_input(
                "Type of Ore (Optional)",
                value=st.session_state.get("ore_type_input", "Bauxite"),
                key="ore_type_input",
            )
            coatings = st.selectbox(
                "Coatings / Additives",
                ["None", "Anodized", "Painted/Epoxy", "Chromium plated", "Nickel plated", "Powder coated", "Galvanized Zinc", "Other"],
                index=0
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # -------- SECTION 3 --------
        st.markdown("<div class='section-card'><h3 style='color:#00EFFF'>♻️ Lifecycle Stages</h3>", unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)

        # -------- SECTION 4 --------
        st.markdown("<div class='section-card'><h3 style='color:#00EFFF'>🚚 Transportation Stages</h3><div style='color:rgba(224,255,255,0.8);font-size:13px;margin-top:6px'>*Example: mine → concentrator → plant*</div>", unsafe_allow_html=True)

        st.markdown("#### Stage 1", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            transport1_stage = st.text_input("Stage Name", value="Mine to Concentrator")
        with col2:
            transport1_mode = st.selectbox("Mode", ["Truck", "Train", "Ship", "Other"], index=0, key="mode1")
        with col3:
            transport1_fuel = st.selectbox("Fuel Type", ["Diesel", "Electric", "Petrol", "Other"], index=0, key="fuel1")
        with col4:
            transport1_dist = st.number_input("Distance (km)", min_value=0.0, value=75.0, step=1.0, key="dist1")

        st.markdown("#### Stage 2", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            transport2_stage = st.text_input("Stage Name", value="Concentrator to Plant")
        with col2:
            transport2_mode = st.selectbox("Mode", ["Train", "Truck", "Ship", "Other"], index=0, key="mode2")
        with col3:
            transport2_fuel = st.selectbox("Fuel Type", ["Diesel", "Electric", "Other"], index=1, key="fuel2")
        with col4:
            transport2_dist = st.number_input("Distance (km)", min_value=0.0, value=250.0, step=1.0, key="dist2")
        st.markdown("</div>", unsafe_allow_html=True)

        # -------- SECTION 5 --------
        st.markdown("<div class='section-card'><h3 style='color:#00EFFF'>⚙️ Advanced Parameters</h3>", unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)

        # -------- SECTION 6 --------
        st.markdown("<div class='section-card'><h3 style='color:#00EFFF'>📊 Data Quality Assessment & Uncertainty (Pedigree Matrix)</h3>", unsafe_allow_html=True)
        reliability = st.slider("Reliability", 1, 5, 4)
        completeness = st.slider("Completeness", 1, 5, 4)
        temporal = st.slider("Temporal Correlation", 1, 5, 4)
        geographical = st.slider("Geographical Correlation", 1, 5, 4)
        technological = st.slider("Technological Correlation", 1, 5, 4)
        st.markdown("</div>", unsafe_allow_html=True)

        # Submit
        submitted = st.form_submit_button("Run Analysis")

    # -----------------------------
    # Handle submission (outside the form)
    # -----------------------------
    if submitted:
        # Build form_data dictionary explicitly (mirrors original variable set)
        form_data = {
            "intended_app": intended_app,
            "intended_audience": intended_audience,
            "system_boundary": system_boundary,
            "study_limitations": study_limitations,
            "comparative_assertion": comparative_assertion,
            "project_name": project_name,
            "category": category,
            "material": material,
            "region": st.session_state.get("analysis_region"),
            "ore_type": st.session_state.get("ore_type_input"),
            "ore_conc": st.session_state.get("ore_conc_input"),
            "coatings": coatings,
            "functional_unit": functional_unit,
            "sec_material_content": sec_material_content,
            "production_process": production_process,
            "use_duration": use_duration,
            "end_life_scenario": end_life_scenario,
            "transport1_stage": transport1_stage,
            "transport1_mode": transport1_mode,
            "transport1_fuel": transport1_fuel,
            "transport1_dist": transport1_dist,
            "transport2_stage": transport2_stage,
            "transport2_mode": transport2_mode,
            "transport2_fuel": transport2_fuel,
            "transport2_dist": transport2_dist,
            "grid_elec_mix": grid_elec_mix,
            "water_source": water_source,
            "proceff": proceff,
            "lifetime_ext": lifetime_ext,
            "waste_method": waste_method,
            "reliability": reliability,
            "completeness": completeness,
            "temporal": temporal,
            "geographical": geographical,
            "technological": technological
        }

        # Animate header progress a little (set to a small visible value immediately)
        try:
            header_progress.progress(5)
        except Exception:
            pass

        # Run the simulation and show results
        try:
            with st.spinner("Running LCA simulation..."):
                results = run_simulation(form_data)
                # for UX, sweep progress to 80% after simulation returns, then finalize
                try:
                    header_progress.progress(80)
                except Exception:
                    pass
                # small animation to 100% to indicate completion
                for p in range(81, 101, 4):
                    try:
                        header_progress.progress(p)
                    except Exception:
                        pass
                    time.sleep(0.02)

            st.success("✅ LCA Simulation completed successfully!")

            # Ensure results carry data_quality from sliders if missing
            if isinstance(results, dict):
                results.setdefault("data_quality", {})
                dq = results["data_quality"]
                dq.setdefault("Reliability", f"{reliability}/5")
                dq.setdefault("Completeness", f"{completeness}/5")
                dq.setdefault("Temporal", f"{temporal}/5")
                dq.setdefault("Geographical", f"{geographical}/5")
                dq.setdefault("Technological", f"{technological}/5")
                try:
                    numeric_vals = [float(reliability), float(completeness), float(temporal), float(geographical), float(technological)]
                    results["data_quality"].setdefault("Aggregated ADQI", round(sum(numeric_vals) / len(numeric_vals), 2))
                except Exception:
                    results["data_quality"].setdefault("Aggregated ADQI", 4.0)
                results["data_quality"].setdefault("Result Uncertainty pct", 14)

            # Call results page
            ai_text = results.get("ai_lifecycle_interpretation", "") if isinstance(results, dict) else ""
            st.markdown("<hr>", unsafe_allow_html=True)
            results_page(results, ai_text)

        except Exception as e:
            st.error(f"❌ Simulation failed: {e}")
            st.text(traceback.format_exc())
            try:
                header_progress.progress(0)
            except Exception:
                pass


# Run for local debug
if __name__ == "__main__":
    full_lca_study_form()
