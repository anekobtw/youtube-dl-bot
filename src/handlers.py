import os

import yt_dlp
from aiogram import F, Router, exceptions, types
from aiogram.filters import CommandStart
from enums import Links, VideoStatusMessages

router = Router()


async def download_video(url: str) -> str:
    opts = {
        "format": "bestvideo[vcodec^=avc1][ext=mp4]+bestaudio[acodec^=mp4a]/mp4",
        "merge-output-format": "mp4",
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return {
            "filename": ydl.prepare_filename(info),
            "width": info.get("width", 0),
            "height": info.get("height", 0),
        }


@router.message(F.text.startswith(tuple(Links.STANDART.value)))
async def handle_standart_download(message: types.Message):
    url = message.text
    await message.react([types.reaction_type_emoji.ReactionTypeEmoji(emoji="👀")])
    msg = await message.answer(VideoStatusMessages.VideoProcessing.value.format(url=url))

    try:
        info = await download_video(url)

        await msg.edit_text(VideoStatusMessages.VideoSuccess.value.format(url=url))

        await message.answer_video(
            video=types.FSInputFile(info["filename"]),
            caption=f"<b><i><a href='https://t.me/free_yt_dl_bot'>via</a> | <a href='{url}'>link</a></i></b>",
            width=info["width"],
            height=info["height"],
        )

    except exceptions.TelegramEntityTooLarge:
        await msg.edit_text(VideoStatusMessages.VideoNotSent.value.format(url=url))
        return

    except Exception:
        await msg.edit_text(VideoStatusMessages.ErrorOccured.value.format(url=url))
        return
    
    else:
        await message.delete()
        await msg.delete()

    finally:
        os.remove(info["filename"])

@router.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.answer(
        text=f"Hello, @{message.from_user.username}! Just send the link to the video.\n\n"\
        "ℹ️ <b>We don’t collect any data.</b>\n\n"\
        "❗ <b>If the bot isn’t working, don’t worry</b> — your request will be processed automatically once we're back online.\n\n"\
        "🙏 <b>Please don’t block the bot</b> — it needs to message you when the download is ready.",
    )
