"""Клавиши"""
from enum import StrEnum


class MainMenu(StrEnum):
    """Главное меню"""
    MY_TICKETS = '🎫 Мои билеты'
    ADD_TICKET = '🆕 Добавить билет'
    SETTINGS = '⚙ Настройки'


class Settings(StrEnum):
    """Настройки"""
    MY_CITIES = '🏙 Мои города'
    ADD_CITY = '🆕 Добавить город'
    DELETE_CITY = '🗑 Удалить город'

    MY_PLACES = '🎭 Мои места'
    ADD_LOCATION = '🆕 Добавить место'
    DELETE_LOCATION = '🗑 Удалить место'

    BACK = '◀️ Назад'
    CLOSE = '❌ Закрыть'


class Action(StrEnum):
    """Кнопки для действий"""
    DELETE = '🗑 Удалить'
