from sqlalchemy import create_engine

from bot.configs import DATABASE_URI

db = create_engine(DATABASE_URI)
