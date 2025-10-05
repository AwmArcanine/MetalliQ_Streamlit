import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="MetalliQ Portal", page_icon="🏛️", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .main {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        .login-card {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 2rem 4rem;
            text-align: center;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            width: 400px;
            margin-bottom: 8px;
        }

        .login-title {
            font-size: 2rem;
            font-weight: 800;
            color: #00fff2;
            text-shadow: 0 0 8px #00fff2, 0 0 20px #00fff2;
            margin-bottom: 0.5rem;
        }

        .login-subtitle {
            font-size: 0.9rem;
            color: #0a0a0a;
            opacity: 0.8;
        }

        .login-buttons {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }

        .stButton > button {
            background: linear-gradient(90deg, #0bbfad, #00897b);
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 10px;
            width: 400px !important;
            height: 45px;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            background: linear-gradient(90deg, #00c6b3, #00a99d);
        }

        .footer {
            position: fixed;
            bottom: 12px;
            text-align: center;
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.75);
        }
    </style>
""", unsafe_allow_html=True)

# --- PAGE CONTENT ---
st.markdown('<div class="main">', unsafe_allow_html=True)

st.markdown("""
    <div class="login-card">
        <div style="font-size: 3rem;">🏛️</div>
        <div class="login-title">MetalliQ Portal</div>
        <div class="login-subtitle">AI-Powered Sustainability</div>
        <p style="color: #1a1a1a; opacity: 0.7;">Sign in to the official platform</p>
    </div>
""", unsafe_allow_html=True)

# --- LOGIN BUTTONS ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("👤 User Login"):
        st.session_state["role"] = "user"
        st.switch_page("src/dashboard.py")
        st.rerun()

    if st.button("🛠️ Admin Login"):
        st.session_state["role"] = "admin"
        st.switch_page("src/admin_dashboard.py")
        st.rerun()

st.markdown("""
    <div class="footer">
        This is a simulated login. No password required.<br>
        Powered by MetalliQ AI • Enabling Circular Futures
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
