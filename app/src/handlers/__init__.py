from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType

from app.src.fsm import UserState
from app.src.handlers.common import cmd_start, registration_completed, not_a_location


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(not_a_location, content_types=[ContentType.TEXT], state=[UserState.first_geolocation_request])
    dp.register_message_handler(registration_completed, content_types=[ContentType.LOCATION], state=[UserState.first_geolocation_request])
