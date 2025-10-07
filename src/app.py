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
from pathlib import Path

hide_streamlit_ui = """
    <style>
    /* Hide top header (navbar with Share, etc.) */
    header[data-testid="stHeader"] {visibility: hidden !important;}
    div[data-testid="stToolbar"] {display: none !important;}

    /* Hide Streamlit footer */
    footer {visibility: hidden !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}

    /* Hide hamburger menu */
    #MainMenu {visibility: hidden !important;}

    /* Hide bottom-right Manage app button (new Streamlit Cloud UI) */
    button[title="Manage app"] {display: none !important;}
    div[data-testid="stActionButtonContainer"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}

    /* Optional: remove spacing left by hidden header/footer */
    section[data-testid="stSidebar"] > div:first-child {padding-top: 1rem !important;}
    </style>
"""
st.markdown(hide_streamlit_ui, unsafe_allow_html=True)
# ===================== PAGE CONFIG =====================
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="MetalliQ Sustainability Platform"
)


# ===================== LOAD EXTERNAL CSS SAFELY =====================
def load_css(file_path: str):
    css_path = Path(__file__).parent / file_path  # ensures correct relative path
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ CSS file not found: {css_path.name}. Using default theme.")


# ===================== MAIN APP =====================
def main_app():
    if "show_login" not in st.session_state:
        st.session_state.show_login = False

    if not st.session_state.show_login:
        show_welcome_page()
        return

    if not st.session_state.get("logged_in"):
        login_page()
        return

    role = st.session_state.get("role", "User")
    username = st.session_state.get("username", "John Doe")

    # ---------- SIDEBAR ----------
    load_css("app.css")

    with st.sidebar:
        # --- Header ---
        st.markdown("""
        <div class="sidebar-header" style="text-align:center; padding:1.2rem 0 0.6rem 0;">
            <img src="https://cdn-icons-png.flaticon.com/512/942/942748.png" alt="icon" style="width:46px;margin-bottom:6px;">
            <h2 style="font-weight:800;font-size:1.35rem;color:#FFFFFF;margin-bottom:-3px;">MetalliQ</h2>
            <p style="color:#A4E0DD;font-size:0.8rem;margin-bottom:1rem;">Sustainability Platform</p>
        </div>

        <div style="margin-top:1.2rem; background:rgba(255,255,255,0.1);
             border-radius:14px;padding:12px 16px 10px 16px;margin:1rem 1.2rem;
             box-shadow:0 6px 16px rgba(0,109,119,0.2);backdrop-filter:blur(8px);">
        """, unsafe_allow_html=True)

        # --- Navigation ---
        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "➕ New Study",
                "📊 Reports",
                "⚖️ Compare Scenarios",
                "👥 Collaborative Workspace",
                "🚪 Sign Out"
            ],
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # --- User Footer ---
        st.markdown(f"""
        <div style="text-align:center; margin-top:40px;">
            <div style="background:linear-gradient(90deg,#006D77,#00A896);
                color:white;padding:6px 10px;border-radius:50%;
                display:inline-block;font-weight:700;">
                {username[:2].upper()}
            </div>
            <div style="color:#CFECEC;margin-top:6px;font-size:0.9em;">
                {"Admin Panel" if role == "Admin" else username}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- PAGE ROUTING ----------
    if page == "🏠 Dashboard":
        if role == "Admin":
            user_info = {"active_users": 33, "lca_studies": 12, "reports_generated": 67}
            show_admin_dashboard(user_info, users_df, datasets_df, ai_models_df)
        else:
            dashboard_page()
        if st.session_state.get("ai_recommendations"):
            display_ai_recommendations(st.session_state["ai_recommendations"])

    elif page == "➕ New Study":
        full_lca_study_form()
        if st.session_state.get("lca_form_submitted"):
            inputs = st.session_state["lca_form_data"]
            with st.spinner("Performing LCA analysis..."):
                results = run_simulation(inputs)
            st.session_state["simulation_results"] = results
            st.session_state["ai_recommendations"] = ai_data_example
            st.session_state["lca_form_submitted"] = False
            st.success("Analysis Completed!")
            results_page(
                st.session_state["simulation_results"],
                st.session_state["ai_recommendations"]
            )

    elif page == "📊 Reports":
        view_reports_page()

    elif page == "⚖️ Compare Scenarios":
        compare_scenarios_page()

    elif page == "👥 Collaborative Workspace":
        collaborative_workspace_page()

    elif page == "🚪 Sign Out":
        st.session_state.clear()
        st.rerun()


# ---------- LOCAL TEST ----------
if __name__ == "__main__":
    main_app()
