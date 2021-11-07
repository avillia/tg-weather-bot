from datetime import datetime
from typing import Optional

from aiogram.types import CallbackQuery, Message
from dateparser import parse as parse_time
from sqlalchemy.exc import IntegrityError as SQLUniqueError

from app.common.models import ScheduledForecast, User
from app.configs.extensions import Session
from app.src.fsm import UserState
from app.src.scheduler import schedule_forecast
from app.src.ui import (cancel_keyboard, default_keyboard,
                        generate_inline_keyboard_for_forecasts)


async def ask_user_time(message: Message):
    await message.reply(
        "Send me time for scheduled forecast:", reply_markup=cancel_keyboard
    )
    await UserState.scheduling.set()


async def process_user_input(message: Message):
    time_for_forecast: Optional[datetime] = parse_time(message.text)
    if not time_for_forecast:
        await message.reply("Not correct time format! Please try again.")
    else:
        try:
            with Session() as session:
                with session.begin():
                    user: User = session.query(User).get(message.from_user.id)
                    session.add(
                        ScheduledForecast(
                            user_id=user.id, time=time_for_forecast.time()
                        )
                    )
                    schedule_forecast(message.bot, time_for_forecast, user)
            await UserState.forecasting.set()
            await message.reply(
                f"Great! Will send you forecasts each day at {time_for_forecast.time()}!",
                reply_markup=default_keyboard,
            )
        except SQLUniqueError:
            await message.reply(
                "Forecast for this time is already scheduled!\n"
                "You can view all your scheduled via button bellow \U0001F447"
            )


async def show_user_forecasts(message: Message):
    with Session() as session:
        user: User = session.query(User).get(message.from_user.id)
        forecasts: list[ScheduledForecast] = user.forecasts
    if not forecasts:
        await message.reply(
            "There is no forecasts scheduled yet!\n"
            "You can schedule them via button down there \U0001F447"
        )
    else:
        await message.reply(
            "Here are your scheduled forecasts. You can delete any of them by tapping related button:",
            reply_markup=generate_inline_keyboard_for_forecasts(forecasts),
        )


async def updated_list_on_deletion(call: CallbackQuery, callback_data: dict):
    forecast_id = callback_data["forecast_id"]
    with Session() as session:
        with session.begin():
            forecast = session.query(ScheduledForecast).get(forecast_id)
            session.delete(forecast)
        user: User = session.query(User).get(call.from_user.id)
        forecasts: list[ScheduledForecast] = user.forecasts
    if not forecasts:
        await call.message.edit_text(
            "There is no forecasts scheduled yet!\n"
            "You can schedule them via button down there \U0001F447"
        )
    else:
        await call.message.edit_reply_markup(
            generate_inline_keyboard_for_forecasts(forecasts)
        )
    await call.answer()
