"""
Helper functions
"""

import urllib.parse

import requests
import youtubesearchpython


def get_video_info(url: str) -> str:
    """Returns a string with basic info about the video"""
    video = youtubesearchpython.Video.getInfo(url)
    return f"<b>Автор:</b> {video['channel']['name']}\n<b>Название:</b> {video['title']}\n<b>Просмотры:</b> {video['viewCount']['text']}\n\n<b>Ссылка:</b> {video['link']}"


def shorten_url(url: str) -> str | None:
    """Returns a shorter url"""
    encoded_url = urllib.parse.quote(url, safe="")
    response = requests.get(f"https://is.gd/create.php?format=simple&url={encoded_url}", timeout=10)
    return response.text if response.status_code == 200 else None
