from aiogram import Router

from . import tiktok, x, youtube

router = Router()
router.include_router(youtube.router)
router.include_router(tiktok.router)
router.include_router(x.router)
