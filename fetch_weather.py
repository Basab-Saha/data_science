import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pytz 

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
CITY = "gangtok"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"

DB_URI = os.getenv("DB_URI")
engine = create_engine(DB_URI)

def fetch_weather_data():
    response=requests.get(URL).json()

    ist = pytz.timezone("Asia/Kolkata")
    utc_now = datetime.utcnow()
    local_time = utc_now.replace(tzinfo=pytz.utc).astimezone(ist)

    weather_data={
        "city":response["name"],
        "temperature":response["main"]["temp"],
        "humidity":response["main"]["humidity"],
        "weather":response["weather"][0]["description"],
        "wind_speed":response["wind"]["speed"],
        "timestamp": local_time.strftime('%Y-%m-%d %H:%M:%S')
    }

    df=pd.DataFrame([weather_data])

    df.to_sql("weather_data",con=engine,if_exists="append",index=False)
    print("Data inserted successfully")


fetch_weather_data()