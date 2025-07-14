import os

for filename in os.listdir():
    if (
        filename.endswith(".mp3")
        or filename.endswith(".mp4")
        or filename.endswith(".part")
        or filename.endswith(".m4a")
        or filename.endswith(".ytdl")
    ):
        os.remove(filename)
