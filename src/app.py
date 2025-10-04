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
# --- Global sidebar style ---
st.markdown("""
    <style>
    /* Sidebar main style */
    section[data-testid="stSidebar"] {
        min-width:260px !important; max-width:330px !important; width:295px !important;
        background: linear-gradient(180deg,#182b3a 0%,#19375F 92%) !important;
        box-shadow: 2px 0 8px #05376917;
    }
    section[data-testid="stSidebar"] * {
        color:#f4faff !important; font-family:'Inter','Segoe UI','Poppins',sans-serif !important;
        font-size:1.05em !important; font-weight:600 !important; letter-spacing:.01em;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5, section[data-testid="stSidebar"] h6 {
        color:#fff !important; font-size:1.14em !important; font-weight:800 !important; margin-bottom:2px !important;
    }
    section[data-testid="stSidebar"] [class*="workspace"] {
        text-transform:uppercase; color:#e0eaff !important; font-size:.93em !important;
        letter-spacing:.054em; font-weight:900 !important; margin-bottom:2px;
    }
    section[data-testid="stSidebar"] ul, section[data-testid="stSidebar"] li {
        color:#f2f8fc !important; font-size:1.05em !important; font-weight:700 !important; letter-spacing:.008em;
        margin-bottom:8px !important; transition:background .2s;
    }
    section[data-testid="stSidebar"] svg { color:#b9c5e0 !important; margin-right:5px; }
    section[data-testid="stSidebar"] [aria-disabled="true"] {
        color:#b2bdcb !important; opacity:.74 !important; font-size:1.01em !important; font-weight:600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------ Sidebar Workspace Switcher & Navigation -----
def workspace_selector():
    st.sidebar.markdown(
        """
        <div style='display:flex;align-items:center;gap:13px;margin-bottom:27px;margin-top:4px'>
            <span style='font-size:2.2rem;line-height:.95;margin-right:10px;'>🏛️</span>
            <div>
                <div style='font-weight:800;font-size:1.19rem;color:#fff;margin-bottom:0px;letter-spacing:-1px;'>MetalliQ</div>
                <div style='color:#b2cce9;font-size:.91rem;margin-top:-3px;'>Sustainability Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )
    st.sidebar.markdown("### WORKSPACES", unsafe_allow_html=True)
    st.sidebar.markdown(
        "<div style='padding:7px 0 7px 0;margin-bottom:7px;border-radius:11px;background:#393c54;color:#fff;font-weight:700;'>"
        "<span style='background:#e94ea7;border-radius:50%;padding:3px 13px 6px 13px;margin-right:9px;font-weight:700;font-size:1.1rem;'>J</span> John's Workspace"
        "</div>"
        "<div style='padding:7px 0 7px 0;margin-bottom:16px;border-radius:11px;background:#252a46;color:#fff;font-weight:700;'>"
        "<span style='background:#6f6beb;border-radius:50%;padding:3px 13px 6px 13px;margin-right:9px;font-weight:700;font-size:1.1rem;'>P</span> Project Phoenix"
        "</div>",
        unsafe_allow_html=True
    )
    ws_choice = st.sidebar.radio(
        "", st.session_state.get("workspaces", []),
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
        {"name": "Create Study", "icon": "📝"},
        {"name": "View Reports", "icon": "📑"},
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

# -------- Welcome Page (centered text, not whole block) -------------
def show_welcome_page():
    import streamlit as st
    import json

    # --------- Background & Heading Styles ----------
    st.markdown("""
    <style>
    body, .stApp {
        background: linear-gradient(108deg, #121c2b 0%, #115e85 100%) !important;
        background-color: #121c2b !important;
    }
    .main-head {
        background: linear-gradient(90deg,#76eaff 40%,#41d2ff 80%,#eaf6ff 98%);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        background-clip:text;text-fill-color:transparent;
        font-size:2.7rem; font-family:'Segoe UI','Poppins','Roboto',sans-serif;
        font-weight:900; letter-spacing:.23px; text-align:center; margin:0.2em 0 0.18em 0;
    }
    .main-desc { font-size:1.17rem; color:#41c7d3; font-weight:600; text-align:center; margin-top:-.18em; margin-bottom:.09em;}
    .center-desc{
        color:#eafeff;text-align:center;max-width:680px;margin:0 auto 1.1em auto;font-size:1.05rem;
    }
    .feature-head { color:#23d6ff;text-align:center;font-size:1.33rem;font-weight:800;margin-top:1.2em;margin-bottom:.45em;}
    </style>
    """, unsafe_allow_html=True)

    # --------- Optional: Lottie Animation (skip if not needed) ----------
    with open("src/Welcome_Animation.json", "r") as f:
        lottie_json = json.load(f)
    from streamlit_lottie import st_lottie
    st_lottie(lottie_json, height=105, key="welcome_lottie")

    st.markdown("<div class='main-head'>MetalliQ LCA Platform</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-desc'>AI-Driven Life Cycle Assessment for Metallurgy</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='center-desc'>"
        "Welcome to <b style='color:#41c7d3'>MetalliQ</b> – your comprehensive platform for advanced Life Cycle Assessment (LCA) of metals, steel, and alloys. "
        "Optimize your product footprint, drive sustainability, and ensure compliance, all through an intuitive, AI-powered interface."
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='feature-head'>Key Features</div>", unsafe_allow_html=True)

    # --------- GRID CARDS SECTION (3 columns x 2 rows) ----------
    st.markdown("""
    <style>
    .key-features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2.3rem 2.3rem;
        justify-content: center;
        margin: 1.7em auto 2.1em auto;
        max-width: 950px;
    }
    .feature-card {
        background: linear-gradient(130deg, #1fd8ff 72%, #46e0ff 110%);
        border-radius: 23px;
        box-shadow: 0 4px 24px #21eefd17;
        padding: 2.14rem 1.12rem 1.15rem 1.12rem;
        text-align: center;
        height: 185px;
        min-width: 0;
        width: 240px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: transform .15s, box-shadow .15s;
    }
    .feature-card:hover {
        transform: translateY(-7px) scale(1.045);
        box-shadow: 0 14px 39px #23d7f42c;
        background: linear-gradient(106deg, #11c1ee 90%, #2fd9f9 120%);
    }
    .card-icon { font-size: 2.22rem; margin-bottom: .7em; }
    .card-title { font-weight:800;font-size:1.14rem;margin-bottom:.30em;color:#195880;}
    .card-desc { font-size:.97rem;color:#134062;font-weight:520;}
    @media (max-width:900px) {.key-features-grid {grid-template-columns:1fr 1fr;}}
    @media (max-width:600px) {.key-features-grid {grid-template-columns:1fr;}}
    </style>
    <div class="key-features-grid">
    """, unsafe_allow_html=True)

    features = [
        {"icon": "🧭", "title": "ISO 14044 LCA Wizard", "desc": "Industry-standard workflow for metals, alloys, and steel."},
        {"icon": "🤖", "title": "AI Autofill & Explain", "desc": "Automatic data input and smart LCA result explanations for engineers."},
        {"icon": "♻️", "title": "Circularity & Eco-Labels", "desc": "Evaluate for circular economy, eco-labels, and maximize sustainability compliance."},
        {"icon": "📊", "title": "Interactive Visuals", "desc": "Animated Sankey diagrams, timelines, and deep analytics for transparency."},
        {"icon": "📄", "title": "Comprehensive Reports", "desc": "Automated PDF reporting for certifications, auditing, and quality checks."},
        {"icon": "☁️", "title": "Cloud AI Integration", "desc": "Seamless Google AI Studio and third-party workflow support."}
    ]
    for f in features:
        st.markdown(f"""
        <div class="feature-card">
            <div class="card-icon">{f['icon']}</div>
            <div class="card-title">{f['title']}</div>
            <div class="card-desc">{f['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Centered Start Button below grid ----------
    st.markdown("""
    <style>
    .welcome-card-btn {
        display:inline-block;
        background:linear-gradient(92deg,#16a6ff 44%,#1173b8 100%);
        color:#fff !important;
        padding:.9em 2.8em;
        border-radius:23px;
        border:none;
        font-size:1.19rem;
        font-weight:800;
        box-shadow:0 1.5px 18px #18d0ff21;
        cursor:pointer;
        letter-spacing:.03rem;
        margin-top:2.1em;
        margin-bottom:1.7em;
        transition:all .13s;
    }
    .welcome-card-btn:hover {
        box-shadow:0 2px 22px #30cbfd31;
        background:linear-gradient(92deg,#19a5ec 44%,#1e65d1 100%);
        color:#eaffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([3, 2, 3])
    with c2:
        if st.button("Start Platform 🚀", key="realstartbutton"):
            st.session_state.show_login = True


def login_page():
    import streamlit as st

    st.markdown("""
    <style>
    body { background: #f4f4f4 !important; }
    .centered-login-card {
        max-width: 420px;
        margin: 110px auto 0 auto;
        padding: 44px 44px 32px 44px;
        border-radius: 20px;
        background: linear-gradient(120deg, rgba(61,177,255,0.15) 60%, #eafdff25 100%);
        box-shadow: 0 6px 32px 0 #25d3fd24, 0 0px 0px 1.5px #2cbcff18;
        text-align: center;
        font-family: 'Segoe UI', 'Inter', sans-serif;
        position: relative;
    }
    .login-logo {
        font-size: 3.2rem;
        margin-bottom: 9px;
        color: #23d6ff;
        text-shadow: 0 2px 6px #33d6ff29;
    }
    .login-title {
        color: #174679;
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: .18em;
    }
    .login-sub {
        color: #44acc7;
        font-size: 1.06rem;
        margin-bottom: 1rem;
        font-weight: 600;
        letter-spacing: -.3px;
    }
    .login-desc {
        color: #444b60;
        font-size: 1.06rem;
        margin-bottom: 1.3rem;
        font-weight: 500;
    }
    .login-btn-row {
        display: flex;
        gap: 1.1em;
        justify-content: center;
        margin-top: 1.1em;
        margin-bottom: .42em;
    }
    .stButton>button, .styled-login-btn {
        padding: .64rem 1.7rem;
        background: linear-gradient(96deg,#1eb3ff 20%,#1590d7 90%);
        color: #fff !important;
        border: none !important;
        font-size: 1.06rem;
        font-weight: 700;
        border-radius: 16px;
        transition: background .18s, box-shadow .17s; 
        margin-bottom: .43em;
        box-shadow: 0 1.5px 18px #3ed6ff0d, 0 0 0 1.5px #29bbff13;
    }
    .stButton>button:hover, .styled-login-btn:hover {
        background: linear-gradient(92deg,#17a7ef 12%,#1363be 100%);
        color: #eafdfe !important;
        box-shadow: 0 3.2px 28px #27eaff24;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        user = st.button("Sign In as User (John Doe)", key="user-btn")
        admin = st.button("Sign In as Admin (Sarah Singh)", key="admin-btn")
        st.markdown("""
            <div class="centered-login-card">
                <div class="login-logo">🏛️</div>
                <div class="login-title">MetalliQ</div>
                <div class="login-sub">AI-Powered Metals Sustainability</div>
                <div class="login-desc">Sign in to the official portal</div>
                <div class="login-btn-row">
                    <div></div>
                    <div></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if user:
            st.session_state.logged_in = True
            st.session_state.role = "Investigator"
            st.session_state.name = "John Doe"
            st.session_state['page'] = 'Dashboard'
            st.rerun()
        if admin:
            st.session_state.logged_in = True
            st.session_state.role = "Admin"
            st.session_state.name = "Sarah Singh"
            st.session_state['page'] = 'Dashboard'
            st.rerun()

def main_app():
    if "show_login" not in st.session_state:
        st.session_state.show_login = False
    if not st.session_state.show_login:
        show_welcome_page()
        return
    if "workspaces" not in st.session_state:
        st.session_state["workspaces"] = ["John's Workspace", "Project Phoenix"]
    if "current_workspace" not in st.session_state:
        st.session_state["current_workspace"] = st.session_state["workspaces"][0]
    if not st.session_state.get('logged_in'):
        login_page()
        return
    name = st.session_state.get('name', "John Doe")
    workspace = workspace_selector()
    page = st.session_state.get('page', "Dashboard")
    nav_page = sidebar_navigation(page)
    st.session_state['page'] = nav_page
    st.sidebar.markdown(f"<div style='margin-bottom:10px; font-weight:bold;'>Welcome, {st.session_state.get('role', 'Guest')}</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='margin-bottom:18px;'>Active workspace: <b>{workspace}</b></div>", unsafe_allow_html=True)

    if nav_page == "Dashboard":
        st.markdown("""
        <style>
        .main-top-bar {
        max-width: 1200px;
        margin: 2.1rem auto 1.1rem auto;
        border-radius: 0 0 39px 39px;
        background: linear-gradient(90deg, #0d7dc1 80%, #158ddb 120%);
        color: #fff;
        font-family: 'Segoe UI', 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        padding: 22px 3vw 15px 36px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 7px 28px #1078c820;
        letter-spacing: .02em;
        }
        .welcome-user {
            font-size: 1.13rem;
            font-weight: 400;
            margin-left: .6em;
            opacity: 0.93;
        }
        @media (max-width: 950px) {.main-top-bar {font-size: 1.29rem; padding: 15px 2vw 12px 16px;}}
        @media (max-width: 700px) {.main-top-bar {font-size: 0.97rem; padding: 11px 2vw 9px 10px;}}
        </style>
        <div class="main-top-bar">
            MetalliQ: AI-Powered Metals Sustainability
            <span class="welcome-user">Welcome, Sarah Singh</span>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get('role') == "Admin":
            user_info = {
                "active_users": 33,
                "lca_studies": 12,
                "reports_generated": 67,
            }
            show_admin_dashboard(user_info, users_df, datasets_df, ai_models_df)
        else:
            dashboard_page()
        if st.session_state.get('ai_recommendations'):
            display_ai_recommendations(st.session_state['ai_recommendations'])

    elif nav_page == "Create Study":
        full_lca_study_form()
        if st.session_state.get('lca_form_submitted'):
            inputs = st.session_state['lca_form_data']
            with st.spinner("Performing Life Cycle Assessment analysis. This may take a minute..."):
                results = run_simulation(inputs)
            st.session_state['simulation_results'] = results
            st.session_state['ai_recommendations'] = ai_data_example
            st.session_state['lca_form_submitted'] = False
            st.success("Analysis Completed!")
            results_page(
                st.session_state['simulation_results'],
                st.session_state['ai_recommendations'],
            )

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
