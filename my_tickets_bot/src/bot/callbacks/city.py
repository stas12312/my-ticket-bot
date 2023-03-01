from aiogram.filters.callback_data import CallbackData

from bot.callbacks.action import EntityAction


class CityCallback(CallbackData, prefix='cities'):
    """CallbackData для работы с городами"""
    action: EntityAction
    city_id: int | None
