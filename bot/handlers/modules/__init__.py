from aiogram import Router

from . import youtube, tiktok, x, spotify, pinterest

router = Router()
router.include_router(youtube.router)
router.include_router(tiktok.router)
router.include_router(x.router)
router.include_router(spotify.router)
router.include_router(pinterest.router)
