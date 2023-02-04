"""Обработчики для работы с билетами"""
from aiogram import Router
from aiogram import types
from aiogram.filters import Text

from ..buttons import MainMenu


async def add_ticket_handler(message: types.Message):
    """Добавление билета"""
    await message.answer('Начало добавления билета')


async def my_tickets_handler(message: types.Message):
    """Отображения билетов"""
    await message.answer('Ваши билеты')


tickets_handler = Router()

tickets_handler.message.register(add_ticket_handler, Text(text=MainMenu.ADD_TICKET))
tickets_handler.message.register(my_tickets_handler, Text(text=MainMenu.MY_TICKETS))
