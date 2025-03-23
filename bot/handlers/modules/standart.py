import yt_dlp
from aiogram import F, Router, types
from enums import Links
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


@router.message(F.text.startswith(tuple(Links.STANDART.value)))
async def tiktok(message: types.Message) -> None:
    filename = f"{message.from_user.id}.mp4"
    await master_handler(
        message=message,
        send_function=message.answer_video,
        download_function=lambda: download_tiktok(message.text, filename),
        url=message.text,
    )
