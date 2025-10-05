import streamlit as st

def login_page():
    st.set_page_config(layout="centered")

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;600&display=swap');

        .stApp {
            background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
            font-family: 'Poppins', sans-serif;
            overflow: hidden; /* No scroll */
        }

        /* Wrapper centers everything horizontally */
        .login-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            height: 100vh;
            padding-top: 7vh; /* Top offset only */
        }

        /* Card styling */
        .centered-login-card {
            width: 420px;
            max-width: 90%;
            background: rgba(255,255,255,0.22);
            border-radius: 16px;
            padding: 28px 30px 24px 30px;
            box-shadow: 0 10px 30px rgba(0,109,119,0.25);
            border: 1px solid rgba(255,255,255,0.18);
            backdrop-filter: blur(8px);
            text-align: center;
            color: #06343a;
            margin-bottom: 15px; /* Small gap before buttons */
        }

        .login-logo {
            font-size: 42px;
            margin-bottom: 8px;
            color: #00A896;
        }

        .login-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: #6FFFE9;
            text-shadow: 0 0 10px rgba(111,255,233,0.8), 0 0 20px rgba(111,255,233,0.4);
            margin-bottom: 4px;
        }

        .login-sub {
            color: #043f45;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .login-desc {
            color: rgba(0,0,0,0.6);
            margin: 0;
        }

        /* Buttons container directly attached to card */
        .button-container {
            width: 420px;
            max-width: 90%;
            margin-top: 0; /* No gap */
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px; /* Just a small space between buttons */
        }

        .stButton > button {
            width: 100% !important;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            font-size: 15px;
            transition: all 0.2s ease;
            padding: 0.6em 0;
        }

        /* User button */
        .button-container .stButton:nth-child(1) button {
            background: linear-gradient(90deg,#00A896 0%, #02C39A 100%);
            color: #fff !important;
        }

        .button-container .stButton:nth-child(1) button:hover {
            box-shadow: 0 0 20px rgba(0,168,150,0.45);
            transform: translateY(-1px);
        }

        /* Admin button */
        .button-container .stButton:nth-child(2) button {
            background: linear-gradient(90deg,#007C91 0%, #006D77 100%);
            color: #E7FDFC !important;
        }

        .button-container .stButton:nth-child(2) button:hover {
            box-shadow: 0 0 20px rgba(0,109,119,0.45);
            transform: translateY(-1px);
        }

        .footer {
            font-size: 0.88rem;
            color: rgba(255,255,255,0.8);
            margin-top: 18px;
            text-align: center;
        }

        @media (max-width:680px) {
            .centered-login-card, .button-container { width: 90%; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Card
    st.markdown("""
        <div class="login-wrapper">
            <div class="centered-login-card">
                <div class="login-logo">🏛️</div>
                <div class="login-title">MetalliQ Portal</div>
                <div class="login-sub">AI-Powered Sustainability</div>
                <div class="login-desc">Sign in to the official platform</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Buttons – directly under the card, aligned center
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2.5, 3, 2.5])
    with col2:
        user_clicked = st.button("👤 User Login")
        admin_clicked = st.button("🛠️ Admin Login")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class='footer'>
            This is a simulated login. No password required.<br>
            Powered by MetalliQ AI • Enabling Circular Futures
        </div>
    """, unsafe_allow_html=True)

    if user_clicked:
        st.session_state.logged_in = True
        st.session_state.role = "Investigator"
        st.session_state.name = "John Doe"
        st.session_state['page'] = 'Dashboard'
        st.experimental_rerun()

    if admin_clicked:
        st.session_state.logged_in = True
        st.session_state.role = "Admin"
        st.session_state.name = "Sarah Singh"
        st.session_state['page'] = 'Dashboard'
        st.experimental_rerun()
