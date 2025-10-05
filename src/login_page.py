import streamlit as st

def login_page():
    st.set_page_config(layout="centered")

    # --- Styles ---
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
            padding: 36px 30px;
            box-shadow: 0 10px 30px rgba(0,109,119,0.22);
            border: 1px solid rgba(255,255,255,0.18);
            backdrop-filter: blur(8px);
            text-align: center;
            color: #06343a;
            margin-bottom: 18px;
        }

        .login-logo {
            font-size: 46px;
            margin-bottom: 8px;
            color: #00A896;
        }

        .login-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: #6FFFE9;  /* neon cyan */
            text-shadow: 0 0 10px rgba(111, 255, 233, 0.8), 0 0 20px rgba(111, 255, 233, 0.4);
            margin-bottom: 6px;
        }

        .login-sub {
            color: rgba(0, 63, 69, 0.95);
            font-weight:600;
            margin-bottom:6px;
        }

        .login-desc {
            color: rgba(0,0,0,0.55);
            margin-bottom: 2px;
        }

        /* Button container and styling */
        .stButton>button {
            width: 420px !important;
            max-width: 92% !important;
            border-radius: 10px;
            padding: 12px 0px;
            font-weight: 700;
            font-size: 15px;
            box-shadow: 0 6px 18px rgba(0,109,119,0.18);
            transition: transform .12s ease, box-shadow .12s ease;
        }

        .stButton>button:first-child {
            background: linear-gradient(90deg,#00A896 0%, #02C39A 100%);
            color: #fff !important;
            border: none;
        }

        .stButton>button:first-child:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 26px rgba(0,150,160,0.25);
        }

        .stButton>button:last-child {
            background: transparent;
            border: 2px solid #00A896;
            color: #003f45 !important;
        }

        .stButton>button:last-child:hover {
            background: rgba(0,168,150,0.08);
        }

        .footer {
            font-size: 0.88rem;
            color: rgba(0,0,0,0.65);
            margin-top: 14px;
            text-align:center;
        }

        @media (max-width:680px) {
            .stButton>button {
                width: 90% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- HTML card ---
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

    # --- Streamlit buttons ---
    user_clicked = st.button("👤 User Login")
    admin_clicked = st.button("🛠️ Admin Login")

    # --- Footer ---
    st.markdown(
        "<div class='footer'>This is a simulated login. No password required.<br>Powered by MetalliQ AI • Enabling Circular Futures</div>",
        unsafe_allow_html=True,
    )

    # --- Button Logic ---
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
