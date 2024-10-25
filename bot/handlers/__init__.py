from aiogram import Router

from handlers import common, youtube_handlers

router = Router()
router.include_router(common.router)
router.include_router(youtube_handlers.router)
