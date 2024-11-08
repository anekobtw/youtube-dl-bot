"""
All the basic commands
"""

import os

import youthon
import youtubesearchpython
import yt_dlp
from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from dotenv import load_dotenv

from handlers import funcs
from keyboards import get_options_keyboard, get_results_kb

router = Router()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    """The first command"""
    await message.answer(text="Напиши название видео для поиска или вставь ссылку.\n\nО боте - /about\nКак пользоваться ботом - /usage")


@router.message(F.text, Command("about"))
async def about(message: types.Message) -> None:
    """Sending basic info about the bot"""
    await message.answer(
        "Привет! На связи anekobtw. Быстро пройдемся по пунктам.\n\n"
        "Этот бот - мой польностью <b>сольный проект</b>, что означает, что только я выбираю вектор развития, а также проект не зависит ни от кого, кроме меня.\n\n"
        "Бот <b>абсолютно бесплатный</b>, и в нем нет и никогда не будет рекламы. Помимо этого, Вы не увидите никаких платных подписок. Проект был создан не с целью заработка, а с целью предоставить людям <b>лучший сервис для скачивания видео и аудио</b>.\n\n"
        "По причине того, что у меня нет финансирования, я использую бесплатные хостинги, и бот может быть иногда офлайн.\n\n"
        "<b>Бот не сохраняет никаких данных о Вас.</b> Поэтому доступ к тому, что Вы скачиваете есть только у Вас.\n\n"
        '(ссылки на "buy me coffee" не будет)',
        )


@router.message(F.text, Command("usage"))
async def usage(message: types.Message) -> None:
    """Sending info how to use the bot"""
    await message.answer(
        "<b>Как скачать видео/песню с ютуба</b>\n\n"
        "<b>Вариант 1. Ссылкой</b>\n"
        "Отправь боту ссылку, которая начинается с https://www.youtube.com/watch?v= или https://youtu.be/, и бот вернет информацию о видео с кнопками для скачивания.\n\nПри отправке ссылки, которая начинается с https://x.com/ или https://twitter.com/, бот сразу отправит видео"
        "<b>Вариант 2. Поиском</b>\n"
        "Отправь боту обычное сообщение и он вернет список видео с таким запросом. После, нажми на название видео, которое хочешь скачать и бот вернет информацию о видео с кнопками для скачивания."
    )


@router.message(F.text)
async def message_handler(message: types.Message) -> None:
    """Handling all text messages"""
    await message.delete()
    youtube_url_prefixes = ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/shorts/"]
    x_url_prefixes = ["https://x.com/", "https://twitter.com/"]

    if any(message.text.startswith(prefix) for prefix in youtube_url_prefixes):
        url = youthon.Video(message.text).video_url
        await message.answer(text=funcs.get_video_info(url), reply_markup=get_options_keyboard(url))
    elif any(message.text.startswith(prefix) for prefix in x_url_prefixes):
        funcs.download_x_video(message.text, f"xvideo - {message.from_user.id}.mp4")
        await message.answer_video(video=types.FSInputFile(f"xvideo - {message.from_user.id}.mp4"), caption="<b>@free_yt_dl_bot</b>")
        os.remove(f"xvideo - {message.from_user.id}.mp4")
    else:
        results = youtubesearchpython.VideosSearch(query=message.text, limit=10)
        await message.answer(text=f"Видео по запросу <b>{message.text}</b>", reply_markup=get_results_kb(results))
