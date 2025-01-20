import asyncio
import os
import time

from aiogram import F, Router, types
from dotenv import load_dotenv
from spotify_music_dl import SpotifyDownloader

from handlers.modules.master import master_handler

router = Router()
load_dotenv()
dl = SpotifyDownloader(os.getenv("SPOTIPY_CLIENT_ID"), os.getenv("SPOTIPY_CLIENT_SECRET"))


def download_spotify_track(url: str, filename: str) -> str:
    asyncio.run(dl.download_track(url, filename))
    return filename


async def download_spotify_playlist(url: str, directory_name: str) -> str:
    await dl.download_playlist(url, directory_name)
    return directory_name


@router.message(F.text.startswith("https://open.spotify.com/track/"))
async def spotify_track(message: types.Message) -> None:
    filename = f"{time.time_ns()}-{message.from_user.id}.mp3"
    await master_handler(
        message=message,
        send_function=message.answer_audio,
        download_function=lambda: download_spotify_track(message.text, filename),
    )


@router.message(F.text.startswith("https://open.spotify.com/playlist/"))
async def spotify_playlist(message: types.Message) -> None:
    msg = await message.answer("Плейлист скачивается, это займет много времени. Пожалуйста, подождите.")

    dirname = f"{time.time_ns()}-{message.from_user.id}"
    await download_spotify_playlist(message.text, dirname)
    for filename in os.listdir(dirname):
        file_path = os.path.join(dirname, filename)
        await message.answer_audio(audio=types.FSInputFile(file_path), caption="@free_yt_dl_bot")
        os.remove(file_path)

    os.removedirs(dirname)
    await msg.delete()
    await message.delete()
