import streamlit as st
import pandas as pd
import plotly.express as px

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
    st.set_page_config(layout="wide")
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;500;600&display=swap');

    body, .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #83C5BE 100%) !important;
        color: #E6FFFF;
        font-family: 'Poppins', sans-serif;
    }

    /* Headers */
    .page-title {
        font-family: 'Orbitron', sans-serif;
        color: #7CF4E3;
        text-shadow: 0 0 18px rgba(124, 244, 227, 0.8);
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .page-desc {
        color: #D8FFFF;
        font-size: 1rem;
        margin-bottom: 25px;
    }

    .section-header {
        color: #7CF4E3;
        font-weight: 700;
        margin: 30px 0 12px 0;
        font-size: 1.25rem;
    }

    /* Cards */
    .stats-row {
        display: flex;
        gap: 24px;
        flex-wrap: wrap;
        margin-bottom: 22px;
    }

    .stats-card {
        flex: 1;
        min-width: 220px;
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(0, 109, 119, 0.3);
        transition: 0.3s;
    }

    .stats-card:hover {
        box-shadow: 0 0 18px rgba(124, 244, 227, 0.7);
        transform: translateY(-4px);
    }

    .stats-title {
        color: #D8FFFF;
        font-size: 1rem;
        font-weight: 600;
    }

    .stats-value {
        color: #7CF4E3;
        font-size: 2rem;
        font-weight: 800;
    }

    /* Table */
    table {
        border: 1.5px solid rgba(124, 244, 227, 0.3) !important;
        border-radius: 12px;
        background: rgba(255,255,255,0.05);
    }
    thead tr {
        background: rgba(124, 244, 227, 0.2) !important;
        color: #7CF4E3 !important;
        font-weight: 600;
    }
    tbody tr {
        color: #E6FFFF !important;
    }

    /* Buttons */
    .primary-btn, .admin-btn {
        background: linear-gradient(90deg, #00A896 0%, #02C39A 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.65em 1.8em;
        cursor: pointer;
        transition: all 0.25s ease;
        box-shadow: 0 0 12px rgba(0, 168, 150, 0.5);
    }
    .primary-btn:hover, .admin-btn:hover {
        box-shadow: 0 0 22px rgba(124, 244, 227, 0.9);
        transform: scale(1.05);
    }

    .status-chip {
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .status-green {
        background: rgba(0, 239, 255, 0.25);
        color: #7CF4E3;
    }
    .status-blue {
        background: rgba(255, 255, 255, 0.2);
        color: #E6FFFF;
    }

    </style>
    """, unsafe_allow_html=True)

    admin_nav = st.sidebar.radio(
        "Admin Sections", [
            "Platform Analytics",
            "All-User Reports",
            "Dataset Management",
            "AI Model Hub"
        ], index=0
    )

    if admin_nav == "Platform Analytics":
        st.markdown('<div class="page-title">MetalliQ Admin Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-desc">System-wide insights, performance analytics, and platform overview.</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stats-row">
            <div class="stats-card"><div class="stats-title">Active Users</div>
                <div class="stats-value">{user_info.get('active_users', 33)}</div>
            </div>
            <div class="stats-card"><div class="stats-title">Ongoing LCA Studies</div>
                <div class="stats-value">{user_info.get('lca_studies', 12)}</div></div>
            <div class="stats-card"><div class="stats-title">Reports Generated</div>
                <div class="stats-value">{user_info.get('reports_generated', 67)}</div></div>
            <div class="stats-card"><div class="stats-title">AI Models Available</div>
                <div class="stats-value">{ai_models_df.shape[0]}</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Impact Trends Over Time</div>', unsafe_allow_html=True)

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
            font=dict(color="#FFFFFF"),
            xaxis=dict(tickfont=dict(color='white')),
            yaxis=dict(tickfont=dict(color='white'))
        )
        st.plotly_chart(fig, use_container_width=True)

    elif admin_nav == "All-User Reports":
        st.markdown('<div class="page-title">All User Reports</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-desc">Explore and manage sustainability reports submitted by users.</div>', unsafe_allow_html=True)
        st.dataframe(users_df, use_container_width=True)

    elif admin_nav == "Dataset Management":
        st.markdown('<div class="page-title">Dataset Management</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Upload or Update Core LCI Dataset</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload New Dataset (CSV or JSON)", type=['csv', 'json'], key="uploader"
        )

        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1].lower()
            if ext == 'csv':
                df = pd.read_csv(uploaded_file)
            elif ext == 'json':
                df = pd.read_json(uploaded_file)
            st.success("✅ Dataset Updated Successfully.")

        st.markdown('<div class="section-header" style="margin-top:25px;">Upload History & Version Control</div>', unsafe_allow_html=True)
        st.dataframe(datasets_df, use_container_width=True)

    elif admin_nav == "AI Model Hub":
        st.markdown('<div class="page-title">AI Model Training Hub</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-desc">Monitor, retrain, and analyze AI-driven sustainability models.</div>', unsafe_allow_html=True)
        st.dataframe(ai_models_df, use_container_width=True)

        st.markdown("""
        <div style="background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.25);
        border-radius:14px;padding:18px 24px;margin-top:20px;">
            <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="font-size:1.15rem;font-weight:700;color:#7CF4E3;">Retrain Models from All Sources</div>
                <button class="admin-btn">🔄 Retrain</button>
            </div>
        </div>
        """, unsafe_allow_html=True)


# Run Admin Dashboard
show_admin_dashboard(user_info, users_df, datasets_df, ai_models_df)
