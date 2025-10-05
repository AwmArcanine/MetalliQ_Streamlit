import streamlit as st
from lca_study_form import full_lca_study_form
from lca_simulation import run_simulation
from dashboard import dashboard_page
from ai_recommendation import display_ai_recommendations, ai_data_example
from results_page import results_page
from admin_dashboard import show_admin_dashboard, users_df, datasets_df, ai_models_df
from Compare_Scenarios import compare_scenarios_page
from view_reports import view_reports_page

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# === METALLIQ THEME: TECH & NATURE HARMONY ===
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Orbitron:wght@500;700&display=swap');

    /* ===== APP BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%);
        font-family: 'Poppins', sans-serif;
        color: #073B4C;
    }

    /* ===== HEADINGS ===== */
    h1, h2, h3, h4, h5 {
        color: #00494D !important;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 0.03em;
        text-shadow: 0 0 8px rgba(0,77,91,0.15);
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #013B44 0%, #00494D 90%) !important;
        border-right: 1px solid #007F8E;
        box-shadow: 3px 0 12px rgba(0,80,90,0.3);
        transition: all 0.3s ease-in-out;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #E0FBFC !important;
        font-weight: 500 !important;
    }

    /* Collapsed sidebar visibility */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* ===== BUTTONS ===== */
    div.stButton > button {
        background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 8px;
        padding: 0.55em 1.8em;
        font-weight: 600;
        transition: all 0.25s ease;
        box-shadow: 0 4px 12px rgba(0,109,119,0.25);
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #007F8E 0%, #009C9A 100%);
        box-shadow: 0 6px 18px rgba(0,150,160,0.3);
        transform: scale(1.03);
    }

    /* ===== INPUTS ===== */
    input, textarea, select {
        background: rgba(255,255,255,0.9) !important;
        color: #00494D !important;
        border: 1px solid #83C5BE !important;
        border-radius: 6px !important;
        font-size: 1rem;
    }

    /* ===== CARDS ===== */
    .card, .stContainer {
        background: rgba(255,255,255,0.5);
        border-radius: 12px;
        border: 1px solid rgba(0,109,119,0.25);
        box-shadow: 0 4px 12px rgba(0,109,119,0.15);
        padding: 18px;
        backdrop-filter: blur(10px);
    }

    /* ===== TOP BAR ===== */
    .main-top-bar {
        background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(0,109,119,0.25);
        border-radius: 0 0 25px 25px;
        font-weight: 600;
        padding: 20px 3vw;
        font-size: 1.5rem;
        letter-spacing: 0.02em;
    }

    /* ===== TEXT ===== */
    p, li, span {
        color: #073B4C;
    }

    /* ===== CHART BACKGROUND ===== */
    .plotly, canvas {
        background-color: transparent !important;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: #006D77;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #008C9E;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# --- Sidebar branding ---
def workspace_selector():
    st.sidebar.markdown("""
        <div style='display:flex;align-items:center;gap:13px;margin-bottom:27px;margin-top:4px'>
            <span style='font-size:2rem;'>🌿</span>
            <div>
                <div style='font-weight:900;font-size:1.3rem;
                            background:linear-gradient(90deg,#00A896,#83C5BE);
                            -webkit-background-clip:text;
                            -webkit-text-fill-color:transparent;'>
                    MetalliQ
                </div>
                <div style='color:#DEF6FF;font-size:.9rem;'>Sustainable AI for Metallurgy</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

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
    selected = st.sidebar.radio("Main Menu", nav_options, index=0)
    st.sidebar.markdown("---")
    return selected.split(" ", 1)[1]


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

    workspace = workspace_selector()
    nav_page = sidebar_navigation("Dashboard")
    st.sidebar.markdown(f"<div style='margin-bottom:10px;'>Active Workspace: <b>{workspace}</b></div>", unsafe_allow_html=True)

    # --- Pages ---
    if nav_page == "Dashboard":
        st.markdown("<div class='main-top-bar'>MetalliQ: AI-Powered Sustainability</div>", unsafe_allow_html=True)
        if st.session_state.get('role') == "Admin":
            show_admin_dashboard({"active_users": 33, "lca_studies": 12, "reports_generated": 67},
                                 users_df, datasets_df, ai_models_df)
        else:
            dashboard_page()
        if st.session_state.get('ai_recommendations'):
            display_ai_recommendations(st.session_state['ai_recommendations'])
    elif nav_page == "Create Study":
        full_lca_study_form()
        if st.session_state.get('lca_form_submitted'):
            inputs = st.session_state['lca_form_data']
            with st.spinner("Running LCA Simulation..."):
                results = run_simulation(inputs)
            st.session_state['simulation_results'] = results
            st.session_state['ai_recommendations'] = ai_data_example
            st.session_state['lca_form_submitted'] = False
            st.success("Analysis Completed!")
            results_page(st.session_state['simulation_results'],
                         st.session_state['ai_recommendations'])
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
