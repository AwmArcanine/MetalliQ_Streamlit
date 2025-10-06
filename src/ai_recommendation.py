import streamlit as st
import pandas as pd

def display_ai_recommendations(ai_data, extra_context=None):
    """Display AI-powered insights and recommendations styled like MetalliQ UI demo."""
    st.header("AI-Powered Insights & Recommendations")

    # --- 0. Always show Ore Grade Warning ---
    if extra_context and "ore_conc" in extra_context:
        st.markdown(
            f"<div style='background:rgba(255,200,0,0.2);color:#222;padding:10px 15px;border-radius:8px;'>"
            f"⚠️ <b>Low ore grade detected:</b> {extra_context['ore_conc']}% concentration. "
            "Processing low-grade ores increases energy use and mining waste. "
            "<b>AI Suggestion:</b> Blend with higher-grade sources or optimize beneficiation.</div>",
            unsafe_allow_html=True
        )

    # --- 1. Always show EV Charging Tips ---
    st.markdown("### Energy-Efficient EV Charging Recommendations")
    st.markdown("""
    - ⚡ Use solar-powered or wind-powered charging stations where possible.
    - ⏰ Schedule EV charging during off-peak grid hours to lower CO₂ intensity.
    - 🧠 Integrate smart charging to balance renewable energy input.
    - 📊 Regularly audit charger efficiency and usage analytics.
    """)

    # --- 2. AI Summary ---
    summary_text = ai_data.get("summary", "AI analysis suggests focusing on material sourcing and energy efficiency.")
    st.info(f"**AI Summary:** {summary_text}")

    # --- 3. Fallback default findings if not provided ---
    findings = ai_data.get("findings", [])
    if not findings:
        findings = [
            {
                "title": "Mitigate High Global Warming Potential from Primary Steel Production",
                "priority": "High Priority",
                "evidence": (
                    "The production stage accounts for 2277 kg CO₂-eq out of a total GWP of 2288 kg CO₂-eq, "
                    "representing over 99% of the material's total carbon footprint."
                ),
                "root_cause": (
                    "Primary steel production relies heavily on fossil fuels for heat and electricity, "
                    "leading to significant greenhouse gas emissions during raw material processing and refining."
                ),
                "action_plan": [
                    {
                        "title": "Explore higher recycled-content steel options",
                        "desc": "Investigate steel suppliers offering higher percentages of recycled content (e.g., 30–50%) to reduce primary production requirements.",
                        "impact": "Reduces GWP, energy demand, and water consumption associated with virgin material extraction.",
                        "effort": "Medium Effort",
                        "confidence": 90
                    },
                    {
                        "title": "Assess steel suppliers’ energy mix and efficiency",
                        "desc": "Engage suppliers to understand their renewable energy use and efficiency measures.",
                        "impact": "Reduces indirect GWP via lower-carbon electricity and process optimization.",
                        "effort": "Medium Effort",
                        "confidence": 80
                    },
                    {
                        "title": "Investigate alternative low-carbon steel technologies",
                        "desc": "Monitor R&D in hydrogen-reduced iron (H₂DRI) or carbon capture-integrated steel production.",
                        "impact": "Drastically reduces long-term GWP potential.",
                        "effort": "High Effort",
                        "confidence": 70
                    }
                ]
            },
            {
                "title": "Enhance Material Circularity and End-of-Life Management",
                "priority": "Medium Priority",
                "evidence": (
                    "The material has a Circularity Score of 50%, suggesting substantial potential for improvement "
                    "in resource recovery and reuse efficiency."
                ),
                "root_cause": (
                    "A 50% circularity score implies a large share of materials still originate from virgin sources "
                    "or are not recovered effectively at end-of-life."
                ),
                "action_plan": [
                    {
                        "title": "Integrate Design for Environment (DfE) principles",
                        "desc": "Design components for easy separation, recovery, and recycling.",
                        "impact": "Improves recyclability and reduces virgin material demand.",
                        "effort": "Medium Effort",
                        "confidence": 85
                    },
                    {
                        "title": "Establish End-of-Life Take-Back Programs",
                        "desc": "Collaborate with recycling infrastructure to ensure systematic collection of end-of-life products.",
                        "impact": "Increases steel recovery, closing the material loop.",
                        "effort": "High Effort",
                        "confidence": 75
                    }
                ]
            }
        ]

    # --- 4. Render Findings in Styled Cards ---
    for find in findings:
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.15);backdrop-filter:blur(12px);border-radius:12px;
                        padding:16px;margin-bottom:16px;border:1px solid rgba(255,255,255,0.25);">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <h4 style="color:#063735;margin:0;">{find.get('title','')}</h4>
                    <span style="background:#1976d2;color:#fff;padding:4px 10px;border-radius:6px;font-size:12px;">
                        {find.get('priority','')}
                    </span>
                </div>
                <p style="margin-top:8px;color:#083a38;"><b>Evidence:</b> {find.get('evidence','')}</p>
                <p style="margin-top:4px;color:#083a38;"><b>Root Cause:</b> {find.get('root_cause','')}</p>
                <p style="margin-top:4px;color:#083a38;"><b>Action Plan:</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Action plan subcards
        for plan in find.get("action_plan", []):
            effort_colors = {
                "Low Effort": "background:#b9f6ca;color:#1b5e20;",
                "Medium Effort": "background:#ffe082;color:#795548;",
                "High Effort": "background:#ff8a80;color:#c62828;",
            }
            effort_style = effort_colors.get(plan["effort"], "background:#ffe082;color:#795548;")
            st.markdown(
                f"""
                <div style="margin-left:20px;margin-top:6px;margin-bottom:8px;padding:10px 14px;
                            background:rgba(255,255,255,0.2);border-radius:8px;">
                    <b>{plan['title']}</b> — {plan['desc']}
                    <br><i>{plan['impact']}</i>
                    <br><span style="{effort_style}border-radius:6px;padding:3px 10px;">
                        {plan['effort']}
                    </span>
                    <span style="color:#555;margin-left:10px;">Confidence: {plan['confidence']}%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --- 5. Always show at end ---
    st.markdown("---")
    st.caption("AI insights are for internal sustainability evaluation and not for external public claims.")

# --- Example AI data (used when real AI generation isn't active) ---
ai_data_example = {
    "summary": "AI analysis highlights key areas for sustainability improvement across production and recycling phases.",
    "findings": [
        {
            "title": "Reduce Global Warming Potential in Production",
            "priority": "High Priority",
            "evidence": "Production accounts for ~65% of GWP due to fossil-based energy sources.",
            "root_cause": "High dependency on coal-based electricity and low recycled input share.",
            "action_plan": [
                {
                    "title": "Increase Recycled Material Input",
                    "desc": "Raise recycled feedstock share from 10% to 40%.",
                    "impact": "Expected reduction of 35% in GWP and 25% in energy demand.",
                    "effort": "Medium Effort",
                    "confidence": 90
                },
                {
                    "title": "Adopt Renewable Power for Smelting",
                    "desc": "Shift 50% of smelter electricity to solar/wind contracts.",
                    "impact": "Large reduction in Scope 2 emissions.",
                    "effort": "High Effort",
                    "confidence": 80
                }
            ]
        },
        {
            "title": "Optimize Water Consumption in Cooling",
            "priority": "Medium Priority",
            "evidence": "Water usage intensity in process stages exceeds benchmark by ~40%.",
            "root_cause": "Open-loop cooling system without heat recovery.",
            "action_plan": [
                {
                    "title": "Install Closed-loop Cooling Systems",
                    "desc": "Capture and reuse process water.",
                    "impact": "Cuts freshwater withdrawal by up to 60%.",
                    "effort": "Medium Effort",
                    "confidence": 85
                }
            ]
        },
        {
            "title": "Enhance Material Circularity",
            "priority": "Low Priority",
            "evidence": "Circularity score currently 50%.",
            "root_cause": "Insufficient recovery and reuse streams.",
            "action_plan": [
                {
                    "title": "Establish Take-back Programs",
                    "desc": "Implement return channels for end-of-life components.",
                    "impact": "Boosts closed-loop potential by 25%.",
                    "effort": "Low Effort",
                    "confidence": 75
                }
            ]
        }
    ]
}
