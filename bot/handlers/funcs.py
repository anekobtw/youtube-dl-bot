"""
Helper functions
"""

import os

import ffmpeg
import youthon
import yt_dlp
from moviepy.editor import VideoFileClip


def get_video_info(url: str) -> str:
    """Returns a string with basic info about the video"""
    video = youthon.Video(url)
    return f"<b>Автор:</b> {video.author_name}\n<b>Название:</b> {video.title}\n<b>Просмотры:</b> {video.views}\n\n<b>Ссылка:</b> {video.video_url}"


def download_video_best(url: str, output_path: str) -> None:
    """Downloading a YouTube shorts video at the best quality possible"""
    if youthon.Video(url).length_seconds > 60:
        raise Exception("Скачивание доступно только для shorts видео.")

    with yt_dlp.YoutubeDL({"format": "bestvideo", "outtmpl": "video.mp4", "quiet": True}) as yt:
        yt.download([url])
    with yt_dlp.YoutubeDL({"format": "bestaudio", "outtmpl": "audio.mp3", "quiet": True}) as yt:
        yt.download([url])

    if not is_shorts("video.mp4"):
        os.remove("video.mp4")
        os.remove("audio.mp3")
        raise Exception("Скачивание доступно только для shorts видео.")

    ffmpeg.output(ffmpeg.input("video.mp4"), ffmpeg.input("audio.mp3"), output_path, vcodec="copy", acodec="copy").run()
    os.remove("video.mp4")
    os.remove("audio.mp3")


def is_shorts(video_path: str) -> bool:
    """Checking whether a video is horizontal or vertical"""
    return VideoFileClip(video_path).size[0] < VideoFileClip(video_path).size[1]
