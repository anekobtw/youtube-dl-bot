"""
Handling options from keyboard.get_options_keyboard()
"""

import os

import yt_dlp
from aiogram import F, Router, types
from youthon import Video

from keyboards import get_options_keyboard
from handlers.funcs import get_video_info

router = Router()


@router.callback_query(F.data == "delete_message")
async def delete_message(callback: types.CallbackQuery):
    """Deleting orginial message"""
    await callback.message.delete()


@router.callback_query(F.data.startswith("https://www.youtube.com/watch?v="))
async def process_video(callback: types.CallbackQuery):
    """Sending a message with options"""
    await callback.message.edit_text(text=get_video_info(callback.data), reply_markup=get_options_keyboard(callback.data))


@router.callback_query(F.data.startswith("audiodl_"))
async def download_audio(callback: types.CallbackQuery):
    """Sending audio"""
    filename = f"@free_dl_music - {callback.message.from_user.id}.mp3"
    with yt_dlp.YoutubeDL({"format": "bestaudio/best", "outtmpl": filename, "quiet": True}) as yt:
        video_info = yt.extract_info(callback.data[8:])

    await callback.message.answer_audio(
        audio=types.FSInputFile(filename),
        title=f"{video_info['title']}",
        caption="<b>@free_yt_dl_bot</b>",
        thumbnail=types.FSInputFile("pfp.jpg"),
    )
    os.remove(filename)


@router.callback_query(F.data.startswith("thumbnaildl_"))
async def download_thumbnail(callback: types.CallbackQuery):
    """Sending a thumbnail"""
    await callback.message.answer_photo(
        photo=types.URLInputFile(Video(callback.data[12:]).thumbnail_url),
        caption="<b>@free_yt_dl_bot</b>",
    )
