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


class SettingsCallback(CallbackData, prefix='settings'):
    """CallbackData для работы с натройками"""
    action: EntityAction


class CityCallback(CallbackData, prefix='cities'):
    """CallbackData для работы с городами"""
    action: EntityAction
    city_id: int | None


class PlaceCallback(CallbackData, prefix='places'):
    """CallbackData для работы с местами"""
    action: EntityAction
    place_id: int | None


class EventCallback(CallbackData, prefix='events'):
    """CallbackData для работы с событиями"""
    action: EntityAction
    event_id: int | None


class TicketCallback(CallbackData, prefix='tickets'):
    """CallbackData для работы с билетами"""
    action: EntityAction
    event_id: int | None
    ticket_id: int | None


class CloseCallback(CallbackData, prefix='close'):
    """CallbackData для закрытия меню"""
