import streamlit as st

def show_welcome_page():
    # ========== STYLES ==========
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;600&display=swap');

    /* Global background and fonts */
    .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
        font-family: 'Poppins', sans-serif;
        color: #073B4C;
    }

    /* Headers */
    h1.app-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 0.3rem;
        color: #7FFFD4;  /* light aqua */
        text-shadow: 0 0 6px rgba(127, 255, 212, 0.6),
                     0 0 12px rgba(0, 200, 180, 0.4);
        letter-spacing: 0.5px;
    }

    h4.app-sub {
        text-align: center;
        color: #C4FFF9;
        font-weight: 600;
        margin-bottom: 1.8rem;
        text-shadow: 0 0 4px rgba(180, 255, 240, 0.5);
    }

    /* Feature grid wrapper */
    .features-wrapper {
        max-width: 1100px;
        margin: 0 auto;
        padding: 0 18px;
    }

    /* Feature card styling */
    .feature-card {
        background: rgba(255,255,255,0.58);
        border-radius: 16px;
        border: 1px solid rgba(0,109,119,0.25);
        box-shadow: 0 3px 10px rgba(0,109,119,0.15);
        padding: 22px 16px;
        text-align: center;
        min-height: 170px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
        margin: 10px; /* Adds spacing between cards */
    }

    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 10px 22px rgba(0, 200, 180, 0.25),
                    0 4px 12px rgba(0,109,119,0.2);
        background: rgba(255,255,255,0.65);
    }

    .feature-card .icon {
        font-size: 2.3rem;
        margin-bottom: 8px;
    }

    .feature-card .title {
        font-weight: 700;
        color: #00494D;
        margin-bottom: 6px;
        font-size: 1.1rem;
    }

    .feature-card .desc {
        color: #073B4C;
        font-size: 0.95rem;
        opacity: 0.95;
    }

    /* Start Platform button */
    div.stButton > button.start-btn {
        background: linear-gradient(90deg, #009688 0%, #00C2A8 100%);
        color: #ffffff !important;
        border: none;
        border-radius: 10px;
        padding: 0.9em 2.2em;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 4px 14px rgba(0,109,119,0.25);
        transition: all 0.3s ease;
        margin: 1.2rem auto 2rem auto;
        display: block;
        letter-spacing: 0.03em;
    }

    div.stButton > button.start-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 22px rgba(0,200,180,0.25);
        background: linear-gradient(90deg, #00A896 0%, #00D8B5 100%);
    }

    @media (max-width: 900px) {
        .feature-card { min-height: 150px; padding: 16px; }
        h1.app-title { font-size: 1.8rem; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ========== HEADER ==========
    st.markdown("<h1 class='app-title'>MetalliQ Sustainability Platform</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='app-sub'>AI-Powered Life Cycle Intelligence for Metals & Alloys</h4>", unsafe_allow_html=True)

    # ========== FEATURE GRID ==========
    st.markdown("<div class='features-wrapper'>", unsafe_allow_html=True)

    features = [
        ("🧭", "ISO 14044 Workflow", "Automated LCA pipeline for metallurgical processes."),
        ("🌿", "Circularity Metrics", "Track sustainability and material reuse efficiency."),
        ("🤖", "AI-Assisted Modeling", "Predict outcomes and simulate sustainability impact."),
        ("📊", "Interactive Dashboards", "Visualize emissions and recycling performance."),
        ("☁️", "Cloud Data Sync", "Integrate AI services and sustainability datasets."),
        ("📄", "Automated Reports", "Generate ISO-compliant sustainability reports."),
    ]

    # Two rows × three columns
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

    # ========== BUTTON ==========
    center = st.columns([1, 0.6, 1])[1]
    with center:
        st.markdown(
            "<div style='text-align:center;'>",
            unsafe_allow_html=True
        )
        if st.button("🚀 Start Platform", key="start_btn"):
            st.session_state.show_login = True
        st.markdown("</div>", unsafe_allow_html=True)
