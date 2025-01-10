from aiogram import Router

from . import pinterest, spotify, tiktok, youtube, x

router = Router()
router.include_router(youtube.router)
router.include_router(tiktok.router)
router.include_router(spotify.router)
router.include_router(pinterest.router)
router.include_router(x.router)
