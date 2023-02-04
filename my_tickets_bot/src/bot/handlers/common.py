"""Роутер с общими обработчиками"""
from aiogram import Router, types
from aiogram.filters import Command

from services.repository import Repo
from ..keybaords import get_menu_keyboard


async def start_handler(
        message: types.Message,
        repo: Repo,
):
    """Обработчик команды /start"""

    keyboard = get_menu_keyboard()

    user = message.from_user

    await repo.save_user(user.id, user.username)

    await message.answer(
        text='Приветствуем в "Мои билеты"',
        reply_markup=keyboard,
    )


common_handlers = Router()

common_handlers.message.register(start_handler, Command(commands='start'))
