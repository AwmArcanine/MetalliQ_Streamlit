import numpy as np
import random
import streamlit as st

def run_simulation(inputs, num_runs=1000):
    """
    Mock Monte Carlo LCA simulation fully compatible with results_page.py.
    Returns a structured 'results' dict with all expected keys and sample data.
    """
    try:
        st.write("⚙️ Starting Life Cycle Assessment simulation...")

        # --- Extract key inputs ---
        material = inputs.get("material", "Steel")
        region = inputs.get("region", "India")
        ore_conc = inputs.get("ore_conc", 50.0)

        # --- Goal & Scope info (ISO 14044) ---
        goal_scope = {
            "Intended Application": inputs.get("intended_app", "Internal R&D material comparison study."),
            "Intended Audience": inputs.get("intended_audience", "Engineering & sustainability team"),
            "System Boundary": inputs.get("system_boundary", "Cradle-to-Gate"),
            "Study Limitations": inputs.get("study_limitations", "Assumes industry-average data."),
            "Comparative Assertion": inputs.get("comparative_assertion", "No"),
        }

        # --- Base environmental impact values (per ton of material) ---
        base_vals = {
            "Global Warming Potential": 2293,  # kg CO₂-eq
            "Energy Demand": 26454,            # MJ
            "Water Consumption": 4.7,          # m³
            "Particulate Matter": 0.76,        # kg PM2.5-eq
            "Acidification Potential": 4.1,    # mol H+ eq
            "Eutrophication Demand": 1.15,     # kg PO4-eq
        }

        # --- Set default uncertainty range (10% of mean) ---
        uncertainties = {k: v * 0.1 for k, v in base_vals.items()}

        # --- Monte Carlo Simulation for uncertainty dashboard ---
        summary = {}
        for impact, base in base_vals.items():
            samples = np.random.normal(loc=base, scale=uncertainties[impact], size=num_runs)
            summary[impact] = {
                "mean": float(np.mean(samples)),
                "median": float(np.median(samples)),
                "std_dev": float(np.std(samples)),
                "ci_95_lower": float(np.percentile(samples, 2.5)),
                "ci_95_upper": float(np.percentile(samples, 97.5)),
                "samples": samples.tolist()[:100],  # smaller preview for Streamlit charts
            }

        # --- Executive Summary (mock representative metrics) ---
        executive_summary = {
            "Global Warming Potential": round(summary["Global Warming Potential"]["mean"], 2),
            "Circularity Score": random.randint(45, 70),
            "Particulate Matter": round(summary["Particulate Matter"]["mean"], 3),
            "Water Consumption": round(summary["Water Consumption"]["mean"], 2),
            "Overall Energy Demand": round(summary["Energy Demand"]["mean"], 2),
        }

        # --- Data Quality (Pedigree Matrix) ---
        data_quality = {
            "Reliability": f"{inputs.get('reliability', 4)}/5",
            "Completeness": f"{inputs.get('completeness', 4)}/5",
            "Temporal": f"{inputs.get('temporal', 4)}/5",
            "Geographical": f"{inputs.get('geographical', 4)}/5",
            "Technological": f"{inputs.get('technological', 4)}/5",
            "Aggregated ADQI": 4.0,
            "Result Uncertainty pct": 14,
        }

        # --- Circularity Analysis ---
        circularity = {
            "Circularity Rate": round(random.uniform(55, 70), 2),
            "Recyclability Rate": round(random.uniform(75, 90), 2),
            "Recovery Efficiency": round(random.uniform(80, 90), 2),
            "Secondary Material Content": round(random.uniform(40, 60), 2),
            "Resource Efficiency": round(random.uniform(80, 95), 2),
            "Extended Product Life": random.randint(10, 20),
            "Reuse Potential": round(random.uniform(35, 55), 2),
            "Material Recovery": round(random.uniform(85, 95), 2),
            "Closed-loop Potential": round(random.uniform(70, 85), 2),
            "Recycling Content": round(random.uniform(40, 55), 2),
            "Landfill Rate": round(random.uniform(5, 15), 2),
            "Energy Recovery": round(random.uniform(1, 5), 2),
        }

        # --- Impact Assessment Metrics ---
        impacts = {
            "Global Warming Potential": summary["Global Warming Potential"]["mean"],
            "Acidification Potential": summary["Acidification Potential"]["mean"],
            "Photochemical Ozone Creation": 2.3,
            "Abiotic Depletion (Fossil)": 29100,
            "Fresh Water Ecotoxicity": 22.9,
            "Energy Demand": summary["Energy Demand"]["mean"],
            "Eutrophication Demand": summary["Eutrophication Demand"]["mean"],
            "Particulate Matter Formation": summary["Particulate Matter"]["mean"],
            "Human Toxicity (Cancer)": 0.23,
            "Ionizing Radiation": 0.02,
            "Water Consumption": summary["Water Consumption"]["mean"],
            "Ozone Depletion Potential": 0.01,
            "Abiotic Depletion (Elements)": 0.01,
            "Human Toxicity (Non-Cancer)": 2.29,
            "Land Use": 229,
        }

        # --- Primary vs Recycled Scenario Comparison ---
        primary_vs_recycled = [
            {"Metric": "GWP (kg CO₂-eq)", "Primary": 2485, "Recycled": 597},
            {"Metric": "Energy (GJ)", "Primary": 28.77, "Recycled": 6.17},
            {"Metric": "Water (m³)", "Primary": 5.0, "Recycled": 2.0},
            {"Metric": "Acidification (kg SO₂-eq)", "Primary": 4.4, "Recycled": 1.35},
            {"Metric": "Eutrophication (kg PO₄-eq)", "Primary": 1.24, "Recycled": 0.30},
        ]

        # --- AI Lifecycle Interpretation ---
        ai_lifecycle_interpretation = (
            f"The {material} lifecycle in {region} shows that most environmental impact "
            f"occurs during the production and ore processing phases. With an ore concentration of "
            f"{ore_conc}%, refining is the dominant contributor to GWP and energy demand. "
            "Increasing recycled content and integrating renewable energy can reduce the total GWP by 50–60%. "
            "Further improvements are possible through higher recovery efficiency and material reuse."
        )

        # --- Uncertainty Dashboard Data ---
        uncertainty_dashboard = {
            "GWP Uncertainty": summary["Global Warming Potential"]["samples"],
            "Energy Uncertainty": summary["Energy Demand"]["samples"],
            "Water Uncertainty": summary["Water Consumption"]["samples"],
        }

        # --- GWP Contribution Breakdown ---
        gwp_contribution = {
            "Production": round(executive_summary["GWP"] * 0.65, 2),
            "Transport": round(executive_summary["GWP"] * 0.25, 2),
            "Use Phase": round(executive_summary["GWP"] * 0.10, 2),
        }

        # --- Energy Source Breakdown ---
        energy_breakdown = {
            "Direct Fuel": 25000,
            "Grid Electricity": 1450,
            "Renewables": 1200,
        }

        # --- Assemble final structured results ---
        results = {
            "goal_scope": goal_scope,
            "executive_summary": executive_summary,
            "data_quality": data_quality,
            "circularity": circularity,
            "impacts": impacts,
            "primary_vs_recycled": primary_vs_recycled,
            "ai_lifecycle_interpretation": ai_lifecycle_interpretation,
            "uncertainty_dashboard": uncertainty_dashboard,
            "gwp_contribution_analysis": gwp_contribution,
            "energy_source_breakdown": energy_breakdown,
            "material": material,
            "region": region,
            "ore_conc": ore_conc,
        }

        st.success("✅ LCA simulation completed successfully!")
        return results

    except Exception as e:
        # st.error(f"❌ Error in run_simulation: {e}")
        return {}
