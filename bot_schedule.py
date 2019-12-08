import time
from bot_main import *


def time_schedule():
    current_time = time.asctime().split()[3][0:5]
    if current_time in database.get_all_times():
        for user in database.get_users_by_time(current_time):
            bot.send_message(user, forecast_message(**obtain_weather(user)))


while True:
    time_schedule()
    time.sleep(60)
