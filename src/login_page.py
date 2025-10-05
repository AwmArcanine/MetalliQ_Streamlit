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
        }

        .login-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 90vh;
        }

        .centered-login-card {
            width: 420px;
            max-width: 92%;
            background: rgba(255,255,255,0.22);
            border-radius: 16px;
            padding: 30px 30px; /* reduced padding slightly */
            box-shadow: 0 10px 30px rgba(0,109,119,0.22);
            border: 1px solid rgba(255,255,255,0.18);
            backdrop-filter: blur(8px);
            text-align: center;
            color: #06343a;
            margin-bottom: 12px; /* reduced from 20px */
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
            color: #6FFFE9; /* neon cyan */
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
            margin-bottom: 2px;
        }

        /* Button styling */
        .stButton>button {
            display: block;
            width: 420px !important;  /* same width as card */
            max-width: 92%;
            margin: 6px auto;
            border-radius: 10px;
            padding: 10px 0px;
            font-weight: 700;
            font-size: 15px;
            transition: all .2s ease;
            border: none;
        }

        .stButton>button:first-child {
            background: linear-gradient(90deg,#00A896 0%, #02C39A 100%);
            color: #fff !important;
            box-shadow: 0 0 14px rgba(0,168,150,0.25);
        }

        .stButton>button:first-child:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 22px rgba(0,168,150,0.4);
        }

        .stButton>button:last-child {
            background: linear-gradient(90deg,#007C91 0%, #006D77 100%);
            color: #e7fdfc !important;
            box-shadow: 0 0 10px rgba(0,109,119,0.3);
        }

        .stButton>button:last-child:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 22px rgba(0,109,119,0.45);
        }

        .footer {
            font-size: 0.88rem;
            color: rgba(255,255,255,0.75);
            margin-top: 10px;
            text-align:center;
        }

        @media (max-width:680px) {
            .centered-login-card { width: 90%; }
            .stButton>button { width: 90% !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="login-wrapper">
            <div class="centered-login-card">
                <div class="login-logo">🏛️</div>
                <div class="login-title">MetalliQ Portal</div>
                <div class="login-sub">AI-Powered Sustainability</div>
                <div class="login-desc">Sign in to the official platform</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Buttons perfectly aligned under card
    c1, c2, c3 = st.columns([2.5, 3, 2.5])
    with c2:
        user_clicked = st.button("👤 User Login")
        admin_clicked = st.button("🛠️ Admin Login")

    st.markdown(
        "<div class='footer'>This is a simulated login. No password required.<br>Powered by MetalliQ AI • Enabling Circular Futures</div>",
        unsafe_allow_html=True,
    )

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
