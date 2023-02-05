"""Формы для добавления сущностей"""
from aiogram.fsm.state import StatesGroup, State


class CityForm(StatesGroup):
    """Добавление города"""
    name = State()
    timezone = State()


class PlaceForm(StatesGroup):
    city_id = State()
    name = State()
    address = State()
