from apscheduler.schedulers.asyncio import AsyncIOScheduler
from requests_cache import CachedSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tzlocal import get_localzone

from app.configs import (
    DATABASE_URI,
    IPGEO_CACHE,
    OPENWEATHER_CACHE,
    SCHEDULER_JOBS_STORE,
)

db = create_engine(DATABASE_URI)
Session = sessionmaker(db)

ipgeo_request = CachedSession("ipgeolocation_cache", IPGEO_CACHE, expire_after=86400)
openweather_request = CachedSession(
    "openweathermap_cache", OPENWEATHER_CACHE, expire_after=300
)

scheduler = AsyncIOScheduler(
    timezone=get_localzone(),
    jobstores={"default": SCHEDULER_JOBS_STORE},
    replace_jobs=True,
)
