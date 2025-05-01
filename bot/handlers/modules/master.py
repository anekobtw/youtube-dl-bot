import asyncio
import os
import random
from typing import Callable

import requests
import yt_dlp
from aiogram import exceptions, types
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from videoprops import get_video_properties

from enums import Databases, ErrorMessage, Keyboards, Messages

currently_downloading = set()


async def async_download(func: Callable) -> str:
    return await asyncio.to_thread(func)


def publish(filename: str) -> str:
    with open(filename, "rb") as file:
        headers = {
            "filename": filename,
            "Content-Type": "application/octet-stream",
        }
        response = requests.post(
            url="https://filebin.net",
            files={"file": file},
            data={"bin": "anekobtw"},
            headers=headers,
        )
    res = response.json()
    return f"https://filebin.net/{res['bin']['id']}/{res['file']['filename']}"


def get_thumbnail(url: str) -> str:
    with yt_dlp.YoutubeDL({"quiet": 1, "skip_download": 1}) as ydl:
        info = ydl.extract_info(url, download=0)
        filename = f"{info['id']}.png"
        open(filename, "wb").write(requests.get(info.get("thumbnail")).content)
        return filename


def download(url: str, filename: str, quality: str) -> str:
    formats = {
        "video": {
            "format": "best",
            "postprocessors": [{"key": "FFmpegFixupM4a"}, {"key": "FFmpegFixupStretched"}],
        },
        "audio": {
            "format": "bestaudio[ext=m4a]",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        },
    }
    opts = {"outtmpl": filename}

    with yt_dlp.YoutubeDL({**opts, **formats[quality]}) as ydl:
        info = ydl.extract_info(url, download=True)
        real_filename = ydl.prepare_filename(info)

    return real_filename


async def message_handler(message: types.Message):
    Databases.ud.value.create_user(message.from_user.id, "en")
    lang = Databases.ud.value.get_lang(message.from_user.id)

    try:
        ydl = yt_dlp.YoutubeDL({"quiet": 1, "format": "best"})
        info = ydl.extract_info(message.text, download=0)

        await message.answer_photo(
            photo=types.URLInputFile(info.get("thumbnail")),
            caption="🖼️ Выберите качество загрузки:" if lang == "ru" else "🖼️ Choose the download quality:",
            reply_markup=Keyboards.quality_keyboard(message.text, lang),
        )
        await message.delete()
    except Exception as e:
        await message.answer(ErrorMessage[f"EXTRACT_VIDEO_{lang.upper()}"].value)


@retry(retry=retry_if_exception_type(exceptions.TelegramNetworkError), stop=stop_after_attempt(3))
async def download_handler(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id

    # Fetching the language of the user
    Databases.ud.value.create_user(user_id, "en")
    lang = Databases.ud.value.get_lang(user_id)

    # A user should not be able to download more than 1 video at a time
    if user_id in currently_downloading:
        await callback.answer(ErrorMessage[f"MULTIPLE_VIDEOS_ERROR_{lang.upper()}"].value)
        return

    # Preparation
    url, quality = callback.data.split("!")
    currently_downloading.add(user_id)
    await callback.answer(Messages[f"PREPARING_{lang.upper()}"].value)

    try:
        # Asynchronously downloading the video
        filename = f"{user_id}.{"mp3" if quality == "audio" else "mp4"}"
        filename = await async_download(lambda: download(url, filename, quality))

        # Sending the video
        if filename.endswith(".mp4"):
            props = get_video_properties(filename)
            await callback.message.answer_video(
                types.FSInputFile(filename),
                caption=Messages[f"BOT_CAPTION_{lang.upper()}"].value,
                height=props["height"],
                width=props["width"],
            )
        else:
            await callback.message.answer_photo(types.FSInputFile(filename), caption=Messages[f"BOT_CAPTION_{lang.upper()}"].value)

        # Deleting the messages in the chat and promoting the telegram channel if no error occured
        await callback.message.delete()

        if random.randint(1, 10) == 1:
            msg = await callback.message.answer(Messages[f"PROMO_{lang.upper()}"].value)
            await asyncio.sleep(15)
            await msg.delete()

    except exceptions.TelegramEntityTooLarge:
        # If the video is too big, publish in to filebin and then send the link to the file
        msg = await callback.message.answer(ErrorMessage[f"SIZE_LIMIT_{lang.upper()}"].value)
        await msg.edit_text(publish(filename))
        await callback.message.delete()

    except yt_dlp.DownloadError as e:
        # If the video is blocked or not available in the hosting's country
        await callback.message.answer(ErrorMessage[f"YT_DLP_ERROR_{lang.upper()}"].value.format(url=url))
        await callback.bot.send_message(
            chat_id=1718021890,
            text=f"<b>❗ Произошёл баг при скачивании видео:</b>\n<code>{url}</code>\n\n{e}",
        )

    except Exception as e:
        # In any other case
        await callback.message.answer(ErrorMessage[f"GENERAL_ERROR_{lang.upper()}"].value),
        await callback.bot.send_message(
            chat_id=1718021890,
            text=f"<b>❗ Произошёл баг при скачивании видео:</b>\n<code>{url}</code>\n\n{e}",
        )

    finally:
        # Finally, delete the file and allow the user to download another video
        currently_downloading.discard(user_id)
        if os.path.exists(filename):
            os.remove(filename)
