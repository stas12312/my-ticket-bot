"""Обработчики для настроек"""
from aiogram import Router
from aiogram import types
from aiogram.filters import Text

from ..buttons import MainMenu
from ..keybaords import get_settings_menu


async def my_settings_handler(message: types.Message):
    """Отображение настроек"""

    settings = get_settings_menu()
    await message.answer(
        text='Выберите нужный пункт',
        reply_markup=settings,
    )


settings_router = Router()
settings_router.message.register(my_settings_handler, Text(text=MainMenu.SETTINGS))
