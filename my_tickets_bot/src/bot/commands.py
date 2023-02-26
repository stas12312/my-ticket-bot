"""Команды бота"""
from enum import StrEnum

from aiogram.types import BotCommand


class AppCommand(StrEnum):
    """Команды бота"""
    START = 'start'
    CANCEL = 'cancel'
    STATISTIC = 'statistic'


BOT_COMMANDS = [
    BotCommand(command=AppCommand.CANCEL, description='Отмена текущего действия'),
    BotCommand(command=AppCommand.STATISTIC, description='Статистика'),
]
