from configparser import ConfigParser

configs = ConfigParser()
configs.read_file("config.ini")

DATABASE_URI = configs.get("DATABASE_URI", "sqlite:///:memory:")

TELEGRAM_BOT_TOKEN = configs["TELEGRAM_BOT_TOKEN"]
IPGEOLOCATION_TOKEN = configs["IPGEOLOCATION_TOKEN"]
OPENWEATHERMAP_TOKEN = configs["OPENWEATHERMAP_TOKEN"]
