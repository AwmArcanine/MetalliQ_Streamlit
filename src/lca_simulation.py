import numpy as np
import streamlit as st

def run_simulation(inputs, num_runs=1000):
    try:
        st.write("Starting Life Cycle Assessment Monte Carlo simulation...")

        # Extract goal & scope info from inputs to return for display
        goal_scope = {
            "Intended Application": inputs.get("intended_app", ""),
            "Intended Audience": inputs.get("intended_audience", ""),
            "System Boundary": inputs.get("system_boundary", ""),
            "Study Limitations": inputs.get("study_limitations", ""),
            "Comparative Assertion": inputs.get("comparative_assertion", "")
        }

        # Data Quality & Uncertainty from inputs
        data_quality = {
            "Reliability": inputs.get("reliability", 0),
            "Completeness": inputs.get("completeness", 0),
            "Temporal Correlation": inputs.get("temporal", 0),
            "Geographical Correlation": inputs.get("geographical", 0),
            "Technological Correlation": inputs.get("technological", 0)
        }

        # Base impact values with correct SI units (per functional unit e.g. per ton of steel)
        base_vals = {
            'Global Warming Potential': 2293,  # kg CO2-eq
            'Energy Demand': 26454,  # MJ
            'Water Consumption': 4.7,  # m3
            'Particulate Matter': 0.76,  # kg PM2.5-eq
            'Acidification': 4.1,  # mol H+ eq
            'Eutrophication': 1.15,  # kg PO4-eq
            'Human Toxicity (Cancer)': 0.23,  # Comparative units
            'Ionizing Radiation': 0.0,  # kBq U235-eq
            'Land Use': 229,  # m2a
            'Ozone Depletion': 0.0,  # kg CFC-11-eq
            'Photochemical Ozone Creation': 2.3,  # kg NMVOC
            'Abiotic Depletion (Fossil)': 29100,  # MJ
            'Abiotic Depletion (Elements)': 0.01,  # kg Sb-eq
            'Human Toxicity (Non-Cancer)': 2.29,  # Comparative units
            'Freshwater Ecotoxicity': 22.93  # Comparative units
        }

        uncertainties = {
            'Global Warming Potential': 100,
            'Energy Demand': 1500,
            'Water Consumption': 0.5,
            'Particulate Matter': 0.1,
            'Acidification': 0.3,
            'Eutrophication': 0.2,
            'Human Toxicity (Cancer)': 0.05,
            'Ionizing Radiation': 0.01,
            'Land Use': 20,
            'Ozone Depletion': 0.01,
            'Photochemical Ozone Creation': 0.5,
            'Abiotic Depletion (Fossil)': 4000,
            'Abiotic Depletion (Elements)': 0.005,
            'Human Toxicity (Non-Cancer)': 0.4,
            'Freshwater Ecotoxicity': 5,
        }

        simulation_data = {}
        summary = {}

        for impact, base in base_vals.items():
            sd = uncertainties.get(impact, base * 0.1)  # default 10% uncertainty if not defined
            samples = np.random.normal(loc=base, scale=sd, size=num_runs)
            simulation_data[impact] = samples
            summary[impact] = {
                'mean': float(np.mean(samples)),
                'median': float(np.median(samples)),
                'std_dev': float(np.std(samples)),
                'ci_95_lower': float(np.percentile(samples, 2.5)),
                'ci_95_upper': float(np.percentile(samples, 97.5))
            }

        circularity_metrics = {
            "Circularity Score": 50,               # Percent
            "Recyclability Rate": 90,              # Percent
            "Recovery Efficiency": 92,             # Percent
            "Secondary Material Content": 10,      # Percent
            "Resource Efficiency": 92,             # Percent
            "Extended Product Life": 110,          # Years
            "Reuse Potential": 40,                  # Percent
            "Material Recovery": 90,                # Percent
            "Closed-loop Potential": 75,            # Percent
            "Recycling Content": 10,                # Percent
            "Landfill Rate": 8,                     # Percent
            "Energy Recovery": 2                    # Percent
        }

        # Sankey example data
        sankey_data = {
            'labels': [
                'Metal Ore Extraction', 'Manufacturing',
                'Transportation', 'Use Phase', 'End of Life',
                'Recycling Process', 'Landfill'
            ],
            'source': [0, 1, 1, 2, 4, 5],
            'target': [1, 2, 3, 3, 5, 6],
            'value': [100, 80, 50, 40, 30, 15]
        }

        ai_life_cycle_interpretation = (
            "AI analysis shows Global Warming Potential highly influenced by primary steel production and transportation. "
            "Recycling contributes to circularity improvements with a circularity score of 50%."
        )

        # Default scenario comparison table with extra parameters
        scenario_comparison_table = [
            {
                "Metric": "Global Warming Potential (kg CO₂-eq)",
                "Primary Material": summary['Global Warming Potential']['mean'],
                "Recycled Material": summary['Global Warming Potential']['mean'] * 0.5
            },
            {
                "Metric": "Energy Demand (MJ)",
                "Primary Material": summary['Energy Demand']['mean'],
                "Recycled Material": summary['Energy Demand']['mean'] * 0.4
            },
            {
                "Metric": "Water Consumption (m³)",
                "Primary Material": summary['Water Consumption']['mean'],
                "Recycled Material": summary['Water Consumption']['mean'] * 0.6
            },
            {
                "Metric": "Cost (USD)",
                "Primary Material": 600,
                "Recycled Material": 350
            },
            {
                "Metric": "Embodied Energy (MJ)",
                "Primary Material": 50000,
                "Recycled Material": 25000
            },
            {
                "Metric": "Freshwater Withdrawal (m³)",
                "Primary Material": 150,
                "Recycled Material": 75
            }
        ]

        # Package all results into dict
        report = {
            "goal_scope": goal_scope,
            "data_quality": data_quality,
            "executive_summary": {
                "Global Warming Potential": summary["Global Warming Potential"]['mean'],
                "Circularity Score": circularity_metrics["Circularity Score"],
                "Particulate Matter": summary["Particulate Matter"]["mean"],
                "Water Consumption": summary["Water Consumption"]['mean'],
                "Supply Chain Hotspots": [],  # Add if available
                "Production Phase GWP": summary["Global Warming Potential"]['mean'] * 0.65,
                "Overall Energy Demand": summary["Energy Demand"]['mean'],
                "Circular Score": circularity_metrics["Circularity Score"],
            },
            "ai_life_cycle_interpretation": ai_life_cycle_interpretation,
            "circularity_analysis": circularity_metrics,
            "material_flow_analysis": sankey_data,
            "key_impact_profiles": summary,
            "uncertainty_dashboard": simulation_data,
            "energy_source_breakdown": {
                "Direct Fuel": 25000,
                "Grid Electricity": 1450
            },
            "gwp_contribution_analysis": {
                "Production": summary["Global Warming Potential"]['mean'] * 0.65,
                "Transport": summary["Global Warming Potential"]['mean'] * 0.25,
                "Use Phase": summary["Global Warming Potential"]['mean'] * 0.10
            },
            "primary_vs_recycled": {
                "comparison_table": scenario_comparison_table
            }
        }

        st.write("LCA simulation completed successfully.")
        return report

    except Exception as e:
        st.error(f"Error in run_simulation: {e}")
        return {}
