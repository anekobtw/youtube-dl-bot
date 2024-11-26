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
        "youtube": ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/shorts/"],
        "x": ["https://x.com/", "https://twitter.com/"],
        "tiktok": ["https://www.tiktok.com/", "https://vt.tiktok.com/"],
        "instagram": ["https://www.instagram.com/reel/", "https://instagram.com/reel/"],
        "pinterest": ["https://pin.it/", "https://www.pinterest.com/pin/", "https://in.pinterest.com/pin/"],
        "spotify": ["https://open.spotify.com/track/"],
    }

    def __init__(self, url: str, filename: str) -> None:
        self.url = url
        self.filename = filename
        platform = self.detect_platform(url)
        if platform == "unsupported":
            raise ValueError("Ссылка не поддерживается. Поддерживаемые ссылки - /supported_links")

        self.filename = self.download(platform)

    def download(self, platform: str) -> str:
        """Download content based on the detected platform."""
        if platform == "youtube":
            if youthon.Video(self.url).length_seconds > 60:
                raise ValueError("Скачивание доступно только для видео короче 1 минуты.")
            return self.download_video(self.url, f"{self.filename}.mp4")
        elif platform in ["instagram", "tiktok", "x"]:
            return self.download_video(self.url, f"{self.filename}.mp4", True)
        elif platform == "pinterest":
            return self.download_pinterest_image(self.url, f"{self.filename}.png")
        elif platform == "spotify":
            return self.download_spotify_track(self.url)
        else:
            raise ValueError("Ссылка не поддерживается. Поддерживаемые ссылки - /supported_links")

    @staticmethod
    def detect_platform(url: str) -> Literal["youtube", "instagram", "x", "tiktok", "spotify", "unsupported"]:
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
        soup = bs4.BeautifulSoup(requests.get(url, headers=Downloader.HEADERS, timeout=10).content, "html.parser")
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
        with requests.get(url, stream=True, headers=Downloader.HEADERS, timeout=10) as r:
            r.raise_for_status()
            with open(filename, "wb") as file:
                for chunk in r.iter_content(1024):
                    file.write(chunk)
