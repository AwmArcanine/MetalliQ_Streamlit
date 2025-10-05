def login_page():
    import streamlit as st

    # === GLOBAL LOGIN PAGE STYLE ===
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Poppins:wght@400;600&display=swap');

    /* ===== BACKGROUND ===== */
    body, .stApp {
        background: linear-gradient(135deg, #001a2e 0%, #003b46 45%, #00b4d8 100%) !important;
        background-attachment: fixed;
        color: #d9faff !important;
        font-family: 'Poppins', sans-serif;
    }

    /* ===== CENTERED CARD ===== */
    .centered-login-card {
        max-width: 420px;
        margin: 110px auto 0 auto;
        padding: 44px 44px 32px 44px;
        border-radius: 25px;
        background: rgba(0, 45, 70, 0.25);
        box-shadow: 0 0 25px #00b4d833, inset 0 0 15px #00f5ff22;
        border: 1px solid #00b4d8;
        backdrop-filter: blur(10px);
        text-align: center;
        position: relative;
        transition: all 0.3s ease;
    }
    .centered-login-card:hover {
        box-shadow: 0 0 35px #00eaff55, inset 0 0 25px #00f5ff33;
        transform: scale(1.01);
    }

    /* ===== LOGO ===== */
    .login-logo {
        font-size: 3rem;
        margin-bottom: 10px;
        color: #00f5ff;
        text-shadow: 0 0 15px #00eaff, 0 0 25px #00b4d8;
    }

    /* ===== TITLE & SUB ===== */
    .login-title {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg,#00f5ff,#00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 10px #00eaff;
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        margin-bottom: 0.3em;
    }
    .login-sub {
        color: #9ef8ff;
        font-size: 1.1rem;
        text-shadow: 0 0 10px #00b4d8;
        font-weight: 600;
        margin-bottom: 0.6em;
    }
    .login-desc {
        color: #d7ffff;
        font-size: 1rem;
        margin-bottom: 1.2rem;
        opacity: 0.85;
    }

    /* ===== BUTTONS ===== */
    .stButton>button, .styled-login-btn {
        background: transparent;
        border: 2px solid #00f5ff;
        color: #00f5ff !important;
        text-shadow: 0 0 8px #00eaff;
        border-radius: 20px;
        padding: 0.7em 2.2em;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        transition: all 0.3s ease;
        box-shadow: 0 0 18px #00b4d822;
        margin: 0.4em;
    }
    .stButton>button:hover, .styled-login-btn:hover {
        background: #00f5ff;
        color: #001f2f !important;
        box-shadow: 0 0 35px #00f5ff;
        transform: scale(1.07);
    }

    /* ===== FOOTER GLOW ===== */
    .login-footer {
        color: #7aeaff;
        font-size: 0.9rem;
        margin-top: 1.2em;
        text-shadow: 0 0 8px #00f5ff88;
    }
    </style>
    """, unsafe_allow_html=True)

    # === CENTERED CARD ===
    st.markdown("""
        <div class="centered-login-card">
            <div class="login-logo">⚙️</div>
            <div class="login-title">MetalliQ Portal</div>
            <div class="login-sub">AI-Powered Sustainability</div>
            <div class="login-desc">Choose your role to sign in</div>
        </div>
    """, unsafe_allow_html=True)

    # === BUTTON ROW ===
    col1, col2 = st.columns(2)
    with col1:
        user = st.button("👤 Sign In as User", key="user-btn")
    with col2:
        admin = st.button("🛠️ Sign In as Admin", key="admin-btn")

    # === FOOTER TEXT ===
    st.markdown("<div class='login-footer'>Powered by MetalliQ AI • Crafted for Circular Future</div>", unsafe_allow_html=True)

    # === BUTTON LOGIC ===
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
