import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# Load global theme
def load_theme():
    theme_path = Path("theme.css")
    if theme_path.exists():
        st.markdown(f"<style>{theme_path.read_text()}</style>", unsafe_allow_html=True)
st.markdown("""
<style>
/* --- Fix for white radio button text --- */
div[role="radiogroup"] label span {
    color: #024B49 !important;   /* dark teal text */
    font-weight: 600 !important;
    letter-spacing: -0.3px;
}

/* Highlight the selected one with teal background + white text */
div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
    background: rgba(0,255,255,0.15) !important;
    border-radius: 6px !important;
    transition: 0.2s ease-in-out;
}
div[role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"] span {
    color: #00A896 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)


# Mock Data
user_info = {
    "active_users": 33,
    "lca_studies": 12,
    "reports_generated": 67
}
users_df = pd.DataFrame([
    {"User": "John Doe", "Role": "Admin", "Last Login": "2025-10-03"},
    {"User": "Jane Smith", "Role": "User", "Last Login": "2025-10-02"},
    {"User": "Alex Wong", "Role": "User", "Last Login": "2025-10-01"},
])
datasets_df = pd.DataFrame([
    {"Dataset": "Aluminium LCA India", "Type": "CSV", "Uploaded": "2025-09-30"},
    {"Dataset": "Bauxite Mining", "Type": "XLSX", "Uploaded": "2025-09-28"},
    {"Dataset": "Steel Europe", "Type": "CSV", "Uploaded": "2025-09-22"},
])
ai_models_df = pd.DataFrame([
    {"Model Name": "CircularityGPT-lite", "Type": "NLP", "Status": "Trained", "Accuracy": "92%"},
    {"Model Name": "MetallIQ-Impactor", "Type": "Regression", "Status": "Training", "Accuracy": "-"},
    {"Model Name": "LCA-ScenarioX", "Type": "ML Ensemble", "Status": "Ready", "Accuracy": "89%"},
])


# --- Function ---
def show_admin_dashboard(user_info, users_df, datasets_df, ai_models_df):
    load_theme()
    st.markdown("<h2 style='color:#00FFFF;font-weight:800;letter-spacing:-0.5px;'>🧠 MetalliQ Admin Dashboard</h2>", unsafe_allow_html=True)
    st.caption("System-wide insights, analytics, and sustainability performance overview.")

    admin_nav = st.radio(
        "Admin Sections", [
            "Platform Analytics",
            "All-User Reports",
            "Dataset Management",
            "AI Model Hub"
        ], horizontal=True
    )

    if admin_nav == "Platform Analytics":
        cols = st.columns(4)
        metrics = ["Active Users", "Ongoing LCA Studies", "Reports Generated", "AI Models"]
        values = [
            user_info.get('active_users', 33),
            user_info.get('lca_studies', 12),
            user_info.get('reports_generated', 67),
            ai_models_df.shape[0]
        ]
        for i in range(4):
            with cols[i]:
                st.metric(metrics[i], values[i])

        impact_data = pd.DataFrame({
            "Month": pd.date_range(start="2025-01-01", periods=10, freq="M"),
            "CO2 Emissions (t)": [120, 110, 113, 108, 105, 102, 99, 100, 96, 95],
            "Water Use (m3)": [800, 740, 720, 735, 710, 700, 695, 670, 665, 660],
            "Circularity (%)": [42, 45, 47, 48, 50, 52, 53, 54, 55, 56]
        })
        impact_long = impact_data.melt(id_vars="Month", var_name="Indicator", value_name="Value")

        fig = px.line(impact_long, x="Month", y="Value", color="Indicator",
                      markers=True, color_discrete_sequence=["#7CF4E3", "#00B8CC", "#02C39A"])
        fig.update_layout(
            height=420,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF")
        )
        st.plotly_chart(fig, use_container_width=True)

    elif admin_nav == "All-User Reports":
        st.dataframe(users_df, use_container_width=True)

    elif admin_nav == "Dataset Management":
        st.file_uploader("Upload New Dataset (CSV or JSON)", type=['csv', 'json'], key="uploader")
        st.dataframe(datasets_df, use_container_width=True)

    elif admin_nav == "AI Model Hub":
        st.dataframe(ai_models_df, use_container_width=True)
        st.markdown(
            "<button style='background:linear-gradient(90deg,#00A896,#02C39A);color:white;border:none;border-radius:8px;padding:8px 18px;font-weight:700;'>🔄 Retrain Models</button>",
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    show_admin_dashboard(user_info, users_df, datasets_df, ai_models_df)
