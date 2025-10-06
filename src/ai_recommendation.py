import streamlit as st
import pandas as pd

def display_ai_recommendations(ai_data, extra_context=None):
    """Display AI-powered insights and recommendations in MetalliQ-style UI."""
    st.header("AI-Powered Insights & Recommendations")

    # Extra contextual warnings
    if extra_context:
        ore_conc = extra_context.get("ore_conc", 50)
        st.warning(
            f"⚠️ Low ore grade detected: {ore_conc}% concentration. "
            "Processing low-grade ores increases energy use and mining waste. "
            "AI Suggestion: Blend with higher-grade sources or optimize beneficiation."
        )

        st.markdown("#### Energy-Efficient EV Charging Recommendations")
        st.markdown(
            """
            - ⚡ Use solar-powered or wind-powered charging stations where possible.  
            - ⏰ Schedule EV charging during off-peak grid hours to lower CO₂ intensity.  
            - 🛰️ Integrate smart charging to balance renewable energy input.  
            - 🧾 Regularly audit charger efficiency and usage analytics.  
            """
        )

    # Summary block
    if "summary" in ai_data:
        st.info(f"**AI Summary:** {ai_data['summary']}")

    # Findings
    for finding in ai_data.get("findings", []):
        st.markdown(
            f"""
            <div style='background:rgba(255,255,255,0.18);backdrop-filter:blur(10px);
            border:1px solid rgba(255,255,255,0.25);padding:14px;border-radius:12px;margin-bottom:16px;'>
            <h4 style='color:#0b6b66;'>{finding.get('title')}</h4>
            <p><b>Priority:</b> <span style='background:#0f8f88;color:#fff;padding:3px 8px;
            border-radius:6px;'>{finding.get('priority',"High Priority")}</span></p>
            <b>Evidence:</b> {finding.get('evidence','N/A')}<br>
            <b>Root Cause:</b> {finding.get('root_cause','N/A')}<br><br>
            <b>Action Plans:</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        for plan in finding.get("action_plan", []):
            color = {
                "Low Effort": "#b9f6ca",
                "Medium Effort": "#ffe082",
                "High Effort": "#ff8a80"
            }.get(plan["effort"], "#ffe082")
            st.markdown(
                f"""
                <div style='margin-left:12px;margin-bottom:8px;padding:10px;
                border-radius:8px;background:{color};color:#083a38;'>
                <b>{plan['title']}</b> — {plan['desc']}  
                <i>{plan['impact']}</i><br>
                <small>Effort: {plan['effort']} | Confidence: {plan['confidence']}%</small>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Comparison Table (optional)
    if ai_data.get("comparison_table") is not None:
        st.markdown("#### Primary vs. Recycled Comparison")
        st.dataframe(pd.DataFrame(ai_data["comparison_table"]))

# --- Default AI mock dataset for results_page.py ---
ai_data_example = {
    "summary": "AI analysis identifies hotspots in the production and material sourcing phases. "
               "Switching to recycled input and renewable power can cut total GWP by up to 60%.",
    "findings": [
        {
            "title": "High GWP from Primary Material Production",
            "priority": "High Priority",
            "evidence": "Primary production accounts for 2485 kg CO₂-eq vs. 597 kg for recycled.",
            "root_cause": "Reliance on coal-based electricity and low scrap utilization.",
            "action_plan": [
                {
                    "title": "Adopt Secondary Processing Routes",
                    "desc": "Increase recycled material content to 50% of total input.",
                    "impact": "Reduces total lifecycle GWP by ~60%.",
                    "effort": "Medium Effort",
                    "confidence": 90
                },
                {
                    "title": "Switch to Renewable Electricity",
                    "desc": "Use solar or hydro power during smelting operations.",
                    "impact": "Cuts Scope 2 emissions by 30–40%.",
                    "effort": "High Effort",
                    "confidence": 80
                }
            ]
        }
    ],
    "comparison_table": [
        {"Metric": "GWP (kg CO₂-eq)", "Primary": 2485, "Recycled": 597},
        {"Metric": "Energy (GJ)", "Primary": 28.77, "Recycled": 6.17},
        {"Metric": "Water (m³)", "Primary": 5.0, "Recycled": 2.0}
    ]
}
