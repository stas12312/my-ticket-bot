"""Обработчики"""
from aiogram import Router

from .common import common_handlers
from .settings import settings_router
from .tickets import tickets_handler

# Главный роутер
main_router = Router()

main_router.include_router(common_handlers)
main_router.include_router(settings_router)
main_router.include_router(tickets_handler)
