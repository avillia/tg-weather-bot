from bot_stats import TOKEN
import telebot
from telebot import types
from db_manager import *
import re, requests, json


bot = telebot.TeleBot(TOKEN)
database = SQLighter()
weatherEncryption = {"01": ("\U00002600", "Sunny"),
                     "02": ("\U0001F324", "Partly cloud"),
                     "03": ("\U000026C5", "Cloud"),
                     "04": ("\U00002601", "Broken cloud"),
                     "09": ("\U0001F327", "Rain"),
                     "10": ("\U0001F326", "Small rain"),
                     "11": ("\U000026A1", "Thunderstorm"),
                     "13": ("\U00002744", "Snow"),
                     "50": ("\U0001F32B", "Foggy")}

weather = "\U00002600 Weather \U000026C5"


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_geo = types.KeyboardButton(text="\U0001F30E Send location! \U0001F30D", request_location=True)
    keyboard.add(button_geo)

    try:
        database.reset(message.chat.id, )
    except TypeError:
        pass

    bot.send_message(message.chat.id,
                     "Hello there!\nI'm bot that can send you information about weather in your place!"
                     " Just send me your location via button under text field:",
                     reply_markup=keyboard)

    database.add_new_user(message.chat.id)
    database.set_user_state(1, message.chat.id, )


@bot.message_handler(func=lambda message: database.get_current_state(message.from_user.id) == 1)
def error_location_initialization(message):
    bot.send_message(message.chat.id,
                     "Please, send me your location with button bellow:")


@bot.message_handler(content_types=['location'],
                     func=lambda message: database.get_current_state(message.from_user.id) == 1)
def set_location_firstly(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    get_weather_button = types.KeyboardButton(text="\U00002600 Weather \U000026C5",)
    keyboard.add(get_weather_button)

    bot.send_message(message.chat.id,
                     "Thanks a lot! Now just ask me to show me weather with buttons bellow:", reply_markup=keyboard)
    database.update_coords(message.location.latitude, message.location.longitude, message.chat.id)
    database.set_user_state(2, message.chat.id, )


@bot.message_handler(content_types=['location'],
                     func=lambda message: database.get_current_state(message.from_user.id) == 2)
def update_location(message):
    bot.send_message(message.chat.id, "Your location is updated!")
    database.update_coords(message.location.latitude, message.location.longitude, message.chat.id)


@bot.message_handler(commands=["time"])
def set_time_of_daily_forecast(message):
    bot.send_message(message.chat.id, "Send me time where I should send you message "
                                      "with weather forecast using format HH:MM")
    database.set_user_state(3, message.chat.id, )


@bot.message_handler(func=lambda message: database.get_current_state(message.from_user.id) == 3)
def error_location_initialization(message):
    if re.match("[0-2][0-9]:[0-5][0-9]", message.text):
        if int(message.text[0:2]) < 24:
            bot.send_message(message.chat.id, f"Time was successfully set!\n"
                                              f"I'll send you daily forecast everyday at {message.text}")
            database.update_time(message.text, message.chat.id)
            database.set_user_state(2, message.chat.id, )
        else:
            bot.send_message(message.chat.id, f"Invalid time format! Try again.\n"
                                              f"Send time in format HH:MM, for example 19:54")
    else:
        bot.send_message(message.chat.id, f"Invalid time format! Try again.\n"
                                          f"Send time in format HH:MM, for example 19:54")


@bot.message_handler(commands=["restart"])
def reset(message):
    bot.send_message(message.chat.id, "All your settings were reset. /start again.")
    try:
        database.reset(message.chat.id, )
        database.set_user_state(0, message.chat.id, )
    except TypeError:
        pass


@bot.message_handler(content_types=["text"],
                     func=lambda message: database.get_current_state(message.from_user.id) == 2)
def non_commands_responding(message):
    if message.text == weather:
        coords = database.get_current_coords(message.chat.id)
        response = requests.get(
                   f"https://api.openweathermap.org/"
                   f"data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid=ef1d46cf281271e9a6cd05ac3fc2d2f7")

        data = json.loads(response.content.decode('utf8').replace("'", '"'))
        forecast = {"description": weatherEncryption[data['weather'][0]['icon'][0:2]],
                    "temperature": (round(data['main']['temp_min'])-273, round(data['main']['temp_max'])-273),
                    "wind": "No wind" if data['wind']['speed'] < 0.2 else "Windy"}
        bot.send_message(message.chat.id,
                         f"{forecast['description'][0]} {forecast['description'][1]} {forecast['description'][0]}"
                         f"\n{forecast['temperature'][0]} - {forecast['temperature'][1]} °C"
                         f"\n{forecast['wind']} for today!")
    else:
        bot.send_message(message.chat.id, "???")


if __name__ == '__main__':
    bot.infinity_polling()
