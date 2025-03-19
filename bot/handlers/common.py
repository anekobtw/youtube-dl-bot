from aiogram import F, Router, types
from aiogram.filters import Command

router = Router()


def news_kb() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="📰 Телеграм канал с новостями", url="t.me/anekobtw_c")]])


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    await message.answer(text="Отправь боту ссылку на видео.\n\n<b>🛡️ Мы не собираем никаких данных о Вас!</b>", reply_markup=news_kb())


@router.callback_query(F.data.startswith("report!"))
async def report(callback: types.CallbackQuery) -> None:
    data = callback.data.split("!")
    await callback.bot.send_message(chat_id=1718021890, text=f"<b>❗ Поступил запрос о баге в видео:</b>\n<code>{data[1]}</code>")
    await callback.answer("Спасибо за помощь! 💖", show_alert=True)
