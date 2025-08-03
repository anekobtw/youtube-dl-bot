from aiogram import Router

from . import commands

router = Router()
router.include_router(commands.router)
