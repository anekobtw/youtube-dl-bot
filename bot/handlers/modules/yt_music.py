import time
from io import BytesIO
from urllib.request import urlopen

import yt_dlp
from aiogram import F, Router, types
from mutagen.id3 import APIC, ID3, TIT2, TPE1
from mutagen.mp3 import MP3
from ytmusicapi import YTMusic

from handlers.modules.master import master_handler

router = Router()
ytmusic = YTMusic()


def set_track_metadata(filename: str, title: str, artist: str, thumbnail_url: str) -> None:
    audio = MP3(filename, ID3=ID3)
    audio.tags.add(TIT2(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=artist))
    with urlopen(thumbnail_url) as response:
        data = BytesIO(response.read())
        audio.tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=data.read()))
    audio.save()


def download_yt_music(url: str, filename: str) -> str:
    ydl_opts = {
        "format": "best",
        "outtmpl": filename.removesuffix(".mp3"),
        "noplaylist": True,
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    metadata = ytmusic.get_song(info["id"])
    set_track_metadata(
        filename=filename,
        title=metadata["videoDetails"]["title"],
        artist=metadata["videoDetails"]["author"],
        thumbnail_url=metadata["microformat"]["microformatDataRenderer"]["thumbnail"]["thumbnails"][-1]["url"],
    )

    return filename


links = ["https://music.youtube.com/watch"]


@router.message(F.text.startswith(tuple(links)))
async def yt_music(message: types.Message) -> None:
    filename = f"{time.time_ns()}-{message.from_user.id}.mp3"
    await master_handler(
        message=message,
        send_function=message.answer_audio,
        download_function=lambda: download_yt_music(message.text, filename),
    )
