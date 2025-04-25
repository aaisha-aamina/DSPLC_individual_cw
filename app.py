import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("infrastructure_lka_cleaned.csv")

# Set page config
st.set_page_config(page_title="Sri Lanka Infrastructure Dashboard", layout="wide")

# Title and instructions
st.title("🇱🇰 Sri Lanka Infrastructure Insights")
st.markdown("#### Select parameters from the sidebar to explore trends and insights.")

# Sidebar filters
st.sidebar.title("🔍 Filter Data")
indicators = df["Indicator Name"].unique()
selected_indicators = st.sidebar.multiselect("Choose indicators", indicators, default=indicators[:3])
years = df["Year"].unique()
year_range = st.sidebar.slider("Select year range", int(min(years)), int(max(years)), (2015, 2023))

# Filter data
filtered = df[
    (df["Indicator Name"].isin(selected_indicators)) &
    (df["Year"].between(year_range[0], year_range[1]))
]

# KPIs
st.markdown("### 📌 Key Performance Insights")
kpi_cols = st.columns(len(selected_indicators))
for i, ind in enumerate(selected_indicators):
    recent = filtered[filtered["Indicator Name"] == ind].sort_values("Year", ascending=False).head(2)
    if len(recent) == 2:
        curr, prev = recent.iloc[0]["Value"], recent.iloc[1]["Value"]
        delta = ((curr - prev) / prev) * 100 if prev != 0 else 0
        kpi_cols[i].metric(label=ind, value=f"{curr:,.0f}", delta=f"{delta:.2f}%", delta_color="normal")

# Line chart
st.markdown("### 📈 Yearly Trend")
line_chart = px.line(filtered, x="Year", y="Value", color="Indicator Name", markers=True)
line_chart.update_layout(legend_title_text='Indicator', title_text='Trends Over Time')
st.plotly_chart(line_chart, use_container_width=True)

# Bar chart
st.markdown("### 📊 Yearly Comparison")
bar_chart = px.bar(filtered, x="Year", y="Value", color="Indicator Name", barmode="group")
bar_chart.update_layout(title_text='Comparison by Year')
st.plotly_chart(bar_chart, use_container_width=True)

# Insights Box
with st.expander("💡 Insights Summary"):
    st.write("- Indicators like **ICT exports** and **access to electricity** show positive trends.")
    st.write("- Significant growth observed in key years, especially post-2020.")
    st.write("- Some fluctuations may indicate global/economic impact (e.g., COVID-19, economic crisis).")

# Download data
st.sidebar.download_button("⬇️ Download Filtered Data", filtered.to_csv(index=False), "filtered_infra.csv", "text/csv")
