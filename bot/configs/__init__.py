from configparser import ConfigParser

from requests_cache import RedisCache
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

configs = ConfigParser()
configs.read_file("config.ini")

storages = configs["DATABASES"]

DATABASE_URI = storages.get("DATABASE_URI", "sqlite:///:memory:")

if fsm_storage := configs.get("FSM_STORAGE", ""):
    FSM_STORAGE = RedisStorage(host=fsm_storage, db=4)
else:
    FSM_STORAGE = MemoryStorage

if requests_cache := configs.get("REQUESTS_CACHE", ""):
    REQUESTS_CACHE = RedisStorage(host=requests_cache)




TELEGRAM_BOT_TOKEN = configs["TELEGRAM_BOT_TOKEN"]
IPGEOLOCATION_TOKEN = configs["IPGEOLOCATION_TOKEN"]
OPENWEATHERMAP_TOKEN = configs["OPENWEATHERMAP_TOKEN"]