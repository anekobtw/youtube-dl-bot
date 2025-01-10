from aiogram import Router

from . import pinterest, spotify, tiktok, youtube

router = Router()
router.include_router(youtube.router)
router.include_router(tiktok.router)
router.include_router(spotify.router)
router.include_router(pinterest.router)
