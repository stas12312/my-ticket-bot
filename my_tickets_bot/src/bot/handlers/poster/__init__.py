from aiogram import Router

from . import show

router = Router()
router.include_router(show.router)
