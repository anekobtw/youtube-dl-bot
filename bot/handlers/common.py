import os

from aiogram import Bot, F, Router, types, methods
from aiogram.filters import Command
from dotenv import load_dotenv
import time

import yt_dlp

from handlers import downloader

router = Router()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    await message.answer(text="Отправь боту ссылку на видео.\nПоддерживаемые ссылки - /supported_links\n\n<b>Мы не собираем никаких данных о Вас!</b>")


@router.message(F.text, Command("supported_links"))
async def usage(message: types.Message) -> None:
    await message.answer(
        """
<b>YouTube shorts</b>
https://www.youtube.com/watch?v=
https://youtu.be/
https://www.youtube.com/shorts/
https://youtube.com/shorts/

<b>Instagram</b>
https://www.instagram.com/reel/
https://instagram.com/reel/

<b>TikTok</b>
https://www.tiktok.com/
https://vt.tiktok.com/

<b>X (Twitter)</b>
https://x.com/
https://twitter.com/

<b>Spotify</b>
https://open.spotify.com/track/

<b>Pinterest</b>
https://www.pinterest.com/pin/
https://in.pinterest.com/pin/
https://pin.it/
"""
    )


@router.message(F.text)
async def message_handler(message: types.Message) -> None:
    msg_text = """
<b>Платформа: {}</b>

Скачивание {}
Отправка {}
    """
    msg = await message.answer(msg_text.format("🟨", "❌", "❌"))
    try:
        # Initialization
        dl = downloader.Downloader()

        # Detecting platform
        platform = dl.detect_platform(message.text)
        try:
            assert platform != "unsupported"
        except AssertionError:
            raise ValueError("Ссылка не поддерживается. Поддерживаемые ссылки - /supported_links")
        await msg.edit_text(msg_text.format(platform, "🟨", "❌"))

        # Downloading
        filename = dl.download(platform, message.text, str(f"{time.time()}-{message.from_user.id}"))
        file_type = {
            ".mp4": "video",
            ".png": "photo",
            ".mp3": "audio"
        }.get(filename[-4:])
        await msg.edit_text(msg_text.format(platform, "✅", "🟨"))
        await getattr(message, f"answer_{file_type}")(types.FSInputFile(filename), caption="<b>@free_yt_dl_bot</b>")
        time.sleep(0.5)  # Rate limits
        await msg.edit_text(msg_text.format(platform, "✅", "✅"))
    except yt_dlp.utils.DownloadError:
        await msg.edit_text("Ссылка не поддерживается. Поддерживаемые ссылки - /supported_links")
    except Exception:
        await msg.edit_text("Произошла ошибка. Просим сообщить о баге @anekobtw")
    else:
        await message.delete()
        await msg.delete()
        os.remove(filename)
