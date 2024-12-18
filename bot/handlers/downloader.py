# Any changes to this file may negatively impact performance.

import os
import subprocess
from typing import Literal

import bs4
import requests
import youthon
import yt_dlp


class Downloader:
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    PLATFORM_PREFIXES = {
        "YouTube": ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/shorts/"],
        "X": ["https://x.com/", "https://twitter.com/"],
        "TikTok": ["https://www.tiktok.com/", "https://vt.tiktok.com/", "https://vm.tiktok.com/"],
        "Instagram": ["https://www.instagram.com/reel/", "https://instagram.com/reel/"],
        "Pinterest": ["https://pin.it/", "https://www.pinterest.com/pin/", "https://in.pinterest.com/pin/"],
        "Spotify": ["https://open.spotify.com/track/"],
    }

    def download(self, platform: str, url: str, filename: str) -> str:
        """Download content based on the detected platform."""
        if platform == "YouTube":
            if youthon.Video(url).length_seconds > 60:
                raise ValueError("Скачивание доступно только для видео короче 1 минуты.")
            return self.download_video(url, f"{filename}.mp4")
        elif platform in ["Instagram", "TikTok", "X"]:
            return self.download_video(url, f"{filename}.mp4", True)
        elif platform == "Pinterest":
            return self.download_pinterest_image(url, f"{filename}.png")
        elif platform == "Spotify":
            return self.download_spotify_track(url)
        else:
            raise ValueError("Ссылка не поддерживается. Поддерживаемые ссылки - /supported_links")

    @staticmethod
    def detect_platform(url: str) -> Literal["YouTube", "Instagram", "X", "TikTok", "Spotify", "unsupported"]:
        """Detects the platform from the URL using prefix matching."""
        for platform, prefixes in Downloader.PLATFORM_PREFIXES.items():
            if any(url.startswith(prefix) for prefix in prefixes):
                return platform
        return "unsupported"

    def download_video(self, url: str, filename: str, extra_args: bool = None) -> str:
        """Download a video from supported platforms."""
        ydl_options = {
            "format": "best",
            "outtmpl": filename,
            "quiet": True,
            "http_headers": Downloader.HEADERS
        }

        if extra_args:
            ydl_options["extractor_args"] = {"tiktok": {"webpage_download": True}}

        with yt_dlp.YoutubeDL(ydl_options) as yt:
            yt.download([url])

        return filename

    def download_pinterest_image(self, url: str, filename: str) -> str:
        """Download an image from Pinterest."""
        soup = bs4.BeautifulSoup(requests.get(url, headers=Downloader.HEADERS).content, "html.parser")
        img_url = soup.find("meta", property="og:image")["content"]
        self.download_file(img_url, filename)
        return filename

    @staticmethod
    def download_spotify_track(url: str) -> str:
        """Download a Spotify track."""
        subprocess.run(["spotdl", url], check=True)
        for filename in os.listdir():
            if filename.endswith(".mp3"):
                return filename
        raise FileNotFoundError("Spotify track download failed.")

    @staticmethod
    def download_file(url: str, filename: str) -> None:
        """Generic file download helper."""
        with requests.get(url, stream=True, headers=Downloader.HEADERS) as r:
            r.raise_for_status()
            with open(filename, "wb") as file:
                for chunk in r.iter_content(1024):
                    file.write(chunk)
