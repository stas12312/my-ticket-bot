"""Формы для добавления сущностей"""
from aiogram.fsm.state import StatesGroup, State


class CityForm(StatesGroup):
    """Добавление города"""
    name = State()
    timezone = State()


class LocationForm(StatesGroup):
    """Добавление места"""
    input_name = State()
    input_address = State()
    input_url = State()


class EventForm(StatesGroup):
    """Добавление события"""
    city_id = State()
    location_id = State()
    event_time = State()
    event_link = State()
    link = State()
    event_name = State()
    file_id = State()


class EditEventForm(StatesGroup):
    """Редактирование события"""
    city_id = State()
    location_id = State()
    name = State()
    time = State()
    link = State()


class TicketForm(StatesGroup):
    """Добавление билета"""
    file = State()
