import schedule
import time
from fetch_weather import fetch_weather_data

schedule.every(1).minutes.do(fetch_weather_data)

print("Scheduler Started....Fetching weather data every 1 minutes")

while True:
    schedule.run_pending()
    time.sleep(1)
