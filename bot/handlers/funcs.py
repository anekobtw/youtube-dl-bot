from typing import Literal

import bs4
import requests
import youthon
import yt_dlp


class Downloader:
    def __init__(self, url: str, filename_prefix: str) -> None:
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        platform = self.detect_platform(url)

        match platform:
            case "youtube":
                self.filename = filename_prefix + ".mp4"
                self.download_yt_video()
            case "instagram":
                self.filename = filename_prefix + ".mp4"
                self.download_yt_video()
            case "tiktok":
                self.filename = filename_prefix + ".mp4"
                self.download_tiktok_video()
            case "x":
                self.filename = filename_prefix + ".mp4"
                self.download_x_video()
            case "pinterest":
                self.filename = filename_prefix + ".png"
                self.download_pinterest_image()
            case "unsupported":
                raise Exception("Данная ссылка не поддерживается.\nПоддерживаемые ссылки - /supported_links")

    def download_yt_video(self) -> None:
        if youthon.Video(self.url).length_seconds > 60:
            raise Exception("Скачивание доступно только для видео типа shorts.")

        with yt_dlp.YoutubeDL({"format": "best", "outtmpl": self.filename, "quiet": True}) as yt:
            yt.download([self.url])

    def download_tiktok_video(self) -> None:
        with yt_dlp.YoutubeDL({"outtmpl": self.filename, "format": "best", "quiet": False, "extractor_args": {"tiktok": {"webpage_download": True}}, "http_headers": self.headers}) as ydl:
            ydl.download([self.url])

    def download_pinterest_image(self) -> None:
        response = requests.get(self.url, headers=self.headers, timeout=10)
        assert response.status_code == 200
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        image_meta = soup.find("meta", property="og:image")
        with open(self.filename, "wb") as image_file:
            image_file.write(requests.get(image_meta["content"], headers=self.headers, timeout=10).content)

    def download_x_video(self) -> None:
        """https://github.com/z1nc0r3/twitter-video-downloader/tree/main"""
        response = requests.get(f"https://twitsave.com/info?url={self.url}", timeout=10)
        data = bs4.BeautifulSoup(response.text, "html.parser")
        download_button = data.find_all("div", class_="origin-top-right")[0]
        quality_buttons = download_button.find_all("a")
        highest_quality_url = quality_buttons[0].get("href")

        response = requests.get(highest_quality_url, stream=True, timeout=10)
        with open(self.filename, "wb") as file:
            for data in response.iter_content(1024):
                file.write(data)

    @staticmethod
    def detect_platform(url: str) -> Literal["youtube", "instagram", "x", "tiktok", "unsupported"]:
        """Detects the platform from the url."""
        youtube_url_prefixes = ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/shorts/"]
        x_url_prefixes = ["https://x.com/", "https://twitter.com/"]
        tiktok_url_prefixes = ["https://www.tiktok.com/", "https://vt.tiktok.com/"]
        pinterest_url_prefixes = ["https://www.pinterest.com/pin/", "https://in.pinterest.com/pin/"]
        instagram_url_prefixes = ["https://instagram.com/reel/"]

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
