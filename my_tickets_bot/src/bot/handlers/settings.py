"""Обработчики для настроек"""
from aiogram import Router
from aiogram import types
from aiogram.filters import Text

from ..buttons import MainMenu


async def my_settings_handler(message: types.Message):
    """Отображение настроек"""
    await message.answer('Ваши настройки')


settings_router = Router()
settings_router.message.register(my_settings_handler, Text(text=MainMenu.SETTINGS))
