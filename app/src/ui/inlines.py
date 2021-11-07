from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from app.common.models import ScheduledForecast

forecast_cb = CallbackData("forecast", "forecast_id")

def generate_inline_keyboard_for_forecasts(forecasts: list[ScheduledForecast]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for forecast in forecasts:
        key = InlineKeyboardButton(f"\U0000274C {forecast.time} \U0000274C", callback_data=forecast_cb.new(forecast.id))
        keyboard.row(key)
    return keyboard
