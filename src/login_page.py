import streamlit as st

def login_page():
    st.set_page_config(layout="wide")

    # Remove all Streamlit default padding and top space
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;600&display=swap');

        .stApp {
            background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
            font-family: 'Poppins', sans-serif;
            overflow: hidden;
        }

        /* Remove built-in Streamlit paddings */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin: 0 auto !important;
        }

        /* Center entire content perfectly in viewport */
        .login-wrapper {
            height: 100vh;
            width: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 6px; /* this is the gap between card and buttons — tiny */
        }

        .login-card {
            width: 400px;
            max-width: 90%;
            background: rgba(255,255,255,0.22);
            border-radius: 16px;
            padding: 28px 30px 22px 30px;
            box-shadow: 0 10px 30px rgba(0,109,119,0.25);
            border: 1px solid rgba(255,255,255,0.18);
            backdrop-filter: blur(8px);
            text-align: center;
        }

        .login-logo {
            font-size: 42px;
            margin-bottom: 10px;
            color: #B8EBD0;
        }

        .login-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: #6FFFE9;
            text-shadow: 0 0 12px rgba(111,255,233,0.8), 0 0 20px rgba(111,255,233,0.4);
            margin-bottom: 5px;
        }

        .login-sub {
            color: #043f45;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .login-desc {
            color: rgba(0,0,0,0.65);
            margin: 0;
        }

        /* Buttons container */
        .btn-container {
            width: 400px;
            max-width: 90%;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .stButton>button {
            width: 100% !important;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            font-size: 15px;
            transition: all 0.2s ease;
            padding: 0.65em 0;
        }

        /* User Button */
        .stButton>button:first-child {
            background: linear-gradient(90deg,#00A896 0%, #02C39A 100%);
            color: #fff !important;
        }
        .stButton>button:first-child:hover {
            box-shadow: 0 0 15px rgba(0,168,150,0.5);
            transform: translateY(-1px);
        }

        /* Admin Button */
        .stButton>button:last-child {
            background: linear-gradient(90deg,#007C91 0%, #006D77 100%);
            color: #E7FDFC !important;
        }
        .stButton>button:last-child:hover {
            box-shadow: 0 0 15px rgba(0,109,119,0.45);
            transform: translateY(-1px);
        }

        .footer {
            text-align: center;
            font-size: 0.88rem;
            color: rgba(255,255,255,0.8);
            margin-top: 8px;
        }

        </style>
    """, unsafe_allow_html=True)

    # Actual centered layout
    st.markdown("""
        <div class="login-wrapper">
            <div class="login-card">
                <div class="login-logo">🏛️</div>
                <div class="login-title">MetalliQ Portal</div>
                <div class="login-sub">AI-Powered Sustainability</div>
                <div class="login-desc">Sign in to the official platform</div>
            </div>
    """, unsafe_allow_html=True)

    # Buttons - tightly grouped below card
    col1, col2, col3 = st.columns([2.5, 3, 2.5])
    with col2:
        user_clicked = st.button("👤 User Login")
        admin_clicked = st.button("🛠️ Admin Login")

    st.markdown("""
            <div class="footer">
                This is a simulated login. No password required.<br>
                Powered by MetalliQ AI • Enabling Circular Futures
            </div>
        </div>
    """, unsafe_allow_html=True)

    if user_clicked:
        st.session_state.logged_in = True
        st.session_state.role = "User"
        st.session_state.page = "Dashboard"
        st.rerun()

    if admin_clicked:
        st.session_state.logged_in = True
        st.session_state.role = "Admin"
        st.session_state.page = "Dashboard"
        st.rerun()
