from aiogram import executor

from app import dp as bot


if __name__ == '__main__':

    executor.start_polling(bot, skip_updates=True)
