import streamlit as st

def login_page():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Poppins:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(135deg, #00494D 0%, #006D77 45%, #83C5BE 100%) !important;
        font-family: 'Poppins', sans-serif;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.55);
        border-radius: 18px;
        padding: 50px 45px 40px 45px;
        box-shadow: 0 6px 18px rgba(0,109,119,0.25);
        text-align: center;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0,109,119,0.2);
        max-width: 400px;
        width: 90%;
        transition: all 0.3s ease;
        margin: auto;
    }

    .login-card:hover {
        transform: scale(1.01);
        box-shadow: 0 8px 22px rgba(0,150,160,0.25);
    }

    .login-title {
        font-family: 'Orbitron', sans-serif;
        color: #00494D;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.4em;
    }

    .login-sub {
        color: #006D77;
        font-size: 1.05rem;
        margin-bottom: 1.3em;
        font-weight: 600;
    }

    .stButton>button {
        background: linear-gradient(90deg, #006D77 0%, #00A896 100%);
        color: #FFFFFF !important;
        border-radius: 10px;
        padding: 0.7em 1.8em;
        font-weight: 600;
        font-size: 1.05rem;
        transition: all 0.25s ease;
        border: none;
        box-shadow: 0 4px 12px rgba(0,109,119,0.25);
        width: 165px;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #007F8E 0%, #00BFA5 100%);
        transform: scale(1.05);
        box-shadow: 0 6px 18px rgba(0,150,160,0.3);
    }

    .button-row {
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }

    .footer {
        text-align: center;
        color: #00494D;
        font-size: 0.9rem;
        margin-top: 1.5em;
        opacity: 0.8;
    }
    </style>
    """, unsafe_allow_html=True)

    # Centering container
    st.markdown("<div style='height:75vh; display:flex; justify-content:center; align-items:center;'>", unsafe_allow_html=True)

    # Login card
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<div class='login-title'>MetalliQ Portal</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-sub'>AI-Powered Sustainability</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        user = st.button("👤 User Login")
    with col2:
        admin = st.button("🛠️ Admin Login")

    st.markdown("<div class='footer'>Powered by MetalliQ AI • Enabling Circular Futures</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Login logic
    if user:
        st.session_state.logged_in = True
        st.session_state.role = "Investigator"
        st.session_state.name = "John Doe"
        st.session_state['page'] = 'Dashboard'
        st.rerun()
    if admin:
        st.session_state.logged_in = True
        st.session_state.role = "Admin"
        st.session_state.name = "Sarah Singh"
        st.session_state['page'] = 'Dashboard'
        st.rerun()
