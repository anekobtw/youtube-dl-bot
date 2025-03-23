import asyncio
import os
import random
from typing import Any, Callable

import requests
import yt_dlp
from aiogram import exceptions, types
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from videoprops import get_video_properties

from enums import ErrorMessage, StatusMessage

currently_downloading = set()


async def async_download(func: Callable) -> Any:
    return await asyncio.to_thread(func)


def publish(filename: str) -> str:
    with open(filename, "rb") as file:
        headers = {"filename": filename, "Content-Type": "application/octet-stream"}
        response = requests.post(
            url="https://filebin.net",
            files={"file": file},
            data={"bin": "anekobtw"},
            headers=headers,
        )
    res = response.json()
    return f"https://filebin.net/{res['bin']['id']}/{res['file']['filename']}"


@retry(retry=retry_if_exception_type(exceptions.TelegramNetworkError), stop=stop_after_attempt(3))
async def master_handler(message: types.Message, send_function: Callable, download_function: Callable, url: str) -> None:
    if message.from_user.id in currently_downloading:
        await message.answer(ErrorMessage.MULTIPLE_VIDEOS_ERROR.value)
        return

    currently_downloading.add(message.from_user.id)
    status_msg = await message.answer(StatusMessage.PREPARING.value)

    try:
        filename = await async_download(download_function)

        if filename.endswith(".mp4"):
            props = get_video_properties(filename)
            await send_function(types.FSInputFile(filename), caption=StatusMessage.BOT_CAPTION.value, height=props["height"], width=props["width"])
        else:
            await send_function(types.FSInputFile(filename), caption=StatusMessage.BOT_CAPTION.value)

        await message.delete()
        await status_msg.delete()

    except exceptions.TelegramEntityTooLarge:
        await status_msg.edit_text(ErrorMessage.SIZE_LIMIT.value)
        await status_msg.edit_text(publish(filename))
        await message.delete()

    except yt_dlp.DownloadError:
        await message.answer(ErrorMessage.YT_DLP_ERROR.value.format(url=url))

    except Exception as e:
        print(e)
        await status_msg.edit_text(
            text=ErrorMessage.GENERAL_ERROR.value,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="📩 Сообщить о проблеме (анонимно)", callback_data=f"report!{url}")]]),
        ),

    else:
        if random.randint(1, 10) == 1:
            msg = await message.answer(StatusMessage.PROMO.value)
            await asyncio.sleep(10)
            await msg.delete()

    finally:
        currently_downloading.discard(message.from_user.id)
        os.remove(filename)
