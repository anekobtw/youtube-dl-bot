import time
import yt_dlp

from aiogram import F, Router, types

from handlers.modules.master import master_handler

router = Router()


def download_yandex(url: str, filename: str) -> str:
    opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
    }
    with yt_dlp.YoutubeDL(opts) as yt:
        yt.download([url])
    return filename

links = [
    "https://music.yandex.ru/track/"
]


@router.message(F.text.startswith(tuple(links)))
async def _(message: types.Message) -> None:
    filename = f"{time.time_ns()}-{message.from_user.id}.mp3"
    await master_handler(
        message=message,
        send_function=message.answer_audio,
        download_function=lambda: download_yandex(message.text, filename),
    )
