from aiogram import F, Router, types
from aiogram.filters import Command

router = Router()


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="📰 A Telegram channel with news", url="t.me/anekobtw_c")]])

    await message.answer(
        f"""
Hello, @{message.from_user.username}! Just send the link to the video.

ℹ️ <b>We don’t collect any data.</b>

❗ <b>If the bot isn’t working, don’t worry</b> — your request will be processed automatically once we're back online.

🙏 <b>Please don’t block the bot</b> — it needs to message you when the download is ready.
""",
        reply_markup=kb,
    )
