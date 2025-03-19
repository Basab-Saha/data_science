import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Database connection
DB_URI = "postgresql://weather_db_owner:npg_23YnzyEIZTJD@ep-royal-unit-a81pyxdv-pooler.eastus2.azure.neon.tech/weather_db?sslmode=require"
engine = create_engine(DB_URI)

# Fetch latest weather data
@st.cache_data(ttl=5)  # Auto refresh every 60 seconds
def fetch_weather_data_from_db():
    query = "SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 1"
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

st.title("🌤 Live Weather Dashboard")

latest_weather = fetch_weather_data_from_db()

if not latest_weather.empty:
    st.subheader(f"📍 {latest_weather['city'].iloc[0]}")
    st.metric(label="🌡 Temperature", value=f"{latest_weather['temperature'].iloc[0] - 273:.2f}°C")
    st.metric(label="💧 Humidity", value=f"{latest_weather['humidity'].iloc[0]}%")
    st.metric(label="🌪 Weather", value=f"{latest_weather['weather'].iloc[0]}")
    st.metric(label="🌬 Wind Speed", value=f"{latest_weather['wind_speed'].iloc[0]} m/s")
    st.write(f"🕒 Timestamp: {latest_weather['timestamp'].iloc[0]}")
else:
    st.error("🚫 No weather data available yet.")

# Auto-refresh button
if st.button("🔄 Refresh"):
    st.rerun()

