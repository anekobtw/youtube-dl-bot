from aiogram import F, Router, types
from aiogram.filters import Command

router = Router()


def news_kb() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="📰 Телеграм канал с новостями", url="t.me/anekobtw_c")]])

@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    await message.answer(text="Отправь боту ссылку на видео.\n\n<b>Мы не собираем никаких данных о Вас!</b>", reply_markup=news_kb())
