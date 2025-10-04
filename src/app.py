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
import json

with open("src/Welcome_Animation.json", "r") as f:  # Update path if needed
    lottie_json = json.load(f)

st_lottie(lottie_json, height=200)

# ==== MetalliQ Universal Theme & Sidebar Styles ====
st.markdown("""
<style>
body { background: #f8f9fb !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#132c43 7%,#15447a 94%) !important;
    color: #ffffff !important;
}
.st-emotion-cache-1v0mbdj p, .st-emotion-cache-1v0mbdj, .st-emotion-cache-10trblm {
    color: #ecdfff !important;
}
button, .stButton button {
    border-radius: 8px !important;
    background: #1366b3 !important;
    color: #fff !important;
    font-weight: 700;
    letter-spacing: .01em;
}
h1, h2, h3, h4, h5, h6 { color: #1366b3 !important; }
.st-emotion-cache-6qob1r, .sidebar-label { color:#fff !important; }
.st-emotion-cache-nahz7x .st-bz { background: #15447a !important; color:#fff !important; border-radius:12px;}
span[data-testid="stSidebarNav"] > div > ul > li > a { color:#f8f9fb !important; font-weight:500 !important;}
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
    # Animated background with mesh gradients (CSS)
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
    .card-container {
        display: flex; flex-wrap: wrap; gap: 1.5rem; justify-content:center; margin-top:2rem; margin-bottom:2.5rem;
    }
    .feature-card {
        background: rgba(24,30,48,0.95);
        border-radius: 19px;
        box-shadow: 0 10px 38px rgba(61,200,255,0.18), 0 2px 5px 2.5px rgba(0,200,245,0.09);
        min-width: 260px; max-width: 330px;
        padding: 1.45rem 1.16rem 1.2rem 1.16rem;
        color: #eafeff;
        font-size:1.09rem;
        margin-bottom: 1.4rem;
        transition: transform .17s, box-shadow .17s;
        border: 1.1px solid #1fa0ff33;
    }
    .feature-card:hover {
        transform: translateY(-10px) scale(1.035);
        box-shadow: 0 22px 42px rgba(0,220,255,0.19);
    }
    .card-title {
        color:#38dbff;font-size:1.17rem;margin-bottom:0.33rem;font-weight:600;letter-spacing:.4px;
    }
    .start-btn {
        background:linear-gradient(90deg,#16a6ff 44%,#12dde4 100%);
        border:none; border-radius:29px; color:#fff;
        font-size:1.28rem; padding:0.8rem 3.3rem;
        font-weight:700; box-shadow:0 1.5px 12px rgba(18,220,255,0.19);
        cursor:pointer; letter-spacing:.5px; margin-top:1.3rem; margin-bottom:1.6rem;
        transition: all 0.11s;
    }
    .start-btn:hover {
        box-shadow:0 2px 16px rgba(30,190,255,.27);
        transform: scale(1.055);
    }
    </style>
    """, unsafe_allow_html=True)

    st.image("src/metalliq_logo.jpg", width=80)

    st.markdown(
        "<h1 style='margin-bottom:0.13em;font-size:2.35rem;font-family:sans-serif;font-weight:880;letter-spacing:0.2px;'>MetalliQ LCA Platform</h1>",
        unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:1.18rem; color:#41c7d3;font-weight:600;margin-bottom:0.23em;'>AI-Driven Life Cycle Assessment for Metallurgy</div>",
        unsafe_allow_html=True)
    st.markdown(
        """<div style='margin-bottom:1.2em; color:#eafeff;'>Welcome to <b style='color:#41c7d3'>MetalliQ</b> – your comprehensive platform for advanced Life Cycle Assessment (LCA) of metals, steel, and alloys. Optimize your product footprint, drive sustainability, and ensure compliance, all through an intuitive, AI-powered interface.</div>""",
        unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top:0.5em;color:#38dbff;'>Key Features</h3>", unsafe_allow_html=True)

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
    st.markdown(
        f"<div style='width:97%;margin:35px auto 5px auto;height:62px;background:linear-gradient(92deg,#1173b8 62%,#15447a 125%);color:#fff;"
        f"border-radius:0 0 22px 22px;display:flex;align-items:center;padding-left:34px;font-size:1.51rem;font-weight:800;letter-spacing:-.2px;'>"
        f"MetalliQ: AI-Powered Metals Sustainability <span style='font-weight:400;font-size:1.09rem;margin-left:29px;opacity:.87;'>Welcome, {name}</span></div>",
        unsafe_allow_html=True
    )
    st.write("") # Spacing

    workspace = workspace_selector()
    page = st.session_state.get('page', "Dashboard")
    nav_page = sidebar_navigation(page)
    st.session_state['page'] = nav_page

    st.sidebar.markdown(f"<div style='margin-bottom:10px; font-weight:bold;'>Welcome, {st.session_state.get('role', 'Guest')}</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='margin-bottom:18px;'>Active workspace: <b>{workspace}</b></div>", unsafe_allow_html=True)

    if nav_page == "Dashboard":
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
