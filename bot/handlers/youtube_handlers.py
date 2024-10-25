import os
import yt_dlp
from aiogram import F, types, Router

from handlers.funcs import get_video_info
from keyboards import get_dl_kb

router = Router()

@router.callback_query(F.data == "delete_message")
async def delete_message(callback: types.CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data.startswith("https://www.youtube.com/watch?v="))
async def process_video(callback: types.CallbackQuery):
    await callback.message.edit_text(text=get_video_info(callback.data), reply_markup=get_dl_kb(callback.data))


@router.callback_query(F.data.startswith("audiodl_"))
async def download_audio(callback: types.CallbackQuery):
    with yt_dlp.YoutubeDL({"format": "bestaudio/best", "outtmpl": "audio.mp3", "quiet": True}) as yt:
        video_info = yt.extract_info(callback.data[8:])

    await callback.message.answer_audio(
        audio=types.FSInputFile("audio.mp3"),
        title=f"{video_info['title']}",
        caption="<b>@free_yt_dl_bot</b>",
        thumbnail=types.FSInputFile("pfp.jpg"),
    )
    os.remove("audio.mp3")
