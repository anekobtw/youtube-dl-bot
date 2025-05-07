from aiogram import F, Router, types
from aiogram.filters import Command

from enums import Links
from handlers.downloader import Downloader

router = Router()


@router.message(F.text.startswith(tuple(Links.STANDART.value)))
async def _(message: types.Message) -> None:
    dl = Downloader(message, message.text, "video")
    await dl.run()


@router.message(F.text, Command("a"))
async def _(message: types.Message) -> None:
    _, url = message.text.split(" ")
    dl = Downloader(message, url, "audio")
    await dl.run()


@router.message(F.text)
async def _(message: types.Message) -> None:
    if message.text.startswith("a "):
        _, url = message.text.split(" ")
        dl = Downloader(message, url, "audio")
        await dl.run()
