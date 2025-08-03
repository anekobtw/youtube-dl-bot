import asyncio
import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pyngrok import ngrok
from yt_dlp import YoutubeDL

os.makedirs("files", exist_ok=True)

app = FastAPI()
ngrok_tunnel = ngrok.connect(8000)
public_url = ngrok_tunnel.public_url


class DownloadRequest(BaseModel):
    url: str


app.mount("/files", StaticFiles(directory="files"), name="files")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/download")
def download_video(request: DownloadRequest):
    ydl_opts = {
        "outtmpl": "files/%(title)s.%(ext)s",
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url)
            filename = ydl.prepare_filename(info)
            video_url = f"{public_url}/files/{os.path.basename(filename)}"
        return {"status": "success", "video_url": video_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    asyncio.run(uvicorn.run("main:app", host="0.0.0.0", port=8000))
