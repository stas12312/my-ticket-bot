"""Формы для добавления сущностей"""
from aiogram.fsm.state import StatesGroup, State


class CityForm(StatesGroup):
    """Добавление города"""
    name = State()
    timezone = State()


class LocationForm(StatesGroup):
    """Добавление места"""
    city_id = State()
    name = State()
    address = State()


class EventForm(StatesGroup):
    """Добавление билета"""
    city_id = State()
    location_id = State()
    event_time = State()
    event_link = State()
    link = State()
    event_name = State()
    file_id = State()
