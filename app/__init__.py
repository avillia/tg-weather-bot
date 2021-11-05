from aiogram import Bot, Dispatcher

from app.configs import TELEGRAM_BOT_TOKEN, TG_STORAGE
from app.src.handlers import register_handlers_common

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, storage=TG_STORAGE)

register_handlers_common(dp)
