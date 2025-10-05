import streamlit as st

def show_welcome_page():
    # ========== GLOBAL STYLE ==========
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Poppins:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
        color: #073B4C;
        font-family: 'Poppins', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        color: #00494D;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.55);
        border-radius: 16px;
        box-shadow: 0 3px 10px rgba(0,109,119,0.15);
        border: 1px solid rgba(0,109,119,0.25);
        text-align: center;
        padding: 1.8rem 1rem;
        transition: all 0.25s ease;
        backdrop-filter: blur(8px);
    }

    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 5px 16px rgba(0,150,160,0.25);
    }

    .launch-btn {
        background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 10px;
        padding: 1.1em 2.5em;
        font-weight: 600;
        font-size: 1.15rem;
        box-shadow: 0 4px 14px rgba(0,109,119,0.25);
        transition: all 0.3s ease;
        letter-spacing: 0.03em;
        cursor: pointer;
        display: block;
        margin: 0 auto;
    }

    .launch-btn:hover {
        background: linear-gradient(90deg, #007F8E 0%, #00BFA5 100%);
        transform: scale(1.04);
        box-shadow: 0 6px 20px rgba(0,150,160,0.3);
    }

    .center-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 3rem;
        min-height: 100vh;
    }

    .features-grid {
        width: 100%;
        max-width: 950px;
        margin: auto;
    }

    @media (max-width: 900px) {
        .features-grid {
            max-width: 700px;
        }
    }

    @media (max-width: 600px) {
        .features-grid {
            max-width: 95%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ========== HEADER ==========
    st.markdown("<h1 style='text-align:center;'>MetalliQ Sustainability Platform</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#00494D;'>AI-Powered Life Cycle Intelligence for Metals & Alloys</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ========== MAIN CONTAINER ==========
    st.markdown("<div class='center-container'>", unsafe_allow_html=True)

    # ========== FEATURE GRID ==========
    st.markdown("<h3 style='text-align:center; color:#00494D;'>Key Features</h3>", unsafe_allow_html=True)
    st.markdown("<div class='features-grid'>", unsafe_allow_html=True)

    features = [
        ("🧭", "ISO 14044 Workflow", "Automated LCA pipeline for metallurgical processes."),
        ("🌿", "Circularity Metrics", "Track sustainability and material reuse efficiency."),
        ("🤖", "AI-Assisted Modeling", "Predict outcomes and simulate sustainability impact."),
        ("📊", "Interactive Dashboards", "Visualize emissions and recycling performance."),
        ("☁️", "Cloud Data Sync", "Integrate AI services and sustainability datasets."),
        ("📄", "Automated Reports", "Generate ISO-compliant sustainability reports."),
    ]

    for i in range(0, len(features), 3):
        c1, c2, c3 = st.columns(3)
        for j, col in enumerate([c1, c2, c3]):
            if i + j < len(features):
                icon, title, desc = features[i + j]
                with col:
                    st.markdown(
                        f"""
                        <div class='feature-card'>
                            <div style='font-size:2.3rem; margin-bottom:0.6em;'>{icon}</div>
                            <div style='font-weight:700; font-size:1.1rem; color:#00494D;'>{title}</div>
                            <div style='font-size:0.95rem; color:#073B4C;'>{desc}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ========== CENTERED BUTTON BELOW GRID ==========
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_center = st.columns([1, 1, 1])
    with col_center[1]:
        if st.button("🚀 Start Platform", key="start_btn", help="Begin your LCA Journey"):
            st.session_state.show_login = True

    st.markdown("</div>", unsafe_allow_html=True)
