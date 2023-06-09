from aiogram.filters.callback_data import CallbackData

from bot.callbacks.action import EntityAction


class TicketCallback(CallbackData, prefix='tickets'):
    """CallbackData для работы с билетами"""
    action: EntityAction
    event_id: int | None
    ticket_id: int | None
