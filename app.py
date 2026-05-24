from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚀 Cryptocurrency Market Dashboard")

import requests

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False,
    "price_change_percentage": "24h"
}

response = requests.get(url, params=params)

data = response.json()

df = pd.DataFrame(data)

df = df[[
    "name",
    "symbol",
    "current_price",
    "market_cap",
    "total_volume",
    "price_change_percentage_24h"
]]

df.columns = [
    "Name",
    "Symbol",
    "Current Price",
    "Market Cap",
    "Volume",
    "24h Change %"
]

filtered_df = df


DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)

# Page config
st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide"
)

st.title("🚀 Cryptocurrency Market Dashboard")

st.caption("Built by Atharva Khachane | Real-Time Crypto Analytics Platform")

# Auto refresh every 60 seconds
st_autorefresh(interval=60000, key="crypto_refresh")


df = pd.read_sql(query, engine)

# Latest records only
latest_df = df.sort_values("timestamp").groupby("coin_name").tail(1)

# Rename columns
latest_df = latest_df.rename(columns={
    "coin_name": "Name",
    "symbol": "Symbol",
    "current_price": "Current Price",
    "market_cap": "Market Cap",
    "total_volume": "Volume",
    "price_change_24h": "24h Change %",
    "timestamp": "Timestamp"
})

# Sidebar
st.sidebar.header("📌 Filters")

search_coin = st.sidebar.text_input("Search Coin")

filtered_df = latest_df

if search_coin:
    filtered_df = filtered_df[
        filtered_df["Name"].str.contains(search_coin, case=False)
    ]

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric(
    "Highest Price Coin",
    filtered_df.iloc[0]["Name"],
    f"${filtered_df.iloc[0]['Current Price']}"
)

col2.metric(
    "Average Market Cap",
    f"${round(filtered_df['Market Cap'].mean(), 2)}"
)

col3.metric(
    "Average 24h Change",
    f"{round(filtered_df['24h Change %'].mean(), 2)}%"
)

# Data table
st.subheader("📊 Cryptocurrency Data")

st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name="crypto_data.csv",
    mime="text/csv"
)


# Bar chart
st.subheader("💰 Current Price Comparison")

fig = px.bar(
    filtered_df,
    x="Name",
    y="Current Price",
    color="Name",
    title="Cryptocurrency Prices"
)

st.plotly_chart(fig, use_container_width=True)

# Pie chart
st.subheader("🏦 Market Cap Distribution")

fig2 = px.pie(
    filtered_df,
    names="Name",
    values="Market Cap",
    title="Market Cap Share"
)

st.plotly_chart(fig2, use_container_width=True)

# Line chart
st.subheader("📈 Trading Volume")

fig3 = px.line(
    filtered_df,
    x="Name",
    y="Volume",
    markers=True,
    title="Trading Volume Analysis"
)

st.plotly_chart(fig3, use_container_width=True)

# Historical Bitcoin Trend

st.subheader("📈 Bitcoin Historical Price Trend")

bitcoin_df = df[df["coin_name"] == "Bitcoin"]

fig4 = px.line(
    bitcoin_df,
    x="timestamp",
    y="current_price",
    title="Bitcoin Price Over Time",
    markers=True
)

st.plotly_chart(fig4, use_container_width=True)


