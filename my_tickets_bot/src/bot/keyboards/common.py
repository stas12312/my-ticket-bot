from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.buttons import MainMenu


def get_menu_keyboard() -> ReplyKeyboardMarkup:
    """Получение клавиатуры для меню"""
    builder = ReplyKeyboardBuilder()

    builder.row(KeyboardButton(text=MainMenu.MY_EVENTS), KeyboardButton(text=MainMenu.ADD_EVENT))
    builder.row(KeyboardButton(text=MainMenu.SETTINGS))

    return builder.as_markup(resize_keyboard=True)
