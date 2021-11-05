from dataclasses import dataclass

from app.configs import OPENWEATHERMAP_TOKEN
from app.configs.extensions import openweather_request

weather_map = {
    "01": ("\U00002600", "Sunny"),
    "02": ("\U0001F324", "Partly cloud"),
    "03": ("\U000026C5", "Cloud"),
    "04": ("\U00002601", "Broken cloud"),
    "09": ("\U0001F327", "Rain"),
    "10": ("\U0001F326", "Small rain"),
    "11": ("\U000026A1", "Thunderstorm"),
    "13": ("\U00002744", "Snow"),
    "50": ("\U0001F32B", "Foggy"),
}


@dataclass
class Forecast:
    emoji: str
    description: str
    temp_min: int
    temp_max: int
    speed_of_wind: float

    @property
    def wind(self):
        return "No wind" if self.speed_of_wind < 4 else "Windy"

    @property
    def as_message(self):
        return (
            f"{self.emoji} {self.description} {self.emoji}\n"
            f"{self.temp_min} - {self.temp_max} °C"
            f"{self.wind} for today!"
        )


def obtain_weather(latitude: float, longitude: float):
    data = openweather_request.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "lat": latitude,
            "lon": longitude,
            "appid": OPENWEATHERMAP_TOKEN,
        },
    ).json()

    return Forecast(
        weather_map[data["weather"][0]["icon"][:2]][0],
        weather_map[data["weather"][0]["icon"][:2]][1],
        round(data["main"]["temp_min"]) - 273,
        round(data["main"]["temp_max"]) - 273,
        data["wind"]["speed"],
    )
