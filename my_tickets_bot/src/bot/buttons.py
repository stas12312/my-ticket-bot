"""Клавиши"""
from enum import StrEnum


class MainMenu(StrEnum):
    """Главное меню"""
    MY_TICKETS = '🎫 Мои билеты'
    ADD_TICKET = '🆕 Добавить билет'
    SETTINGS = '⚙ Настройки'
