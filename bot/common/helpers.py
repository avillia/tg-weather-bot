import requests

from aiogram.types import Message


def forecast_message(description: list, temperature: list, wind: str):
    return (f"{description[0]} {description[1]} {description[0]}"
            f"\n{temperature[0]} - {temperature[1]} °C"
            f"\n{wind} for today!")
