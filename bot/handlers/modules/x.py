import json
import re
import time

import yt_dlp
from aiogram import F, Router, types

from handlers.modules.master import master_handler

router = Router()


def vids_count(url: str) -> int:
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        if "entries" in info:
            return len(info["entries"])
        return 1


def download_x(url: str, filename: str, video_index: int = 0) -> str:
    with yt_dlp.YoutubeDL({"outtmpl": filename, "format": "best"}) as ydl:
        info = ydl.extract_info(url, download=False)
        if "entries" in info:
            url = info["entries"][video_index]["url"]
        ydl.download([url])
    return filename


links = [
    "https://x.com/",
    "https://twitter.com/",
]


def keyboard(number: int, url: str) -> types.InlineKeyboardMarkup:
    kb = [[types.InlineKeyboardButton(text=f"Видео {i+1}", callback_data=f"{url}!{i}")] for i in range(number)]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


@router.message(F.text.startswith(tuple(links)))
async def x(message: types.Message) -> None:
    count = vids_count(message.text)

    if count > 1:
        await message.delete()
        await message.answer("В публикации найдено несколько видео. Пожалуйста, выберите какое именно хотите скачать", reply_markup=keyboard(count, message.text))
    else:
        filename = f"{time.time_ns()}-{message.from_user.id}.mp4"
        await master_handler(
            message=message,
            send_function=message.answer_video,
            download_function=lambda: download_x(message.text, filename),
        )


@router.callback_query(lambda c: c.data.startswith(tuple(links)))
async def x2(callback: types.CallbackQuery) -> None:
    data = callback.data.split("!")
    filename = f"{time.time_ns()}-{callback.message.from_user.id}.mp4"

    await master_handler(
        message=callback.message,
        send_function=callback.message.answer_video,
        download_function=lambda: download_x(data[0], filename, int(data[-1])),
    )
