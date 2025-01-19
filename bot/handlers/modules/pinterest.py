import time

import requests
from aiogram import F, Router, types
from bs4 import BeautifulSoup

from handlers.modules.master import master_handler

router = Router()


def download_pinterest(url: str, filename: str) -> str:
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"}
    img_url = BeautifulSoup(requests.get(url, headers=HEADERS).content, "html.parser").find("meta", property="og:image")["content"]
    with requests.get(img_url, stream=True, headers=HEADERS) as r, open(filename, "wb") as file:
        for chunk in r.iter_content(1024):
            file.write(chunk)
    return filename


links = [
    "https://pin.it/",
    "https://www.pinterest.com/pin/",
    "https://in.pinterest.com/pin/",
]


@router.message(F.text.startswith(tuple(links)))
async def pinterest(message: types.Message) -> None:
    filename = f"{time.time_ns()}-{message.from_user.id}.png"
    await master_handler(
        message=message,
        send_function=message.answer_photo,
        download_function=lambda: download_pinterest(message.text, filename),
    )
