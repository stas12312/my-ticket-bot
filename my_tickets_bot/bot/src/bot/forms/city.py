from aiogram.fsm.state import StatesGroup, State


class CityForm(StatesGroup):
    """Добавление города"""
    name = State()
    timezone = State()
