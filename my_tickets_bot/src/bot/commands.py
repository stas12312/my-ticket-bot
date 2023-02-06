"""Команды бота"""
from enum import StrEnum

from aiogram.types import BotCommand


class AppCommand(StrEnum):
    START = 'start'
    CANCEL = 'cancel'


BOT_COMMANDS = [
    BotCommand(command=AppCommand.CANCEL, description='Отмена текущего действия'),
]
