import asyncio
import os
import shutil
from typing import Any, Callable

import requests
from aiogram import exceptions, types
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from videoprops import get_video_properties

ERROR_MESSAGES = {
    "size_limit": "К сожалению, из-за ограничений телеграма, мы не можем отправлять видео больше 50 мегабайт. Попытка выложить файл на filebin.net",
    "general_error": "Произошла ошибка. Просим сообщить о баге @anekobtw",
}


async def async_download(function: Callable) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, function)


def publish(filename: str) -> str:
    with open(filename, "rb") as file:
        headers = {"filename": filename, "Content-Type": "application/octet-stream"}
        response = requests.post(
            "https://filebin.net",
            files={"file": file},
            data={"bin": "anekobtw"},
            headers=headers,
        )
    res = response.json()
    return f"https://filebin.net/{res['bin']['id']}/{res['file']['filename']}"


@retry(retry=retry_if_exception_type(exceptions.TelegramNetworkError), stop=stop_after_attempt(3))
async def master_handler(message: types.Message, send_function: Callable, download_function: Callable) -> None:
    status_msg = await message.answer("Файл подготавливается. Пожалуйста, подождите немного.")

    try:
        filename = await async_download(download_function)

        if filename.endswith(".mp4"):
            props = get_video_properties(filename)
            await send_function(types.FSInputFile(filename), caption="<b>@free_yt_dl_bot</b>", height=props["height"], width=props["width"])
        else:
            await send_function(types.FSInputFile(filename), caption="<b>@free_yt_dl_bot</b>")

    except exceptions.TelegramEntityTooLarge:
        await status_msg.edit_text(ERROR_MESSAGES["size_limit"])
        await status_msg.edit_text(publish(filename))
        await message.delete()

    except Exception as e:
        print(e)
        await status_msg.edit_text(ERROR_MESSAGES["general_error"])

    else:
        await message.delete()
        await status_msg.delete()
        if os.path.isfile(filename):
            os.remove(filename)
        elif os.path.isdir(filename):
            shutil.rmtree(filename)
