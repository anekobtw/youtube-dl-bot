import yt_dlp
from aiogram import F, Router, types
from handlers.modules.master import master_handler
from youthon import Video

from enums import Links

router = Router()


def download_youtube(url: str, filename: str, quality: str) -> str:
    formats = {
        "fhd": {"format": "bestvideo[height<=1080][vcodec^=avc1][ext=mp4]+bestaudio[acodec^=mp4a][ext=m4a]/best[height<=1080][ext=mp4]", "merge_output_format": "mp4"},
        "hd": {"format": "best[height<=720][ext=mp4]"},
        "sd": {"format": "best[height<=480][ext=mp4]"},
        "audio": {"format": "bestaudio[ext=m4a]", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]},
    }
    opts = {
        "outtmpl": filename[:-4] if quality in ["fhd", "audio"] else filename,
        "postprocessors": [{"key": "FFmpegFixupM4a"}, {"key": "FFmpegFixupStretched"}],
    }
    with yt_dlp.YoutubeDL({**opts, **formats[quality]}) as ydl:
        ydl.download([url])
    return filename


def keyboard(url: str) -> types.InlineKeyboardMarkup:
    kb = []
    kb.append([types.InlineKeyboardButton(text="📹 Full HD (1080p) (Долго)", callback_data=f"{url}!fhd")])
    kb.append([types.InlineKeyboardButton(text="📹 HD (720p) (Быстро)", callback_data=f"{url}!hd")])
    kb.append([types.InlineKeyboardButton(text="📹 SD (480p) (Быстро)", callback_data=f"{url}!sd")])
    kb.append([types.InlineKeyboardButton(text="🎵 Только аудио", callback_data=f"{url}!audio")])

    return types.InlineKeyboardMarkup(inline_keyboard=kb)


@router.message(F.text.startswith(tuple(Links.YOUTUBE.value)))
async def _(message: types.Message) -> None:
    try:
        await message.answer_photo(
            photo=Video(message.text).thumbnail_url,
            caption="🖼️ Выберите качество загрузки:",
            reply_markup=keyboard(message.text),
        )
        await message.delete()
    except Exception:
        await message.answer("⚠️ Ошибка при получении данных видео.")


@router.callback_query(lambda c: c.data.startswith(tuple(Links.YOUTUBE.value)))
async def youtube(callback: types.CallbackQuery) -> None:
    url, quality = callback.data.split("!")
    filename = f"{callback.message.from_user.id}.{"mp3" if quality == "audio" else "mp4"}"

    await master_handler(
        message=callback.message,
        send_function=callback.message.answer_video if quality != "audio" else callback.message.answer_audio,
        download_function=lambda: download_youtube(url, filename, quality),
        url=url,
    )
