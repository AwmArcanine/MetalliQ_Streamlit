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
    from streamlit_lottie import st_lottie

    # Custom global background gradient
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
    .feature-head { color:#23d6ff;text-align:center;font-size:1.33rem;font-weight:800;margin-top:1.2em;margin-bottom:.45em;}
    .center-desc{
        color:#eafeff;text-align:center;max-width:680px;margin:0 auto 1.1em auto;font-size:1.05rem;
    }
    .features-flex-row {
        width:100vw;
        display:flex;
        flex-wrap:wrap;
        justify-content:center;
        gap:2.8rem 2.1rem;
        margin-top:.9em;
    }
    .feature-card {
        background: linear-gradient(130deg, #1c7ae0 97%, #41f6ff12 115%);
        border-radius: 19px;
        min-width: 305px;
        max-width: 350px;
        flex: 1 1 326px;
        box-shadow: 0 4px 22px 0 #0cb1ff12, 0 0px 1.5px 4px #29bbff11;
        margin-bottom: 14px;
        padding: 1.15em 1.2em 1.05em 1.36em;
        text-align: left;
        border: 1.5px solid #1cf3ff22;
        display: flex; flex-direction: row; gap: 1.13em; align-items: flex-start;
        transition: box-shadow .15s, transform .15s;
    }
    .feature-card:hover {
        box-shadow: 0 2px 32px #13e5ff51;
        transform: translateY(-4px) scale(1.022);
        background: linear-gradient(120deg, #29bafc 85%, #41f6ff3a 115%);
        border: 1.5px solid #27e3fa55;
    }
    .card-emoji {
        font-size: 2.14rem;
        margin-right: .36em;
    }
    .card-content { display:flex; flex-direction:column;}
    .card-title {
        font-weight: 800;
        color: #e8ffff;
        font-size: 1.18rem;
        margin-bottom: 0.15em;
        letter-spacing: .03px;
    }
    .card-desc {
        color: #eafafd;
        font-size: 1.03rem;
        font-weight:510;
        letter-spacing:.004em;
    }
    @media (max-width: 900px) {
        .features-flex-row {flex-direction:column;align-items:center;gap:1.2rem;}
        .feature-card {max-width:92vw;}
    }
    .welcome-card-btn {
        display:inline-block;
        background:linear-gradient(92deg,#16a6ff 44%,#1173b8 100%);
        color:#fff !important;
        padding:.7em 2.8em;
        border-radius:19px;
        border:none;
        font-size:1.1rem;
        font-weight:800;
        box-shadow:0 1.5px 12px rgba(18,220,255,0.14);
        cursor:pointer;
        letter-spacing:.04rem;
        margin-top:1.15em;
        margin-bottom:1.55em;
        transition:all .13s;
    }
    .welcome-card-btn:hover {
        box-shadow:0 2px 16px rgba(30,190,255,.18);
        background:linear-gradient(92deg,#19a5ec 44%,#1e65d1 100%);
        color:#f2ffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Lottie animation (bot)
    with open("src/Welcome_Animation.json", "r") as f:
        lottie_json = json.load(f)
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
    features = [
        {
            "title": "ISO 14044 LCA Wizard",
            "desc": "Industry-standard workflow for metals, alloys, and steel.",
            "emoji": "🧭"
        },
        {
            "title": "AI Autofill & Explain",
            "desc": "Automatic data input and smart LCA result explanations for engineers.",
            "emoji": "🤖"
        },
        {
            "title": "Circularity & Eco-Labels",
            "desc": "Evaluate for circular economy, eco-labels, and maximize sustainability compliance.",
            "emoji": "♻️"
        },
        {
            "title": "Interactive Visuals",
            "desc": "Animated Sankey diagrams, timelines, and deep analytics for transparency.",
            "emoji": "📊"
        },
        {
            "title": "Comprehensive Reports",
            "desc": "Automated PDF reporting for certifications, auditing, and quality checks.",
            "emoji": "📄"
        },
        {
            "title": "Cloud AI Integration",
            "desc": "Seamless Google AI Studio and third-party workflow support.",
            "emoji": "☁️"
        },
    ]

    st.markdown('<div class="features-flex-row">', unsafe_allow_html=True)
    for feat in features:
        card = f"""
        <div class="feature-card">
            <span class="card-emoji">{feat["emoji"]}</span>
            <div class="card-content">
                <div class="card-title">{feat["title"]}</div>
                <div class="card-desc">{feat["desc"]}</div>
            </div>
        </div>
        """
        st.markdown(card, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;">
        <button class="welcome-card-btn" onclick="window.location.href='#'">Start Platform 🚀</button>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Platform", key="realstartbutton"):
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
    .stButton>button, .styled-login-btn {
        padding: .64rem 1.7rem;
        background: linear-gradient(96deg,#1eb3ff 20%,#1590d7 90%);
        color: #fff !important;
        border: none !important;
        font-size: 1.06rem;
        font-weight: 700;
        margin-top: .13em;
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
        st.markdown("""
            <div class="centered-login-card">
                <div class="login-logo">🏛️</div>
                <div class="login-title">MetalliQ</div>
                <div class="login-sub">AI-Powered Metals Sustainability</div>
                <div class="login-desc">Sign in to the official portal</div>
            """, unsafe_allow_html=True)
        # Modern styled buttons
        user = st.button("Sign In as User (John Doe)", key="user-btn")
        admin = st.button("Sign In as Admin (Sarah Singh)", key="admin-btn")
        st.markdown("</div>", unsafe_allow_html=True)

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
        st.markdown(
        f"""
        <div style='width:100vw; min-width:100vw; max-width:100vw; left:0; margin:0; height:54px; background:linear-gradient(92deg,#1173b8 62%,#15447a 125%);
        color:#fff;border-radius:0 0 22px 22px;display:flex;align-items:center;padding-left:34px;
        font-size:1.43rem;font-weight:800;letter-spacing:-.2px;box-sizing:border-box;z-index:100;'>
            MetalliQ: AI-Powered Metals Sustainability
            <span style='font-weight:400;font-size:1.08rem;margin-left:29px;opacity:.86;'>Welcome, {name}</span>
        </div>
        """,
        unsafe_allow_html=True
        )
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
