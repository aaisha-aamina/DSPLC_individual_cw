# Enhanced Streamlit Dashboard with Advanced Styling (Dark Theme)

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

# Load dataset
df = pd.read_csv("infrastructure_lka_cleaned.csv")

# Page config
st.set_page_config(page_title="Sri Lanka Infrastructure Dashboard", layout="wide")

# Apply dark theme custom fonts and styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Playfair+Display:wght@600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background-color: #0D1117;
        color: #F8F8F2;
    }
    .main h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif;
        color: #00FFAA;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation
page = st.sidebar.radio("📁 Select Page", ["About", "Dashboard"])

# ----------- ABOUT PAGE -----------
if page == "About":
    st.title("About the Dashboard")
    st.markdown("""
    This dashboard presents interactive visualizations of key infrastructure indicators in **Sri Lanka**, 
    from **1960 to 2023**, across multiple sectors like ICT, Transport, Water, and Innovation.

    ### Dataset Columns Explained
    - **Country Name**: Country (always Sri Lanka)
    - **Year**: Year the data was recorded
    - **Indicator Name**: The type of infrastructure metric
    - **Value**: Numerical value of the indicator for that year
    - **Indicator Code**: Unique code for each indicator (e.g., IND_01)
    - **Sector**: Grouping (ICT, Water, Transport, etc.) for usability
    - **YoY Change (%)**: Year-on-year percentage change in the value
    - **Growth Label**: Categorized change (Surge, Drop, Stable)
                
     ### Why This Dashboard?
    - Visualize long-term development patterns
    - Identify rapid changes or declines
    - Enable policymakers, students, and analysts to interact with national infrastructure trends

    Navigate to the **Dashboard** using the sidebar to begin exploring!
    """)

# ----------- DASHBOARD PAGE -----------
elif page == "Dashboard":
    st.title("🌍 Infrastructure Insights")

    # Sidebar Filters
    st.sidebar.header("📌 Filters")
    selected_sector = st.sidebar.selectbox("Select Sector", sorted(df["Sector"].unique()))
    indicators = df[df["Sector"] == selected_sector]["Indicator Name"].unique()
    selected_indicator = st.sidebar.selectbox("Select Indicator", sorted(indicators))
    year_range = st.sidebar.slider("Select Year Range", int(df["Year"].min()), int(df["Year"].max()), (2000, 2023))

    filtered = df[
        (df["Sector"] == selected_sector) &
        (df["Indicator Name"] == selected_indicator) &
        (df["Year"].between(year_range[0], year_range[1]))
    ]

    # KPI Metrics
    st.subheader("📌 Key Metrics")
    latest = filtered.sort_values("Year", ascending=False).iloc[0]
    k1, k2, k3 = st.columns(3)
    k1.metric("📅 Year", latest["Year"])
    k2.metric("📈 Latest Value", f"{latest['Value']:.2f}")
    k3.metric("📊 YoY Change", f"{latest['YoY Change (%)']:.2f}" if not pd.isna(latest['YoY Change (%)']) else "N/A")
    
    # Style metric cards (Dark Theme)
    style_metric_cards(
        background_color="#161B22",
        border_left_color="#00FFAA",
        border_color="#2C2F36",
        box_shadow="0 4px 8px rgba(0, 0, 0, 0.6)",
        border_radius_px=15
    )

    # Line Chart
    st.subheader("📈 Trend Over Time")
    fig_trend = px.line(filtered, x="Year", y="Value", title=f"{selected_indicator} Over Time", markers=True,
                        template="plotly_dark")
    st.plotly_chart(fig_trend, use_container_width=True)

    # Growth Label Bar
    st.subheader("Growth Label by Year")
    fig_growth = px.bar(
        filtered, x="Year", y="Value", color="Growth Label", text="Growth Label",
        title="Growth Classification",
        template="plotly_dark",
        color_discrete_map={"Surge": "lime", "Drop": "red", "Stable": "orange", "N/A": "gray"}
    )
    st.plotly_chart(fig_growth, use_container_width=True)

    # Box Plot (Individual)
    st.subheader("Box Plot: Indicator Value Distribution")
    fig_box = px.box(
        df[df["Indicator Name"] == selected_indicator],
        y="Value",
        points="all",
        title=f"Distribution of '{selected_indicator}' (1960–2023)",
        color_discrete_sequence=["#EF553B"],
        template="plotly_dark"
    )
    fig_box.update_layout(
        xaxis_title=None,
        yaxis_title="Value",
        showlegend=False
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Area Chart
    st.subheader("Area Chart View")
    fig_area = px.area(filtered, x="Year", y="Value", title="Cumulative Progression",
                       color_discrete_sequence=["#00CC96"], template="plotly_dark")
    st.plotly_chart(fig_area, use_container_width=True)

    # Multi-Indicator Comparison (Improved Layout)
    st.markdown("## 📊 Multi-Indicator Comparison")
    st.sidebar.markdown("---")
    st.sidebar.subheader("📌 Compare Multiple Indicators")
    compare_inds = st.sidebar.multiselect(
        "Select Indicators (within the same sector):", 
        df[df["Sector"] == selected_sector]["Indicator Name"].unique(),
        default=[selected_indicator]
    )
    multi_df = df[
        (df["Sector"] == selected_sector) &
        (df["Indicator Name"].isin(compare_inds)) &
        (df["Year"].between(year_range[0], year_range[1]))
    ]
    if not multi_df.empty:
        # Line chart
        st.subheader("📈 Trend Comparison")
        fig_multi_line = px.line(
            multi_df, x="Year", y="Value", color="Indicator Name", markers=True,
            template="plotly_dark"
        )
        st.plotly_chart(fig_multi_line, use_container_width=True)

        # Box chart
        st.subheader("📊 Distribution Comparison")
        fig_multi_box = px.box(
            multi_df, x="Indicator Name", y="Value", color="Indicator Name",
            template="plotly_dark"
        )
        st.plotly_chart(fig_multi_box, use_container_width=True)


    # Insights
    with st.expander("💡 Key Takeaways"):
        st.write(f"- **{selected_indicator}** in **{selected_sector}** peaked at **{latest['Value']:.2f}** in **{latest['Year']}**.")
        if not pd.isna(latest["YoY Change (%)"]):
            st.write(f"- This was a change of **{latest['YoY Change (%)']:.2f}%** from the previous year.")
        st.write("- Use box plots to identify variability and stability.")
        st.write("- Compare multiple indicators to understand trends across the sector.")

    # Download Button
    st.sidebar.download_button(
        "⬇️ Download Filtered Data",
        filtered.to_csv(index=False),
        file_name="filtered_infra_data.csv",
        mime="text/csv"
    )
