import asyncio
import os
import random
import uuid

import requests
from aiogram import F, Router, types, exceptions
from aiogram.filters import Command

from enums import Links
from handlers.downloader import Downloader

router = Router()


def publish(user_id: int, filename: str) -> str:
    url = f"https://filebin.net/{uuid.uuid4()}/{uuid.uuid4()}"
    headers = {"accept": "application/json", "cid": str(user_id), "Content-Type": "application/octet-stream"}

    with open(filename, "rb") as f:
        data = f.read()

    response = requests.post(url, headers=headers, data=data)
    res = response.json()
    return url


async def log(message: types.Message, text: str):
    await message.bot.send_message(chat_id=1718021890, text=text, link_preview_options=types.LinkPreviewOptions(is_disabled=True))


@router.message(F.text.startswith(tuple(Links.STANDART.value)))
async def handle_download(message: types.Message):
    # prepare
    await message.react([types.reaction_type_emoji.ReactionTypeEmoji(emoji="👀")])
    caption = f"<b><i><a href='https://t.me/free_yt_dl_bot'>via</a> | <a href='{message.text}'>link</a></i></b>"
    msg = await message.answer(f"<code>{message.text}</code>\n\nYour download will start soon.")


    # download
    try:
        downloader = Downloader(message.text, msg)
        video_path, (width, height) = await downloader.run()
    except Exception as e:
        await log(message, f"❗ <code>{message.text}</code>\n\n{e}")
        await msg.edit_text(f"<code>{message.text}</code>\n\n⚠️ An error occurred during download. This usually happens because the video is age-restricted (18+).")
        return


    # send
    try:
        await message.answer_video(types.FSInputFile(video_path), caption=caption, width=width, height=height)
    except exceptions.TelegramEntityTooLarge:
        await msg.edit_text(f"<code>{message.text}</code>\n\n⏳ The video is too large for Telegram. Uploading to Filebin...")
        try:
            filebin_url = publish(message.from_user.id, video_path)
            await message.answer(f"{filebin_url}\n\n{caption}")
            await log(message, f"<code>{filebin_url}</code>")
        except Exception as e:
            await msg.edit_text("😔 We've hit all the limits. Filebin is temporarily not available.")


    # log and cleanup
    await log(message, f"✅ <code>{message.text}</code>")
    await message.delete()
    await msg.delete()
    os.remove(video_path)


    # Promote my telegram channel
    if random.randint(1, 5) == 1:
        promo_msg = await message.answer("Hi! I'm <b>@free_yt_dl_bot</b> — completely free, no ads, no mandatory subscriptions. If you like my work, check out my <b><a href='https://t.me/anekobtw_c'>Telegram news channel</a></b> — it’s a big support! 😊\n\n<b>This message will self-delete in 15 seconds</b>")
        await asyncio.sleep(15)
        await promo_msg.delete()
