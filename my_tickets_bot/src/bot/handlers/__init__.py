"""Обработчики"""
from aiogram import Router

from .cities import cities_handler
from .common import common_handlers
from .location import locations_handler
from .settings import settings_router
from .event import events_handler

# Главный роутер
main_router = Router()

main_router.include_router(common_handlers)
main_router.include_router(settings_router)
main_router.include_router(events_handler)
main_router.include_router(cities_handler)
main_router.include_router(locations_handler)
