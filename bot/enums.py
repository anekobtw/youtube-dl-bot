from enum import Enum

from aiogram import types

from db import UsersDatabase


class Databases(Enum):
    ud = UsersDatabase()


class Keyboards(Enum):
    MAIN_RU = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="🇷🇺 Русский ⭐️", callback_data="lang_ru"),
                types.InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
            ],
            [types.InlineKeyboardButton(text="📰 Телеграм канал с новостями", url="t.me/anekobtw_c")],
        ]
    )
    MAIN_EN = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="🇷🇺 Russian", callback_data="lang_ru"),
                types.InlineKeyboardButton(text="🇬🇧 English ⭐️", callback_data="lang_eng"),
            ],
            [types.InlineKeyboardButton(text="📰 A Telegram channel with news", url="t.me/anekobtw_c")],
        ]
    )


class ErrorMessage(Enum):
    SIZE_LIMIT_RU = "⚠️ К сожалению, из-за ограничений Телеграма, мы не можем отправлять видео больше 50 МБ. Пробуем загрузить файл на filebin.net"
    SIZE_LIMIT_EN = "⚠️ Unfortunately, due to Telegram restrictions, we cannot send videos larger than 50 MB. Attempting to upload the file to filebin.net"

    GENERAL_ERROR_RU = "⚠️ Произошла ошибка."
    GENERAL_ERROR_EN = "⚠️ An error occurred."

    MULTIPLE_VIDEOS_ERROR_RU = "⚠️ Пожалуйста, дождитесь загрузки предыдущего видео и попробуйте снова."
    MULTIPLE_VIDEOS_ERROR_EN = "⚠️ Please wait until the previous video is downloaded and try again."

    YT_DLP_ERROR_RU = "⚠️ Видео могло не загрузиться из-за особенностей хостинга. Попробуйте наше зеркало (не работает 24/7):\n\n<b>@free_yt_dl_mirror_bot</b>"
    YT_DLP_ERROR_EN = "⚠️ The video may not have downloaded due to hosting specifics. Try our mirror (not available 24/7):\n\n<b>@free_yt_dl_mirror_bot</b>"


class Messages(Enum):
    START_RU = "Выберите язык общения:\n\n<b>ℹ️ Мы сохраняем ваш выбор языка для удобства использования бота. Никакие другие данные не собираются!</b>"
    START_EN = "Choose your preferred language:\n\n<b>ℹ️ We store your language preference for a better bot experience. No other data is collected!</b>"

    PREPARING_RU = "⏳ Файл подготавливается. Пожалуйста, подождите."
    PREPARING_EN = "⏳ The file is being prepared. Please wait."

    PROMO_RU = "Привет! Я <b>@free_yt_dl_bot</b> — полностью бесплатный, без рекламы и обязательных подписок. Если тебе нравится моя работа, загляни на мой <b><a href='https://t.me/anekobtw_c'>телеграм канал с новостями</a></b> — это большая поддержка! 😊\n\n<b>Это сообщение удалится через 15 секунд</b>"
    PROMO_EN = "Hi! I'm <b>@free_yt_dl_bot</b> — completely free, no ads, no mandatory subscriptions. If you like my work, check out my <b><a href='https://t.me/anekobtw_c'>Telegram news channel</a></b> — it’s a big support! 😊\n\n<b>This message will self-delete in 15 seconds</b>"

    BOT_CAPTION_RU = "<b>@free_yt_dl_bot</b>"
    BOT_CAPTION_EN = "<b>@free_yt_dl_bot</b>"


class Links(Enum):
    YOUTUBE = [
        "https://www.youtube.com/",
        "https://youtu.be/",
        "https://www.youtube.com/shorts/",
        "https://youtube.com/shorts/",
    ]
    STANDART = [
        "https://www.tiktok.com/",
        "https://vt.tiktok.com/",
        "https://vm.tiktok.com/",
        "https://www.instagram.com/reel/",
        "https://instagram.com/reel/",
        "https://www.instagram.com/share/",
        "https://x.com/",
        "https://twitter.com/",
    ]
