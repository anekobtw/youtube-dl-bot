"""
Helper functions
"""

import os

import bs4
import ffmpeg
import requests
import youthon
import yt_dlp
from videoprops import get_video_properties


def download_video_best(url: str, output_path: str) -> None:
    """Downloading a YouTube shorts video at the best quality possible"""
    if youthon.Video(url).length_seconds > 60:
        raise Exception("Скачивание доступно только для видео типа shorts.")

    with yt_dlp.YoutubeDL({"format": "bestvideo", "outtmpl": "video.mp4", "quiet": True}) as yt:
        yt.download([url])
        if not is_shorts("video.mp4"):
            os.remove("video.mp4")
            raise Exception("Скачивание доступно только для видео типа shorts.")
    with yt_dlp.YoutubeDL({"format": "bestaudio", "outtmpl": "audio.mp3", "quiet": True}) as yt:
        yt.download([url])

    ffmpeg.output(ffmpeg.input("video.mp4"), ffmpeg.input("audio.mp3"), output_path, vcodec="copy", acodec="copy").run()
    os.remove("video.mp4")
    os.remove("audio.mp3")


def is_shorts(video_path: str) -> bool:
    """Checking whether a video is horizontal or vertical"""
    props = get_video_properties(video_path)
    return props['width'] < props['height']


def download_video(url: str, filename: str) -> None:
    """https://github.com/z1nc0r3/twitter-video-downloader/tree/main"""
    response = requests.get(url, stream=True)
    block_size = 1024

    with open(filename, "wb") as file:
        for data in response.iter_content(block_size):
            file.write(data)


def download_x_video(url: str, filename: str) -> None:
    """https://github.com/z1nc0r3/twitter-video-downloader/tree/main"""
    response = requests.get(f"https://twitsave.com/info?url={url}")
    data = bs4.BeautifulSoup(response.text, "html.parser")
    download_button = data.find_all("div", class_="origin-top-right")[0]
    quality_buttons = download_button.find_all("a")
    highest_quality_url = quality_buttons[0].get("href") # Highest quality video url
    download_video(highest_quality_url, filename)
