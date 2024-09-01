import os

import youtubesearchpython
from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from dotenv import load_dotenv

import handlers.funcs as funcs
from keyboards import get_dl_kb, get_results_kb

router = Router()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    await message.answer(text="Напиши название видео для поиска или вставь ссылку.\n\nО боте - /about\nКак пользоваться ботом - /usage")


@router.message(F.text, Command("about"))
async def faq(message: types.Message) -> None:
    await message.answer(
        "Привет! На связи anekobtw. Быстро пройдемся по пунктам.\n\n"
        "Этот бот - мой польностью <b>сольный проект</b>, что означает, что только я выбираю вектор развития, а также проект не зависит ни от кого, кроме меня.\n\n"
        "Бот <b>абсолютно бесплатный</b>, и в нем нет и никогда не будет рекламы. Помимо этого, Вы не увидите никаких платных подписок. Проект был создан не с целью заработка, а с целью предоставить людям <b>лучший сервис для скачивания видео и аудио</b>. Эту парадигму менять не собираюсь.\n\n"
        "По причине того, что у меня нет финансирования, я использую бесплатные хостинги, и бот может быть иногда офлайн. Обо всем я буду оповещать в телеграм канале бота - @free_yt_dl_channel\n\n"
        "<b>Бот не сохраняет никаких данных о Вас.</b> Поэтому доступ к тому, что Вы скачиваете есть только у Вас.\n\n"
        '(ссылки на "buy me coffee" не будет)',
    )


@router.message(F.text, Command("usage"))
async def usage(message: types.Message) -> None:
    await message.answer(
        "<b>Как скачать видео/песню с ютуба</b>\n\n"
        "<b>Вариант 1. Ссылкой</b>\n"
        "Отправь боту ссылку, которая начинается с https://www.youtube.com/watch?v= или https://youtu.be/, и бот вернет информацию о видео с кнопками для скачивания.\n\n"
        "<b>Вариант 2. Поиском</b>\n"
        "Отправь боту обычное сообщение и он вернет список видео с таким запросом. После, нажми на название видео, которое хочешь скачать и бот вернет информацию о видео с кнопками для скачивания."
        "<b>Вариант 3. Голосовым сообщением (только на русском)</b>\n"
        "Запиши голосовое сообщение (желательно говорить внятно и без постороннего шума) с названием видео и бот список видео с таким запросом. После, нажми на название видео, которое хочешь скачать и бот вернет информацию о видео с кнопками для скачивания."
    )


@router.message(F.text)
async def message_handler(message: types.Message) -> None:
    await message.delete()
    url_prefixes = ["https://www.youtube.com/watch?v=", "https://youtu.be/"]

    if any(message.text.startswith(prefix) for prefix in url_prefixes):
        await message.answer(text=funcs.get_video_info(message.text), reply_markup=get_dl_kb(message.text))
    else:
        results = youtubesearchpython.VideosSearch(query=message.text, limit=10)
        await message.answer(
            text=f"Видео по запросу <b>{message.text}</b>",
            reply_markup=get_results_kb(results),
        )


@router.message(F.content_type.in_("voice"))
async def voice_handler(message: types.Message) -> None:
    await message.delete()
    file = await bot.get_file(message.voice.file_id)
    filename = f"voice_{message.from_user.id}.mp3"
    await bot.download_file(file.file_path, filename)

    query = funcs.Transcryptor().transcrypt(file_path=filename)
    await message.answer(
        text=f"Видео по запросу <b>{query}</b>",
        reply_markup=get_results_kb(youtubesearchpython.VideosSearch(query=query, limit=10)),
    )

    os.remove(filename)
