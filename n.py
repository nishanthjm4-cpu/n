import streamlit as st
import pandas as pd
import os

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Monthly Trends & Engagement Rate",
    layout="wide"
)

# ----------------------------
# Load dataset
# ----------------------------
@st.cache_data
def load_data():
    filename = "social_media_engagement_enhanced (1).csv"

    if not os.path.exists(filename):
        st.error("CSV file not found. Upload 'social_media_engagement_enhanced (1).csv'")
        st.stop()

    df = pd.read_csv(filename)

    # Date processing
    df["date"] = pd.to_datetime(df["date"])
    df["year_month"] = df["date"].dt.to_period("M")

    # Engagement calculation
    df["engagement"] = df["likes"] + df["comments"] + df["shares"]

    # Engagement Rate (%)
    df["engagement_rate"] = (df["engagement"] / df["views"]) * 100

    return df

df = load_data()

# ----------------------------
# DASHBOARD TITLE
# ----------------------------
st.title("📊 Monthly Trends & Engagement Rate Analysis")

# ======================================================
# 1️⃣ MONTHLY ENGAGEMENT TREND (PER PLATFORM)
# ======================================================
st.subheader("📈 Monthly Engagement Trend (Platform-wise)")

platforms = df["platform"].unique()

for platform in platforms:
    st.write(f"📱 {platform}")
    platform_df = df[df["platform"] == platform]

    monthly_trend = (
        platform_df.groupby("year_month")["engagement"]
        .sum()
    )

    st.line_chart(monthly_trend)

# ======================================================
# 2️⃣ ENGAGEMENT RATE (%)
# ======================================================
st.subheader("💬 Engagement Rate (%) by Platform")

engagement_rate_platform = (
    df.groupby("platform")["engagement_rate"]
    .mean()
)

st.bar_chart(engagement_rate_platform)

best_engagement_platform = engagement_rate_platform.idxmax()
st.metric("🏆 Highest Engagement Rate Platform", best_engagement_platform)

# ----------------------------
# DATA TABLE
# ----------------------------
with st.expander("📄 View Data"):
    st.dataframe(df)
