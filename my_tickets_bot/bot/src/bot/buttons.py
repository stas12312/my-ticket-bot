"""Клавиши"""
from enum import StrEnum


class MainMenu(StrEnum):
    """Главное меню"""
    MY_EVENTS = '✨ Мои мероприятия'
    ADD_EVENT = '➕ Добавить'
    SETTINGS = '⚙ Настройки'
    POSTER = '🗓 Афиша'


class Settings(StrEnum):
    """Настройки"""
    CITIES_AND_PLACES = '🏙 Города и места'
    ADD_CITY = '➕ Добавить город'
    DELETE_CITY = '🗑 Удалить город'
    PLACES = '🎭 Места'

    MY_PLACES = '🎭 Мои места'
    ADD_LOCATION = '➕ Добавить место'
    DELETE_LOCATION = '🗑 Удалить место'

    BACK = '◀️ Назад'
    CLOSE = '❌ Закрыть'


class Action(StrEnum):
    """Кнопки для действий"""
    DELETE = '🗑 Удалить'
    ADD = '➕ Добавить'
    PASS = '▶️ Пропустить'
    EDIT = '✏ Редактировать'
    BACK = '◀️ Назад'


class Event(StrEnum):
    """Кнопки для мероприятий"""
    ADD_TICKET = '➕ Билет'
    ADD_IN_CALENDAR = '🗓 Добавить в календарь'
    PLANNED = '📆 Планируемые'
    PAST = '🗃 Прошедшие'


class Pagination(StrEnum):
    """Кнопки для пагинации"""
    NEXT = '⏭'
    PREV = '⏮'
