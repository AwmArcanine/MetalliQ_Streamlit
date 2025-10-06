import streamlit as st
import pandas as pd
import datetime
import random

def view_reports_page():
    # ---------- THEME STYLING ----------
    st.markdown("""
    <style>
    /* ---------- Page Container ---------- */
    .report-container {
        background: rgba(255,255,255,0.65);
        border-radius: 16px;
        box-shadow: 0 8px 28px rgba(0,109,119,0.15);
        padding: 25px 30px;
        backdrop-filter: blur(10px);
        width: 98%;
        margin: 20px auto;
        animation: fadeIn 0.5s ease-in-out;
    }

    /* ---------- Header ---------- */
    .report-title {
        font-size: 3em;
        font-weight: 800;
        letter-spacing: -1px;
        color: #00FFFF;
        margin-top: 10px;
        margin-bottom: 4px;
        font-family: 'Poppins', sans-serif;
    }
    .report-caption {
        color: #ffffff;
        font-weight: 500;
        margin-bottom: 18px;
        font-family: 'Inter', sans-serif;
    }

    /* ---------- Filter Cards ---------- */
    .filter-card {
        background: rgba(255,255,255,0.7);
        border-radius: 12px;
        box-shadow: 0 3px 14px rgba(0,109,119,0.1);
        padding: 15px 20px 8px 20px;
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
        transition: all 0.2s ease-in-out;
    }
    .filter-card:hover {
        box-shadow: 0 5px 18px rgba(0,109,119,0.15);
    }

    /* ---------- Table Styling ---------- */
    .report-table {
        border-collapse: separate !important;
        border-spacing: 0;
        width: 100%;
        margin: 10px auto;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        table-layout: fixed;
        background: rgba(255,255,255,0.75);
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(0,109,119,0.08);
    }
    .report-table thead tr th {
        background: linear-gradient(90deg, #007F8E, #00A896);
        color: #ffffff;
        font-weight: 800;
        font-size: 1.05em;
        padding: 12px 6px;
        text-align: center;
        border-right: 2px solid rgba(255,255,255,0.1);
    }
    .report-table tbody tr {
        position: relative;
        overflow: hidden;
        background: rgba(255,255,255,0.6);
        transition: background 0.15s ease-in-out;
    }
    .report-table tbody tr:nth-child(even) {
        background: rgba(245,250,250,0.7);
    }
    .report-table tbody tr:hover {
        background: rgba(0,168,150,0.07);
    }
    .report-table td {
        font-size: 1.02em;
        padding: 11px 6px;
        color: #ffffff;
        text-align: center;
        border-bottom: 1.2px solid rgba(0,109,119,0.15);
    }
    .report-table td.title {
        text-align: left;
        font-weight: 600;
        color: #00494D;
        padding-left: 18px;
    }
    .serial-no {
        color: #00A896;
        font-weight: 700;
    }

    /* ---------- Shimmer Animation ---------- */
    .report-table tbody tr::after {
        content: "";
        position: absolute;
        top: 0;
        left: -75%;
        width: 50%;
        height: 100%;
        background: linear-gradient(
            120deg,
            rgba(255,255,255,0) 0%,
            rgba(255,255,255,0.6) 50%,
            rgba(255,255,255,0) 100%
        );
        transform: skewX(-20deg);
        opacity: 0;
        transition: opacity 0.2s ease-in-out;
    }
    .report-table tbody tr:hover::after {
        animation: shimmer 1s forwards;
        opacity: 1;
    }
    @keyframes shimmer {
        from { left: -75%; }
        to { left: 125%; }
    }

    /* ---------- View Button ---------- */
    .view-btn {
        background: linear-gradient(90deg, #006D77, #00A896);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 7px 15px;
        font-size: 1.02em;
        text-align: center;
        cursor: pointer;
        transition: all 0.25s ease;
    }
    .view-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0,168,150,0.25);
    }

    /* ---------- Fade In ---------- */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- DATA GENERATION ----------
    authors = ["John Doe", "Sarah Singh", "Alice Brown", "David Kumar", "Priya Patel", "Alex Wang"]
    titles = [
        "Steel for New Building Frame", "Steel for Residential Building", "Aluminium for Automotive Chassis",
        "Copper for Copper Wiring", "Cement for Foundation", "Steel for Project Alpha",
        "Aluminium for Commercial Cladding", "Steel for High-Rise Beam", "Copper for Power Cable", "Cement for Pavement"
    ]
    materials = ["Steel", "Aluminium", "Copper", "Cement", "Polymers (PET)"]

    def random_date():
        base = datetime.datetime(2025, 9, 15)
        days = random.randint(0, 20)
        dt = base + datetime.timedelta(days=days)
        time = datetime.time(random.randint(8,18), random.choice([0,15,30,45]))
        return dt.replace(hour=time.hour, minute=time.minute)

    reports = []
    for i in range(50):
        date = random_date()
        author = random.choice(authors)
        material = random.choice(materials)
        title = titles[i % len(titles)] + (f" (Recycled)" if random.random() < 0.2 else "")
        gwp = random.randint(600, 3000)
        reports.append({
            "Serial": i+1,
            "Report Title": title,
            "Author": author,
            "Date & Time": date.strftime("%d/%m/%Y %H:%M"),
            "Material": material,
            "GWP": f"{gwp} kg CO₂-eq"
        })
    df = pd.DataFrame(reports)

    # ---------- MAIN CONTENT ----------
    st.markdown("<div class='report-container'>", unsafe_allow_html=True)
    st.markdown("<div class='report-title'>📄 All Reports</div>", unsafe_allow_html=True)
    st.markdown("<div class='report-caption'>Browse all your generated LCA and scenario reports. Click to view any report in detail.</div>", unsafe_allow_html=True)

    # Filter Cards
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='filter-card'>", unsafe_allow_html=True)
        f_author = st.selectbox("Filter by Author", ["All"] + authors)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='filter-card'>", unsafe_allow_html=True)
        f_material = st.selectbox("Filter by Material", ["All"] + materials)
        st.markdown("</div>", unsafe_allow_html=True)

    filtered_df = df.copy()
    if f_author != "All":
        filtered_df = filtered_df[filtered_df["Author"] == f_author]
    if f_material != "All":
        filtered_df = filtered_df[filtered_df["Material"] == f_material]
    filtered_df = filtered_df.reset_index(drop=True)

    # ---------- TABLE RENDER ----------
    st.markdown("""
    <table class="report-table">
    <thead>
        <tr>
            <th>Sr. No.</th>
            <th>Report Title</th>
            <th>Author</th>
            <th>Date & Time</th>
            <th>Material</th>
            <th>GWP</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
    """, unsafe_allow_html=True)

    for _, row in filtered_df.iterrows():
        st.markdown(
            f"<tr>"
            f"<td class='serial-no'>{row['Serial']}</td>"
            f"<td class='title'>{row['Report Title']}</td>"
            f"<td>{row['Author']}</td>"
            f"<td>{row['Date & Time']}</td>"
            f"<td>{row['Material']}</td>"
            f"<td>{row['GWP']}</td>"
            f"<td><button class='view-btn' onclick=\"window.location.href='/view_report?id={row['Serial']}'\">View Report</button></td>"
            f"</tr>", unsafe_allow_html=True
        )

    st.markdown("</tbody></table></div>", unsafe_allow_html=True)
