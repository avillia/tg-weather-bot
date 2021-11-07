from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    first_geolocation_request = State()
    forecasting = State()
    scheduling = State()
