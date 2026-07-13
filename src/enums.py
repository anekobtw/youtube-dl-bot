from enum import Enum


class Links(Enum):
    STANDART = [
        # YouTube
        "https://www.youtube.com/",
        "https://youtu.be/",
        "https://www.youtube.com/shorts/",
        "https://youtube.com/shorts/",
        # TikTok
        "https://www.tiktok.com/",
        "https://vt.tiktok.com/",
        "https://vm.tiktok.com/",
        # Instagram
        "https://www.instagram.com/reel/",
        "https://instagram.com/reel/",
        "https://www.instagram.com/share/",
        # Twitter (X)
        "https://x.com/",
        "https://twitter.com/",
        # Facebook
        "https://www.facebook.com/reel/",
        "https://www.facebook.com/share/",
    ]


class VideoStatusMessages(Enum):
    VideoProcessing = "<code>{url}</code>\n\n⏳ Your video is being processed..."
    VideoSuccess = "<code>{url}</code>\n\n✅ Your video has been successfully downloaded. Sending..."
    VideoHostRedirect = (
        "⚠️ The video is too large to send through Telegram.\n"
        "We're temporarily hosting it on our servers. Please save it locally if you need it later.\n\n"
        "{download_url}\n\n"
        "<b><i>downloaded via @free_yt_dl_bot</i></b>"
    )
    VideoError = "<code>{url}</code>\n\n⚠️ An error occurred during the download."
    Caption = "<b><i><a href='https://t.me/free_yt_dl_bot'>via</a> | <a href='{url}'>link</a></i></b>"


class ProgressState(Enum):
    PREPARING = "Preparing"
    VIDEO_DOWNLOADING = "Downloading video"
    AUDIO_DOWNLOADING = "Downloading audio"
    FINALIZING = "Finalizing"
