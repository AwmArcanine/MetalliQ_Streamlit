import streamlit as st

def login_page():
    st.set_page_config(layout="wide")

    # ===== CSS for strict layout =====
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;600&display=swap');

    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #83C5BE 100%) !important;
        font-family: 'Poppins', sans-serif;
        overflow: hidden !important;
    }

    /* ✅ Wrapper: Perfect center */
    .main-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        gap: 14px;
    }

    /* ✅ Card Styling */
    .login-card {
        width: 380px;
        background: rgba(255, 255, 255, 0.18);
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 109, 119, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
    }

    /* ✅ Title */
    .login-logo {
        font-size: 42px;
        margin-bottom: 8px;
        color: #D4BEE4;
    }

    .login-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #7CF4E3;
        text-shadow: 0 0 14px rgba(124, 244, 227, 0.9);
        margin-bottom: 5px;
    }

    .login-sub {
        font-weight: 600;
        color: #044B4D;
        margin-bottom: 4px;
    }

    .login-desc {
        color: rgba(0, 0, 0, 0.65);
        margin: 0;
    }

    /* ✅ Buttons Section */
    .button-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        width: 380px;
    }

    .stButton>button {
        width: 100% !important;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        font-size: 15px;
        transition: all 0.25s ease;
        padding: 0.7em 0;
        cursor: pointer;
    }

    /* ✅ User button */
    .stButton>button:first-child {
        background: linear-gradient(90deg, #00A896 0%, #02C39A 100%);
        color: #fff !important;
        box-shadow: 0 0 12px rgba(0,168,150,0.6);
    }
    .stButton>button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 18px rgba(0,168,150,0.8);
    }

    /* ✅ Admin button */
    .stButton>button:last-child {
        background: linear-gradient(90deg, #007C91 0%, #006D77 100%);
        color: #E7FDFC !important;
        box-shadow: 0 0 12px rgba(0,109,119,0.5);
    }
    .stButton>button:last-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 18px rgba(0,109,119,0.8);
    }

    /* ✅ Footer */
    .footer {
        text-align: center;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.85);
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== Layout =====
    st.markdown("""
    <div class="main-container">
        <div class="login-card">
            <div class="login-logo">🏛️</div>
            <div class="login-title">MetalliQ Portal</div>
            <div class="login-sub">AI-Powered Sustainability</div>
            <div class="login-desc">Sign in to the official platform</div>
        </div>

        <div class="button-section">
    """, unsafe_allow_html=True)

    # Buttons (strictly centered below the card)
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
