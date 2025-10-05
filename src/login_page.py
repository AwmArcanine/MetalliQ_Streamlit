import streamlit as st

def login_page():
    st.set_page_config(layout="wide")

    # --- CSS Styling ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;500;600&display=swap');

    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #83C5BE 100%) !important;
        font-family: 'Poppins', sans-serif;
        overflow: hidden;
    }

    .main-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 50vh;
        text-align: center;
    }

    .login-card {
        width: 90%;
        max-width: 400px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 28px 20px;
        box-shadow: 0 8px 25px rgba(0, 109, 119, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        margin-bottom: -8px; /* small gap */
    }

    .login-logo {
        font-size: 44px;
        margin-bottom: 8px;
        color: #D4BEE4;
    }

    .login-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.9rem;
        font-weight: 600;
        color: #7CF4E3;
        text-shadow: 0 0 15px rgba(124, 244, 227, 0.85);
        margin-bottom: 6px;
    }

    .login-sub {
        font-weight: 600;
        color: #022C2D;
        margin-bottom: 4px;
    }

    .login-desc {
        color: rgba(0, 0, 0, 0.7);
        margin-bottom: 0;
    }

    .button-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        width: 100%;
        max-width: 400px;
    }

    .stButton>button {
        width: 100% !important;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 15px;
        padding: 0.75em 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .user-btn button {
        background: linear-gradient(90deg, #00A896 0%, #02C39A 100%);
        color: white !important;
        box-shadow: 0 0 10px rgba(0,168,150,0.6);
    }

    .user-btn button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 20px rgba(0,168,150,0.9);
    }

    .admin-btn button {
        background: linear-gradient(90deg, #007C91 0%, #006D77 100%);
        color: #E7FDFC !important;
        box-shadow: 0 0 10px rgba(0,109,119,0.5);
    }

    .admin-btn button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 20px rgba(0,109,119,0.8);
    }

    .footer {
        margin-top: 14px;
        font-size: 0.9rem;
        color: rgba(255,255,255,0.9);
        text-align: center;
    }

    @media (max-width: 600px) {
        .login-card, .button-container {
            max-width: 320px;
        }
        .login-title {
            font-size: 1.6rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Layout ---
    st.markdown("""
    <div class="main-container">
        <div class="login-card">
            <div class="login-logo">🏛️</div>
            <div class="login-title">MetalliQ Portal</div>
            <div class="login-sub">AI-Powered Sustainability</div>
            <div class="login-desc">Sign in to the official platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Buttons ---
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user = st.button("👤 User Login", key="user_btn", use_container_width=True)
        admin = st.button("🛠️ Admin Login", key="admin_btn", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
        <div class="footer">
            This is a simulated login. No password required.<br>
            Powered by MetalliQ AI • Enabling Circular Futures
        </div>
    """, unsafe_allow_html=True)

    # --- Navigation (OLD WORKING METHOD) ---
    if user:
        st.query_params["page"] = "user_dashboard"
        st.rerun()

    if admin:
        st.query_params["page"] = "admin_dashboard"
        st.rerun()
