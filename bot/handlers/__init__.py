from aiogram import Router

from . import common, standart

router = Router()
router.include_router(common.router)
router.include_router(standart.router)
