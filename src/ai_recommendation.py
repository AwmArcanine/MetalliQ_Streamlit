import streamlit as st
import pandas as pd

def display_ai_recommendations(ai_data,extra_context=None):
    """Display AI-powered insights and recommendations styled like MetalliQ UI demo."""
    st.header("AI-Powered Insights & Recommendations")

    # 0. Extra post-LCA context (ore grade, EV charging)
    if extra_context:
        # Low Ore Grade Warning
        
        st.warning(
            f"⚠️ Low ore grade detected: {extra_context['ore_conc']}% metal ore concentration. "
            "Processing low-grade ores uses much more energy and increases mining waste. "
            "AI Suggestion: Consider higher-grade blending, alternative sourcing, or process optimization for improved sustainability."
        )
        # Electric Vehicle Charging Suggestion
        st.markdown("#### Energy-Efficient Charging Recommendations")
        st.markdown(
            """
            - Install solar-powered EV charging stations to maximize renewable energy use.
            - Use smart chargers with demand-response capability to charge during off-peak hours.
            - Source grid electricity from certified green power (solar, wind, hydro).
            - Monitor charging station efficiency and optimize placement for reduced transmission loss.
            - Regularly audit charging infrastructure for leaks, inefficiency, and outdated hardware.
            - Offer real-time charging usage analytics to employees to encourage optimal charging behaviors.
            """
        )

    # 1. AI Summary (highlight)
    if "summary" in ai_data:
        st.info(f"**AI Summary:** {ai_data['summary']}")

    # 2. Findings panel/cards
    findings = ai_data.get("findings", [])
    for find in findings:
        with st.container():
            st.markdown(
                f"""<div style='display:flex;justify-content:space-between;align-items:center;'>
                    <h4>{find.get('title', '')}</h4>
                    <span style='background:#1976d2;color:#fff;padding:4px 12px;border-radius:7px;font-size:13px;'>
                        {find.get('priority',"High Priority")}
                    </span>
                </div>""", unsafe_allow_html=True)
            # Evidence
            st.markdown(f"**Evidence**")
            st.markdown(
                f"<div style='background:#f5f5fa;padding:9px 12px;border-radius:7px;'>{find.get('evidence','')}</div>",
                unsafe_allow_html=True)
            # Root Cause
            st.markdown("**Root Cause**")
            st.markdown(f"<div style='padding:6px 0;'>{find.get('root_cause','')}</div>", unsafe_allow_html=True)
            # Action Plan(s)
            st.markdown("**Action Plan**")
            for plan in find.get("action_plan", []):
                styl = {
                    "Medium Effort": "background:#ffe082;color:#795548;",
                    "High Effort": "background:#ff8a80;color:#c62828;",
                    "Low Effort": "background:#b9f6ca;color:#1b5e20;"
                }
                effort_color = styl.get(plan["effort"], "background:#ffe082;color:#795548;")
                row = f"""<div style="margin-bottom:9px;padding:10px 14px;border-radius:9px;background:#f0f4fc;">
                    <b>{plan['title']}</b> — {plan['desc']}
                    <br><i>{plan['impact']}</i>
                    <span style="{effort_color}border-radius:6px;padding:4px 12px;margin-left:16px;">
                        {plan['effort']}
                    </span>
                    <span style="color:#888;margin-left:8px;font-size:12px;">Confidence: {plan['confidence']}%</span>
                </div>"""
                st.markdown(row, unsafe_allow_html=True)

    # 3. Scenario Comparison Table (if included)
    if ai_data.get("comparison_table") is not None:
        st.markdown("#### Primary vs. Recycled Route Comparison")
        df = pd.DataFrame(ai_data["comparison_table"])
        st.dataframe(df)

# Example reusable ai_data object (can pass this for preview and testing)
ai_data_example = {
    "summary": "AI analysis suggests focusing on material sourcing and energy efficiency.",
    "findings": [
        {
            "title": "Mitigate High Global Warming Potential from Primary Steel Production",
            "priority": "High Priority",
            "evidence": "The production phase accounts for 2282 kg CO₂-eq of the total 2293 kg CO₂-eq Global Warming Potential (GWP), representing approximately 99.5% of the total GWP for the steel material.",
            "root_cause": "The high reliance on primary steel production processes, which are inherently energy-intensive and often involve the reduction of iron ore using carbon-intensive coking coal, leads to significant greenhouse gas emissions.",
            "action_plan": [
                {
                    "title": "Increase Recycled Steel Content",
                    "desc": "Explore opportunities to increase the proportion of recycled steel used in the material composition beyond the current 10%, reducing the demand for primary production processes.",
                    "impact": "Significantly reduce GWP and energy demand by leveraging less energy-intensive secondary production routes for steel.",
                    "effort": "Medium Effort",
                    "confidence": 90
                },
                {
                    "title": "Transition to Renewable Energy in Production",
                    "desc": "Investigate and implement the use of renewable energy sources (e.g., solar, wind, hydropower) to power the steel production process, thereby decarbonizing electricity consumption.",
                    "impact": "Directly reduce Scope 2 greenhouse gas emissions associated with electricity usage in the production phase.",
                    "effort": "High Effort",
                    "confidence": 75
                },
                {
                    "title": "Implement Process Efficiency Improvements",
                    "desc": "Identify and implement process optimizations within the existing primary production route to reduce energy consumption and improve material yields. Examples include improved furnace efficiency or waste heat recovery systems.",
                    "impact": "Modestly reduce GWP and overall energy demand per unit of material produced, enhancing operational sustainability.",
                    "effort": "Medium Effort",
                    "confidence": 85
                },
            ]
        }
    ]
}
