"""Клавиатуры"""
from typing import List

from aiogram.utils.keyboard import (
    ReplyKeyboardMarkup,
    ReplyKeyboardBuilder,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardBuilder,
)

from models import City
from .buttons import (
    MainMenu,
    Settings,
)
from .callbacks import CityCallback, EntityAction, PlaceCallback


def get_menu_keyboard() -> ReplyKeyboardMarkup:
    """Получение клавиатуры для меню"""
    builder = ReplyKeyboardBuilder()

    builder.row(KeyboardButton(text=MainMenu.MY_TICKETS), KeyboardButton(text=MainMenu.ADD_TICKET))
    builder.row(KeyboardButton(text=MainMenu.SETTINGS))

    return builder.as_markup(resize_keyboard=True)


def get_settings_menu() -> InlineKeyboardMarkup:
    """Получение клавиатуры для настроек"""
    builder = InlineKeyboardBuilder()
    print(CityCallback(action=EntityAction.list).pack())
    builder.row(
        InlineKeyboardButton(
            text=Settings.MY_CITIES,
            callback_data=CityCallback(action=EntityAction.list).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=Settings.MY_PLACES,
            callback_data=PlaceCallback(action=EntityAction.list).pack()
        ),
    )

    return builder.as_markup()


def get_cities_menu(
        cities: List[City]
) -> InlineKeyboardMarkup:
    """Получение клавиатуры для выбора города"""
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=Settings.ADD_CITY, callback_data=CityCallback(action=EntityAction.add)))

    return builder.as_markup()
