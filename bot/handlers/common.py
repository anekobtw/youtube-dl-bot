import os

from aiogram import Bot, F, Router, types, methods, exceptions
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
async def supported_links(message: types.Message) -> None:
    await message.answer(downloader.PlatformDetector().get_links_text())


@router.message(F.text)
async def message_handler(message: types.Message) -> None:
    msg_text = "<b>Платформа: {}</b>\nСкачивание {}\nОтправка {}"
    msg = await message.answer(msg_text.format("🟨", "❌", "❌"))

    try:
        # Initialization
        dl = downloader.Downloader()
        detector = downloader.PlatformDetector()
        platform = detector.detect_platform(message.text)
        await msg.edit_text(msg_text.format(platform, "🟨", "❌"))

        # Downloading
        filename = dl.download(platform, message.text, str(f"{time.time_ns()}-{message.from_user.id}"))
        await msg.edit_text(msg_text.format(platform, "✅", "🟨"))

        # Sending
        file_type = {".mp4": "video", ".png": "photo", ".mp3": "audio"}.get(filename[-4:])
        await getattr(message, f"answer_{file_type}")(types.FSInputFile(filename), caption="<b>@free_yt_dl_bot</b>")
        await msg.edit_text(msg_text.format(platform, "✅", "✅"))

    except (yt_dlp.utils.DownloadError, exceptions.TelegramEntityTooLarge):
        await msg.edit_text("К сожалению, из-за ограничений телеграма, мы не можем отправлять видео больше 50 мегабайт.")

    except ValueError as e:
        await msg.edit_text("Ссылка не поддерживается. Поддерживаемые ссылки - /supported_links")
        print(e)

    except Exception as e:
        await msg.edit_text("Произошла ошибка. Просим сообщить о баге @anekobtw")
        print(e)

    else:
        await message.delete()
        await msg.delete()
        os.remove(filename)
