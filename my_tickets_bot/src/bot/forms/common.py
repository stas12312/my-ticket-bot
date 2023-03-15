from aiogram.fsm.state import StatesGroup, State


class CheckDateForm(StatesGroup):
    """Состояние для проверки даты"""
    input_date = State()
