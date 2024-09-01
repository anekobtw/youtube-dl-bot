import os

import youthon
import yt_dlp
from aiogram import F, exceptions, types

from handlers.common import router
from handlers.funcs import get_video_info
from keyboards import get_dl_kb


@router.callback_query(F.data == "delete_message")
async def delete_message(callback: types.CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data.startswith("https://www.youtube.com/watch?v="))
async def process_video(callback: types.CallbackQuery):
    await callback.message.edit_text(text=get_video_info(callback.data), reply_markup=get_dl_kb(callback.data))


@router.callback_query(F.data.startswith("audiodl_"))
async def download_audio(callback: types.CallbackQuery):
    msg = await callback.message.answer("[1/3] Подготовка к скачиванию")
    yt = yt_dlp.YoutubeDL(
        {
            "format": "bestaudio/best",
            "outtmpl": f"{callback.message.from_user.id}",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
        }
    )

    await msg.edit_text("[2/3] Скачивание аудио")
    yt.download(callback.data[8:])

    try:
        await msg.edit_text("[3/3] Отправка аудио")
        video_info = youthon.Video(callback.data[8:])
        await callback.message.answer_audio(
            audio=types.FSInputFile(path=f"{callback.message.from_user.id}.mp3"),
            title=f"{video_info.title}.mp3",
            caption="<b>@free_yt_dl_bot</b>",
            thumbnail=types.URLInputFile(video_info.thumbnail_url),
        )
        await msg.delete()
        os.remove(f"{callback.message.from_user.id}.mp3")
    except exceptions.TelegramEntityTooLarge:
        await msg.edit_text("Ошибка: Аудио слишком большое. Пожалуйста, выберите видео покороче.")


@router.callback_query(F.data.startswith("thumbnaildl_"))
async def download_thumbnail(callback: types.CallbackQuery):
    thumbnail_url = youthon.Video(callback.data[12:]).thumbnail_url
    await callback.message.answer_photo(photo=types.URLInputFile(thumbnail_url))
