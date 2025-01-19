import asyncio
import os
from typing import Any, Callable

import requests
from aiogram import exceptions, types
from videoprops import get_video_properties

ERROR_MESSAGES = {
    "size_limit": "К сожалению, из-за ограничений телеграма, мы не можем отправлять видео больше 50 мегабайт. Попытка выложить файл на filebin.net",
    "general_error": "Произошла ошибка. Просим сообщить о баге @anekobtw",
}


async def async_download(function: Callable) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, function)


async def master_handler(
    message: types.Message,
    send_function: Callable,
    download_function: Callable,
) -> None:
    status_msg = await message.answer("Файл подготавливается. Пожалуйста, подождите немного.")

    try:
        filename = await async_download(download_function)

        if filename.endswith(".mp4"):
            props = get_video_properties(filename)
            await send_function(types.FSInputFile(filename), caption="@free_yt_dl_bot", height=props["height"], width=props["width"])
        else:
            await send_function(types.FSInputFile(filename), caption="@free_yt_dl_bot")

    except exceptions.TelegramEntityTooLarge:
        await status_msg.edit_text(ERROR_MESSAGES["size_limit"])
        with open(filename, "rb") as file:
            headers = {"filename": filename, "Content-Type": "application/octet-stream"}
            response = requests.post(
                "https://filebin.net",
                files={"file": file},
                data={"bin": "anekobtw"},
                headers=headers,
            )
        res = response.json()
        await message.delete()
        await status_msg.edit_text(f"https://filebin.net/{res['bin']['id']}/{res['file']['filename']}")

    except exceptions.TelegramNetworkError:
        attempts = 3
        for attempt in range(attempts):
            try:
                await send_function(types.FSInputFile(filename), caption="@free_yt_dl_bot")
                break
            except exceptions.TelegramNetworkError:
                if attempt == attempts - 1:
                    await status_msg.edit_text(ERROR_MESSAGES["general_error"])
                    break
                await asyncio.sleep(2**attempt)

    except Exception as e:
        print(e)
        await status_msg.edit_text(ERROR_MESSAGES["general_error"])

    else:
        await message.delete()
        await status_msg.delete()
        os.remove(filename)
