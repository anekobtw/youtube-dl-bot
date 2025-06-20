import asyncio
from pathlib import Path
from typing import Callable

import yt_dlp


class Downloader:
    currently_downloading = set()

    async def run(self, url: str, quality: str) -> str:
        if quality == "video":
            return await self._async_download(lambda: self.download_video(url))
        elif quality == "audio":
            return await self._async_download(lambda: self.download_audio(url))

    @staticmethod
    async def _async_download(func: Callable) -> str:
        return await asyncio.to_thread(func)

    @staticmethod
    def download_video(url: str) -> str:
        opts = {
            "format": "best",
            "quiet": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename, (info['width'], info['height'])

    @staticmethod
    def download_audio(url: str) -> str:
        opts = {
            "format": "bestaudio[ext=m4a]/bestaudio",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                    "preferredquality": "320",
                }
            ],
            "quiet": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
