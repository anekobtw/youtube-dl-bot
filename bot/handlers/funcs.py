import os
import subprocess
from typing import Literal

import bs4
import requests
import youthon
import yt_dlp
from videoprops import get_video_properties


def download_yt_video(url: str, filename: str) -> None:
    """Downloading a YouTube shorts video at the best quality possible"""
    if youthon.Video(url).length_seconds > 60:
        raise Exception("Скачивание доступно только для видео типа shorts.")

    with yt_dlp.YoutubeDL({"format": "bv+ba/b", "outtmpl": filename}) as yt:
        yt.download([url])
        props = get_video_properties(filename + ".webm")
        if props["width"] > props["height"]:
            os.remove("video.mp4")
            raise Exception("Скачивание доступно только для видео типа shorts.")

    convert_command = ["ffmpeg", "-i", filename + ".webm", "-c:v", "copy", "-c:a", "copy", filename]
    subprocess.run(convert_command, check=True)
    os.remove(filename + ".webm")


def download_instagram_reel(url: str, filename: str) -> None:
    """Downloading instagram reels"""
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": filename,
        "quiet": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download complete!")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_x_video(url: str, filename: str) -> None:
    """https://github.com/z1nc0r3/twitter-video-downloader/tree/main"""
    response = requests.get(f"https://twitsave.com/info?url={url}", timeout=10)
    data = bs4.BeautifulSoup(response.text, "html.parser")
    download_button = data.find_all("div", class_="origin-top-right")[0]
    quality_buttons = download_button.find_all("a")
    highest_quality_url = quality_buttons[0].get("href")  # Highest quality video url

    response = requests.get(highest_quality_url, stream=True, timeout=10)
    block_size = 1024

    with open(filename, "wb") as file:
        for data in response.iter_content(block_size):
            file.write(data)


def download_tiktok_video(url: str, filename: str) -> str:
    """Saves a tiktok video and returns its filename"""
    ydl_opts = {"outtmpl": filename, "format": "best", "noplaylist": True, "quiet": False, "extractor_args": {"tiktok": {"webpage_download": True}}, "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_pinterest_image(url: str, filename: str) -> None:
    """Downloads pinterest image"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers, timeout=10)
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    image_meta = soup.find("meta", property="og:image")
    with open(filename, "wb") as image_file:
        image_file.write(requests.get(image_meta["content"], headers=headers, timeout=10).content)


def detect_platform(url: str) -> Literal["youtube", "instagram", "x", "tiktok", "unsupported"]:
    """Detects the platform from the url."""
    youtube_url_prefixes = ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/shorts/"]
    x_url_prefixes = ["https://x.com/", "https://twitter.com/"]
    tiktok_url_prefixes = ["https://www.tiktok.com/", "https://vt.tiktok.com/"]
    pinterest_url_prefixes = ["https://www.pinterest.com/pin/", "https://in.pinterest.com/pin/"]
    instagram_url_prefixes = ["https://instagram.com/reel/", "https://www.instagram.com/reel/"]

    if any(url.startswith(prefix) for prefix in youtube_url_prefixes):
        return "youtube"
    if any(url.startswith(prefix) for prefix in x_url_prefixes):
        return "x"
    if any(url.startswith(prefix) for prefix in tiktok_url_prefixes):
        return "tiktok"
    if any(url.startswith(prefix) for prefix in instagram_url_prefixes):
        return "instagram"
    if any(url.startswith(prefix) for prefix in pinterest_url_prefixes):
        return "pinterest"
    return "unsupported"
