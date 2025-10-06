import streamlit as st
import datetime

def collaborative_workspace_page():
    # ---------- PAGE STYLE ----------
    st.markdown("""
    <style>
    .section-title {
        font-size: 1.4em;
        font-weight: 800;
        color: #00494D;
        border-left: 4px solid #00A896;
        padding-left: 8px;
        margin-top: 20px;
        margin-bottom: 12px;
    }
    .study-card {
        background: rgba(255,255,255,0.75);
        border: 1.5px solid rgba(0,168,150,0.2);
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(0,109,119,0.08);
        padding: 14px 18px 10px 18px;
        margin-bottom: 14px;
        transition: all 0.25s ease;
    }
    .study-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,168,150,0.25);
    }
    .study-header {
        font-weight: 700;
        font-size: 1.05em;
        color: #004D4D;
    }
    .meta {
        color: #036b63;
        font-size: 0.9em;
        margin-top: 3px;
    }
    .status {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.85em;
        font-weight: 600;
        margin-left: 6px;
    }
    .open-btn, .comment-btn {
        background: linear-gradient(90deg,#006D77,#00A896);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 6px 12px;
        font-size: 0.9em;
        margin-right: 6px;
        cursor: pointer;
        transition: all 0.25s ease;
    }
    .open-btn:hover, .comment-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 10px rgba(0,168,150,0.25);
    }
    .comment-card {
        background: rgba(245,250,250,0.8);
        border-radius: 10px;
        padding: 10px 14px;
        margin: 6px 0;
        border-left: 3px solid #00A896;
    }
    .comment-meta {
        color: #004D4D;
        font-size: 0.9em;
        font-weight: 600;
    }
    .comment-text {
        color: #012f2d;
        margin-top: 2px;
    }
    .add-btn {
        background: linear-gradient(90deg,#00A896,#007F8E);
        color: white;
        font-weight: 700;
        font-size: 0.95em;
        border: none;
        border-radius: 10px;
        padding: 10px 18px;
        box-shadow: 0 3px 12px rgba(0,168,150,0.25);
        cursor: pointer;
        transition: all 0.25s ease;
    }
    .add-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 18px rgba(0,168,150,0.35);
    }
    .modal {
        background: rgba(255,255,255,0.95);
        border-radius: 18px;
        box-shadow: 0 8px 28px rgba(0,109,119,0.25);
        padding: 25px 25px 20px 25px;
        backdrop-filter: blur(8px);
        width: 85%;
        margin: auto;
        border: 1.5px solid rgba(0,168,150,0.25);
        animation: fadeIn 0.4s ease-in-out;
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- PAGE STRUCTURE ----------
    st.markdown("<h2 style='color:#006D77;font-weight:800;letter-spacing:-0.4px;'>🤝 Collaborative Workspace</h2>", unsafe_allow_html=True)
    st.caption("Work together on shared LCA studies — view, discuss, and manage progress in real time.")

    # ---------- Session Initialization ----------
    if "workspace_studies" not in st.session_state:
        st.session_state.workspace_studies = [
            {"name": "Steel for Automotive Chassis", "owner": "Roshani Lagad", "updated": "2025-10-04", "status": "In Review"},
            {"name": "Aluminium for Building Frame", "owner": "Priya Patel", "updated": "2025-10-03", "status": "Active"},
            {"name": "Copper Cable Life-Cycle Study", "owner": "David Kumar", "updated": "2025-09-29", "status": "Completed"},
        ]
    if "workspace_comments" not in st.session_state:
        st.session_state.workspace_comments = {s["name"]: [] for s in st.session_state.workspace_studies}
    if "show_new_study" not in st.session_state:
        st.session_state.show_new_study = False

    # ---------- NEW STUDY BUTTON ----------
    if not st.session_state.show_new_study:
        if st.button("➕ New Study", key="add_new", help="Add a new collaborative study"):
            st.session_state.show_new_study = True
            st.experimental_rerun()

    # ---------- NEW STUDY MODAL ----------
    if st.session_state.show_new_study:
        st.markdown("<div class='modal'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#006D77;margin-bottom:8px;'>🆕 Add New Study</h4>", unsafe_allow_html=True)
        new_name = st.text_input("Study Name")
        new_owner = st.text_input("Owner")
        new_status = st.selectbox("Status", ["Active", "In Review", "Completed"])
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("✅ Add Study"):
                if new_name and new_owner:
                    st.session_state.workspace_studies.append({
                        "name": new_name.strip(),
                        "owner": new_owner.strip(),
                        "updated": datetime.datetime.now().strftime("%Y-%m-%d"),
                        "status": new_status
                    })
                    st.session_state.workspace_comments[new_name.strip()] = []
                    st.session_state.show_new_study = False
                    st.experimental_rerun()
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.show_new_study = False
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- STUDY DASHBOARD ----------
    st.markdown("<div class='section-title'>📁 Shared Studies Dashboard</div>", unsafe_allow_html=True)
    for study in st.session_state.workspace_studies:
        col1, col2, col3 = st.columns([5,2,3])
        with col1:
            st.markdown(f"<div class='study-card'><div class='study-header'>{study['name']}</div>"
                        f"<div class='meta'>Owner: <b>{study['owner']}</b> | Last Updated: {study['updated']}</div>"
                        f"<div style='margin-top:6px;'>"
                        f"<span class='status' style='background:#e0faf4;color:#006D77;'>{study['status']}</span></div>", 
                        unsafe_allow_html=True)
        with col2:
            st.markdown(f"<button class='open-btn'>Open</button>", unsafe_allow_html=True)
        with col3:
            if st.button("💬 Comments", key=f"toggle_{study['name']}"):
                st.session_state[f"show_comments_{study['name']}"] = not st.session_state.get(f"show_comments_{study['name']}", False)
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- DISCUSSION THREAD ----------
        if st.session_state.get(f"show_comments_{study['name']}", False):
            st.markdown("<div class='section-title' style='margin-top:8px;'>💭 Discussion Thread</div>", unsafe_allow_html=True)
            comments = st.session_state.workspace_comments.get(study["name"], [])
            if comments:
                for c in comments:
                    st.markdown(f"<div class='comment-card'><div class='comment-meta'>{c['user']} • {c['time']}</div>"
                                f"<div class='comment-text'>{c['text']}</div></div>", unsafe_allow_html=True)
            else:
                st.info("No comments yet. Start the discussion below!")

            new_comment = st.text_input(f"Add a comment for '{study['name']}'", key=f"input_{study['name']}")
            if st.button(f"Post Comment ({study['name']})"):
                if new_comment.strip():
                    st.session_state.workspace_comments[study["name"]].append({
                        "user": "You",
                        "text": new_comment.strip(),
                        "time": datetime.datetime.now().strftime("%d %b %Y, %H:%M")
                    })
                    st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- Local Testing ----------
if __name__ == "__main__":
    collaborative_workspace_page()
