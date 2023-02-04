"""Callback данные"""
from enum import StrEnum

from aiogram.utils.keyboard import CallbackData


class EntityAction(StrEnum):
    """Действия с сущностями"""
    add = 'add'
    update = 'update'
    delete = 'delete'
    list = 'list'
    show = 'show'


class CityCallback(CallbackData, prefix='cities'):
    """CallbackData для работы с городами"""
    action: EntityAction
    city_id: int | None


class PlaceCallback(CallbackData, prefix='places'):
    """CallbackData для работы с местами"""
    action: EntityAction
    place_id: int | None
