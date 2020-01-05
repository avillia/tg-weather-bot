import telebot
from telebot import types
from db_manager import *
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import re, json, time
import requests


TOKEN = "881112302:AAGkYLGYifiKyUmUrtIvwfIjab01FVn6GFc"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
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

weather_button_text = "\U00002600 Weather \U000026C5"
time_button_text = "\U0001F562 Set time of daily forecast \U0001F551"
stop_button_text = "\U0001F6D1 Stop \U0001F6D1"

location_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_geo = types.KeyboardButton(text="\U0001F30E Send location! \U0001F30D", request_location=True)
location_keyboard.add(button_geo)

default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
get_weather_button = types.KeyboardButton(text=weather_button_text, )
get_time_button = types.KeyboardButton(text=time_button_text, )
default_keyboard.row(get_weather_button)
default_keyboard.row(get_time_button)

stop_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
stop_button = types.KeyboardButton(text=stop_button_text, )
stop_keyboard.add(stop_button)

empty_keyboard = types.ReplyKeyboardRemove(selective=False)


def time_schedule():
    current_time = time.asctime().split()[3][0:5]
    if current_time in database.get_all_times():
        for user in database.get_users_by_time(current_time):
            bot.send_message(user, forecast_message(**obtain_weather(user)))


def obtain_weather(chat):
    coords = database.get_current_coords(chat)
    response = requests.get(
        f"https://api.openweathermap.org/"
        f"data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid=ef1d46cf281271e9a6cd05ac3fc2d2f7")

    data = json.loads(response.content.decode('utf8').replace("'", '"'))
    forecast = {"description": weatherEncryption[data['weather'][0]['icon'][0:2]],
                "temperature": (round(data['main']['temp_min']) - 273, round(data['main']['temp_max']) - 273),
                "wind": "No wind" if data['wind']['speed'] < 0.3 else "Windy"}

    return forecast


def forecast_message(description, temperature, wind):
    return (f"{description[0]} {description[1]} {description[0]}"
            f"\n{temperature[0]} - {temperature[1]} °C"
            f"\n{wind} for today!")


@bot.message_handler(commands=["start"])
def start(message):
    try:
        database.reset_user(message.chat.id, )
    except TypeError:
        pass

    bot.send_message(message.chat.id,
                     "Hello there!\nI'm bot that can send you information about weather in your place!"
                     " Just send me your location via button under text field:",
                     reply_markup=location_keyboard)
    try:
        database.add_new_user(message.chat.id)
    except sqlite3.IntegrityError:
        pass
    database.set_user_state(1, message.chat.id, )


@bot.message_handler(commands=["restart"])
def reset(message):
    bot.send_message(message.chat.id, "All your settings were reset. /start again.", reply_markup=empty_keyboard)
    try:
        database.reset_user(message.chat.id, )
        database.set_user_state(0, message.chat.id, )
    except TypeError:
        pass


@bot.message_handler(commands=["weather"])
def weather_command(message):
    try:
        forecast = obtain_weather(message.chat.id)
        bot.send_message(message.chat.id, forecast_message(**forecast))
    except TypeError:
        bot.send_message(message.chat.id, "Nothing is configured yet! Use but bellow to set your location")
    except KeyError:
        bot.send_message(message.chat.id, "Nothing is configured yet! Use but bellow to set your location")


@bot.message_handler(commands=["stop"],
                     func=lambda message: database.get_current_state(message.from_user.id) in [2, 3])
def reset_time(message):
    bot.send_message(message.chat.id, "You've canceled daily forecasts!", reply_markup=default_keyboard)
    try:
        database.remove_user_time(message.chat.id)
        database.set_user_state(2, message.chat.id)
    except TypeError:
        pass


@bot.message_handler(commands=["time"])
def set_time_of_daily_forecast(message):
    bot.send_message(message.chat.id, "Send me time when I should send you message "
                                      "with weather forecast using format HH:MM : ",
                     reply_markup=stop_keyboard)
    database.set_user_state(3, message.chat.id, )


@bot.message_handler(func=lambda message: database.get_current_state(message.from_user.id) == 1)
def error_location_initialization(message):
    bot.send_message(message.chat.id,
                     "Please, send me your location with button bellow:")


@bot.message_handler(content_types=['location'],
                     func=lambda message: database.get_current_state(message.from_user.id) == 1)
def set_location_firstly(message):

    bot.send_message(message.chat.id,
                     "Thanks a lot! Now just ask me to show me weather with buttons bellow, "
                     "or you can set time when I should sent you daily forecast:", reply_markup=default_keyboard)
    database.update_coords(message.location.latitude, message.location.longitude, message.chat.id)
    database.set_user_state(2, message.chat.id, )


@bot.message_handler(content_types=['location'],
                     func=lambda message: database.get_current_state(message.from_user.id) == 2)
def update_location(message):
    bot.send_message(message.chat.id, "Your location is updated!")
    database.update_coords(message.location.latitude, message.location.longitude, message.chat.id)


@bot.message_handler(func=lambda message: database.get_current_state(message.from_user.id) == 3)
def time_processing(message):
    if re.match("[0-2][0-9]:[0-5][0-9]", message.text):
        if int(message.text[0:2]) < 24:
            bot.send_message(message.chat.id, f"Time was successfully set!\n"
                                              f"I'll send you daily forecast everyday at {message.text}. "
                                              f"You can easily discard it with /stop command.",
                             reply_markup=default_keyboard)
            database.update_time(message.text, message.chat.id)
            database.set_user_state(2, message.chat.id, )
        else:
            bot.send_message(message.chat.id, f"Invalid time format! Try again.\n"
                                              f"Send time in format HH:MM, for example 19:54 .",)
    elif message.text == stop_button_text:
        bot.send_message(message.chat.id, "You've canceled daily forecasts!",
                         reply_markup=default_keyboard)
        try:
            database.remove_user_time(message.chat.id)
            database.set_user_state(2, message.chat.id)
        except TypeError:
            pass
    else:
        bot.send_message(message.chat.id, f"Invalid time format! Try again.\n"
                                          f"Send time in format HH:MM, for example 19:54 .",)


@bot.message_handler(content_types=["text"],
                     func=lambda message: database.get_current_state(message.from_user.id) in [2, 3])
def non_commands_responding(message):
    if message.text == weather_button_text:
        forecast = obtain_weather(message.chat.id)
        bot.send_message(message.chat.id, forecast_message(**forecast))
    elif message.text == time_button_text:
        bot.send_message(message.chat.id, "Send me time when I should send you message "
                                          "with weather forecast using format HH:MM",
                         reply_markup=stop_keyboard)
        database.set_user_state(3, message.chat.id, )
    else:
        bot.send_message(message.chat.id, "???")


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Launched successfully!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://avillia-weather-bot.herokuapp.com/' + TOKEN)
    return "<b>Deployed and launched successfully!</b>", 200


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=time_schedule, trigger="interval", seconds=60)
    scheduler.start()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
