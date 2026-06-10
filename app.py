"""
🇳🇴 Norwegian Job Market Dashboard — Streamlit App
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Resolve paths relative to this script's location, not the terminal's cwd
_HERE = os.path.dirname(os.path.abspath(__file__))

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Norway Jobs Dashboard",
    page_icon="🇳🇴",
    layout="wide"
)

# ── Title ──────────────────────────────────────────────────────────────────
st.title("Norwegian Job Market Dashboard")
st.markdown("*Live data from NAV (Arbeidsplassen.no). Run the notebook first to refresh the data*")
st.divider()

# ── Load data ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load the CSV file saved by the notebook."""
    # Check both the project root and a data/ subfolder
    candidates = [
        os.path.join(_HERE, "norway_jobs_summary.csv"),
        os.path.join(_HERE, "data", "norway_jobs_summary.csv"),
    ]
    csv_path = next((p for p in candidates if os.path.exists(p)), None)
    if csv_path is None:
        st.error("❌ Data file not found! Please run the Jupyter notebook first to generate norway_jobs_summary.csv")
        st.stop()
    df = pd.read_csv(csv_path, parse_dates=["last_updated"])
    return df

df = load_data()

# ── Sidebar filters ────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filter Listings")

all_cities = sorted(df["location"].dropna().unique())
selected_cities = st.sidebar.multiselect(
    "City / location",
    options=all_cities,
    default=[],
    placeholder="All cities"
)

all_cats = sorted(df["category"].dropna().unique())
selected_cats = st.sidebar.multiselect(
    "Job Category",
    options=all_cats,
    default=[],
    placeholder="All categories"
)

# Apply filters
filtered = df.copy()
if selected_cities:
    filtered = filtered[filtered["location"].isin(selected_cities)]
if selected_cats:
    filtered = filtered[filtered["category"].isin(selected_cats)]

st.sidebar.divider()
st.sidebar.markdown(f"**Showing:** {len(filtered):,} jobs")

# ── KPI row ────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("🗂️ Active Jobs",      f"{len(filtered):,}")
col2.metric("🏢 Unique Employers", f"{filtered['employer'].nunique():,}")
col3.metric("🏙️ Cities",           f"{filtered['location'].nunique():,}")
col4.metric("📂 Categories",       f"{filtered['category'].nunique():,}")

st.divider()

# ── Row 1: Cities + Categories ─────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    city_counts = filtered["location"].value_counts().head(15)
    fig_cities = px.bar(
        x=city_counts.values,
        y=city_counts.index,
        orientation="h",
        title="🏙️ Top 15 Cities",
        labels={"x": "Jobs", "y": ""},
        color=city_counts.values,
        color_continuous_scale="Blues",
        text=city_counts.values
    )
    fig_cities.update_layout(
        yaxis={"categoryorder": "total ascending"},
        showlegend=False,
        height=420,
        coloraxis_showscale=False
    )
    fig_cities.update_traces(textposition="outside")
    st.plotly_chart(fig_cities, use_container_width=True)

with col_right:
    cat_counts = filtered["category"].value_counts()
    fig_cat = px.pie(
        values=cat_counts.values,
        names=cat_counts.index,
        title="📊 Job Categories",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_cat.update_traces(textinfo="percent+label")
    fig_cat.update_layout(height=420, showlegend=True)
    st.plotly_chart(fig_cat, use_container_width=True)

# ── Row 2: Top employers ───────────────────────────────────────────────────
employer_counts = filtered["employer"].value_counts().head(15)
fig_emp = px.bar(
    x=employer_counts.values,
    y=employer_counts.index,
    orientation="h",
    title="🏢 Top 15 Employers with Most Active Job Ads",
    labels={"x": "Job Ads", "y": ""},
    color=employer_counts.values,
    color_continuous_scale="Greens",
    text=employer_counts.values
)
fig_emp.update_layout(
    yaxis={"categoryorder": "total ascending"},
    showlegend=False,
    height=450,
    coloraxis_showscale=False
)
fig_emp.update_traces(textposition="outside")
st.plotly_chart(fig_emp, use_container_width=True)

# ── Row 3: Timeline ────────────────────────────────────────────────────────
if "last_updated" in filtered.columns and filtered["last_updated"].notna().sum() > 0:
    filtered["date"] = filtered["last_updated"].dt.date
    daily = (
        filtered.groupby("date")
        .size()
        .reset_index(name="job_count")
        .sort_values("date")
    )
    fig_time = px.line(
        daily, x="date", y="job_count",
        title="📅 Jobs Posted Per Day",
        labels={"date": "Date", "job_count": "Jobs"},
        markers=True
    )
    fig_time.update_traces(line_color="royalblue", marker_color="royalblue")
    fig_time.update_layout(height=350)
    st.plotly_chart(fig_time, use_container_width=True)

# ── Data table ─────────────────────────────────────────────────────────────
st.subheader("📋 Browse Listings")
display_df = (
    filtered[["title", "employer", "location", "category"]]
    .rename(columns={
        "title"        : "Job Title",
        "employer"     : "Employer",
        "location"     : "City",
        "category"     : "Category"
    })
    .reset_index(drop=True)
)
st.dataframe(display_df, use_container_width=True, height=380)

# ── Footer ─────────────────────────────────────────────────────────────────
st.divider()
st.caption("Data source: NAV Arbeidsplassen (pam-stilling-feed.nav.no) · Built with Python + Streamlit")
