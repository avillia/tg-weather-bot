from dataclasses import dataclass


weatherEncryption = {"01d": ("\U00002600", "Sunny"),
                     "02d": ("\U0001F324", "Partly cloud"),
                     "03d": ("\U000026C5", "Cloud"),
                     "04d": ("\U00002601", "Broken cloud"),
                     "09d": ("\U0001F327", "Rain"),
                     "10d": ("\U0001F326", "Small rain"),
                     "11d": ("\U000026A1", "Thunderstorm"),
                     "13d": ("\U00002744", "Snow"),
                     "50d": ("\U0001F32B", "Foggy")}


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
