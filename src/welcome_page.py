import streamlit as st

def show_welcome_page():
    # ========== THEME & STYLES ==========
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;600&display=swap');

    /* App background and base */
    .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
        color: #073B4C;
        font-family: 'Poppins', sans-serif;
    }

    /* Header sizing - keep small margins so layout does not push down */
    h1.app-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 34px;
        margin: 8px 0 4px 0;
        text-align: center;
        color: #00494D;
    }
    h4.app-sub {
        margin: 0 0 14px 0;
        text-align: center;
        color: #00494D;
        font-weight: 600;
    }

    /* Features wrapper - centered and constrained width */
    .features-wrapper {
        max-width: 1100px;
        margin: 0 auto;
        padding: 6px 18px;
    }

    /* Card style */
    .feature-card {
        background: rgba(255,255,255,0.62);
        border-radius: 14px;
        border: 1px solid rgba(0,109,119,0.18);
        box-shadow: 0 3px 10px rgba(0,109,119,0.12);
        padding: 18px;
        text-align: center;
        min-height: 160px; /* keeps consistent height */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .feature-card .icon {
        font-size: 2.2rem;
        margin-bottom: 8px;
    }
    .feature-card .title {
        font-weight: 700;
        color: #00494D;
        margin-bottom: 6px;
    }
    .feature-card .desc {
        color: #073B4C;
        font-size: 0.95rem;
        opacity: 0.95;
    }

    /* Start button (styled global buttons too) */
    div.stButton > button.start-btn {
        background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
        color: #ffffff !important;
        border: none;
        border-radius: 10px;
        padding: 0.9em 2.2em;
        font-weight: 600;
        box-shadow: 0 4px 14px rgba(0,109,119,0.20);
        transition: transform .15s ease, box-shadow .15s ease;
        display: inline-block;
        margin: 0 auto;
    }
    div.stButton > button.start-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,150,160,0.22);
    }

    /* Small responsive tweaks */
    @media (max-width: 900px) {
        .feature-card { min-height: 150px; padding: 14px; }
        h1.app-title { font-size: 28px; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ========== HEADER ==========
    st.markdown("<h1 class='app-title'>MetalliQ Sustainability Platform</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='app-sub'>AI-Powered Life Cycle Intelligence for Metals & Alloys</h4>", unsafe_allow_html=True)

    # ========== FEATURES GRID (3 x 2) ==========
    st.markdown("<div class='features-wrapper'>", unsafe_allow_html=True)

    features = [
        ("🧭", "ISO 14044 Workflow", "Automated LCA pipeline for metallurgical processes."),
        ("🌿", "Circularity Metrics", "Track sustainability and material reuse efficiency."),
        ("🤖", "AI-Assisted Modeling", "Predict outcomes and simulate sustainability impact."),
        ("📊", "Interactive Dashboards", "Visualize emissions and recycling performance."),
        ("☁️", "Cloud Data Sync", "Integrate AI services and sustainability datasets."),
        ("📄", "Automated Reports", "Generate ISO-compliant sustainability reports."),
    ]

    # Two rows of three columns — Streamlit columns used for stable layout
    for row_start in (0, 3):
        cols = st.columns(3)
        for col_index, col in enumerate(cols):
            idx = row_start + col_index
            if idx < len(features):
                icon, title, desc = features[idx]
                with col:
                    st.markdown(
                        f"""
                        <div class='feature-card'>
                            <div class='icon'>{icon}</div>
                            <div class='title'>{title}</div>
                            <div class='desc'>{desc}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ========== START BUTTON (centered beneath the grid) ==========
    # Use three columns so the center column holds the button exactly in the middle
    c1, c2, c3 = st.columns([1, 0.6, 1])
    with c2:
        # two ways to ensure styling + functionality:
        # - assign a CSS class to the Streamlit button via the global selector using the "start-btn" class.
        # Streamlit doesn't let us attach a class attribute directly, but we can reuse global button styling.
        # To make it explicit, we style all buttons above; here we create a streamlit button and apply the start-btn
        btn = st.button("🚀 Start Platform", key="start_btn")
        # add a small JS-free visual duplicate (optional) — NOT NEEDED because our global button CSS styles the st.button already.

    # trigger login if clicked
    if st.session_state.get("start_btn", False) or btn:
        # Some versions of Streamlit set the button return to True in `btn`.
        # Ensure the session flag is set and the navigation is triggered.
        st.session_state.show_login = True
