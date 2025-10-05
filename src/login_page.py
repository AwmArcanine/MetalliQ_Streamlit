import streamlit as st

def login_page():
    st.set_page_config(layout="wide")

    # --- CSS: Futuristic theme + perfect layout alignment ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;500;600&display=swap');

    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #83C5BE 100%) !important;
        font-family: 'Poppins', sans-serif;
        overflow: hidden !important;
    }

    /* Center entire layout */
    .main-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        text-align: center;
    }

    /* Card */
    .login-card {
        width: 90%;
        max-width: 400px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 28px 20px;
        box-shadow: 0 8px 25px rgba(0, 109, 119, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }

    .login-logo {
        font-size: 44px;
        margin-bottom: 10px;
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

    /* Buttons container */
    .button-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        margin-top: 8px;
    }

    /* Buttons */
    .stButton>button {
        width: 100% !important;
        max-width: 400px;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 15px;
        padding: 0.75em 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    /* User Login Button */
    .stButton>button:first-child {
        background: linear-gradient(90deg, #00A896 0%, #02C39A 100%);
        color: white !important;
        box-shadow: 0 0 10px rgba(0,168,150,0.6);
    }

    .stButton>button:first-child:hover {
        transform: scale(1.03);
        box-shadow: 0 0 20px rgba(0,168,150,0.9);
    }

    /* Admin Login Button */
    .stButton>button:last-child {
        background: linear-gradient(90deg, #007C91 0%, #006D77 100%);
        color: #E7FDFC !important;
        box-shadow: 0 0 10px rgba(0,109,119,0.5);
    }

    .stButton>button:last-child:hover {
        transform: scale(1.03);
        box-shadow: 0 0 20px rgba(0,109,119,0.8);
    }

    /* Footer */
    .footer {
        margin-top: 12px;
        font-size: 0.9rem;
        color: rgba(255,255,255,0.9);
        text-align: center;
    }

    @media (max-width: 600px) {
        .login-card, .stButton>button {
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
        <div class="button-container">
    """, unsafe_allow_html=True)

    # Buttons (functional + responsive)
    user = st.button("👤 User Login")
    admin = st.button("🛠️ Admin Login")

    st.markdown("""
        </div>
        <div class="footer">
            This is a simulated login. No password required.<br>
            Powered by MetalliQ AI • Enabling Circular Futures
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Logic
    if user:
        st.session_state.page = "User Dashboard"
        st.rerun()
    if admin:
        st.session_state.page = "Admin Dashboard"
        st.rerun()
