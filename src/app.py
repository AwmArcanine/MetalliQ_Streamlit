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

# Streamlit configuration
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="MetalliQ Sustainability Platform")

# ===================== GLOBAL STYLE =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Poppins:wght@400;600&display=swap');

.stApp {
  background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
  color: #073B4C;
  font-family: 'Poppins', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: rgba(0, 73, 77, 0.96);
  border-right: 2px solid rgba(0,168,150,0.35);
  box-shadow: 2px 0 12px rgba(0,109,119,0.25);
}
section[data-testid="stSidebar"] * {
  color: #EAF4F4 !important;
  font-weight: 600;
  font-size: 1.05rem;
}
section[data-testid="stSidebar"] h2 {
  color: #00A896 !important;
  text-shadow: 0 0 8px rgba(0,168,150,0.3);
}

/* Buttons */
div.stButton > button {
  background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
  color: white !important;
  border: none;
  border-radius: 10px;
  padding: 0.6em 1.8em;
  font-weight: 600;
  box-shadow: 0 4px 14px rgba(0,109,119,0.25);
  transition: all 0.3s ease;
}
div.stButton > button:hover {
  background: linear-gradient(90deg, #007F8E 0%, #00BFA5 100%);
  transform: scale(1.05);
}

/* Card */
.card {
  background: rgba(255, 255, 255, 0.55);
  border-radius: 15px;
  box-shadow: 0 4px 18px rgba(0,109,119,0.15);
  padding: 1.5rem;
  border: 1px solid rgba(0,109,119,0.25);
}
footer, #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ===================== MAIN APP =====================
def main_app():
    if "show_login" not in st.session_state:
        st.session_state.show_login = False

    # Welcome page first
    if not st.session_state.show_login:
        show_welcome_page()
        return

    # Login next
    if not st.session_state.get('logged_in'):
        login_page()
        return

    # Sidebar always visible when logged in
    st.sidebar.title("🌿 MetalliQ")
    st.sidebar.markdown("**Sustainability Platform**")
    page = st.sidebar.radio("Navigation", ["Dashboard", "Create Study", "View Reports", "Compare Scenarios", "Sign Out"])

    if page == "Dashboard":
        if st.session_state.get('role') == "Admin":
            user_info = {"active_users": 33, "lca_studies": 12, "reports_generated": 67}
            show_admin_dashboard(user_info, users_df, datasets_df, ai_models_df)
        else:
            dashboard_page()
        if st.session_state.get('ai_recommendations'):
            display_ai_recommendations(st.session_state['ai_recommendations'])

    elif page == "Create Study":
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

    elif page == "View Reports":
        view_reports_page()

    elif page == "Compare Scenarios":
        compare_scenarios_page()

    elif page == "Sign Out":
        st.session_state.clear()
        st.rerun()


if __name__ == "__main__":
    main_app()
