import streamlit as st
import pandas as pd
import datetime
import random

def view_reports_page():
    st.markdown("""
    <style>
    .report-table {
        border-collapse: separate !important;
        border-spacing: 0;
        width: 98%;
        margin: auto;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        table-layout: fixed;
        background: #fff;
    }
    .report-table thead tr th {
        background: #171c23;
        color: #fff;
        font-weight: 800;
        font-size: 1.04em;
        padding: 12px 6px;
        border-right: 2px solid #fff1;
        text-align: center;
        letter-spacing: -.2px;
    }
    .report-table thead tr th:first-child {
        border-top-left-radius: 10px;
    }
    .report-table thead tr th:last-child {
        border-top-right-radius: 10px;
        border-right: none;
    }
    .report-table tbody tr {
        background: #fff;
        transition: background 0.13s;
    }
    .report-table tbody tr:nth-child(even) {
        background: #f3f6fa;
    }
    .report-table tbody tr:hover {
        background: #e8f2ff;
    }
    .report-table td {
        font-size: 1.05em;
        padding: 11px 6px;
        color: #22333b;
        text-align: center;
        border-bottom: 1.5px solid #e8e8ef;
    }
    .report-table td.title {
        text-align: left;
        font-weight: 500;
        color: #0c232f;
        padding-left: 18px;
    }
    .serial-no {
        color: #3780e8;
        font-weight: 700;
        text-align: center;
    }
    .view-btn {
        background: #eaf3fb;
        color: #1766a7;
        font-weight: 700;
        border-radius: 7px;
        border: 1.5px solid #bbe2fa;
        padding: 7px 15px;
        font-size: 1.05em;
        text-align: center;
        cursor: pointer;
        transition: background 0.18s, border 0.18s;
    }
    .view-btn:hover {
        background: #d0eafd;
        border: 1.7px solid #89c7f4;
    }
    </style>
    """, unsafe_allow_html=True)

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

    st.markdown("<div style='font-size:2.2em; font-weight:800; letter-spacing:-1px; color:#10132d; margin-top:12px;'>All Reports</div>", unsafe_allow_html=True)
    st.caption("Browse all your generated LCA and scenario reports. Click to view any report in detail.")

    c1, c2 = st.columns(2)
    with c1:
        f_author = st.selectbox("Filter by Author", ["All"] + authors)
    with c2:
        f_material = st.selectbox("Filter by Material", ["All"] + materials)

    filtered_df = df.copy()
    if f_author != "All":
        filtered_df = filtered_df[filtered_df["Author"] == f_author]
    if f_material != "All":
        filtered_df = filtered_df[filtered_df["Material"] == f_material]
    filtered_df = filtered_df.reset_index(drop=True)

    st.markdown(f"""
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

    for idx, row in filtered_df.iterrows():
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

    st.markdown("</tbody></table>", unsafe_allow_html=True)
