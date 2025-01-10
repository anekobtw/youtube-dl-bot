import os

from aiogram import F, Router, types
from dotenv import load_dotenv
from spotify_music_dl import SpotifyDownloader

from handlers.modules.master import master_handler

router = Router()


def download_spotify(url: str) -> str:
    load_dotenv()
    dl = SpotifyDownloader(os.getenv("SPOTIPY_CLIENT_ID"), os.getenv("SPOTIPY_CLIENT_SECRET"))
    dl.download_track(url)
    return next((f for f in os.listdir() if f.endswith(".mp3")))


links = [
    "https://open.spotify.com/track/",
]


@router.message(F.text.startswith(tuple(links)))
async def spotify(message: types.Message) -> None:
    await master_handler(
        message=message,
        send_function=message.answer_audio,
        download_function=lambda: download_spotify(message.text),
    )
