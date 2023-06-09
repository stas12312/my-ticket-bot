from aiogram import Router

from . import add, delete, show, edit

router = Router()
router.include_router(add.router)
router.include_router(delete.router)
router.include_router(show.router)
router.include_router(edit.router)
