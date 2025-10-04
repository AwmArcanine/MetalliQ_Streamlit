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


st.markdown("""
<style>
/* Sidebar: background, width */
section[data-testid="stSidebar"] {
    min-width: 260px !important;
    max-width: 330px !important;
    width: 300px !important;
    background: linear-gradient(180deg,#182b3a 0%,#19375F 92%) !important;
    box-shadow: 2px 0 8px #05376917;
}

/* Main sidebar font/settings */
section[data-testid="stSidebar"] * {
    color: #f4faff !important;
    font-family: 'Inter', 'Segoe UI', 'Poppins', sans-serif !important;
    font-size: 1.05em !important;
    font-weight: 600 !important;
    letter-spacing: .01em;
    text-shadow: none !important;
}

/* Logo + MetalliQ title */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] h5,
section[data-testid="stSidebar"] h6 {
    color: #fff !important;
    font-size: 1.14em !important;
    font-weight: 800 !important;
    margin-bottom: 2px !important;
}

/* WORKSPACES heading  */
section[data-testid="stSidebar"] [class*="workspace"] {
    text-transform: uppercase;
    color: #e0eaff !important;
    font-size: 0.93em !important;
    letter-spacing: .054em;
    font-weight: 900 !important; 
    margin-bottom: 2px;
}

/* Workspace selection chips */
section[data-testid="stSidebar"] .st-emotion-cache-1b7j0ig, 
section[data-testid="stSidebar"] .st-emotion-cache-1b7j0ig * {
    color: #fff !important;
    font-size: 1.01em !important;
    font-weight: 800 !important;
    border-radius: 15px !important;
    padding-top: 4px !important; padding-bottom: 4px !important;
    background: #232f42 !important;
    margin-bottom: 7px !important;
    box-shadow: none !important;
}

/* Navigation icons and text */
section[data-testid="stSidebar"] ul,
section[data-testid="stSidebar"] li {
    color: #f2f8fc !important;
    font-size: 1.05em !important;
    font-weight: 700 !important;
    letter-spacing: .008em;
    margin-bottom: 8px !important;
    transition: background 0.2s;
}
section[data-testid="stSidebar"] svg {
    color: #b9c5e0 !important;
    margin-right: 5px;
}
section[data-testid="stSidebar"] [aria-disabled="true"] {
    color: #b2bdcb !important;
    opacity: 0.74 !important;
    font-size: 1.01em !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Let main container expand and center when sidebar is collapsed */
@media (max-width: 1250px) {
    .block-container {
        margin-left: auto !important;
        margin-right: auto !important;
        max-width: 720px !important;
        min-width: 388px;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        transition: margin 0.28s;
    }
}
/* If sidebar is collapsed, center the main block regardless of container */
[data-testid="collapsedControl"] ~ div section.main .block-container {
    margin-left: auto !important;
    margin-right: auto !important;
    max-width: 760px !important;
    min-width: 388px;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}
.welcome-center, .centered-card, .main-head, .main-desc, .card-container {
    margin-left: auto !important;
    margin-right: auto !important;
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)



# -------------------- Sidebar Logo + Workspace Switcher ----------------------
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

def show_welcome_page():
    import json
    with open("src/Welcome_Animation.json", "r") as f:
        lottie_json = json.load(f)

    # Animated background and styling
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(120deg,#101d2b 0%,#1b3255 59%,#0ac9e8 100%);
        background-attachment: fixed;
        min-height: 100vh;
        animation: gradientMove 12s ease-in-out infinite alternate;
        transition: background 2s;
    }
    @keyframes gradientMove {
        0% {background-position: 0% 50%;}
        100% {background-position: 100% 50%;}
    }
    /* Centering the welcome section */
    .welcome-center {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        min-height: 70vh;
        margin-top: 2.2rem;
    }
    /* Futuristic light blue-gradient heading */
    .main-head {
        background: linear-gradient(90deg,#76eaff 40%,#41d2ff 70%,#eaf6ff 98%);
        color: #38dbff; /* fallback */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-fill-color: transparent;
        font-size: 2.56rem;
        font-family: 'Segoe UI', 'Poppins', 'Roboto', sans-serif;
        font-weight: 880;
        letter-spacing: 0.2px;
        margin-bottom: 0.13em;
        margin-top: 0.4em;
        text-align: center;
        filter: brightness(1.18) drop-shadow(0 3px 10px #1fd6ff22);
    }
    .main-desc {
        font-size:1.18rem; color:#41c7d3;font-weight:600;margin-bottom:0.23em;
        text-align:center;
        margin-top:-0.2em;
    }
    </style>
    """, unsafe_allow_html=True)

    # -- Center block for all animated/content elements --
    st.markdown("<div class='welcome-center'>", unsafe_allow_html=True)
    st_lottie(lottie_json, height=200, key="welcome_lottie")

    st.markdown(
        "<div class='main-head'>MetalliQ LCA Platform</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='main-desc'>AI-Driven Life Cycle Assessment for Metallurgy</div>",
        unsafe_allow_html=True)
    st.markdown(
        """<div style='margin-bottom:1.2em; color:#eafeff;text-align:center;'>Welcome to <b style='color:#41c7d3'>MetalliQ</b> – your comprehensive platform for advanced Life Cycle Assessment (LCA) of metals, steel, and alloys. Optimize your product footprint, drive sustainability, and ensure compliance, all through an intuitive, AI-powered interface.</div>""",
        unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top:0.5em;color:#38dbff;text-align:center;'>Key Features</h3>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <div class="feature-card">
            <div class="card-title">ISO 14044 LCA Wizard</div>
            <div>Industry-standard workflow for metals, alloys, and steel.</div>
        </div>
        <div class="feature-card">
            <div class="card-title">AI Autofill & Explain</div>
            <div>Automatic data input and smart LCA result explanations for engineers.</div>
        </div>
        <div class="feature-card">
            <div class="card-title">Circularity & Eco-Labels</div>
            <div>Evaluate for circular economy, eco-labels, and maximize sustainability compliance.</div>
        </div>
        <div class="feature-card">
            <div class="card-title">Interactive Visuals</div>
            <div>Animated Sankey diagrams, timelines, and deep analytics for transparency.</div>
        </div>
        <div class="feature-card">
            <div class="card-title">Comprehensive Reports</div>
            <div>Automated PDF reporting for certifications, auditing, and quality checks.</div>
        </div>
        <div class="feature-card">
            <div class="card-title">Cloud AI Integration</div>
            <div>Seamless Google AI Studio and third-party workflow support.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;">
        <form action="#">
            <button class="start-btn" type="submit">Start Platform 🚀</button>
        </form>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close .welcome-center

    if st.button("Start Platform", key="realstartbutton"):
        st.session_state.show_login = True

# -------------------- LOGIN PAGE (pure card, no bar/header shown) ---------------------
def login_page():
    st.markdown("""
        <style>
        body {
            background: #f4f4f4 !important;
        }
        .centered-card {
            max-width: 420px;
            margin: 110px auto 0 auto;
            padding: 44px 44px 28px 44px;
            border-radius: 18px;
            background: #fff;
            box-shadow: 0 4px 32px #1b23362d;
            text-align: center;
            font-family: 'Segoe UI', 'Inter', sans-serif;
        }
        .bigicon {
            font-size:2.9rem;
            color:#174679;
            margin-bottom: 11px;
        }
        .title-bold {
            color:#174679;
            font-size:1.45rem;
            font-weight: 700;
            letter-spacing:-0.5px;
        }
        .subtle {
            color: #444b60;
            font-size:1.07rem;
            margin-bottom: 0.62rem;
            font-weight:500;
        }
        </style>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2,4,2])
    with col2:
        st.markdown("""
            <div class="centered-card">
                <div class="bigicon">🏛️</div>
                <div class="title-bold">MetalliQ</div>
                <div style="font-size:1.07rem;color: #313a4a;margin-bottom:1.05rem;">AI-Powered Metals Sustainability</div>
                <div class="subtle">Sign in to the official portal</div>
            </div>
        """, unsafe_allow_html=True)
        user = st.button("Sign In as User (John Doe)", key="user-btn")
        admin = st.button("Sign In as Admin (Sarah Singh)", key="admin-btn")
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

    # --- Only show the MetalliQ header bar after login
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
        <div style='
            width:100vw;
            min-width:100vw;
            max-width:100vw;
            left:0;
            margin:0;
            height:54px;
            background:linear-gradient(92deg,#1173b8 62%,#15447a 125%);
            color:#fff;
            border-radius:0 0 22px 22px;
            display:flex;
            align-items:center;
            padding-left:34px;
            font-size:1.43rem;
            font-weight:800;
            letter-spacing:-.2px;
            box-sizing:border-box;
            z-index:100;'>
            MetalliQ: AI-Powered Metals Sustainability
            <span style='font-weight:400;font-size:1.08rem;margin-left:29px;opacity:.86;'>
                Welcome, {name}
            </span>
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
