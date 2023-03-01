from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

from bot.callbacks import EntityAction


class EditEventField(StrEnum):
    """Названия полей для редактирования"""
    LOCATION = 'location'
    NAME = 'name'
    TIME = 'time'
    LINK = 'link'


class EventCallback(CallbackData, prefix='events'):
    """CallbackData для работы с событиями"""
    action: EntityAction
    event_id: int | None


class EditEventCallback(CallbackData, prefix='edit_event'):
    """CallbackData для редактирования события"""
    event_id: int | None
    field_name: EditEventField
