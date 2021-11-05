from datetime import datetime
from pytz import timezone

from apscheduler.triggers.date import DateTrigger

from app.configs.extensions import Session, scheduler
from app.common.models import ScheduledForecast
from app import bot
from app.common.services.weather import obtain_weather


async def send_forecast_for_user(user_id: int, latitude: float, longitude: float):
    await bot.send_message(user_id, obtain_weather(latitude, longitude).as_message)


def schedule_forecasts_in_db():
    with Session() as session:
        forecasts: list[ScheduledForecast] = session.query(ScheduledForecast).all()
    for forecast in forecasts:
        scheduled_time = DateTrigger(forecast.time, timezone(forecast.user.timezone))
        scheduler.add_job(send_forecast_for_user, args=[forecast.user_id, forecast.user.last_latitude, forecast.user.last_longitude], replace_existing=True)

# def setup_scheduler()