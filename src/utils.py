import asyncio
import uuid
from pathlib import Path

import yt_dlp
from aiogram import types

from enums import ProgressState

VIDEOS_DIR = Path("videos")
VIDEOS_DIR.mkdir(exist_ok=True)


def format_bytes(value: int | float | None) -> str:
    if value is None:
        return "N/A"

    value = float(value)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024:
            return f"{value:.1f} {unit}"
        value /= 1024

    return f"{value:.1f} TB"


def format_time(seconds: int | None) -> str:
    if seconds is None:
        return "N/A"

    minutes, seconds = divmod(seconds, 60)
    if minutes >= 60:
        hours, minutes = divmod(minutes, 60)
        return f"{hours}:{minutes:02}:{seconds:02}"

    return f"{minutes:02}:{seconds:02}"


def get_percentage(data: dict) -> float:
    downloaded = data.get("downloaded_bytes", 0)
    total = data.get("total_bytes") or data.get("total_bytes_estimate")

    return downloaded / total * 100 if total else 0


def format_message(
    state: ProgressState,
    progress: float = 0,
) -> str:
    steps = [
        ProgressState.PREPARING,
        ProgressState.VIDEO_DOWNLOADING,
        ProgressState.AUDIO_DOWNLOADING,
        ProgressState.FINALIZING,
    ]

    lines = []

    for step in steps:
        if steps.index(step) < steps.index(state):
            lines.append(f"✅ {step.value}")
        elif step == state:
            if step in (
                ProgressState.VIDEO_DOWNLOADING,
                ProgressState.AUDIO_DOWNLOADING,
            ):
                lines.append(f"🔄 {step.value} ({progress:.1f}%)")
            else:
                lines.append(f"🔄 {step.value}")
        else:
            lines.append(f"⏳ {step.value}")

    return "\n".join(lines)


async def download_video(msg: types.Message, url: str):
    loop = asyncio.get_running_loop()
    last_update = [0.0]
    progress = [0.0]
    current_state = [ProgressState.VIDEO_DOWNLOADING]

    async def update_progress() -> None:
        await msg.edit_text(
            format_message(
                current_state[0],
                progress[0],
            )
        )

    def progress_hook(data):
        if data["status"] != "downloading":
            return

        info = data.get("info_dict", {})

        if info.get("vcodec") == "none":
            current_state[0] = ProgressState.AUDIO_DOWNLOADING
        else:
            current_state[0] = ProgressState.VIDEO_DOWNLOADING

        progress[0] = get_percentage(data)

        now = loop.time()
        if now - last_update[0] < 1:
            return

        last_update[0] = now

        asyncio.run_coroutine_threadsafe(
            update_progress(),
            loop,
        )

    def download():
        video_id = str(uuid.uuid4())

        options = {
            "format": "bestvideo[vcodec^=avc1][ext=mp4]+bestaudio[acodec^=mp4a]/mp4",
            "merge_output_format": "mp4",
            "outtmpl": str(VIDEOS_DIR / f"{video_id}.%(ext)s"),
            "noplaylist": True,
            "concurrent_fragment_downloads": 4,
            "progress_hooks": [progress_hook],
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)

            return {
                "filename": ydl.prepare_filename(info),
                "width": info.get("width", 0),
                "height": info.get("height", 0),
            }

    info = await loop.run_in_executor(None, download)

    await msg.edit_text(format_message(ProgressState.FINALIZING))

    return {
        "filename": info["filename"],
        "width": info["width"],
        "height": info["height"],
    }
