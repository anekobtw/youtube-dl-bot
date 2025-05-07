import asyncio
import os
import random
from typing import Callable

import requests
import videoprops
import yt_dlp
from aiogram import exceptions, types

from enums import Databases, ErrorMessage, Messages


class Downloader:
    currently_downloading = set()

    def __init__(self, message: types.Message, url: str, quality: str):
        self.message = message
        self.user_id = message.from_user.id
        self.url = url.strip()
        self.quality = quality
        self.filename = f"{self.user_id}.{'m4a' if quality == 'audio' else 'mp4'}"
        Databases.ud.value.create_user(self.user_id, "en")
        self.lang = Databases.ud.value.get_lang(self.user_id)

    async def run(self) -> None:
        if self.user_id in Downloader.currently_downloading:
            await self.message.answer(ErrorMessage.MULTIPLE_VIDEOS_ERROR.value[self.lang])
            return

        Downloader.currently_downloading.add(self.user_id)
        status_msg = await self.message.answer(Messages.PREPARING.value[self.lang])

        try:
            self.filename = await self._async_download(lambda: self._download(self.url, self.filename, self.quality))
            self.filename = os.path.basename(self.filename)
            if self.filename.endswith(".mp4"):
                props = videoprops.get_video_properties(self.filename)
                await self.message.answer_video(types.FSInputFile(self.filename), caption=Messages.BOT_CAPTION.value, height=props["height"], width=props["width"])
            else:
                await self.message.answer_audio(types.FSInputFile(self.filename), caption=Messages.BOT_CAPTION.value)

            await self.message.delete()
            await status_msg.delete()

            if random.randint(1, 5) == 1:
                promo_msg = await self.message.answer(Messages.PROMO.value[self.lang])
                await asyncio.sleep(15)
                await promo_msg.delete()

        except exceptions.TelegramEntityTooLarge:
            msg = await self.message.answer(ErrorMessage.SIZE_LIMIT.value[self.lang])
            await msg.edit_text(self._publish(self.filename))
            await self.message.delete()

        except yt_dlp.DownloadError as e:
            await self._log_error(ErrorMessage.YT_DLP_ERROR.value[self.lang].format(url=self.url), e)

        except Exception as e:
            await self._log_error(ErrorMessage.GENERAL_ERROR.value[self.lang], e)

        finally:
            Downloader.currently_downloading.discard(self.user_id)
            if os.path.exists(self.filename):
                os.remove(self.filename)

    @staticmethod
    async def _async_download(func: Callable) -> str:
        return await asyncio.to_thread(func)

    @staticmethod
    def _download(url: str, filename: str, quality: str) -> str:
        opts = {
            "format": "best" if quality == "video" else "bestaudio[ext=m4a]",
            "outtmpl": "%(title)s.%(ext)s",
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)

    @staticmethod
    def _publish(filename: str) -> str:
        with open(filename, "rb") as file:
            headers = {"filename": filename, "Content-Type": "application/octet-stream"}
            response = requests.post(
                url="https://filebin.net",
                files={"file": file},
                data={"bin": "anekobtw"},
                headers=headers,
            )
        res = response.json()
        return f"https://filebin.net/{res['bin']['id']}/{res['file']['filename']}"

    async def _log_error(self, user_message: str, exception_obj: Exception):
        await self.message.answer(user_message)
        await self.message.bot.send_message(
            chat_id=1718021890,
            text=f"<b>❗ Произошёл баг при скачивании видео:</b>\n<code>{self.url}</code>\n\n{exception_obj}",
        )
