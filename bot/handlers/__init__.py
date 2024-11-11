"""
Router variable from here is used in main.py file
"""

from aiogram import Router

from handlers import common

router = Router()
router.include_router(common.router)
