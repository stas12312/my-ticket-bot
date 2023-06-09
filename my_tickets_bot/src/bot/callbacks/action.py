from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class CloseCallback(CallbackData, prefix='close'):
    """CallbackData для закрытия меню"""


class EntityAction(StrEnum):
    """Действия с сущностями"""
    ADD = 'add'
    UPDATE = 'update'
    DELETE = 'delete'
    LIST = 'list'
    SHOW = 'show'
    EDIT = 'edit'
