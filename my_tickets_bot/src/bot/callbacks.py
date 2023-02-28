"""Callback данные"""
from enum import StrEnum

from aiogram.utils.keyboard import CallbackData


class EntityAction(StrEnum):
    """Действия с сущностями"""
    ADD = 'add'
    UPDATE = 'update'
    DELETE = 'delete'
    LIST = 'list'
    SHOW = 'show'
    EDIT = 'edit'


class EditEventField(StrEnum):
    """Названия полей для редактирования"""
    LOCATION = 'location'
    NAME = 'name'
    TIME = 'time'
    LINK = 'link'


class SettingsCallback(CallbackData, prefix='settings'):
    """CallbackData для работы с натройками"""
    action: EntityAction


class CityCallback(CallbackData, prefix='cities'):
    """CallbackData для работы с городами"""
    action: EntityAction
    city_id: int | None


class LocationCallback(CallbackData, prefix='locations'):
    """CallbackData для работы с местами"""
    action: EntityAction
    city_id: int | None
    location_id: int | None


class EventCallback(CallbackData, prefix='events'):
    """CallbackData для работы с событиями"""
    action: EntityAction
    event_id: int | None


class EditEventCallback(CallbackData, prefix='edit_event'):
    """CallbackData для редактирования события"""
    event_id: int | None
    field_name: EditEventField


class TicketCallback(CallbackData, prefix='tickets'):
    """CallbackData для работы с билетами"""
    action: EntityAction
    event_id: int | None
    ticket_id: int | None


class CloseCallback(CallbackData, prefix='close'):
    """CallbackData для закрытия меню"""


class PaginationCallback(CallbackData, prefix='page'):
    """CallbackData для пагинации"""
    object_name: str
    page: int | None
