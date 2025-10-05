import streamlit as st
from lca_study_form import full_lca_study_form
from lca_simulation import run_simulation
from dashboard import dashboard_page
from ai_recommendation import display_ai_recommendations, ai_data_example
from results_page import results_page
from admin_dashboard import show_admin_dashboard, users_df, datasets_df, ai_models_df
from Compare_Scenarios import compare_scenarios_page
from view_reports import view_reports_page
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# === FUTURISTIC GLOBAL THEME ===
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&family=Poppins:wght@400;600&display=swap');

    /* ===== APP BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #001a2e 0%, #003b46 40%, #00b4d8 100%);
        font-family: 'Poppins', sans-serif;
        color: #d9faff !important;
    }

    /* ===== HEADINGS ===== */
    h1, h2, h3, h4, h5 {
        color: #00f5ff !important;
        text-shadow: 0 0 12px #00f5ff, 0 0 25px #00b4d8;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 0.02em;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001f2f 0%, #003e4d 90%) !important;
        box-shadow: 2px 0 12px #00f5ff33;
        border-right: 1px solid #00f5ff44;
    }
    section[data-testid="stSidebar"] * {
        color: #c9faff !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
        color: #00f5ff !important;
        text-shadow: 0 0 8px #00f5ff;
    }

    /* ===== BUTTONS ===== */
    div.stButton > button {
        background-color: transparent;
        border: 2px solid #00f5ff;
        color: #00f5ff;
        border-radius: 10px;
        padding: 0.6em 1.8em;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px #00f5ff55;
        text-shadow: 0 0 5px #00eaff;
    }
    div.stButton > button:hover {
        background-color: #00f5ff;
        color: #001f2f !important;
        box-shadow: 0 0 25px #00f5ff;
        transform: scale(1.07);
    }

    /* ===== INPUT FIELDS ===== */
    input, textarea, select {
        background: rgba(0, 30, 40, 0.4) !important;
        color: #c9faff !important;
        border: 1px solid #00b4d8 !important;
        border-radius: 8px !important;
    }

    /* ===== CARD STYLING ===== */
    .card, .stContainer {
        background: rgba(0, 50, 70, 0.25);
        border-radius: 15px;
        border: 1px solid #00b4d8;
        box-shadow: 0 0 20px #00b4d833;
        padding: 20px;
        backdrop-filter: blur(8px);
    }

    /* ===== TOGGLE & RADIO ===== */
    div[role="radiogroup"] label {
        color: #00eaff !important;
    }

    /* ===== TOP BAR ===== */
    .main-top-bar {
        background: linear-gradient(90deg, #00b4d8 0%, #0077b6 100%);
        color: #e0ffff;
        text-shadow: 0 0 8px #00eaff;
        box-shadow: 0 4px 18px #00b4d833;
        border-radius: 0 0 25px 25px;
    }

    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR HEADER ---
def workspace_selector():
    st.sidebar.markdown(
        """
        <div style='display:flex;align-items:center;gap:13px;margin-bottom:27px;margin-top:4px'>
            <span style='font-size:2.2rem;line-height:.95;margin-right:10px;'>⚙️</span>
            <div>
                <div style='font-weight:900;font-size:1.25rem;
                            background:linear-gradient(90deg,#00f5ff,#00b4d8);
                            -webkit-background-clip:text;
                            -webkit-text-fill-color:transparent;
                            text-shadow:0 0 15px #00eaff;'>
                    MetalliQ
                </div>
                <div style='color:#87f5ff;font-size:.93rem;'>Futuristic LCA Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )
    st.sidebar.markdown("### WORKSPACES", unsafe_allow_html=True)
    ws_choice = st.sidebar.radio(
        "", st.session_state.get("workspaces", ["John's Workspace", "Project Phoenix"]),
        index=st.session_state.get("workspaces", ["John's Workspace", "Project Phoenix"]).index(
            st.session_state.get("current_workspace", "John's Workspace")),
        key="workspace_radio"
    )
    st.session_state["current_workspace"] = ws_choice
    st.sidebar.markdown("---")
    return ws_choice


def sidebar_navigation(active):
    menu = [
        {"name": "Dashboard", "icon": "🏠"},
        {"name": "Create Study", "icon": "🧪"},
        {"name": "View Reports", "icon": "📊"},
        {"name": "Compare Scenarios", "icon": "🔄"},
        {"name": "Sign Out", "icon": "🚪"}
    ]
    nav_options = [f"{item['icon']} {item['name']}" for item in menu]
    default_index = 0
    for idx, option in enumerate(nav_options):
        if option.endswith(active):
            default_index = idx
            break
    selected = st.sidebar.radio("Main Menu", nav_options, index=default_index)
    st.sidebar.markdown("---")
    return selected.split(" ", 1)[1]


# --- MAIN APP FUNCTION ---
def main_app():
    if "show_login" not in st.session_state:
        st.session_state.show_login = False
    if not st.session_state.show_login:
        from welcome_page import show_welcome_page
        show_welcome_page()
        return

    if "workspaces" not in st.session_state:
        st.session_state["workspaces"] = ["John's Workspace", "Project Phoenix"]
    if "current_workspace" not in st.session_state:
        st.session_state["current_workspace"] = st.session_state["workspaces"][0]

    if not st.session_state.get('logged_in'):
        from login_page import login_page
        login_page()
        return

    name = st.session_state.get('name', "John Doe")
    workspace = workspace_selector()
    page = st.session_state.get('page', "Dashboard")
    nav_page = sidebar_navigation(page)
    st.session_state['page'] = nav_page

    st.sidebar.markdown(f"<div style='margin-bottom:10px; font-weight:bold;'>Welcome, {st.session_state.get('role', 'Guest')}</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='margin-bottom:18px;'>Active workspace: <b>{workspace}</b></div>", unsafe_allow_html=True)

    # --- PAGE ROUTING ---
    if nav_page == "Dashboard":
        st.markdown("""
        <div class="main-top-bar">
            MetalliQ: AI-Powered Sustainability
            <span class="welcome-user" style="font-size:1.1rem;opacity:0.8;">Welcome, Sarah Singh</span>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.get('role') == "Admin":
            user_info = {"active_users": 33, "lca_studies": 12, "reports_generated": 67}
            show_admin_dashboard(user_info, users_df, datasets_df, ai_models_df)
        else:
            dashboard_page()
        if st.session_state.get('ai_recommendations'):
            display_ai_recommendations(st.session_state['ai_recommendations'])

    elif nav_page == "Create Study":
        full_lca_study_form()
        if st.session_state.get('lca_form_submitted'):
            inputs = st.session_state['lca_form_data']
            with st.spinner("Performing Life Cycle Assessment analysis..."):
                results = run_simulation(inputs)
            st.session_state['simulation_results'] = results
            st.session_state['ai_recommendations'] = ai_data_example
            st.session_state['lca_form_submitted'] = False
            st.success("Analysis Completed!")
            results_page(st.session_state['simulation_results'], st.session_state['ai_recommendations'])

    elif nav_page == "View Reports":
        view_reports_page()
    elif nav_page == "Compare Scenarios":
        compare_scenarios_page()
    elif nav_page == "Sign Out":
        st.session_state.clear()
        st.rerun()
    else:
        st.info("Page under development.")


if __name__ == "__main__":
    main_app()
