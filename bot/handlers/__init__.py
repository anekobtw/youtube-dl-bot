from aiogram import Router

from . import common, modules

router = Router()
router.include_router(common.router)
router.include_router(modules.router)
