from dotenv import load_dotenv
from locations import get_locations
import os
import requests
import pandas as pd
import json
from datetime import datetime
from database import engine
from zoneinfo import ZoneInfo

def load_api_key():
    """API anahtarını .env dosyasından yükler."""
    load_dotenv()

    api_key = os.getenv("TOMTOM_API_KEY")

    if not api_key:
        raise ValueError("TOMTOM_API_KEY bulunamadı!")

    return api_key



def fetch_traffic_data(api_key, location):
    """TomTom API'den trafik verisini çeker."""

    url = (
        "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
        f"?point={location['lat']},{location['lon']}&key={api_key}"
    )

    response = requests.get(url, timeout=10)

    response.raise_for_status()

    return response.json()["flowSegmentData"]


def print_traffic_data(location, traffic_data):
    """Trafik bilgisini ekrana yazdırır."""

    print("=" * 50)
    print(f"📍 Konum               : {location['isim']}")
    print(f"🚗 Mevcut Hız          : {traffic_data['currentSpeed']} km/h")
    print(f"🛣️ Normal Yol Hızı     : {traffic_data['freeFlowSpeed']} km/h")
    print(f"⏱️ Tahmini Yol Süresi  : {traffic_data['currentTravelTime']} saniye")
    print(f"🎯 Veri Güven Skoru    : {traffic_data['confidence']}")
    print(f"🚧 Yol Kapalı mı?      : {'Evet' if traffic_data['roadClosure'] else 'Hayır'}")
    print("=" * 50)
    print()


def main():
    batch_time = (
        datetime.now(ZoneInfo("Europe/Istanbul"))
        .replace(second=0, microsecond=0)
    )
    api_key = load_api_key()

    locations = get_locations()

    traffic_records = []

    for location in locations:

        traffic_data = fetch_traffic_data(api_key, location)

        print_traffic_data(location, traffic_data)

        traffic_records.append({
            "created_at": batch_time,
            "location_name": location["isim"],

            "latitude": location["lat"],
            "longitude": location["lon"],

            "road_geometry": json.dumps(
                traffic_data["coordinates"]["coordinate"]
            ),

            "current_speed": traffic_data["currentSpeed"],
            "free_flow_speed": traffic_data["freeFlowSpeed"],
            "current_travel_time": traffic_data["currentTravelTime"],
            "free_flow_travel_time": traffic_data["freeFlowTravelTime"],
            "confidence": traffic_data["confidence"],
            "road_closed": traffic_data["roadClosure"]
        })

    df = pd.DataFrame(traffic_records)

    print("\nDataFrame:")
    print(df)

    df.to_sql(
        "traffic_raw",
        engine,
        schema="bronze",
        if_exists="append",
        index=False
    )

    print("\n✅ Veriler başarıyla PostgreSQL'e yazıldı.")


if __name__ == "__main__":
    main()