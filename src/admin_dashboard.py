import streamlit as st
import pandas as pd
import plotly.express as px

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

def show_admin_dashboard(user_info, users_df, datasets_df, ai_models_df):
    st.markdown("""
    <style>
    body{font-family:'Inter',sans-serif !important;}
    .page-title{font-size:2.5em;font-weight:800;letter-spacing:-1.1px;color:#232738;margin:30px 0 10px 4px;}
    .page-desc{font-size:1.15em;color:#7a8795;margin-bottom:28px;}
    .stats-row{display:flex;gap:32px;margin-bottom:24px;margin-top:15px;}
    .stats-card{background:#fff;border-radius:15px;box-shadow:0 4px 22px #202a3212;
        padding:29px 30px 21px 31px;text-align:left;flex:1;}
    .stats-title{color:#6f7481;font-size:1.04em;font-weight:700;}
    .stats-value{color:#181f28;font-size:2.25em;font-weight:800;}
    .table-block{background:#fff;border-radius:13px;box-shadow:0 4px 24px #cddcfc12;padding:0 0 13px 0;margin-bottom:18px;}
    .section-header{font-weight:800;color:#191f28;font-size:1.31em;margin:18px 0 19px 10px;}
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
        st.markdown('<div class="page-title">Admin Panel</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-desc">System oversight and management dashboard.</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stats-row">
            <div class="stats-card"><div class="stats-title">Active Users</div>
                <div class="stats-value">{user_info.get('active_users', 33)}</div>
            </div>
            <div class="stats-card"><div class="stats-title">Ongoing LCA Studies</div>
                <div class="stats-value">{user_info.get('lca_studies', 12)}</div></div>
            <div class="stats-card"><div class="stats-title">Total Reports Generated</div>
                <div class="stats-value">{user_info.get('reports_generated', 67)}</div></div>
            <div class="stats-card"><div class="stats-title">AI Models Available</div>
                <div class="stats-value">{ai_models_df.shape[0]}</div></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="section-header">Impact Trends Over Time</div>', unsafe_allow_html=True)

        # Sample data for impact trends
        impact_data = pd.DataFrame({
            "Month": pd.date_range(start="2025-01-01", periods=10, freq="M"),
            "CO2 Emissions (t)": [120, 110, 113, 108, 105, 102, 99, 100, 96, 95],
            "Water Use (m3)": [800, 740, 720, 735, 710, 700, 695, 670, 665, 660],
            "Circularity (%)": [42, 45, 47, 48, 50, 52, 53, 54, 55, 56]
        })

        # Melt for multi-line plot
        impact_long = impact_data.melt(id_vars="Month", var_name="Indicator", value_name="Value")
        fig = px.line(impact_long, x="Month", y="Value", color="Indicator",
                    markers=True, title="Impact Trends Over Time",
                    labels={"Month": "Month", "Value": "Value", "Indicator": "Indicator"})
        fig.update_layout(legend_title_text='Indicator', height=410)

        st.plotly_chart(fig, use_container_width=True)

    elif admin_nav == "All-User Reports":
        st.markdown('<div class="page-title">All User Reports Explorer</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="padding:14px 0 12px 0;">
        <select style="border-radius:4px;padding:7px 18px;border:1.3px solid #dde6ee;font-size:1.07em;margin-right:15px;">
            <option>All Users</option>
            <option>John Doe</option>
            <option>Jane Smith</option>
            <option>Alex Wong</option>
        </select>
        <select style="border-radius:4px;padding:7px 18px;border:1.3px solid #dde6ee;font-size:1.07em;">
            <option>All Materials</option>
            <option>Steel</option>
            <option>Aluminium</option>
            <option>Bauxite</option>
        </select>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(users_df, use_container_width=True)

    elif admin_nav == "Dataset Management":
        st.markdown("""
        <style>
        .primary-btn, .admin-btn {
            background: linear-gradient(92deg, #16a6ff 44%, #1173b8 100%);
            color: #fff !important;
            padding: 0.68em 2.4em;
            border-radius: 19px;
            border: none;
            font-size: 1.17rem;
            font-weight: 750;
            box-shadow: 0 1.5px 11px rgba(18,220,255,0.09);
            cursor: pointer;
            letter-spacing: 0.08px;
            transition: all 0.14s;
            margin-bottom: 8px;
            margin-top: 2px;
        }
        .primary-btn:hover, .admin-btn:hover {
            box-shadow:0 2px 16px rgba(30,190,255,.17);
            background:linear-gradient(91deg,#19a5ec 24%,#1e65d1 100%);
            transform: scale(1.045);
            color:#f2ffff !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="page-title">Database Management</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Update Core LCI Database</div>', unsafe_allow_html=True)

        # Upload logic
        uploaded_file = st.file_uploader(
            "Upload New Dataset (CSV or JSON)", type=['csv', 'json'], key="uploader"
        )

        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1].lower()
            if ext == 'csv':
                df = pd.read_csv(uploaded_file)
            elif ext == 'json':
                df = pd.read_json(uploaded_file)
            st.success("Dataset Updated successfully.")

        st.markdown('<div class="section-header" style="margin-top:30px;">Upload History & Version Control</div>', unsafe_allow_html=True)
        st.dataframe(datasets_df, use_container_width=True)


    elif admin_nav == "AI Model Hub":
        st.markdown('<div class="page-title">AI Model Training Hub</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Model Info</div>', unsafe_allow_html=True)
        st.dataframe(ai_models_df, use_container_width=True)
        st.markdown("""
        <div class="table-block" style="padding: 19px 18px 11px 18px;">
        <div style="display:flex;align-items:center;gap:35px;">
            <div style="flex:1;">
            <div class="stats-title" style="margin-bottom:4px;">Model Version</div>
            <div style="font-size:2.05em;color:#138ad7;font-weight:800;margin-bottom:5px;">2.1</div>
            </div>
            <div style="flex:1;">
            <div class="stats-title" style="margin-bottom:4px;">Model Accuracy</div>
            <div style="font-size:2.05em;color:#138ad7;font-weight:800;margin-bottom:5px;">96.5%</div>
            </div>
            <div style="flex:1;">
            <div class="stats-title" style="margin-bottom:4px;">Last Trained</div>
            <div style="font-size:1.47em;color:#13192d;font-weight:800;margin-bottom:5px;">2023-10-15</div>
            </div>
            <div style="flex:2; text-align:right;">
            <button class="admin-btn">Retrain Model from All Sources</button>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="section-header" style="margin-top: 35px;">Training Logs</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="table-block" style="box-shadow:none;">
        <div style="background:#181f20;color:#a7ffd0;border-radius:10px;font-family:'JetBrains Mono',monospace;font-size:1.08em;padding:19px 24px;min-height:80px;">
        [2023-10-15 18:00 UTC] [Success]: Retraining Cycle - Accuracy improved to 96.5%. New data from ecoinvent_v3.8 incorporated.<br>
        [2023-09-01 14:30 UTC] [Success]: Initial Model Training - Baseline model trained with 94.2% accuracy.
        </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="section-header" style="margin-top:34px;">Continuous Learning Sources</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="table-block" style="box-shadow:none;">
        <div style="background:#fff;padding:23px 29px 9px 29px;border-radius:12px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
            <div style="font-weight:700;font-size:1.06em;color:#1b3545;">Ecoinvent API</div>
            <span class="status-chip status-green">Connected</span>
            </div>
            <div style="font-size:.99em;color:#64788f;margin-bottom:9px;">LCI Database | Last Sync: 2023-10-15</div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
            <div style="font-weight:700;font-size:1.06em;color:#1b3545;">World Steel Association</div>
            <span class="status-chip status-green">Connected</span>
            </div>
            <div style="font-size:.99em;color:#64788f;margin-bottom:9px;">Industry Data | Last Sync: 2023-10-14</div>
            <div style="display:flex;align-items:center;justify-content:space-between;">
            <div style="font-weight:700;font-size:1.06em;color:#1b3545;">IEA Energy Stats</div>
            <span class="status-chip status-blue">Syncing</span>
            </div>
            <div style="font-size:.99em;color:#64788f;">Energy Grid Mix | Last Sync: 2023-10-13</div>
        </div>
        </div>
        """, unsafe_allow_html=True)

# To run the dashboard
show_admin_dashboard(user_info, users_df, datasets_df, ai_models_df)
