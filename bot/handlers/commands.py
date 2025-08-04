import asyncio
import os
import random

import httpx
import requests
import yt_dlp
from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from enums import Links, Messages
from find import find

router = Router()


async def download_video(url: str):
    opts = {
        "format": "bestvideo[filesize<45M]+bestaudio[filesize<5M]/worstvideo+worstaudio",
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def link_button(text: str, url: str):
    return types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=text, url=url)]])


@router.message(F.text.startswith(tuple(Links.STANDART.value)))
async def handle_download(message: types.Message):
    # --- Preparing ---
    await message.react([types.reaction_type_emoji.ReactionTypeEmoji(emoji="👀")])
    msg = await message.answer(Messages.API_Finding.f(url=message.text))
    ip = find()

    try:
        # --- Downloading from API ---
        if ip:
            await msg.edit_text(Messages.API_Found.f(url=message.text))

            async with httpx.AsyncClient(timeout=None) as client:
                r = await client.post(f"http://{ip}:8000/download", json={"url": message.text})
                response = r.json()

            if response["filesize"] < 50 * 1024 * 1024:
                await message.answer_video(
                    video=types.URLInputFile(response["video_url"]),
                    cover=types.URLInputFile(response["thumbnail_url"]),
                    caption=Messages.Caption.f(url=message.text),
                )
            else:
                await message.answer_photo(
                    photo=types.URLInputFile(response["thumbnail_url"]),
                    caption=Messages.VideoDownloaded.f(url=message.text),
                    reply_markup=link_button("Open url", response["video_url"]),
                )

        # --- Downloading on current device ---
        else:
            await msg.edit_text(Messages.API_NotFound.f(url=message.text))

            video_path = await download_video(message.text)

            await message.answer_video(
                video=types.FSInputFile(video_path),
                caption=Messages.Caption.f(url=message.text),
            )

            os.remove(video_path)

    except Exception:
        await msg.edit_text(Messages.ErrorOccured.f(url=message.text))
        return

    # --- Clearing up and promoting ---
    await message.delete()
    await msg.delete()

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


@router.message(Command("api"))
async def api(message: types.Message) -> None:
    await message.answer(Messages.Api.f(status="🟢 Online" if find() else "🔴 Offline"))
