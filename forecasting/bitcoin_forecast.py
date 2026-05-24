import pandas as pd
from prophet import Prophet
from sqlalchemy import create_engine
import plotly.express as px
import streamlit as st

# Database connection
username = "root"
password = "password"
host = "127.0.0.1"
port = "3306"
database = "crypto_dashboard"

DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)

# Load Bitcoin data
query = """
SELECT * FROM crypto_prices
WHERE coin_name = 'Bitcoin'
"""

df = pd.read_sql(query, engine)

# Prepare Prophet data
df = df[["timestamp", "current_price"]]

df.columns = ["ds", "y"]

# Remove duplicates
df = df.drop_duplicates()

# Create Prophet model
model = Prophet()

model.fit(df)

# Future predictions
future = model.make_future_dataframe(periods=7, freq='D')

forecast = model.predict(future)

# Streamlit UI
st.subheader("🔮 Bitcoin 7-Day Forecast")

fig = px.line(
    forecast,
    x="ds",
    y="yhat",
    title="Predicted Bitcoin Prices"
)

st.plotly_chart(fig, use_container_width=True)