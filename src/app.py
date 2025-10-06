import streamlit as st
from welcome_page import show_welcome_page
from login_page import login_page
from lca_study_form import full_lca_study_form
from lca_simulation import run_simulation
from dashboard import dashboard_page
from ai_recommendation import display_ai_recommendations, ai_data_example
from results_page import results_page
from admin_dashboard import show_admin_dashboard, users_df, datasets_df, ai_models_df
from Compare_Scenarios import compare_scenarios_page
from view_reports import view_reports_page
from collaborative_workspace_page import collaborative_workspace_page

# ===================== PAGE CONFIG =====================
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="MetalliQ Sustainability Platform"
)

# ===================== GLOBAL SIDEBAR STYLING =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

/* Sidebar base */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2C33 0%, #003F46 60%, #00494D 100%);
    padding: 0 !important;
    font-family: 'Poppins', sans-serif;
    box-shadow: 3px 0 14px rgba(0, 109, 119, 0.35);
}

/* Logo header */
.sidebar-header {
    text-align: center;
    padding: 1.4rem 0 0.8rem 0;
}
.sidebar-header img {
    width: 44px;
    margin-bottom: 6px;
}
.sidebar-header h2 {
    font-weight: 800;
    font-size: 1.35rem;
    color: #FFFFFF;
    margin-bottom: -3px;
}
.sidebar-header p {
    color: #A4E0DD;
    font-size: 0.8rem;
    margin-bottom: 1.2rem;
}

/* Workspaces */
.workspace-section {
    padding: 0 1.2rem;
}
.workspace-section h4 {
    font-size: 0.8rem;
    font-weight: 700;
    color: #8EDDD0;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}
.workspace-box {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 8px 10px;
    margin: 4px 0 8px 0;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
}
.workspace-box:hover {
    background: rgba(255, 255, 255, 0.18);
}
.workspace-badge {
    display: inline-block;
    font-weight: 700;
    border-radius: 6px;
    width: 26px;
    height: 26px;
    text-align: center;
    line-height: 26px;
    color: white;
    margin-right: 10px;
}
.workspace-title {
    font-weight: 600;
    color: #EAF4F4;
}

/* Navigation */
.sidebar-nav {
    margin-top: 1.2rem;
    padding: 0 1.2rem;
}
.nav-item {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    border-radius: 8px;
    margin: 3px 0;
    color: #D8F3DC;
    font-weight: 500;
    transition: all 0.2s ease;
}
.nav-item:hover {
    background: rgba(255, 255, 255, 0.1);
}
.nav-active {
    background: rgba(255, 255, 255, 0.15);
    border-left: 4px solid #00A896;
}
.nav-icon {
    margin-right: 10px;
    font-size: 1.05em;
}

/* Footer */
.sidebar-footer {
    position: absolute;
    bottom: 20px;
    width: 100%;
    text-align: center;
}
.user-badge {
    background: #00494D;
    color: white;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    text-align: center;
    line-height: 36px;
    display: inline-block;
    font-weight: 700;
    font-size: 0.9em;
}
.user-name {
    color: #CFECEC;
    margin-top: 6px;
    font-size: 0.9em;
    font-weight: 600;
}
footer, #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ===================== MAIN APP =====================
def main_app():
    if "show_login" not in st.session_state:
        st.session_state.show_login = False

    if not st.session_state.show_login:
        show_welcome_page()
        return

    if not st.session_state.get('logged_in'):
        login_page()
        return

    role = st.session_state.get('role', 'User')
    username = st.session_state.get('username', 'John Doe')

    # ---------- SIDEBAR ----------
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <img src="https://cdn-icons-png.flaticon.com/512/942/942748.png" alt="icon">
            <h2>MetalliQ</h2>
            <p>Sustainability Platform</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='workspace-section'><h4>WORKSPACES</h4>", unsafe_allow_html=True)
        st.markdown("""
        <div class='workspace-box'>
            <div class='workspace-badge' style='background:#E84393;'>J</div>
            <div class='workspace-title'>John's Workspace</div>
        </div>
        <div class='workspace-box'>
            <div class='workspace-badge' style='background:#4F46E5;'>P</div>
            <div class='workspace-title'>Project Phoenix</div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='sidebar-nav'>", unsafe_allow_html=True)
        page = st.radio(
            "Navigation",
            ["Dashboard", "New Study", "Reports", "Compare Scenarios", "Collaborative Workspace", "Sign Out"],
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='sidebar-footer'>
            <div class='user-badge'>{username[0:2].upper()}</div>
            <div class='user-name'>{'Admin Panel' if role == 'Admin' else username}</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- PAGE ROUTING ----------
    if page == "Dashboard":
        if role == "Admin":
            user_info = {"active_users": 33, "lca_studies": 12, "reports_generated": 67}
            show_admin_dashboard(user_info, users_df, datasets_df, ai_models_df)
        else:
            dashboard_page()
        if st.session_state.get('ai_recommendations'):
            display_ai_recommendations(st.session_state['ai_recommendations'])

    elif page == "New Study":
        full_lca_study_form()
        if st.session_state.get('lca_form_submitted'):
            inputs = st.session_state['lca_form_data']
            with st.spinner("Performing LCA analysis..."):
                results = run_simulation(inputs)
            st.session_state['simulation_results'] = results
            st.session_state['ai_recommendations'] = ai_data_example
            st.session_state['lca_form_submitted'] = False
            st.success("Analysis Completed!")
            results_page(st.session_state['simulation_results'], st.session_state['ai_recommendations'])

    elif page == "Reports":
        view_reports_page()

    elif page == "Compare Scenarios":
        compare_scenarios_page()

    elif page == "Collaborative Workspace":
        collaborative_workspace_page()

    elif page == "Sign Out":
        st.session_state.clear()
        st.rerun()


# ---------- LOCAL TEST ----------
if __name__ == "__main__":
    main_app()
