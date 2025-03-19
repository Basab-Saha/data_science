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
DB_URI = os.getenv("DB_URI")
engine = create_engine(DB_URI)

# List of cities you want to fetch data for
CITIES = ["Gangtok", "Ravangla", "Pelling", "Siliguri", "Namchi", "Kolkata"]

def fetch_weather_data():
    ist = pytz.timezone("Asia/Kolkata")
    utc_now = datetime.utcnow()
    local_time = utc_now.replace(tzinfo=pytz.utc).astimezone(ist)
    
    all_weather_data = []
    
    for city in CITIES:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url).json()

        if response.get("cod") == 200:  # Ensure valid response
            weather_data = {
                "city": response["name"],
                "temperature": response["main"]["temp"],
                "humidity": response["main"]["humidity"],
                "weather": response["weather"][0]["description"],
                "wind_speed": response["wind"]["speed"],
                "timestamp": local_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            all_weather_data.append(weather_data)
        else:
            print(f"Failed to fetch data for {city}: {response.get('message', 'Unknown error')}")

    if all_weather_data:
        df = pd.DataFrame(all_weather_data)
        df.to_sql("weather_data", con=engine, if_exists="append", index=False)
        print("Data inserted successfully for all cities.")

fetch_weather_data()
