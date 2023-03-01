from aiogram.fsm.state import StatesGroup, State


class LocationForm(StatesGroup):
    """Добавление места"""
    input_name = State()
    input_address = State()
    input_url = State()
