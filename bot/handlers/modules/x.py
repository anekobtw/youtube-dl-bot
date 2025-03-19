import time

import yt_dlp
from aiogram import F, Router, types

from handlers.modules.master import master_handler

router = Router()


def download_x(url: str, filename: str) -> str:
    with yt_dlp.YoutubeDL({"outtmpl": filename, "format": "best"}) as ydl:
        ydl.download([url])
    return filename


links = [
    "https://x.com/",
    "https://twitter.com/",
]


@router.message(F.text.startswith(tuple(links)))
async def x(message: types.Message) -> None:
    filename = f"{time.time_ns()}-{message.from_user.id}.mp4"
    await master_handler(
        message=message,
        send_function=message.answer_video,
        download_function=lambda: download_x(message.text, filename),
    )
