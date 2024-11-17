from aiogram import Router

from handlers import common

router = Router()
router.include_router(common.router)
