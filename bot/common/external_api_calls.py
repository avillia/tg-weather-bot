from requests_cache import CachedSession, SQLiteCache

from bot.configs import IPGEOLOCATION_TOKEN, OPENWEATHERMAP_TOKEN

ipgeo_request = CachedSession("ipgeolocation_cache", )


def fetch_timezone(latitude: float, longitude: float) -> int:
    data = requests.get(f"https://api.ipgeolocation.io/timezone?apiKey="
                        f"&lat={latitude}&long={longitude}").json()
    correction = (round(data['dst_savings']) if data['is_dst'] else 0)
    timezone = data['timezone_offset'] +


def obtain_weather(latitude: float, longitude: float):
    data = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "lat": latitude,
            "lon": longitude,
            "appid": OPENWEATHERMAP_TOKEN,
        },
    ).json()


    forecast = {"description": weatherEncryption[data['weather'][0]['icon'][0:2]],
                "temperature": (round(data['main']['temp_min']) - 273, round(data['main']['temp_max']) - 273),
                "wind": "No wind" if data['wind']['speed'] < 4 else "Windy"}

    forecast = Forecast()

    return forecast