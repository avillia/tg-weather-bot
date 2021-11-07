from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.common.models import User
from app.common.services.timezone import fetch_timezone
from app.common.services.weather import obtain_weather
from app.configs.extensions import Session
from app.src.fsm import UserState
from app.src.ui import default_keyboard


async def weather_by_location(message: Message, state: FSMContext):
    latitude, longitude = message.location.latitude, message.location.longitude
    with Session() as session:
        with session.begin():
            user = session.query(User).get(message.from_user.id)
            user.last_latitude, user.last_longitude = latitude, longitude
            user.timezone = fetch_timezone(latitude, longitude)

    current_state = await state.get_state()
    if "first" in current_state:
        text_to_reply = (
            "Thanks a lot! Now just ask me to show me weather "
            "with buttons bellow, or you can set time when "
            "I should sent you daily forecast.\n"
            "\U00002600 Have a nice day! \U00002600"
        )
        await UserState.forecasting.set()
    else:
        text_to_reply = "Your location is updated!"

    await message.reply(text_to_reply, reply_markup=default_keyboard)
    await message.answer(obtain_weather(latitude, longitude).as_message)


async def weather_by_button(message: Message):
    with Session() as session:
        user = session.query(User).get(message.from_user.id)
    await message.reply(
        obtain_weather(user.last_latitude, user.last_longitude).as_message
    )
