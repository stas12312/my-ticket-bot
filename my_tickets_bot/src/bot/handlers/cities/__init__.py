"""Обработчики для городов"""
from aiogram import Router

from . import add, delete, show

router = Router()
router.include_router(add.router)
router.include_router(delete.router)
router.include_router(show.router)
