from datetime import datetime, time
from typing import Union

from aiogram import Bot
from apscheduler.triggers.date import DateTrigger
from dateparser import parse as parse_time
from pytz import timezone

from app.common.models import ScheduledForecast, User
from app.common.services.weather import obtain_weather
from app.configs.extensions import Session, scheduler


async def send_forecast_for_user(
    bot: Bot, user_id: int, latitude: float, longitude: float
):
    await bot.send_message(user_id, obtain_weather(latitude, longitude).as_message)


def schedule_forecast(bot: Bot, forecast_time: Union[time, datetime], user: User):
    if isinstance(forecast_time, datetime):
        forecast_time = forecast_time.time()
    scheduled_time = DateTrigger(
        parse_time(str(forecast_time)), timezone(user.timezone)
    )
    scheduler.add_job(
        send_forecast_for_user,
        args=[bot, user.id, user.last_latitude, user.last_longitude],
        trigger=scheduled_time,
        replace_existing=True,
    )


def schedule_forecasts_in_db(bot: Bot):
    with Session() as session:
        forecasts: list[ScheduledForecast] = session.query(ScheduledForecast).all()
    for forecast in forecasts:
        schedule_forecast(bot, forecast.time, forecast.user)


def setup_scheduler(bot: Bot):
    scheduler.add_job(
        schedule_forecasts_in_db,
        args=[bot],
        replace_existing=True,
        trigger="cron",
        hour=0,
        minute=0,
    )
    scheduler.start()
