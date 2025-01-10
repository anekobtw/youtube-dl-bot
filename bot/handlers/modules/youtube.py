import time

import yt_dlp
from aiogram import F, Router, types

from handlers.modules.master import master_handler

router = Router()


def download_youtube(url: str, filename: str) -> str:
    ydl_opts = {
        "outtmpl": filename,
        "merge_output_format": "mp4",
        "format": "bestvideo[height<=1080][filesize<=45M]+bestaudio[filesize<=5M]/best[vcodec=h264][height<=1080][filesize<=50M]",
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
            {"key": "FFmpegFixupM4a"},
            {"key": "FFmpegFixupStretched"},
        ],
        "postprocessor_args": ["-c:v", "h264", "-c:a", "aac"],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename


links = [
    "https://www.youtube.com/watch?v=",
    "https://youtu.be/",
    "https://www.youtube.com/shorts/",
    "https://youtube.com/shorts/",
]


@router.message(F.text.startswith(tuple(links)))
async def youtube(message: types.Message) -> None:
    filename = f"{time.time_ns()}-{message.from_user.id}.mp4"
    await master_handler(
        message=message,
        send_function=message.answer_video,
        download_function=lambda: download_youtube(message.text, filename),
    )
