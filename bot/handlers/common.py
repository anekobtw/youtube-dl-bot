"""
All the basic commands
"""

import os

from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from dotenv import load_dotenv

from handlers import funcs
from keyboards import get_options_keyboard

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
        "Отправь боту ссылку на ютуб видео, и бот вернет информацию о видео с кнопками для скачивания.\nПри отправке ссылки с твиттера (X), бот сразу отправит видео\n\n"
    )


@router.message(F.text)
async def message_handler(message: types.Message) -> None:
    """Handling all text messages"""
    await message.delete()
    youtube_url_prefixes = ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/shorts/"]
    x_url_prefixes = ["https://x.com/", "https://twitter.com/"]

    if any(message.text.startswith(prefix) for prefix in youtube_url_prefixes):
        await message.answer(text=message.text, reply_markup=get_options_keyboard(message.text))
    elif any(message.text.startswith(prefix) for prefix in x_url_prefixes):
        funcs.download_x_video(message.text, f"xvideo - {message.from_user.id}.mp4")
        await message.answer_video(video=types.FSInputFile(f"xvideo - {message.from_user.id}.mp4"), caption="<b>@free_yt_dl_bot</b>")
        os.remove(f"xvideo - {message.from_user.id}.mp4")
    else:
        await message.answer(text="/supported_links")
