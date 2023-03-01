from aiogram.filters.callback_data import CallbackData

from bot.callbacks.action import EntityAction


class SettingsCallback(CallbackData, prefix='settings'):
    """CallbackData для работы с натройками"""
    action: EntityAction
