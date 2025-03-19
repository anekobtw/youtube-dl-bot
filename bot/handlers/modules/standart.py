import yt_dlp
from aiogram import F, Router, types

from handlers.modules.master import master_handler

router = Router()


def download_tiktok(url: str, filename: str) -> str:
    opts = {
        "format": "best",
        "outtmpl": filename,
        "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"},
    }
    with yt_dlp.YoutubeDL(opts) as yt:
        yt.download([url])
    return filename


links = [
    "https://www.tiktok.com/",
    "https://vt.tiktok.com/",
    "https://vm.tiktok.com/",
    "https://www.instagram.com/reel/",
    "https://instagram.com/reel/",
    "https://www.instagram.com/share/",
    "https://x.com/",
    "https://twitter.com/",
]


@router.message(F.text.startswith(tuple(links)))
async def tiktok(message: types.Message) -> None:
    filename = f"{message.from_user.id}.mp4"
    await master_handler(
        message=message,
        send_function=message.answer_video,
        download_function=lambda: download_tiktok(message.text, filename),
        url=message.text,
    )
