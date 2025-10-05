# login_page.py
import streamlit as st
from urllib.parse import urlencode

def login_page():
    """
    Login page implemented as a self-contained HTML card.
    Buttons are HTML links (href="?login=user" / "?login=admin").
    We detect the query param and set session_state accordingly.
    This avoids Streamlit DOM-wrapping issues and keeps the card visually intact.
    """

    # 1) If the URL contains ?login=user or ?login=admin -> handle and redirect
    params = st.experimental_set_query_params()
    if "login" in params:
        choice = params.get("login", [""])[0].lower()
        if choice == "user":
            st.session_state.logged_in = True
            st.session_state.role = "Investigator"
            st.session_state.name = "John Doe"
            st.session_state["page"] = "Dashboard"
            # clear query params and rerun to avoid repeated triggers
            st.experimental_set_query_params()
            st.rerun()
        elif choice == "admin":
            st.session_state.logged_in = True
            st.session_state.role = "Admin"
            st.session_state.name = "Sarah Singh"
            st.session_state["page"] = "Dashboard"
            st.experimental_set_query_params()
            st.rerun()

    # 2) Styles + HTML card (matches your theme, centered and stable)
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;600&display=swap');

        /* App background kept consistent with theme */
        .stApp {
            background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
            font-family: 'Poppins', sans-serif;
            color: #073B4C;
        }

        /* Centering wrapper: uses viewport height to center card */
        .login-wrap {
            display:flex;
            align-items:center;
            justify-content:center;
            height:calc(100vh - 70px); /* leave small room for top bar */
            width:100%;
            padding: 10px;
            box-sizing: border-box;
        }

        /* Card */
        .login-card {
            width: 420px;
            max-width: 94%;
            background: rgba(255,255,255,0.60);
            border-radius: 16px;
            padding: 36px 30px;
            box-shadow: 0 10px 30px rgba(0,109,119,0.24);
            border: 1px solid rgba(0,109,119,0.14);
            text-align: center;
            backdrop-filter: blur(6px);
        }

        .login-icon {
            font-size: 48px;
            margin-bottom: 6px;
            color: #006D77;
        }

        .login-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 22px;
            color: #00494D;
            margin-bottom: 6px;
            font-weight: 700;
        }

        .login-sub {
            font-size: 14px;
            color: #00494D;
            margin-bottom: 14px;
            font-weight: 600;
            opacity: 0.92;
        }

        .login-desc {
            font-size: 14px;
            color: #073B4C;
            margin-bottom: 18px;
            opacity: 0.9;
        }

        /* Buttons are styled anchor tags so they visually behave like buttons */
        .btn {
            display: inline-block;
            width: 100%;
            padding: 12px 16px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 700;
            font-size: 15px;
            margin: 8px 0;
            box-sizing: border-box;
            transition: all 0.18s ease;
        }

        .btn-primary {
            background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
            color: #fff;
            border: none;
            box-shadow: 0 6px 18px rgba(0,109,119,0.18);
        }
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 26px rgba(0,150,160,0.20);
        }

        .btn-secondary {
            background: rgba(255,255,255,0.06);
            color: #00494D;
            border: 2px solid rgba(0,109,119,0.16);
        }
        .btn-secondary:hover {
            background: rgba(0,109,119,0.06);
        }

        .login-footer {
            margin-top: 14px;
            font-size: 12px;
            color: #00494D;
            opacity: 0.85;
        }

        /* Small screens */
        @media (max-width: 460px){
            .login-card { padding: 26px 18px; }
            .login-title { font-size: 20px; }
        }
        </style>

        <div class="login-wrap">
            <div class="login-card">
                <div class="login-icon">🏛️</div>
                <div class="login-title">MetalliQ Portal</div>
                <div class="login-sub">AI-Powered Sustainability</div>
                <div class="login-desc">Sign in to the official platform</div>

                <!-- Buttons: using query params so Streamlit can react on reload -->
                <a href="?login=user" class="btn btn-primary">👤 Sign In as User (John Doe)</a>
                <a href="?login=admin"  class="btn btn-secondary">🛠️ Sign In as Admin (Sarah Singh)</a>

                <div class="login-footer">
                    This is a simulated login. No password needed.<br>
                    Powered by MetalliQ AI • Enabling Circular Futures
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
