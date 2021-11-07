from configparser import ConfigParser

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.memory import MemoryJobStore
from redis import Redis
from requests_cache import RedisCache

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
else:
    TG_STORAGE = MemoryStorage()
    IPGEO_CACHE = OPENWEATHER_CACHE = "memory"

# FIXME: implement pickling bot info so forecast jobs could be stored to db/redis
lSCHEDULER_JOBS_STORaE = MemoryJobStore()

tokens = configs["TOKENS"]
TELEGRAM_BOT_TOKEN = tokens["TELEGRAM_BOT_TOKEN"]
IPGEOLOCATION_TOKEN = tokens["IPGEOLOCATION_TOKEN"]
OPENWEATHERMAP_TOKEN = tokens["OPENWEATHERMAP_TOKEN"]
