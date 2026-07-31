import os
from locations import get_locations
import requests
import pandas as pd
from datetime import datetime
from database import engine
from zoneinfo import ZoneInfo


def fetch_weather(location):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={location['lat']}"
        f"&longitude={location['lon']}"
        "&current="
        "temperature_2m,"
        "relative_humidity_2m,"
        "apparent_temperature,"
        "precipitation,"
        "rain,"
        "cloud_cover,"
        "wind_speed_10m,"
        "weather_code"
    )

    response = requests.get(url, timeout=10)

    response.raise_for_status()

    return response.json()["current"]


def main():
    batch_time = (
        datetime.now(ZoneInfo("Europe/Istanbul"))
        .replace(second=0, microsecond=0)
    )
    locations = get_locations()
    weather_records = []

    for location in locations:
        weather = fetch_weather(location)

        print("=" * 50)
        print(location["isim"])
        print(weather)

        weather_records.append({

            "created_at": batch_time,

            "location_name": location["isim"],

            "latitude": location["lat"],
            "longitude": location["lon"],

            "temperature": weather["temperature_2m"],

            "apparent_temperature": weather["apparent_temperature"],

            "humidity": weather["relative_humidity_2m"],

            "precipitation": weather["precipitation"],

            "rain": weather["rain"],

            "cloud_cover": weather["cloud_cover"],

            "wind_speed": weather["wind_speed_10m"],

            "weather_code": weather["weather_code"]
        })
    df = pd.DataFrame(weather_records)

    print(df.head())
    df.to_sql(
        "weather_raw",
        engine,
        schema="bronze",
        if_exists="append",
        index=False
    )

    print("✅ Hava durumu verileri PostgreSQL'e kaydedildi.")

if __name__ == "__main__":
    main()



