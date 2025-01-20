import time

import yt_dlp
from aiogram import F, Router, types
from youthon import Video

from handlers.modules.master import master_handler

router = Router()


def get_ydl_opts(quality: str, filename: str) -> dict:
    formats = {
        "fhd": {"format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]", "merge_output_format": "mp4", "postprocessor_args": ["-c:v", "h264", "-c:a", "aac"]},
        "hd": {"format": "best[height<=720][ext=mp4]"},
        "sd": {"format": "best[height<=480][ext=mp4]"},
        "audio": {"format": "bestaudio[ext=m4a]", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]},
    }
    opts = {"outtmpl": filename, "postprocessors": [{"key": "FFmpegFixupM4a"}, {"key": "FFmpegFixupStretched"}]}
    return {**opts, **formats[quality]}


def download_youtube(url: str, filename: str, quality: str) -> str:
    fname = filename[:-4] if quality in ["best", "fhd", "audio"] else filename
    with yt_dlp.YoutubeDL(get_ydl_opts(quality, fname)) as ydl:
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
    try:
        await message.answer_photo(
            photo=Video(message.text).thumbnail_url,
            caption="Выберите качество загрузки:",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(text="📹 Full HD (1080p) (Долго)", callback_data=f"{message.text}!fhd")],
                    [types.InlineKeyboardButton(text="📹 HD (720p) (Быстро)", callback_data=f"{message.text}!hd")],
                    [types.InlineKeyboardButton(text="📹 SD (480p) (Быстро)", callback_data=f"{message.text}!sd")],
                    [types.InlineKeyboardButton(text="🎵 Только аудио", callback_data=f"{message.text}!audio")],
                ],
            ),
        )
        await message.delete()
    except Exception as e:
        await message.answer(f"Ошибка при получении информации о видео: {str(e)}")


@router.callback_query(lambda c: c.data.count("!") == 1)
async def process_download(callback: types.CallbackQuery) -> None:
    url, quality = callback.data.split("!")
    extension = "mp3" if quality == "audio" else "mp4"
    filename = f"{time.time_ns()}-{callback.message.from_user.id}.{extension}"

    await master_handler(
        message=callback.message,
        send_function=callback.message.answer_video if quality != "audio" else callback.message.answer_audio,
        download_function=lambda: download_youtube(url, filename, quality),
    )
