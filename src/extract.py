from dotenv import load_dotenv
import os
import requests
import pandas as pd
from database import engine
import json


def load_api_key():
    """API anahtarını .env dosyasından yükler."""
    load_dotenv()

    api_key = os.getenv("TOMTOM_API_KEY")

    if not api_key:
        raise ValueError("TOMTOM_API_KEY bulunamadı!")

    return api_key


def get_locations():
    """İzlenecek lokasyonlar."""

    return [
        {
            "isim": "Mecidiyeköy",
            "lat": 41.0660,
            "lon": 28.9920
        },
        {
            "isim": "Altunizade",
            "lat": 41.0217,
            "lon": 29.0458
        },
        {
            "isim": "Şile Yolu",
            "lat": 41.0319,
            "lon": 29.1661
        },
        {
            "isim": "15 Temmuz Şehitler Köprüsü",
            "lat": 41.0456,
            "lon": 29.0343
        },
        {
            "isim": "FSM Köprüsü Avrupa Yakası Yönü",
            "lat": 41.0913,
            "lon": 29.0609
        },
        {
            "isim": "FSM Köprüsü Anadolu Yakası Yönü",
            "lat": 41.0912,
            "lon": 29.0612
        },

        {
            "isim": "Seyrantepe FSM Bağlantısı",
            "lat": 41.1019,
            "lon": 28.9941
        },




        {
            "isim": "Mahmutbey Gişeler",
            "lat": 41.0558,
            "lon": 28.8222

        },


        {
            "isim": "Şirinevler D-100",
            "lat": 40.9930,
            "lon": 28.8475
        },

        {
            "isim": "Zincirlikuyu Anadolu Yönü",
            "lat": 41.065002,
            "lon": 29.014457
        },



        {
            "isim": "Cevizlibağ",
            "lat": 41.0152,
            "lon": 28.9048
        },
        {
            "isim": "Kozyatağı E-5",
            "lat": 40.9749,
            "lon": 29.0988
        },
        {
            "isim": "Uzunçayır Kavşağı",
            "lat": 40.9997,
            "lon": 29.0538
        },
        {
            "isim": "Maslak Büyükdere Cd.",
            "lat": 41.1092,
            "lon": 29.0199
        },
        {
            "isim": "Kavacık Kavşağı",
            "lat": 41.0850,
            "lon": 29.0910
        },
        {
            "isim": "Avcılar E-5",
            "lat": 40.9858,
            "lon": 28.7188
        }
    ]

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

    api_key = load_api_key()

    locations = get_locations()

    traffic_records = []

    for location in locations:

        traffic_data = fetch_traffic_data(api_key, location)

        print_traffic_data(location, traffic_data)

        traffic_records.append({
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