import asyncio
import os
import random
from typing import Any, Callable

import requests
import yt_dlp
from aiogram import exceptions, types
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from videoprops import get_video_properties

from enums import Databases, ErrorMessage, Keyboards, Messages

currently_downloading = set()


async def async_download(func: Callable) -> Any:
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


@retry(retry=retry_if_exception_type(exceptions.TelegramNetworkError), stop=stop_after_attempt(3))
async def master_handler(
    message: types.Message | types.CallbackQuery,
    send_function: Callable,
    download_function: Callable,
    url: str,
) -> None:
    # Fetching the language of the user
    Databases.ud.value.create_user(message.from_user.id, "en")
    lang = Databases.ud.value.get_lang(message.from_user.id)
    if not lang:
        lang = "en"

    # A user should not be able to download more than 1 video at a time
    if message.from_user.id in currently_downloading:
        await message.answer(ErrorMessage[f"MULTIPLE_VIDEOS_ERROR_{lang.upper()}"].value)
        return

    # Preparation
    message = message.message if isinstance(message, types.CallbackQuery) else message
    currently_downloading.add(message.from_user.id)
    status_msg = await message.answer(Messages[f"PREPARING_{lang.upper()}"].value)

    try:
        # Asynchronously downloading the video
        filename = await async_download(download_function)

        # Sending the video
        if filename.endswith(".mp4"):
            props = get_video_properties(filename)
            await send_function(
                types.FSInputFile(filename),
                caption=Messages[f"BOT_CAPTION_{lang.upper()}"].value,
                height=props["height"],
                width=props["width"],
            )
        else:
            await send_function(types.FSInputFile(filename), caption=Messages[f"BOT_CAPTION_{lang.upper()}"].value)

        # Deleting the messages in the chat and promoting the telegram channel if no error occured
        await message.delete()
        await status_msg.delete()

        if random.randint(1, 10) == 1:
            msg = await message.answer(Messages[f"PROMO_{lang.upper()}"].value)
            await asyncio.sleep(15)
            await msg.delete()

    except exceptions.TelegramEntityTooLarge:
        # If the video is too big, publish in to filebin and then send the link to the file
        await status_msg.edit_text(ErrorMessage[f"SIZE_LIMIT_{lang.upper()}"].value)
        await status_msg.edit_text(publish(filename))
        await message.delete()

    except yt_dlp.DownloadError:
        # If the video is blocked or not available in the hosting's country
        await status_msg.edit_text(ErrorMessage[f"YT_DLP_ERROR_{lang.upper()}"].value.format(url=url))
        await message.bot.send_message(
            chat_id=1718021890,
            text=f"<b>❗ Произошёл баг при скачивании видео:</b>\n<code>{url}</code>",
        )

    except Exception:
        # In any other case
        await status_msg.edit_text(ErrorMessage[f"GENERAL_ERROR_{lang.upper()}"].value),
        await message.bot.send_message(
            chat_id=1718021890,
            text=f"<b>❗ Произошёл баг при скачивании видео:</b>\n<code>{url}</code>",
        )

    finally:
        # Finally, delete the file and allow the user to download another video
        currently_downloading.discard(message.from_user.id)
        if os.path.exists(filename):
            os.remove(filename)
