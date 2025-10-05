def login_page():
    import streamlit as st

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Poppins:wght@400;600&display=swap');

    /* ===== GLOBAL BACKGROUND ===== */
    body, .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
        font-family: 'Poppins', sans-serif;
        color: #073B4C;
    }

    /* ===== FLEX WRAPPER ===== */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 85vh;
        width: 100%;
    }

    /* ===== LOGIN CARD ===== */
    .login-card {
        background: rgba(255, 255, 255, 0.55);
        border-radius: 18px;
        padding: 50px 45px 40px 45px;
        box-shadow: 0 6px 18px rgba(0,109,119,0.25);
        text-align: center;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0,109,119,0.2);
        max-width: 400px;
        width: 90%;
        transition: all 0.3s ease;
    }

    .login-card:hover {
        transform: scale(1.01);
        box-shadow: 0 8px 22px rgba(0,150,160,0.25);
    }

    /* ===== TITLE SECTION ===== */
    .login-logo {
        font-size: 3rem;
        color: #006D77;
        margin-bottom: 10px;
        text-shadow: 0 2px 8px rgba(0,109,119,0.25);
    }

    .login-title {
        font-family: 'Orbitron', sans-serif;
        color: #00494D;
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        margin-bottom: 0.2em;
    }

    .login-sub {
        color: #006D77;
        font-size: 1.05rem;
        margin-bottom: 1.3em;
        font-weight: 600;
    }

    /* ===== BUTTON CONTAINER ===== */
    .button-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 0.5em;
    }

    .stButton>button {
        background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
        color: #FFFFFF !important;
        border-radius: 10px;
        padding: 0.7em 1.8em;
        font-weight: 600;
        font-size: 1.05rem;
        transition: all 0.25s ease;
        border: none;
        box-shadow: 0 4px 12px rgba(0,109,119,0.25);
        width: 165px;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #007F8E 0%, #00BFA5 100%);
        transform: scale(1.05);
        box-shadow: 0 6px 18px rgba(0,150,160,0.3);
    }

    /* ===== FOOTER ===== */
    .login-footer {
        text-align: center;
        color: #00494D;
        font-size: 0.9rem;
        margin-top: 1.8em;
        opacity: 0.8;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 600px) {
        .button-row {
            flex-direction: column;
            gap: 0.8rem;
        }
        .stButton>button {
            width: 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== LAYOUT =====
    st.markdown("<div class='login-wrapper'><div class='login-card'>", unsafe_allow_html=True)

    # --- Title Section ---
    st.markdown("""
        <div class="login-logo">🌿</div>
        <div class="login-title">MetalliQ Portal</div>
        <div class="login-sub">AI-Powered Sustainability</div>
    """, unsafe_allow_html=True)

    # --- Button Row ---
    col1, col2 = st.columns(2)
    with col1:
        user = st.button("👤 User Login")
    with col2:
        admin = st.button("🛠️ Admin Login")

    # --- Footer ---
    st.markdown("<div class='login-footer'>Powered by MetalliQ AI • Enabling Circular Futures</div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ===== FUNCTIONALITY =====
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
