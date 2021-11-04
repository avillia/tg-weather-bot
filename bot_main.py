import requests

import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request

from db_manager import *

#######################################################UX SECTION#######################################################

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
time_button_text = "\U0001F562 New time of daily forecast \U0001F551"
stop_button_text = "\U0001F6D1 Stop daily forecasts \U0001F6D1"
cancel_button_text = "\U0000274C Cancel \U0000274C"
scheduled_button_text = "\U0001f55d Show scheduled \U00002753"

location_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_geo = types.KeyboardButton(text="\U0001F30E Send location! \U0001F30D", request_location=True)
location_keyboard.add(button_geo)

default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
get_weather_button = types.KeyboardButton(text=weather_button_text, )
get_time_button = types.KeyboardButton(text=time_button_text, )
stop_button = types.KeyboardButton(text=stop_button_text, )
show_scheduled_button = types.KeyboardButton(text=scheduled_button_text, )
default_keyboard.row(get_weather_button)
default_keyboard.row(get_time_button)
default_keyboard.row(show_scheduled_button, stop_button)

cancel_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = types.KeyboardButton(text=cancel_button_text, )
cancel_keyboard.add(cancel_button)

empty_keyboard = types.ReplyKeyboardRemove(selective=False)

####################################################HANDY FUNCTIONS#####################################################


def time_schedule():
    for time in database.get_all_times():
        for user in database.get_users_by_time(time):
            schedule_forecast(user=user, hours=time[2:], minute=time[-3:])


def schedule_forecast(user, hours, minute):
    scheduler.add_job(func=lambda: bot.send_message(user, forecast_message(**obtain_weather(user))),
                      id=str(user), trigger="cron", hour=str(hours), minute=str(minute), replace_existing=True)


def obtain_weather(chat):
    coords = database.get_current_coords(chat)
    data = requests.get(
        f"https://api.openweathermap.org/"
        f"data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid=ef1d46cf281271e9a6cd05ac3fc2d2f7").json()
    forecast = {"description": weatherEncryption[data['weather'][0]['icon'][0:2]],
                "temperature": (round(data['main']['temp_min']) - 273, round(data['main']['temp_max']) - 273),
                "wind": "No wind" if data['wind']['speed'] < 4 else "Windy"}

    return forecast


def forecast_message(description, temperature, wind):
    return (f"{description[0]} {description[1]} {description[0]}"
            f"\n{temperature[0]} - {temperature[1]} °C"
            f"\n{wind} for today!")


def get_coords_and_timezone_from_message(message):
    database.update_coords(message.location.latitude, message.location.longitude, message.chat.id)
    data = requests.get(f"https://api.ipgeolocation.io/timezone?apiKey=650c12f9f1ac4ebf9f5fc98aea31362d"
                        f"&lat={message.location.latitude}&long={message.location.longitude}").json()
    timezone = data['timezone_offset'] + (round(data['dst_savings']) if data['is_dst'] else 0)
    database.update_time_offset(timezone, message.chat.id, )

#######################################################MAIN MAGIC#######################################################


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


@bot.message_handler(content_types=['location'])
def updating_location(message):
    get_coords_and_timezone_from_message(message)

    if database.get_current_state(message.from_user.id) == 1:
        database.set_user_state(2, message.chat.id, )
        bot.send_message(message.chat.id,
                         "Thanks a lot! Now just ask me to show me weather "
                         "with buttons bellow, or you can set time when "
                         "I should sent you daily forecast:",
                         reply_markup=default_keyboard)
        forecast = obtain_weather(message.chat.id)
        bot.send_message(message.chat.id, forecast_message(**forecast))

    elif database.get_current_state(message.from_user.id) == 2:
        bot.send_message(message.chat.id, "Your location is updated!")
        forecast = obtain_weather(message.chat.id)
        bot.send_message(message.chat.id, forecast_message(**forecast))


@bot.message_handler(content_types=["text"])
def non_commands_responding(message):
    try:
        current_state = database.get_current_state(message.from_user.id)
        if current_state == 1:
            bot.send_message(message.chat.id,
                             "Please, send me your location with button bellow:")
        elif current_state == 2:
            if message.text == weather_button_text:
                try:
                    forecast = obtain_weather(message.chat.id)
                    bot.send_message(message.chat.id, forecast_message(**forecast),
                                     reply_markup=default_keyboard, )
                except TypeError or KeyError:
                    bot.send_message(message.chat.id,
                                     "Nothing is configured yet! "
                                     "Please, send me your location by a menu "
                                     "or using the button bellow:")
            elif message.text == time_button_text:
                database.set_user_state(3, message.chat.id, )
                bot.send_message(message.chat.id,
                                 "Send me time when I should send you message "
                                 "with weather forecast using format HH:MM : ",
                                 reply_markup=cancel_keyboard, )
            elif message.text == stop_button_text:
                bot.send_message(message.chat.id,
                                 "You've canceled daily forecasts!",
                                 reply_markup=default_keyboard, )
                database.remove_user_time(message.chat.id)
            elif message.text == scheduled_button_text:
                scheduled_info_message = database.get_time_by_user(message.chat.id)
                if scheduled_info_message:
                    hours, minutes = [int(i) for i in scheduled_info_message.split(":")]
                    hours = (hours + database.get_time_offset(message.chat.id)) % 24
                    bot.send_message(message.chat.id,
                                     f"You've scheduled your forecast for "
                                     f"{hours}:{minutes:02d} "
                                     f"\U0001f564",
                                     reply_markup=default_keyboard, )
                else:
                    bot.send_message(message.chat.id,
                                     f"No scheduled forecasts... yet! "
                                     f"\U0001f564",
                                     reply_markup=default_keyboard, )
            else:
                bot.send_message(message.chat.id, "???")
        elif current_state == 3:
            if message.text == cancel_button_text:
                database.set_user_state(2, message.chat.id)
                bot.send_message(message.chat.id,
                                 "Operation cancelled!",
                                 reply_markup=default_keyboard)
            else:
                try:
                    hours, minutes = [int(i) for i in message.text.split(":")]
                    if 0 <= hours < 24 and 0 <= minutes < 60:
                        time = f"{hours:02d}:{minutes:02d}"
                        hours = f"{((hours - database.get_time_offset(message.chat.id)) % 24):02d}"
                        minutes = f"{minutes:02d}"
                        database.update_time(f"{hours}:{minutes}",message.chat.id, )
                        schedule_forecast(user=message.chat.id, hours=hours, minute=minutes, )
                        database.set_user_state(2, message.chat.id, )
                        bot.send_message(message.chat.id,
                                         f"Time was successfully set!\n"
                                         f"I'll send you daily forecast everyday at {time}. "
                                         f"You can easily discard it with stop button.",
                                         reply_markup=default_keyboard, )
                    else:
                        raise ValueError
                except ValueError:
                    bot.send_message(message.chat.id,
                                     f"Invalid time format! Try again.\n"
                                     f"Send time in format HH:MM, for example 19:54.", )
    except TypeError:
        bot.send_message(message.chat.id,
                         "It seems to me that my creator once again "
                         "f*cked up with databases, what a shame!\U0001f622\n"
                         "Please, /restart and /start again.")


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Launched successfully!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://avillia-weather-bot.herokuapp.com/" +
                        TOKEN)
    return "<b>Deployed and launched successfully!</b>", 200


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=time_schedule, trigger="cron", hour=0, minute=0, )
    scheduler.start()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), debug=False, )
