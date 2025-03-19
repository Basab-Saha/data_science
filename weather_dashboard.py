import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

DB_URI = "postgresql://weather_db_owner:npg_23YnzyEIZTJD@ep-royal-unit-a81pyxdv-pooler.eastus2.azure.neon.tech/weather_db?sslmode=require"
engine = create_engine(DB_URI)

#fetching weather data from my mySQL workbench
def fetch_weather_data_from_db():
    query="select * from weather_data order by timestamp DESC limit 1"
    df=pd.read_sql(query,engine)
    return df

st.title("Live Weather Dashboard")

latest_weather=fetch_weather_data_from_db()

if not latest_weather.empty:
    st.write(f"City: {latest_weather['city'].iloc[0]}")
    st.write(f"Temperature: {latest_weather['temperature'].iloc[0] - 273:.2f}°C")
    st.write(f"Humidity: {latest_weather['humidity'].iloc[0]}%")
    st.write(f"Weather: {latest_weather['weather'].iloc[0]}")
    st.write(f"Wind Speed: {latest_weather['wind_speed'].iloc[0]} m/s")
    st.write(f"Timestamp: {latest_weather['timestamp'].iloc[0]}")
else:
    st.write("No data available yet.")