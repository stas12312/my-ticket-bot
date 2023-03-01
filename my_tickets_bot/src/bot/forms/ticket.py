from aiogram.fsm.state import StatesGroup, State


class TicketForm(StatesGroup):
    """Добавление билета"""
    file = State()
