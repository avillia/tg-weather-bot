from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.common.models import User
from app.common.services.weather import obtain_weather
from app.configs.extensions import Session


async def cmd_start(message: Message, state: FSMContext):
    with Session() as session:
        user = session.query(User).get(message.from_user.id)
    await message.reply(
        obtain_weather(user.last_latitude, user.last_longitude).as_message
    )