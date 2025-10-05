# login_page.py
import streamlit as st

def login_page():
    # Optional: ensure a centered layout for this page
    st.set_page_config(layout="centered")

    # --- Styles (keeps the teal/aqua theme and glass card look) ---
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;600&display=swap');

        /* Page background & typography */
        .stApp {
            background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
            font-family: 'Poppins', sans-serif;
        }

        /* Centering outer container - we render the card then native buttons below */
        .login-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 40px;
            margin-bottom: 40px;
        }

        /* Glass card */
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

        .login-logo { font-size: 46px; margin-bottom: 8px; color:#00A896; }
        .login-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 22px;
            margin-bottom: 6px;
            color: #003f45;
            text-shadow: 0 0 6px rgba(127,255,212,0.35);
        }
        .login-sub { color: rgba(0, 63, 69, 0.95); font-weight:600; margin-bottom:6px; }
        .login-desc { color: rgba(0,0,0,0.55); margin-bottom: 2px; }

        /* Buttons styling (applies to native Streamlit buttons) */
        div.stButton > button {
            border-radius: 10px;
            padding: 10px 22px;
            font-weight: 700;
            font-size: 15px;
            box-shadow: 0 6px 18px rgba(0,109,119,0.18);
            transition: transform .12s ease, box-shadow .12s ease;
        }
        /* Primary look */
        div.stButton > button.primary {
            background: linear-gradient(90deg,#00A896 0%, #02C39A 100%);
            color: #fff !important;
            border: none;
        }
        div.stButton > button.primary:hover { transform: translateY(-3px); box-shadow: 0 10px 26px rgba(0,150,160,0.22); }

        /* Secondary look */
        div.stButton > button.secondary {
            background: transparent;
            border: 2px solid rgba(0,168,150,0.95);
            color: #003f45 !important;
        }
        div.stButton > button.secondary:hover { background: rgba(0,168,150,0.06); }

        /* Buttons container to keep them horizontally centered and responsive */
        .button-row {
            display:flex;
            gap:16px;
            justify-content:center;
            align-items:center;
            flex-wrap:wrap;
            margin-top: 10px;
            margin-bottom: 6px;
        }

        .footer {
            font-size: 0.88rem;
            color: rgba(0,0,0,0.65);
            margin-top: 12px;
            text-align:center;
        }

        /* Mobile: stack buttons */
        @media (max-width:680px) {
            .button-row { flex-direction: column; gap:10px; width: 90%; }
            div.stButton > button { width:100% !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Card HTML (purely visual) ---
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

    # --- Native Streamlit buttons placed below the card and centered ---
    # Use columns so buttons appear centered on wide screens and stacked nicely on narrow screens
    c1, c2, c3 = st.columns([1, 0.6, 1])
    with c2:
        # The styling class names 'primary' and 'secondary' are applied by adding a wrapper <div>,
        # but streamlit doesn't allow adding class to the button directly. To keep appearance consistent
        # we rely on the global button styles above and add small inline wrappers to differentiate.
        user_clicked = st.button("👤 User Login", key="user-btn")
        st.write("")  # small spacing
        admin_clicked = st.button("🛠️ Admin Login", key="admin-btn")

    # Footer text centered under buttons
    st.markdown("<div class='footer'>This is a simulated login. No password required.<br>Powered by MetalliQ AI • Enabling Circular Futures</div>", unsafe_allow_html=True)

    # --- Button logic (same behavior as before) ---
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
