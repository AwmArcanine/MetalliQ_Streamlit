import streamlit as st

def login_page():
    # --- Handle URL-based login using st.query_params ---
    params = st.query_params
    if "login" in params:
        choice = params.get("login", "").lower()
        if choice == "user":
            st.session_state.logged_in = True
            st.session_state.role = "Investigator"
            st.session_state.name = "John Doe"
            st.session_state['page'] = 'Dashboard'
            st.query_params.clear()
            st.rerun()
        elif choice == "admin":
            st.session_state.logged_in = True
            st.session_state.role = "Admin"
            st.session_state.name = "Sarah Singh"
            st.session_state['page'] = 'Dashboard'
            st.query_params.clear()
            st.rerun()

    # --- Page style ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
        font-family: 'Poppins', sans-serif;
    }

    .login-wrapper {
        height: 90vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .login-card {
        width: 400px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 18px;
        box-shadow: 0 10px 28px rgba(0, 109, 119, 0.25);
        padding: 45px 35px;
        text-align: center;
        border: 1px solid rgba(0, 109, 119, 0.2);
        backdrop-filter: blur(8px);
    }

    .login-icon {
        font-size: 3rem;
        color: #006D77;
        margin-bottom: 12px;
    }

    .login-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem;
        color: #00494D;
        margin-bottom: 6px;
        text-shadow: 0 0 10px rgba(100, 255, 230, 0.45);
    }

    .login-subtitle {
        font-size: 1rem;
        font-weight: 600;
        opacity: 0.9;
        margin-bottom: 12px;
    }

    .login-desc {
        font-size: 0.95rem;
        opacity: 0.9;
        margin-bottom: 18px;
    }

    .btn {
        display: inline-block;
        width: 100%;
        padding: 12px 0;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 10px;
        text-decoration: none;
        margin-top: 10px;
        transition: all 0.25s ease;
        box-sizing: border-box;
    }

    .btn-primary {
        background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
        color: #fff !important;
        box-shadow: 0 6px 18px rgba(0, 109, 119, 0.25);
        border: none;
    }

    .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 26px rgba(0, 150, 160, 0.3);
    }

    .btn-secondary {
        background: transparent;
        border: 2px solid #006D77;
        color: #00494D !important;
    }

    .btn-secondary:hover {
        background: rgba(0, 109, 119, 0.1);
    }

    .login-footer {
        font-size: 0.85rem;
        opacity: 0.8;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- HTML Layout ---
    html_content = """
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-icon">🏛️</div>
            <div class="login-title">MetalliQ Portal</div>
            <div class="login-subtitle">AI-Powered Sustainability</div>
            <div class="login-desc">Sign in to the official platform</div>
            <a href="?login=user" class="btn btn-primary">👤 Sign In as User (John Doe)</a>
            <a href="?login=admin" class="btn btn-secondary">🛠️ Sign In as Admin (Sarah Singh)</a>
            <div class="login-footer">
                This is a simulated login. No password required.<br>
                Powered by MetalliQ AI • Enabling Circular Futures
            </div>
        </div>
    </div>
    """

    st.components.v1.html(html_content, height=600)
