from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    last_latitude = Column(Float, unique=False)
    last_longitude = Column(Float, unique=False)
    forecasts = relationship("ScheduledForecast")


class ScheduledForecast(Base):
    __tablename__ = 'scheduled_forecasts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    latitude = Column(Float, unique=False)
    longitude = Column(Float, unique=False)
