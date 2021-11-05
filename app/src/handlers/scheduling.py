from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.common.models import User
from app.common.services.weather import obtain_weather
from app.common.services.timezone import fetch_timezone
from app.configs.extensions import Session, scheduler
from app.src.fsm import UserState
from app.src.ui import cancel_keyboard


async def ask_user_time(message: Message):
    with Session() as session:
        user: User = session.query(User).get(message.from_user.id)
