"""Роутеры для мероприятия"""
from aiogram import Router

from . import add
from . import edit
from . import show

router = Router()
router.include_router(add.router)
router.include_router(edit.router)
router.include_router(show.router)
