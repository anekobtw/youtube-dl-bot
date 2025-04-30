from aiogram import F, Router, exceptions, types
from aiogram.filters import Command

from enums import Databases, Keyboards, Messages

router = Router()


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    Databases.ud.value.create_user(message.from_user.id, "en")
    lang = Databases.ud.value.get_lang(message.from_user.id)
    await message.answer(text=Messages[f"START_{lang.upper()}"].value, reply_markup=Keyboards[f"MAIN_{lang.upper()}"].value)


@router.callback_query(F.data.startswith("lang_"))
async def change_language(callback: types.CallbackQuery) -> None:
    new_lang = callback.data.split("_")[1]
    Databases.ud.value.update_user(callback.from_user.id, new_lang)
    try:
        await callback.message.edit_text(text=Messages[f"START_{new_lang.upper()}"].value, reply_markup=Keyboards[f"MAIN_{new_lang.upper()}"].value)
    except exceptions.TelegramBadRequest:
        pass
