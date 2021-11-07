# avillia-weather-bot
Small telegram bot to get weather forecasts.

## How to setup?
1. Create `configs.ini` _(use `sample.configs.ini` as en example)_
2. Obtain tokens:   
    1. Create your bot token in [BotFather](https://t.me/BotFather) ([here](https://core.telegram.org/bots#6-botfather) is detailed instruction)
    2. Register and obtain api token in [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)
    3. Same step for [IpGeolocation](https://ipgeolocation.io/signup.html)
3. Paste them in related fields in `configs.ini`
4. Set up your dbs (however, this step is __optional__, by default data stored in memory):
    1. Set up your db and set `DATABASE_URI` in `configs.ini`
    2. Set up your redis and set `REDIS_HOST`
5. Run `bot.py`

## Why it doesn't work on my desktop???
Ah, and yes, there is no desktop version support, because of using geolocation. And it will probably __never__ come. Only mobile.
