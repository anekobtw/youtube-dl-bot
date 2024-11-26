import os

from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from dotenv import load_dotenv

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
    try:
        dl = downloader.Downloader(message.text, str(message.from_user.id))
        filename = dl.filename

        file_extension_map = {
            ".mp4": ("video", types.FSInputFile(filename)),
            ".png": ("photo", types.FSInputFile(filename)),
            ".mp3": ("audio", types.FSInputFile(filename)),
        }

        file_type, file_input = file_extension_map.get(os.path.splitext(filename)[-1].lower(), (None, None))
        await getattr(message, f"answer_{file_type}")(file_input, caption="<b>@free_yt_dl_bot</b>")

    except Exception as e:
        await message.answer(str(e))
    else:
        await message.delete()
    finally:
        os.remove(filename)
