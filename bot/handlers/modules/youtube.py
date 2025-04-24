import yt_dlp
from aiogram import F, Router, types
from youthon import Video

from enums import Databases, Links
from handlers.modules.master import master_handler

router = Router()


def download_youtube(url: str, filename: str, quality: str) -> str:
    formats = {
        "fhd": {
            "format": "bestvideo[height<=1080][vcodec^=avc1][ext=mp4]+bestaudio[acodec^=mp4a][ext=m4a]/best[height<=1080][ext=mp4]",
            "merge_output_format": "mp4",
        },
        "hd": {"format": "best[height<=720][ext=mp4]"},
        "sd": {"format": "best[height<=480][ext=mp4]"},
        "audio": {
            "format": "bestaudio[ext=m4a]",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        },
    }
    opts = {
        "outtmpl": filename[:-4] if quality in ["fhd", "audio"] else filename,
        "postprocessors": [
            {"key": "FFmpegFixupM4a"},
            {"key": "FFmpegFixupStretched"},
        ],
    }
    with yt_dlp.YoutubeDL({**opts, **formats[quality]}) as ydl:
        ydl.download([url])
    return filename


def keyboard(url: str, lang: str) -> types.InlineKeyboardMarkup:
    buttons = []
    quality = ["fhd", "hd", "sd", "audio"]
    texts = {"ru": {"fhd": "📹 Full HD (1080p) (Долго)", "hd": "📹 HD (720p) (Быстро)", "sd": "📹 SD (480p) (Быстро)", "audio": "🎵 Только аудио"}, "en": {"fhd": "📹 Full HD (1080p) (Long)", "hd": "📹 HD (720p) (Fast)", "sd": "📹 SD (480p) (Fast)", "audio": "🎵 Only audio"}}

    for q in quality:
        buttons.append([types.InlineKeyboardButton(text=texts[lang][q], callback_data=f"{url}!{q}")])

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(F.text.startswith(tuple(Links.YOUTUBE.value)))
async def _(message: types.Message) -> None:
    Databases.ud.value.create_user(message.from_user.id, "en")
    lang = Databases.ud.value.get_lang(message.from_user.id)

    try:
        await message.answer_photo(
            photo=Video(message.text).thumbnail_url,
            caption="🖼️ Выберите качество загрузки:" if lang == "ru" else "🖼️ Choose the download quality:",
            reply_markup=keyboard(message.text, lang if lang else "en"),
        )
        await message.delete()
    except Exception:
        await message.answer("⚠️ Ошибка при получении данных видео." if lang == "ru" else "⚠️ Error getting video data.")


@router.callback_query(lambda c: c.data.startswith(tuple(Links.YOUTUBE.value)))
async def youtube(callback: types.CallbackQuery) -> None:
    url, quality = callback.data.split("!")
    filename = f"{callback.message.from_user.id}.{"mp3" if quality == "audio" else "mp4"}"

    await master_handler(
        message=callback,
        send_function=(callback.message.answer_video if quality != "audio" else callback.message.answer_audio),
        download_function=lambda: download_youtube(url, filename, quality),
        url=url,
    )
