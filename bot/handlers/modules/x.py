import time

import yt_dlp
from aiogram import F, Router, types
import re

from handlers.modules.master import master_handler

router = Router()


def download_x(url: str, filename: str) -> str:
    video_number = int(url.split('/')[-1])
    if video_number < 100:
        url = url.removesuffix(f"/{video_number}")
    else:
        video_number = 1

    opts = {
        "format": "best",
        "outtmpl": filename,
        "download_playlist": False,
        "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"},
    }

    with yt_dlp.YoutubeDL(opts) as yt:
        info = yt.extract_info(url, download=False)
        yt.download([info["entries"][video_number - 1]["url"]])

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
