# Any changes to this file may negatively impact performance.

import os
import subprocess
from typing import Literal

import bs4
import requests
import youthon
import yt_dlp
from dotenv import load_dotenv
from spotify_music_dl import SpotifyDownloader


class Downloader:
    def __init__(self) -> None:
        self.HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"}

    def download(self, platform: str, url: str, filename: str) -> str:
        platform_methods = {
            "YouTube": lambda u, f: self.download_youtube(u, f),
            "Instagram": lambda u, f: self.download_tiktok(u, f"{f}.mp4"),
            "TikTok": lambda u, f: self.download_tiktok(u, f"{f}.mp4"),
            "X": lambda u, f: self.download_tiktok(u, f"{f}.mp4"),
            "Pinterest": lambda u, f: self.download_pinterest(u, f"{f}.png"),
            "Spotify": lambda u, _: self.download_spotify(u),
        }

        if platform in platform_methods:
            return platform_methods[platform](url, filename)

        raise ValueError("Ссылка не поддерживается. Поддерживаемые ссылки - /supported_links")

    def download_youtube(self, url: str, filename: str) -> str:
        ydl_opts = {
            "outtmpl": f"{filename}.%(ext)s",
            "merge_output_format": "mp4",
            "format": f"bestvideo[height<=1080][filesize<=45M]+bestaudio[filesize<=5M]/best[vcodec=h264][height<=1080][filesize<=50M]",
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
                {"key": "FFmpegFixupM4a"},
                {"key": "FFmpegFixupStretched"},
            ],
            "postprocessor_args": ["-c:v", "h264", "-c:a", "aac"],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"{filename}.mp4"

    def download_tiktok(self, url: str, filename: str) -> str:
        with yt_dlp.YoutubeDL({"format": "best", "outtmpl": filename, "http_headers": self.HEADERS}) as yt:
            yt.download([url])
        return filename

    def download_pinterest(self, url: str, filename: str) -> str:
        img_url = bs4.BeautifulSoup(requests.get(url, headers=self.HEADERS).content, "html.parser").find("meta", property="og:image")["content"]
        with requests.get(img_url, stream=True, headers=self.HEADERS) as r, open(filename, "wb") as file:
            for chunk in r.iter_content(1024):
                file.write(chunk)
        return filename

    @staticmethod
    def download_spotify(url: str) -> str:
        load_dotenv()
        dl = SpotifyDownloader(os.getenv("SPOTIPY_CLIENT_ID"), os.getenv("SPOTIPY_CLIENT_SECRET"))
        dl.download_track(url)
        return next((f for f in os.listdir() if f.endswith(".mp3")), None)


class PlatformDetector:
    def __init__(self) -> None:
        self.PLATFORMS = {
            "YouTube": ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/shorts/"],
            "X": ["https://x.com/", "https://twitter.com/"],
            "TikTok": ["https://www.tiktok.com/", "https://vt.tiktok.com/", "https://vm.tiktok.com/"],
            "Instagram": ["https://www.instagram.com/reel/", "https://instagram.com/reel/", "https://www.instagram.com/share/"],
            "Pinterest": ["https://pin.it/", "https://www.pinterest.com/pin/", "https://in.pinterest.com/pin/"],
            "Spotify": ["https://open.spotify.com/track/"],
        }

    def detect_platform(self, url: str) -> str:
        return next((platform for platform, prefixes in self.PLATFORMS.items() if any(url.startswith(p) for p in prefixes)), "unsupported")

    def get_links_text(self) -> str:
        res = ""
        for platform, links in self.PLATFORMS.items():
            res += f"<b>{platform}</b>\n" + "\n".join(links) + "\n\n"
        return res
