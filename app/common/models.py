from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.configs.extensions import db

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    last_latitude = Column(Float, unique=False, nullable=True)
    last_longitude = Column(Float, unique=False, nullable=True)
    timezone = Column(String(32), unique=False, nullable=True)
    forecasts = relationship("ScheduledForecast", backref="user")


class ScheduledForecast(Base):
    __tablename__ = "scheduled_forecasts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float, unique=False)
    longitude = Column(Float, unique=False)


Base.metadata.create_all(db)
