def show_welcome_page():
    import streamlit as st
    import json
    from streamlit_lottie import st_lottie

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Poppins:wght@400;600&display=swap');

    body, .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
        color: #073B4C;
        font-family: 'Poppins', sans-serif;
    }

    /* ===== HEADINGS ===== */
    .main-head {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.8rem;
        background: linear-gradient(90deg, #006D77 20%, #00A896 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-top: 1em;
        margin-bottom: 0.3em;
    }

    .main-desc {
        text-align: center;
        color: #00494D;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.7em;
    }

    .key-features-title {
        text-align: center;
        color: #00494D;
        font-weight: 700;
        font-size: 1.5rem;
        margin-top: 2em;
        margin-bottom: 1.5em;
    }

    /* ===== MAIN CONTAINER ===== */
    .features-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 4rem;
        flex-wrap: wrap;
        width: 100%;
        margin: 2em auto;
    }

    /* ===== LEFT START SECTION ===== */
    .start-section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    .launch-btn {
        background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
        color: #FFFFFF !important;
        padding: 1.1em 2.5em;
        border-radius: 10px;
        border: none;
        font-size: 1.15rem;
        font-weight: 600;
        box-shadow: 0 4px 14px rgba(0,109,119,0.25);
        cursor: pointer;
        transition: all 0.3s ease;
        letter-spacing: 0.03em;
        text-align: center;
    }

    .launch-btn:hover {
        background: linear-gradient(90deg, #007F8E 0%, #00BFA5 100%);
        box-shadow: 0 6px 20px rgba(0,150,160,0.3);
        transform: scale(1.04);
    }

    /* ===== RIGHT FEATURES GRID ===== */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 240px);
        grid-gap: 1.8rem;
        justify-content: center;
        align-items: center;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.55);
        border: 1px solid rgba(0, 109, 119, 0.25);
        border-radius: 16px;
        box-shadow: 0 3px 10px rgba(0,109,119,0.15);
        padding: 1.8rem 1rem;
        text-align: center;
        transition: all 0.25s ease;
        backdrop-filter: blur(8px);
        height: 190px;
    }

    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 5px 16px rgba(0,150,160,0.25);
    }

    .card-icon {
        font-size: 2.3rem;
        margin-bottom: 0.6em;
        color: #006D77;
    }

    .card-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #00494D;
        margin-bottom: 0.3em;
    }

    .card-desc {
        font-size: 0.95rem;
        color: #073B4C;
        opacity: 0.9;
    }

    /* ===== RESPONSIVE ADJUSTMENTS ===== */
    @media (max-width: 1200px) {
        .features-grid {
            grid-template-columns: repeat(2, 240px);
        }
    }
    @media (max-width: 800px) {
        .features-container {
            flex-direction: column;
            gap: 2rem;
        }
        .features-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Optional animation (non-blocking)
    try:
        with open("src/Welcome_Animation.json", "r") as f:
            lottie_json = json.load(f)
        st_lottie(lottie_json, height=110, key="welcome_lottie")
    except:
        pass

    # Headings
    st.markdown("<div class='main-head'>MetalliQ Sustainability Platform</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-desc'>AI-Powered Life Cycle Intelligence for Metals & Alloys</div>", unsafe_allow_html=True)
    st.markdown("<div class='key-features-title'>Key Features</div>", unsafe_allow_html=True)

    # --- MAIN FLEX CONTAINER ---
    st.markdown("<div class='features-container'>", unsafe_allow_html=True)

    # Left column (Start button)
    st.markdown("<div class='start-section'><button class='launch-btn'>🚀 Start Platform</button></div>", unsafe_allow_html=True)

    # Right column (Features grid)
    features = [
        {"icon": "🧭", "title": "ISO 14044 Workflow", "desc": "Standardized and automated LCA pipeline for metallurgical processes."},
        {"icon": "🌿", "title": "Circularity Metrics", "desc": "Quantify sustainability and material reuse efficiency in real-time."},
        {"icon": "🤖", "title": "AI-Assisted Modeling", "desc": "Predict missing values and simulate environmental outcomes intelligently."},
        {"icon": "📊", "title": "Interactive Dashboards", "desc": "Visualize emissions, energy flows, and recycling potential seamlessly."},
        {"icon": "☁️", "title": "Cloud Data Sync", "desc": "Secure integration with AI services and cloud sustainability datasets."},
        {"icon": "📄", "title": "Automated Reports", "desc": "Instant, audit-ready ISO-compliant LCA summaries."}
    ]

    html = "<div class='features-grid'>"
    for f in features:
        html += f"""
        <div class='feature-card'>
            <div class='card-icon'>{f['icon']}</div>
            <div class='card-title'>{f['title']}</div>
            <div class='card-desc'>{f['desc']}</div>
        </div>
        """
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Functional Button (real Streamlit button trigger) ---
    if st.button("Launch Platform 🚀", key="real_launch_btn"):
        st.session_state.show_login = True
