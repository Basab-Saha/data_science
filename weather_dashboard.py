import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Database connection
DB_URI = "postgresql://weather_db_owner:npg_23YnzyEIZTJD@ep-royal-unit-a81pyxdv-pooler.eastus2.azure.neon.tech/weather_db?sslmode=require"
engine = create_engine(DB_URI)

# Fetch latest weather data
@st.cache_data(ttl=5)  # Auto refresh every 5 seconds
def fetch_weather_data_from_db():
    query = """
        SELECT city, temperature, humidity, weather, wind_speed, timestamp
        FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY city ORDER BY timestamp DESC) AS rn
            FROM weather_data
        ) AS ranked
        WHERE rn = 1  -- Only fetch the latest record per city
    """
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

st.title("🌤 Live Multi-City Weather Dashboard")

latest_weather = fetch_weather_data_from_db()

# ✅ Ensure DataFrame is not empty before proceeding
if not latest_weather.empty:
    cities = latest_weather["city"].unique().tolist()  # 🔥 FIXED HERE
    
    # Create a tab for each city
    tabs = st.tabs(cities)
    
    for tab, city in zip(tabs, cities):
        with tab:
            city_data = latest_weather[latest_weather["city"] == city].iloc[0]
            
            st.subheader(f"📍 {city_data['city']}")
            st.metric(label="🌡 Temperature", value=f"{city_data['temperature'] - 273:.2f}°C")
            st.metric(label="💧 Humidity", value=f"{city_data['humidity']}%")
            st.metric(label="🌪 Weather", value=f"{city_data['weather']}")
            st.metric(label="🌬 Wind Speed", value=f"{city_data['wind_speed']} m/s")
            st.write(f"🕒 Timestamp: {city_data['timestamp']}")

else:
    st.error("🚫 No weather data available yet.")

# Auto-refresh button
if st.button("🔄 Refresh"):
    st.rerun()
