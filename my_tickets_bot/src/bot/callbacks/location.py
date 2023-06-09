from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

from bot.callbacks.action import EntityAction


class LocationEditField(StrEnum):
    """Поля для редактирования места"""
    NAME = 'name'
    URL = 'url'
    ADDRESS = 'address'


class LocationCallback(CallbackData, prefix='locations'):
    """CallbackData для работы с местами"""
    action: EntityAction
    city_id: int | None
    location_id: int | None


class LocationEditCallback(CallbackData, prefix='edit_location'):
    """CallbackData для редактирования места"""
    location_id: int
    field: LocationEditField
