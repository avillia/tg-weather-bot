from configparser import ConfigParser

from redis import Redis
from requests_cache import RedisCache
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

configs = ConfigParser()
configs.read("config.ini")

storages = configs["DATABASES"]

DATABASE_URI = storages.get("DATABASE_URI", "sqlite:///:memory:")

if fsm_redis_host := storages.get("FSM_STORAGE_REDIS", ""):
    TG_STORAGE = RedisStorage2(host=fsm_redis_host, db=4)
else:
    TG_STORAGE = MemoryStorage

if cache_redis_host := storages.get("REQUESTS_CACHE_REDIS", ""):
    ipgeo_redis = Redis(host=cache_redis_host, db=5)
    IPGEO_CACHE = RedisCache(connection=ipgeo_redis)
    openweather_redis = Redis(host=cache_redis_host, db=6)
    OPENWEATHER_CACHE = RedisCache(connection=openweather_redis)
else:
    IPGEO_CACHE = OPENWEATHER_CACHE = "memory"

tokens = configs["TOKENS"]

TELEGRAM_BOT_TOKEN = tokens["TELEGRAM_BOT_TOKEN"]
IPGEOLOCATION_TOKEN = tokens["IPGEOLOCATION_TOKEN"]
OPENWEATHERMAP_TOKEN = tokens["OPENWEATHERMAP_TOKEN"]
