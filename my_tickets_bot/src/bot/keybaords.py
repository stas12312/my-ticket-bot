"""Клавиатуры"""
from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder, KeyboardButton

from .buttons import MainMenu


def get_menu_keyboard() -> ReplyKeyboardMarkup:
    """Получение клавиатуры для меню"""
    builder = ReplyKeyboardBuilder()

    builder.row(KeyboardButton(text=MainMenu.MY_TICKETS), KeyboardButton(text=MainMenu.ADD_TICKET))
    builder.row(KeyboardButton(text=MainMenu.SETTINGS))

    return builder.as_markup(resize_keyboard=True)
