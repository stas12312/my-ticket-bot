"""Роутер с общими обработчиками"""
from aiogram import Router, types
from aiogram.filters import Command


async def start_handler(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        text='Приветствуем в "Мои билеты"',
    )


common_handlers = Router()

common_handlers.message.register(start_handler, Command(commands='start'))
