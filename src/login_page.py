import streamlit as st

def login_page():
    # --- Use new Streamlit API for query params ---
    query_params = st.query_params

    # --- Apply CSS (futuristic sustainability theme) ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 40%, #83C5BE 100%) !important;
        font-family: 'Poppins', sans-serif;
    }

    .login-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 90vh;
        text-align: center;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.25);
        border-radius: 18px;
        padding: 45px 35px;
        width: 380px;
        box-shadow: 0 8px 30px rgba(0, 109, 119, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        color: #00494D;
        margin-bottom: 25px;
    }

    .login-icon {
        font-size: 3rem;
        color: #00A896;
        margin-bottom: 15px;
    }

    .login-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem;
        margin-bottom: 6px;
        text-shadow: 0 0 8px rgba(0, 255, 255, 0.4);
    }

    .login-subtitle {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 12px;
        color: rgba(0,0,0,0.7);
    }

    .login-desc {
        font-size: 0.95rem;
        opacity: 0.8;
    }

    .btn-container {
        display: flex;
        gap: 20px;
        justify-content: center;
        flex-wrap: wrap;
    }

    .btn {
        display: inline-block;
        padding: 12px 22px;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 10px;
        text-decoration: none;
        transition: all 0.25s ease;
        box-sizing: border-box;
    }

    .btn-primary {
        background: linear-gradient(90deg, #00A896 0%, #02C39A 100%);
        color: white !important;
        border: none;
        box-shadow: 0 6px 18px rgba(0, 109, 119, 0.3);
    }

    .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 26px rgba(0, 150, 160, 0.4);
    }

    .btn-secondary {
        background: transparent;
        border: 2px solid #00A896;
        color: #00494D !important;
    }

    .btn-secondary:hover {
        background: rgba(0, 109, 119, 0.1);
    }

    .login-footer {
        font-size: 0.85rem;
        opacity: 0.8;
        margin-top: 25px;
        color: #00494D;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- HTML Layout ---
    html_content = """
    <div class="login-container">
        <div class="login-card">
            <div class="login-icon">🏛️</div>
            <div class="login-title">MetalliQ Portal</div>
            <div class="login-subtitle">AI-Powered Sustainability</div>
            <div class="login-desc">Sign in to the official platform</div>
        </div>
        <div class="btn-container">
            <a href="?login=user" class="btn btn-primary">👤 Sign In as User (John Doe)</a>
            <a href="?login=admin" class="btn btn-secondary">🛠️ Sign In as Admin (Sarah Singh)</a>
        </div>
        <div class="login-footer">
            This is a simulated login. No password required.<br>
            Powered by MetalliQ AI • Enabling Circular Futures
        </div>
    </div>
    """

    st.components.v1.html(html_content, height=700, scrolling=False)
