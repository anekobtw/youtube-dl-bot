import asyncio
import os
from typing import Any

from aiogram import exceptions, types


async def async_download(function) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, function)


async def master_handler(
    message: types.Message,
    send_function,
    download_function,
) -> None:
    msg = await message.answer("Файл подготавливается. Пожалуйста, подождите немного.")

    try:
        filename = await async_download(download_function)
        await send_function(types.FSInputFile(filename), caption="@free_yt_dl_bot")
        await message.answer_document(types.FSInputFile(filename), caption="@free_yt_dl_bot")

    except exceptions.TelegramEntityTooLarge:
        await msg.edit_text("К сожалению, из-за ограничений телеграма, мы не можем отправлять видео больше 50 мегабайт.")

    except Exception as e:
        await msg.edit_text("Произошла ошибка. Просим сообщить о баге @anekobtw")
        print(e)

    else:
        if os.path.exists(filename):
            os.remove(filename)
        await message.delete()
        await msg.delete()
