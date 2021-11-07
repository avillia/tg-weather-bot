from app.configs import IPGEOLOCATION_TOKEN
from app.configs.extensions import ipgeo_request


def fetch_timezone(latitude: float, longitude: float) -> str:
    data = ipgeo_request.get(
        "https://api.ipgeolocation.io/timezone",
        params={"lat": latitude, "long": longitude, "apiKey": IPGEOLOCATION_TOKEN},
    ).json()
    return data["timezone"]
