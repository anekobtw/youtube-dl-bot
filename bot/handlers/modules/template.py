import time

from aiogram import F, Router, types

from handlers.modules.master import master_handler

router = Router()


def download_(url: str, filename: str) -> str:
    return filename


links = []


@router.message(F.text.startswith(tuple(links)))
async def _(message: types.Message) -> None:
    filename = f"{time.time_ns()}-{message.from_user.id}."
    await master_handler(
        message=message,
        send_function=message.answer_audio,
        download_function=lambda: download_(message.text, filename),
    )
