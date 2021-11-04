from aiogram import Bot, Dispatcher

from bot.configs import TELEGRAM_BOT_TOKEN

bot = Bot(TELEGRAM_BOT_TOKEN)
dp = Dispatcher(Bot)
