import json
import subprocess
import urllib.parse

import requests
import youtubesearchpython
from vosk import KaldiRecognizer, Model


class Transcryptor:
    def __init__(self) -> None:
        self.sample_rate = 16000
        self.model = Model("vosk-model-small-ru-0.22")
        self.rec = KaldiRecognizer(self.model, self.sample_rate)
        self.cur_res = ""

    def __append(self, res) -> None:
        js = json.loads(res)
        if "text" in js.keys():
            self.cur_res += js["text"]
        if "partial" in js.keys():
            self.cur_res += js["partial"]
        self.cur_res += ".\n"

    def transcrypt(self, file_path) -> str:
        self.cur_res = ""
        process = subprocess.Popen(
            [
                "ffmpeg",
                "-loglevel",
                "quiet",
                "-i",
                file_path,
                "-ar",
                str(self.sample_rate),
                "-ac",
                "1",
                "-f",
                "s16le",
                "-",
            ],
            stdout=subprocess.PIPE,
        )
        while True:
            data = process.stdout.read(4000)

            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                self.__append(self.rec.Result())
            else:
                print(self.rec.PartialResult())
        self.__append(self.rec.FinalResult())

        self.cur_res = self.cur_res[:-2]
        return self.cur_res


def get_video_info(url: str) -> str:
    video = youtubesearchpython.Video.getInfo(url)
    return f"<b>Автор:</b> {video['channel']['name']}\n" f"<b>Название:</b> {video['title']}\n" f"<b>Просмотры:</b> {video['viewCount']['text']}\n\n" f"<b>Ссылка:</b> {video['link']}"


def shorten_url(url: str) -> str:
    encoded_url = urllib.parse.quote(url, safe="")
    response = requests.get(f"https://is.gd/create.php?format=simple&url={encoded_url}")
    if response.status_code == 200:
        return {response.text}
