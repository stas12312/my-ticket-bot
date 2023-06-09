"""Команды бота"""
from enum import StrEnum

from aiogram.types import BotCommand


class AppCommand(StrEnum):
    """Команды бота"""
    START = 'start'
    CANCEL = 'cancel'
    STATISTIC = 'statistic'
    CHECK_DATE = 'check_date'


BOT_COMMANDS = [
    BotCommand(command=AppCommand.CANCEL, description='Отмена текущего действия'),
    BotCommand(command=AppCommand.STATISTIC, description='Статистика'),
    BotCommand(command=AppCommand.CHECK_DATE, description='Проверить занятость для даты')
]
