import os
import subprocess
from typing import Literal

import bs4
import requests
import youthon
import yt_dlp


class Downloader:
    def __init__(self, url: str, filename: str) -> None:
        self.url = url
        self.filename = filename
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

        platform = self.detect_platform(url)
        if platform == "unsupported":
            raise ValueError("Ссылка не поддерживается. Поддерживаемые ссылки - /supported_links")

        self.filename = self.download(platform)

    def download(self, platform: str) -> str:
        """Download the content based on the detected platform."""
        match platform:
            case "youtube" | "instagram":
                if platform == "youtube" and youthon.Video(self.url).length_seconds > 60:
                    raise ValueError("Only YouTube Shorts can be downloaded.")
                return download_video(self.url, self.filename + ".mp4")
            case "tiktok":
                return download_tiktok_video(self.url, self.filename + ".mp4", self.headers)
            case "x":
                return download_x_video(self.url, self.filename + ".mp4")
            case "pinterest":
                return download_pinterest_image(self.url, self.filename + ".png", self.headers)
            case "spotify":
                return download_spotify_track(self.url)
            case _:
                raise ValueError("Ссылка не поддерживается. Поддерживаемые ссылки - /supported_links")

    @staticmethod
    def detect_platform(url: str) -> Literal["youtube", "instagram", "x", "tiktok", "spotify", "unsupported"]:
        """Detects the platform from the URL using prefix matching."""
        platform_prefixes = {
            "youtube": ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/shorts/"],
            "x": ["https://x.com/", "https://twitter.com/"],
            "tiktok": ["https://www.tiktok.com/", "https://vt.tiktok.com/"],
            "instagram": ["https://www.instagram.com/reel/", "https://instagram.com/reel/"],
            "pinterest": ["https://pin.it/", "https://www.pinterest.com/pin/", "https://in.pinterest.com/pin/"],
            "spotify": ["https://open.spotify.com/track/"],
        }

        for platform, prefixes in platform_prefixes.items():
            if any(url.startswith(prefix) for prefix in prefixes):
                return platform
        return "unsupported"


# ------------------ Handlers ------------------


def download_video(url: str, filename: str) -> None:
    """Download a YouTube or Instagram video (similar logic for both)."""
    with yt_dlp.YoutubeDL({"format": "best", "outtmpl": filename, "quiet": True}) as yt:
        yt.download([url])


def download_tiktok_video(url: str, filename: str, headers: dict) -> None:
    """Download a TikTok video."""
    with yt_dlp.YoutubeDL({"outtmpl": filename, "format": "best", "quiet": False, "extractor_args": {"tiktok": {"webpage_download": True}}, "http_headers": headers}) as ydl:
        ydl.download([url])


def download_x_video(url: str, filename: str) -> None:
    """Download a video from X (formerly Twitter)."""
    response = requests.get(f"https://twitsave.com/info?url={url}", timeout=10)
    response.raise_for_status()
    highest_quality_url = bs4.BeautifulSoup(response.text, "html.parser").find("div", class_="origin-top-right").find("a")["href"]

    with requests.get(highest_quality_url, stream=True, timeout=10) as r, open(filename, "wb") as file:
        r.raise_for_status()
        for chunk in r.iter_content(1024):
            file.write(chunk)


def download_pinterest_image(url: str, filename: str, headers: dict) -> None:
    """Download an image from Pinterest."""
    soup = bs4.BeautifulSoup(requests.get(url, headers=headers, timeout=10).content, "html.parser")
    img_url = soup.find("meta", property="og:image")["content"]
    with open(filename, "wb") as image_file:
        image_file.write(requests.get(img_url, headers=headers, timeout=10).content)


def download_spotify_track(url: str) -> None:
    """Download a Spotify track."""
    subprocess.run(["spotdl", url], check=True)
    for filename in os.listdir():
        if filename.endswith(".mp3"):
            return filename
