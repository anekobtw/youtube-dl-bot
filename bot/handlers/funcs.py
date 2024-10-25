import urllib.parse

import requests
import youtubesearchpython


def get_video_info(url: str) -> str:
    video = youtubesearchpython.Video.getInfo(url)
    return f"<b>Автор:</b> {video['channel']['name']}\n" f"<b>Название:</b> {video['title']}\n" f"<b>Просмотры:</b> {video['viewCount']['text']}\n\n" f"<b>Ссылка:</b> {video['link']}"


def shorten_url(url: str) -> str:
    encoded_url = urllib.parse.quote(url, safe="")
    response = requests.get(f"https://is.gd/create.php?format=simple&url={encoded_url}")
    if response.status_code == 200:
        return response.text
