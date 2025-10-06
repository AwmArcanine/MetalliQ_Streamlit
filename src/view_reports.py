import streamlit as st
import pandas as pd
import datetime
import random


def view_reports_page():
    # ======= PAGE HEADER =======
    st.markdown("""
    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:1rem;
    ">
        <div>
            <h1 style="color:#003f46;font-weight:800;letter-spacing:-0.5px;margin-bottom:0.3rem;">
                📄 All Reports
            </h1>
            <p style="color:#4b6365;font-size:0.9rem;margin:0;">
                Browse and manage your generated LCA and scenario reports.
            </p>
        </div>
        <button style="
            background-color:#006D77;
            color:white;
            font-weight:600;
            border:none;
            border-radius:8px;
            padding:8px 16px;
            font-size:0.95rem;
            cursor:pointer;
            transition:all 0.2s ease;
        " onmouseover="this.style.backgroundColor='#009A9F'" 
          onmouseout="this.style.backgroundColor='#006D77'">
            ⟳ Refresh
        </button>
    </div>
    """, unsafe_allow_html=True)

    # ======= DATA GENERATION =======
    authors = ["John Doe", "Sarah Singh", "Alice Brown", "David Kumar", "Priya Patel", "Alex Wang"]
    materials = ["Steel", "Aluminium", "Copper", "Cement", "Polymers (PET)"]

    def random_date():
        base = datetime.datetime(2025, 9, 15)
        days = random.randint(0, 20)
        dt = base + datetime.timedelta(days=days)
        time = datetime.time(random.randint(8, 18), random.choice([0, 15, 30, 45]))
        return dt.replace(hour=time.hour, minute=time.minute)

    reports = []
    for i in range(15):
        reports.append({
            "Sr No": i + 1,
            "Report Title": f"LCA Study #{i + 1}",
            "Author": random.choice(authors),
            "Date & Time": random_date().strftime("%d/%m/%Y %H:%M"),
            "Material": random.choice(materials),
            "GWP": f"{random.randint(600, 3000)} kg CO₂-eq"
        })
    df = pd.DataFrame(reports)

    # ======= INLINE CSS =======
    st.markdown("""
    <style>
    .report-card {
        background: rgba(255,255,255,0.9);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(0, 109, 119, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .report-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 109, 119, 0.25);
    }
    .report-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .report-title {
        font-weight: 700;
        color: #00494D;
        font-size: 1.1rem;
    }
    .report-meta {
        color: #4b6365;
        font-size: 0.88rem;
    }
    .report-buttons {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    .btn-open {
        background-color: #006D77;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: background 0.2s;
    }
    .btn-open:hover { background-color: #009A9F; }
    .btn-comment {
        background-color: white;
        color: #6b5aa1;
        font-weight: 600;
        border: 1.5px solid #d2ccf2;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    .btn-comment:hover {
        background-color: #f2edff;
        border-color: #b9a9f4;
    }
    </style>
    """, unsafe_allow_html=True)

    # ======= REPORT CARDS =======
    for _, row in df.iterrows():
        st.markdown(f"""
        <div class="report-card">
            <div class="report-header">
                <div class="report-title">{row['Report Title']}</div>
                <div class="report-meta">{row['Date & Time']}</div>
            </div>
            <div class="report-meta">
                Author: <b>{row['Author']}</b> &nbsp;|&nbsp; 
                Material: <b>{row['Material']}</b> &nbsp;|&nbsp; 
                GWP: <b>{row['GWP']}</b>
            </div>
            <div class="report-buttons">
                <button class="btn-open">Open</button>
                <button class="btn-comment">💬 Comments</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
