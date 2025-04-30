from aiogram import Router

from . import standart

router = Router()
router.include_router(standart.router)
