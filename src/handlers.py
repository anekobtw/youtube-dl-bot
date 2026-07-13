import logging
import os
import shutil
from pathlib import Path

from aiogram import F, Router, exceptions, types
from aiogram.filters import Command, CommandStart
from dotenv import load_dotenv

from enums import Links, ProgressState, VideoStatusMessages
from utils import VIDEOS_DIR, download_video, format_bytes, format_message

router = Router()
load_dotenv()

MAX_TELEGRAM_SIZE = 50 * 1024 * 1024
FILES_URL = os.getenv("FILES_URL")


@router.message(F.text.startswith(tuple(Links.STANDART.value)))
async def handle_standart_download(message: types.Message):
    filename = None
    url = message.text
    if not url:
        return

    await message.react([types.reaction_type_emoji.ReactionTypeEmoji(emoji="👀")])
    msg = await message.answer(format_message(ProgressState.PREPARING))

    try:
        info = await download_video(msg, url)
        filename = info["filename"]

        if os.path.getsize(filename) > MAX_TELEGRAM_SIZE:
            await msg.edit_text(
                VideoStatusMessages.VideoHostRedirect.value.format(
                    download_url=f"{FILES_URL}/{os.path.basename(filename)}"
                )
            )
            return

        await message.answer_video(
            video=types.FSInputFile(filename),
            caption=(VideoStatusMessages.Caption.value.format(url=url)),
            width=info["width"],
            height=info["height"],
        )
    except exceptions.TelegramEntityTooLarge:
        if filename:
            await message.answer(
                VideoStatusMessages.VideoHostRedirect.value.format(
                    download_url=f"{FILES_URL}/{os.path.basename(filename)}"
                )
            )
    except Exception as e:
        logging.exception(f"Download failed: {e}")
        await message.answer(VideoStatusMessages.VideoError.value)
    else:
        await msg.delete()
        await message.delete()


@router.message(Command("stats"))
async def stats(message: types.Message):
    if message.from_user.id != int(os.getenv("ADMIN_ID")):
        return

    counts = {}
    total_size = 0
    total_files = 0

    for file in VIDEOS_DIR.rglob("*"):
        if file.is_file():
            total_files += 1
            total_size += file.stat().st_size
            counts[file.suffix or "[none]"] = counts.get(file.suffix or "[none]", 0) + 1

    disk = shutil.disk_usage("/")
    text = [
        "<b>Videos:</b>",
        f"Files: {total_files}",
        f"Size: {format_bytes(total_size)}",
        "",
        "<b>Extensions:</b>",
    ]

    for ext, count in sorted(counts.items()):
        text.append(f"{ext}: {count}")

    text += [
        "",
        "<b>Disk:</b>",
        f"Used: {format_bytes(disk.used)} / {format_bytes(disk.total)}",
        f"Free: {format_bytes(disk.free)}",
    ]
    await message.answer("\n".join(text))


@router.message(Command("clean"))
async def clean(message: types.Message):
    if message.from_user.id != int(os.getenv("ADMIN_ID")):
        return

    deleted = 0
    for file in filter(Path.is_file, VIDEOS_DIR.rglob("*")):
        file.unlink()
        deleted += 1

    await message.answer(f"Deleted {deleted} files.")


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        f"Hello, @{message.from_user.username}! Just send the link to the video.\n\n"
        "ℹ️ <b>We don't collect any data.</b>\n\n"
        "❗ <b>If the bot isn't working, don't worry</b> — "
        "your request will be processed automatically once we're back online.\n\n"
        "🙏 <b>Please don't block the bot</b> — "
        "it needs to message you when the download is ready.",
    )
