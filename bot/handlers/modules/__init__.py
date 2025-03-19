from aiogram import Router

from . import standart, youtube

router = Router()
router.include_router(youtube.router)
router.include_router(standart.router)
