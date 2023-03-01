from aiogram.filters.callback_data import CallbackData

from bot.callbacks.action import EntityAction


class LocationCallback(CallbackData, prefix='locations'):
    """CallbackData для работы с местами"""
    action: EntityAction
    city_id: int | None
    location_id: int | None
