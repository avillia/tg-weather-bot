from aiogram import types


weather_button_text = "\U00002600 Weather \U000026C5"
time_button_text = "\U0001F562 New time of daily forecast \U0001F551"
stop_button_text = "\U0001F6D1 Stop daily forecasts \U0001F6D1"
cancel_button_text = "\U0000274C Cancel \U0000274C"
scheduled_button_text = "\U0001f55d Show scheduled \U00002753"

location_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_geo = types.KeyboardButton(
    text="\U0001F30E Send location! \U0001F30D", request_location=True
)
location_keyboard.add(button_geo)

default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
get_weather_button = types.KeyboardButton(
    text=weather_button_text,
)
get_time_button = types.KeyboardButton(
    text=time_button_text,
)
stop_button = types.KeyboardButton(
    text=stop_button_text,
)
show_scheduled_button = types.KeyboardButton(
    text=scheduled_button_text,
)
default_keyboard.row(get_weather_button)
default_keyboard.row(get_time_button)
default_keyboard.row(show_scheduled_button, stop_button)

cancel_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = types.KeyboardButton(
    text=cancel_button_text,
)
cancel_keyboard.add(cancel_button)

empty_keyboard = types.ReplyKeyboardRemove(selective=False)
