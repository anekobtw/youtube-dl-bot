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
    await message.answer(text="Отправь боту ссылку на видео.\nПоддерживаемые ссылки - /supported_links\n\n<b>Мы не собираем никаких данных о Вас!</b>")


@router.message(F.text, Command("supported_links"))
async def usage(message: types.Message) -> None:
    await message.answer(
        """
<b>YouTube</b>
https://www.youtube.com/watch?v=
https://youtu.be/
https://www.youtube.com/shorts/
https://youtube.com/shorts/

<b>Instagram</b>
https://www.instagram.com/reel/

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
    try:
        dl = funcs.Downloader(message.text, str(message.from_user.id))
        filename = dl.filename
        if filename.endswith(".mp4"):
            await message.answer_video(video=types.FSInputFile(filename), caption="<b>@free_yt_dl_bot</b>")
        elif filename.endswith(".png"):
            await message.answer_photo(photo=types.FSInputFile(filename), caption="<b>@free_yt_dl_bot</b>")
    except Exception as e:
        await message.answer(str(e))
    else:
        await message.delete()
        os.remove(filename)
