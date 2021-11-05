from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.common.models import User
from app.common.services.weather import obtain_weather
from app.configs.extensions import Session
from app.src.fsm import UserState
from app.src.ui import location_keyboard, default_keyboard


async def cmd_start(message: Message, state: FSMContext):
    with Session() as session:
        with session.begin():
            if user := session.query(User).get(message.from_user.id):
                session.delete(user)
            user = User(id=message.from_user.id)
            session.add(user)
    await UserState.first_geolocation_request.set()
    await message.reply(
        "Hello there!\n"
        "I'm bot that can send you information about weather in your place!"
        "Just send me your location via button under text field:",
        reply_markup=location_keyboard,
    )


async def not_a_location(message: Message):
    await message.reply(
        "Please, send me your location with button bellow:"
    )


async def registration_completed(message: Message):
    latitude, longitude = message.location.latitude, message.location.longitude
    with Session() as session:
        with session.begin():
            user = session.query(User).get(message.from_user.id)
            user.last_latitude, user.last_longitude = latitude, longitude
    await UserState.next()
    await message.answer(
        "Thanks a lot! Now just ask me to show me weather "
        "with buttons bellow, or you can set time when "
        "I should sent you daily forecast:",
        reply_markup=default_keyboard,
    )
    await message.reply(
        obtain_weather(latitude, longitude).as_message
    )


async def cmd_cancel(message: Message):
    await UserState.forecasting.set()
    await message.reply(
        "Action cancelled. Something else?",
        reply_markup=default_keyboard
    )
