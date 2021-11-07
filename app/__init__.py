from aiogram import Bot, Dispatcher

from app.configs import TELEGRAM_BOT_TOKEN, TG_STORAGE
from app.src.handlers import register_handlers_common, register_handlers_forecast, register_handlers_scheduling, register_handlers_none_of_above
from app.src.scheduler import setup_scheduler

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, storage=TG_STORAGE)

setup_scheduler(bot)

register_handlers_common(dp)
register_handlers_forecast(dp)
register_handlers_scheduling(dp)
register_handlers_none_of_above(dp)
