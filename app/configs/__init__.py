from configparser import ConfigParser

from redis import Redis
from requests_cache import RedisCache
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.redis import RedisJobStore

configs = ConfigParser()
configs.read("config.ini")

storages = configs["DATABASES"]
DATABASE_URI = storages.get("DATABASE_URI", "sqlite:///:memory:")

redis_host = storages.get("REDIS", "")
if redis_host:
    TG_STORAGE = RedisStorage2(host=redis_host, db=4)
    ipgeo_redis = Redis(host=redis_host, db=5)
    IPGEO_CACHE = RedisCache(connection=ipgeo_redis)
    openweather_redis = Redis(host=redis_host, db=6)
    OPENWEATHER_CACHE = RedisCache(connection=openweather_redis)
    SCHEDULER_JOBS_STORE = RedisJobStore(host=redis_host, db=7)
else:
    TG_STORAGE = MemoryStorage()
    IPGEO_CACHE = OPENWEATHER_CACHE = "memory"
    SCHEDULER_JOBS_STORE = SQLAlchemyJobStore(url=DATABASE_URI)

tokens = configs["TOKENS"]
TELEGRAM_BOT_TOKEN = tokens["TELEGRAM_BOT_TOKEN"]
IPGEOLOCATION_TOKEN = tokens["IPGEOLOCATION_TOKEN"]
OPENWEATHERMAP_TOKEN = tokens["OPENWEATHERMAP_TOKEN"]
