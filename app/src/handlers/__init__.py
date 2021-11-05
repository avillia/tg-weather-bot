from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from app.src.fsm import UserState
from app.src.handlers.common import cmd_start, registration_completed, not_a_location


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(not_a_location, content_types=["location"], state=[UserState.first_geolocation_request])
    dp.register_message_handler(registration_completed, content_types=["location"], state=[UserState.first_geolocation_request])
