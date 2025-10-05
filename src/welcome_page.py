def show_welcome_page():
    import streamlit as st
    import json
    from streamlit_lottie import st_lottie

    # === GLOBAL STYLE FOR WELCOME PAGE ===
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Poppins:wght@400;600&display=swap');

    body, .stApp {
        background: linear-gradient(135deg, #001a2e 0%, #003b46 45%, #00b4d8 100%) !important;
        background-attachment: fixed;
        color: #c9faff;
        font-family: 'Poppins', sans-serif;
    }

    /* ===== HEADINGS ===== */
    .main-head {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.8rem;
        background: linear-gradient(90deg,#00f5ff 10%,#00b4d8 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 15px #00eaff, 0 0 25px #00b4d8;
        text-align: center;
        font-weight: 800;
        margin-top: 1.2em;
        margin-bottom: 0.4em;
        letter-spacing: 0.02em;
    }

    .main-desc {
        text-align: center;
        color: #aef9ff;
        text-shadow: 0 0 10px #00eaff;
        font-weight: 600;
        margin-bottom: 0.8em;
        font-size: 1.15rem;
    }

    .center-desc {
        text-align: center;
        max-width: 700px;
        margin: 0 auto;
        font-size: 1.05rem;
        color: #d7ffff;
        line-height: 1.5;
        text-shadow: 0 0 8px #00b4d8aa;
    }

    /* ===== FEATURE GRID ===== */
    .key-features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2.3rem;
        max-width: 950px;
        margin: 2em auto 3em auto;
        box-sizing: border-box;
    }

    .feature-card {
        background: rgba(0, 45, 70, 0.25);
        border: 1px solid #00b4d8;
        border-radius: 20px;
        box-shadow: 0 0 25px #00b4d822;
        padding: 2rem 1rem;
        text-align: center;
        transition: all 0.25s ease;
        backdrop-filter: blur(8px);
    }

    .feature-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 0 35px #00eaff55;
        border: 1px solid #00f5ff;
    }

    .card-icon {
        font-size: 2.4rem;
        margin-bottom: 0.7em;
        color: #00f5ff;
        text-shadow: 0 0 12px #00f5ff88;
    }

    .card-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 1.2rem;
        color: #00f5ff;
        margin-bottom: 0.3em;
        text-shadow: 0 0 10px #00eaff88;
    }

    .card-desc {
        font-size: 0.95rem;
        color: #d9faff;
        line-height: 1.4;
    }

    /* ===== BUTTON ===== */
    .welcome-card-btn {
        display: inline-block;
        background: transparent;
        border: 2px solid #00f5ff;
        color: #00f5ff !important;
        text-shadow: 0 0 8px #00eaff;
        border-radius: 25px;
        padding: 0.9em 3em;
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        box-shadow: 0 0 20px #00b4d844;
        transition: all 0.3s ease;
    }

    .welcome-card-btn:hover {
        background: #00f5ff;
        color: #001f2f !important;
        box-shadow: 0 0 35px #00f5ff;
        transform: scale(1.05);
    }

    /* ===== SECTION HEADERS ===== */
    .feature-head {
        color: #00f5ff;
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 1.6rem;
        font-weight: 700;
        text-shadow: 0 0 12px #00f5ff;
        margin-top: 2em;
        margin-bottom: 1em;
    }
    </style>
    """, unsafe_allow_html=True)

    # === Lottie Animation (optional) ===
    try:
        with open("src/Welcome_Animation.json", "r") as f:
            lottie_json = json.load(f)
        st_lottie(lottie_json, height=110, key="welcome_lottie")
    except:
        st.write("")  # skip if not found

    # === HEADERS ===
    st.markdown("<div class='main-head'>MetalliQ LCA Platform</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-desc'>AI-Driven Sustainability for Metals & Alloys</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='center-desc'>
        <b>MetalliQ</b> empowers you to conduct comprehensive <b>Life Cycle Assessments</b> 
        with AI-driven insights, scenario simulation, and data-driven circularity analysis.  
        Explore advanced analytics, visualize material flows, and accelerate your sustainability roadmap.
        </div>
    """, unsafe_allow_html=True)

    # === FEATURE SECTION ===
    st.markdown("<div class='feature-head'>Core Capabilities</div>", unsafe_allow_html=True)

    features = [
        {"icon": "🧭", "title": "ISO 14044 Workflow", "desc": "Complete, compliant LCA process automation for metals."},
        {"icon": "🤖", "title": "AI Autofill", "desc": "Predict missing parameters & interpret sustainability metrics."},
        {"icon": "♻️", "title": "Circularity Dashboard", "desc": "Analyze circular economy metrics and eco-label readiness."},
        {"icon": "📊", "title": "3D Visual Analytics", "desc": "Interactive Sankey, radar, and time-based insights."},
        {"icon": "📄", "title": "Instant Reports", "desc": "Auto-generate ISO-standardized sustainability reports."},
        {"icon": "☁️", "title": "Cloud AI Models", "desc": "Integrate AI Studio and train LCA prediction models."}
    ]

    st.markdown("<div class='key-features-grid'>", unsafe_allow_html=True)
    for f in features:
        st.markdown(f"""
        <div class='feature-card'>
            <div class='card-icon'>{f['icon']}</div>
            <div class='card-title'>{f['title']}</div>
            <div class='card-desc'>{f['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # === LAUNCH BUTTON ===
    c1, c2, c3 = st.columns([3, 2, 3])
    with c2:
        clicked = st.button("Launch Platform 🚀", key="start_button")
        if clicked:
            st.session_state.show_login = True
    st.markdown("<div style='text-align:center;margin-top:2em;'><a class='welcome-card-btn'>Launch Platform 🚀</a></div>", unsafe_allow_html=True)
