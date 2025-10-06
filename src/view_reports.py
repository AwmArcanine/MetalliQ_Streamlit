import streamlit as st
import pandas as pd
import datetime
import random
from pathlib import Path


def load_theme():
    theme_path = Path("theme.css")
    if theme_path.exists():
        st.markdown(f"<style>{theme_path.read_text()}</style>", unsafe_allow_html=True)


def view_reports_page():
    load_theme()

    st.markdown("<h2 style='color:#00FFFF;font-weight:800;letter-spacing:-0.5px;'>📄 All Reports</h2>", unsafe_allow_html=True)
    st.caption("Browse all your generated LCA and scenario reports below.")

    authors = ["John Doe", "Sarah Singh", "Alice Brown", "David Kumar", "Priya Patel", "Alex Wang"]
    materials = ["Steel", "Aluminium", "Copper", "Cement", "Polymers (PET)"]

    def random_date():
        base = datetime.datetime(2025, 9, 15)
        days = random.randint(0, 20)
        dt = base + datetime.timedelta(days=days)
        time = datetime.time(random.randint(8, 18), random.choice([0, 15, 30, 45]))
        return dt.replace(hour=time.hour, minute=time.minute)

    reports = []
    for i in range(20):
        reports.append({
            "Sr No": i + 1,
            "Report Title": f"LCA Study #{i + 1}",
            "Author": random.choice(authors),
            "Date & Time": random_date().strftime("%d/%m/%Y %H:%M"),
            "Material": random.choice(materials),
            "GWP": f"{random.randint(600, 3000)} kg CO₂-eq"
        })
    df = pd.DataFrame(reports)

    st.dataframe(df, use_container_width=True)
