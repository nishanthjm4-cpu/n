import streamlit as st
import pandas as pd
import os

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Social Media Analytics Dashboard",
    layout="wide"
)

# ----------------------------
# Load dataset
# ----------------------------
@st.cache_data
def load_data():
    filename = "social_media_engagement_enhanced (1).csv"

    if not os.path.exists(filename):
        st.error("CSV file not found. Please upload 'social_media_engagement_enhanced (1).csv'")
        st.stop()

    df = pd.read_csv(filename)

    # Date processing
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M")
    df["hour"] = df["date"].dt.hour

    # Engagement calculation
    df["engagement"] = df["likes"] + df["comments"] + df["shares"]

    # Campaign ROI (assumed cost)
    df["campaign_cost"] = 5000
    df["roi"] = ((df["engagement"] - df["campaign_cost"]) / df["campaign_cost"]) * 100

    return df

df = load_data()

# ----------------------------
# Dashboard title
# ----------------------------
st.title("📊 Social Media Engagement Analytics")
st.write("Campaign ROI, Optimal Posting Time, and Monthly Trends")

# ----------------------------
# ROI SECTION
# ----------------------------
st.subheader("💰 Campaign ROI by Platform")

roi_platform = df.groupby("platform")["roi"].mean()

st.bar_chart(roi_platform)

best_roi_platform = roi_platform.idxmax()
st.metric("🏆 Best ROI Platform", best_roi_platform)

# ----------------------------
# OPTIMAL POSTING TIME (PER PLATFORM)
# ----------------------------
st.subheader("⏰ Optimal Posting Time (Per Platform)")

optimal_time = (
    df.groupby(["platform", "hour"])["engagement"]
    .mean()
    .reset_index()
    .loc[lambda x: x.groupby("platform")["engagement"].idxmax()]
)

st.dataframe(optimal_time[["platform", "hour"]])

# Line plot for each platform
for platform in df["platform"].unique():
    st.write(f"📱 {platform} – Engagement Trend by Hour")
    platform_df = df[df["platform"] == platform]
    st.line_chart(
        platform_df.groupby("hour")["engagement"].mean()
    )

# ----------------------------
# MONTHLY TREND (3 YEARS)
# ----------------------------
st.subheader("📈 Monthly Engagement Trend (3 Years)")

monthly_trend = df.groupby("month")["engagement"].sum()
st.line_chart(monthly_trend)

# ----------------------------
# DATA TABLE
# ----------------------------
with st.expander("📄 View Full Dataset"):
    st.dataframe(df)
