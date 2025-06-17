import os
import random
import asyncio
import uuid

import requests
from aiogram import F, Router, types
from aiogram.filters import Command

from enums import Links
from handlers.downloader import Downloader

router = Router()


def publish(user_id: int, filename: str) -> str:
    url = f"https://filebin.net/{user_id}/{uuid.uuid4()}"
    headers = {"accept": "application/json", "cid": str(user_id), "Content-Type": "application/octet-stream"}

    with open(filename, "rb") as f:
        data = f.read()

    response = requests.post(url, headers=headers, data=data)
    res = response.json()
    return url


@router.message(F.text.startswith(tuple(Links.STANDART.value)))
async def handle_download(message: types.Message):
    msg = await message.answer(f"<code>{message.text}</code>\n\n⏳ Video | ⏳ Audio")
    caption = f"<b><i><a href='https://t.me/free_yt_dl_bot'>via</a> | <a href='{message.text}'>link</a></i></b>"

    downloader = Downloader()

    # download
    try:
        video_path = await downloader.run(message.text, "video")
        await msg.edit_text(f"<code>{message.text}</code>\n\n✔️ Video | ⏳ Audio")

        audio_path = await downloader.run(message.text, "audio")
        await msg.edit_text(f"<code>{message.text}</code>\n\n✔️ Video | ✔️ Audio")
    except Exception as e:
        await message.bot.send_message(
            chat_id=1718021890,
            text=f"❗ <code>{message.text}</code>\n\n{e}",
        )
        await msg.edit_text(f"<code>{message.text}</code>\n\n⚠️ An error occurred during download. This usually happens because the video is age-restricted (18+) or unavailable in the hosting country")
        return

    try:
        await message.answer_video(types.FSInputFile(video_path), caption=caption)
        await message.answer_audio(types.FSInputFile(audio_path), caption=caption)
    except Exception as e:
        await msg.edit_text(f"<code>{message.text}</code>\n\n⏳ Ошибка отправки файла в телеграм. Попытка выложить файл на filebin.")
        await message.answer(publish(message.from_user.id, video_path) + "\n\n" + caption)
        await message.answer_audio(types.FSInputFile(audio_path), caption=caption)


    # cleanup
    await message.delete()
    await msg.delete()
    os.remove(video_path)
    os.remove(audio_path)


    # Promote my telegram channel
    if random.randint(1, 5) == 1:
        promo_msg = await message.answer("Hi! I'm <b>@free_yt_dl_bot</b> — completely free, no ads, no mandatory subscriptions. If you like my work, check out my <b><a href='https://t.me/anekobtw_c'>Telegram news channel</a></b> — it’s a big support! 😊\n\n<b>This message will self-delete in 15 seconds</b>")
        await asyncio.sleep(15)
        await promo_msg.delete()


@router.message(F.text)
async def _(message: types.Message) -> None:
    if message.text.startswith("a "):
        _, url = message.text.split(" ")
        dl = Downloader(message, url, "audio")
        await dl.run()
