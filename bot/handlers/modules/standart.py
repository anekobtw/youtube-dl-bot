from aiogram import F, Router, types

from enums import Links
from handlers.modules.master import download_handler, message_handler

router = Router()


@router.message(F.text.startswith(tuple(Links.STANDART.value)))
async def _(message: types.Message) -> None:
    await message_handler(message)


@router.callback_query(lambda c: c.data.startswith(tuple(Links.STANDART.value)))
async def _(callback: types.CallbackQuery) -> None:
    await download_handler(callback)
