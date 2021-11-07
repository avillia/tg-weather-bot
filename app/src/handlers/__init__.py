from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType

from app.src.fsm import UserState
from app.src.handlers.common import (cmd_cancel, cmd_start, not_a_location,
                                     not_found)
from app.src.handlers.forecast import weather_by_button, weather_by_location
from app.src.handlers.scheduling import (ask_user_time, process_user_input,
                                         show_user_forecasts,
                                         updated_list_on_deletion)
from app.src.ui import (cancel_button_text, forecasts_button_text,
                        schedule_button_text, weather_button_text)
from app.src.ui.inlines import forecast_cb


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(
        cmd_cancel, Text(equals=cancel_button_text), state=[UserState.scheduling]
    )


def register_handlers_forecast(dp: Dispatcher):
    dp.register_message_handler(
        weather_by_location,
        content_types=[ContentType.LOCATION],
        state=[UserState.first_geolocation_request, UserState.forecasting],
    )
    dp.register_message_handler(
        weather_by_button,
        Text(equals=weather_button_text),
        state=[UserState.forecasting],
    )


def register_handlers_scheduling(dp: Dispatcher):
    dp.register_message_handler(
        ask_user_time, Text(equals=schedule_button_text), state=[UserState.forecasting]
    )
    dp.register_message_handler(
        process_user_input,
        content_types=[ContentType.TEXT],
        state=[UserState.scheduling],
    )
    dp.register_message_handler(
        show_user_forecasts,
        Text(equals=forecasts_button_text),
        state=[UserState.forecasting],
    )
    dp.register_callback_query_handler(
        updated_list_on_deletion, forecast_cb.filter(), state=[UserState.forecasting]
    )


def register_handlers_none_of_above(dp: Dispatcher):
    dp.register_message_handler(
        not_a_location, state=[UserState.first_geolocation_request]
    )
    dp.register_message_handler(not_found, state="*")
