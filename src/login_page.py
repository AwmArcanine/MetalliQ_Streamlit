import streamlit as st

def login_page():
    # ====== PAGE STYLE ======
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
        font-family: 'Poppins', sans-serif;
    }

    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 90vh;
        text-align: center;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.55);
        border-radius: 16px;
        padding: 50px 45px 40px 45px;
        box-shadow: 0 8px 28px rgba(0, 109, 119, 0.25);
        backdrop-filter: blur(8px);
        max-width: 400px;
        width: 90%;
        border: 1px solid rgba(0, 109, 119, 0.25);
    }

    .login-icon {
        font-size: 3rem;
        color: #006D77;
        margin-bottom: 8px;
    }

    .login-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #00494D;
        margin-bottom: 6px;
    }

    .login-subtitle {
        font-size: 1rem;
        color: #00494D;
        font-weight: 600;
        margin-bottom: 20px;
    }

    .login-desc {
        font-size: 0.95rem;
        color: #073B4C;
        margin-bottom: 24px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        font-size: 1.05rem;
        padding: 0.8em 0;
        margin-top: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    /* User button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
        color: #ffffff !important;
        box-shadow: 0 3px 10px rgba(0, 109, 119, 0.25);
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #007F8E 0%, #00BFA5 100%);
        box-shadow: 0 5px 14px rgba(0, 150, 160, 0.25);
    }

    /* Admin button */
    .stButton > button[kind="secondary"] {
        background: transparent;
        color: #00494D !important;
        border: 2px solid #006D77 !important;
        box-shadow: none;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(0, 109, 119, 0.1);
    }

    .login-footer {
        font-size: 0.9rem;
        color: #00494D;
        opacity: 0.8;
        margin-top: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # ====== LAYOUT ======
    st.markdown("<div class='login-container'><div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<div class='login-icon'>🏛️</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-title'>MetalliQ Portal</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-subtitle'>AI-Powered Sustainability</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-desc'>Sign in to the official platform</div>", unsafe_allow_html=True)

    # ====== BUTTONS ======
    user_login = st.button("👤 Sign In as User (John Doe)", key="user-btn", type="primary")
    admin_login = st.button("🛠️ Sign In as Admin (Sarah Singh)", key="admin-btn", type="secondary")

    # ====== FOOTER ======
    st.markdown("<div class='login-footer'>This is a simulated login. No password required.<br>Powered by MetalliQ AI • Enabling Circular Futures</div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ====== LOGIC ======
    if user_login:
        st.session_state.logged_in = True
        st.session_state.role = "Investigator"
        st.session_state.name = "John Doe"
        st.session_state['page'] = 'Dashboard'
        st.rerun()
    if admin_login:
        st.session_state.logged_in = True
        st.session_state.role = "Admin"
        st.session_state.name = "Sarah Singh"
        st.session_state['page'] = 'Dashboard'
        st.rerun()
