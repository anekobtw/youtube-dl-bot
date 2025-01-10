import os
import time

from aiogram import F, Router, types
from dotenv import load_dotenv
from spotify_music_dl import SpotifyDownloader

from handlers.modules.master import master_handler

router = Router()


async def download_spotify_song(url: str, filename: str) -> str:
    load_dotenv()
    dl = SpotifyDownloader(os.getenv("SPOTIPY_CLIENT_ID"), os.getenv("SPOTIPY_CLIENT_SECRET"))
    await dl.download_track(url, filename)
    return filename

async def download_spotify_playlist(url: str, directory_name: str) -> str:
    load_dotenv()
    dl = SpotifyDownloader(os.getenv("SPOTIPY_CLIENT_ID"), os.getenv("SPOTIPY_CLIENT_SECRET"))
    await dl.download_playlist(url, directory_name)
    return directory_name


@router.message(F.text.startswith("https://open.spotify.com/track/"))
async def spotify_song(message: types.Message) -> None:
    msg = await message.answer("Плейлист скачивается, это займет много времени. Пожалуйста, подождите.")

    filename = f"{time.time_ns()}-{message.from_user.id}.mp3"
    await download_spotify_song(message.text, filename)
    await message.answer_audio(types.FSInputFile(filename), caption="@free_yt_dl_bot")
    os.remove(filename)

    await msg.delete()
    await message.delete()



@router.message(F.text.startswith("https://open.spotify.com/playlist/"))
async def spotify_playlist(message: types.Message) -> None:
    msg = await message.answer("Плейлист скачивается, это займет много времени. Пожалуйста, подождите.")

    dirname = f"{time.time_ns()}-{message.from_user.id}"
    # dirname = "1736535679254233724-1718021890"
    await download_spotify_playlist(message.text, dirname)
    for filename in os.listdir(dirname):
        file_path = os.path.join(dirname, filename)
        await message.answer_audio(audio=types.FSInputFile(file_path), caption="@free_yt_dl_bot")
        os.remove(file_path)

    os.removedirs(dirname)
    await msg.delete()
    await message.delete()
