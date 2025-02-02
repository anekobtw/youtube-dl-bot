from aiogram import Router

from . import tiktok, x, youtube, yt_music

router = Router()
router.include_router(youtube.router)
router.include_router(tiktok.router)
router.include_router(x.router)
router.include_router(yt_music.router)
