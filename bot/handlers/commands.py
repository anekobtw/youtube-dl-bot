import asyncio
import os
import random

import yt_dlp
from aiogram import F, Router, exceptions, types
from aiogram.filters import CommandStart

from enums import Links, Messages

router = Router()


async def download_video(url: str) -> str:
    opts = {
        "format": "bestvideo[ext=mp4][filesize<45M]+bestaudio[filesize<5M]/worstvideo[ext=mp4]+worstaudio",
        "merge-output-format": "mp4",
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def link_button(text: str, url: str) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=text, url=url)]])


@router.message(F.text.startswith(tuple(Links.STANDART.value)))
async def handle_download(message: types.Message):
    # --- Preparing ---
    await message.react([types.reaction_type_emoji.ReactionTypeEmoji(emoji="👀")])
    msg = await message.answer(Messages.VideoDownloading.f(url=message.text))

    # --- Downloading ---
    try:
        video_path = await download_video(message.text)

        await msg.edit_text(Messages.VideoDownloaded.f(url=message.text))

        await message.answer_video(
            video=types.FSInputFile(video_path),
            caption=Messages.Caption.f(url=message.text),
        )

    except exceptions.TelegramEntityTooLarge:
        await msg.edit_text(Messages.VideoNotSent.f(url=message.text))
        return

    except Exception:
        await msg.edit_text(Messages.ErrorOccured.f(url=message.text))
        return

    # --- Clearing up and promoting ---
    await message.delete()
    await msg.delete()
    os.remove(video_path)

    if random.randint(1, 5) == 1:
        promo_msg = await message.answer(Messages.Promo.value)
        await asyncio.sleep(15)
        await promo_msg.delete()


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.answer(
        text=Messages.Start.f(username=message.from_user.username),
        reply_markup=link_button("📰 A Telegram channel with news", "t.me/anekobtw_c"),
    )
