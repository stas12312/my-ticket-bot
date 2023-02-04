"""Роутер с общими обработчиками"""
from aiogram import Router, types
from aiogram.filters import Command

from ..keybaords import get_menu_keyboard


async def start_handler(message: types.Message):
    """Обработчик команды /start"""

    keyboard = get_menu_keyboard()

    await message.answer(
        text='Приветствуем в "Мои билеты"',
        reply_markup=keyboard,
    )


common_handlers = Router()

common_handlers.message.register(start_handler, Command(commands='start'))
