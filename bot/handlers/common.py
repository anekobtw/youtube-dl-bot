"""
All the basic commands
"""

import os

from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from dotenv import load_dotenv

from handlers import funcs

router = Router()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    """Start command"""
    await message.answer(text="Отправь боту ссылку на видео.\nПоддерживаемые ссылки - /supported_links\n\n<b>Мы не собираем никаких данных о Вас!</b>")


@router.message(F.text, Command("supported_links"))
async def usage(message: types.Message) -> None:
    """Sending a message with all the supported links."""
    await message.answer(
        """
<b>YouTube</b>
https://www.youtube.com/watch?v=
https://youtu.be/
https://www.youtube.com/shorts/
https://youtube.com/shorts/

<b>X (Twitter)</b>
https://x.com/
https://twitter.com/

<b>TikTok</b>
https://www.tiktok.com/
https://vt.tiktok.com/

<b>Pinterest</b>
https://www.pinterest.com/pin/
https://in.pinterest.com/pin/
"""
    )


@router.message(F.text)
async def message_handler(message: types.Message) -> None:
    """Handles all text messages by detecting the platform and responding accordingly."""
    uid = message.from_user.id
    platform = funcs.detect_platform(message.text)

    platform_cfgs = {"youtube": (funcs.download_yt_video, f"ytvideo - {uid}.mp4", message.answer_video), "x": (funcs.download_x_video, f"xvideo - {uid}.mp4", message.answer_video), "tiktok": (funcs.download_tiktok_video, f"ttvideo - {uid}.mp4", message.answer_video), "pinterest": (funcs.download_pinterest_image, f"pinimage - {uid}.png", message.answer_photo)}

    if platform in platform_cfgs:
		await message.delete()
        download_func, fname, send_media = platform_cfgs[platform]

        try:
            download_func(message.text, fname)
            file_input = types.FSInputFile(fname)
            await send_media(file_input, caption="<b>@free_yt_dl_bot</b>")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
        finally:
            os.remove(fname)
    else:
        await message.answer(text="Данная ссылка не поддерживается.\nПоддерживаемые ссылки - /supported_links")
