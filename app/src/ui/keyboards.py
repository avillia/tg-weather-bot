from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

button_geo_text = "\U0001F30E Send location! \U0001F30D"
weather_button_text = "\U00002600 Weather \U000026C5"
schedule_button_text = "\U0001F562 Schedule forecast \U0001F551"
forecasts_button_text = "\U0001f55d Show scheduled \U00002753"
cancel_button_text = "\U0000274C Cancel \U0000274C"

location_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_geo = KeyboardButton(text=button_geo_text, request_location=True)
location_keyboard.add(button_geo)

default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
get_weather_button = KeyboardButton(
    text=weather_button_text,
)
schedule_forecast_button = KeyboardButton(
    text=schedule_button_text,
)
show_scheduled_button = KeyboardButton(
    text=forecasts_button_text,
)
default_keyboard.row(get_weather_button)
default_keyboard.row(schedule_forecast_button)
default_keyboard.row(show_scheduled_button)

cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = KeyboardButton(
    text=cancel_button_text,
)
cancel_keyboard.add(cancel_button)

empty_keyboard = ReplyKeyboardRemove(selective=False)
