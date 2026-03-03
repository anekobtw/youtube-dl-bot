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
    VideoNotSent = "<code>{url}</code>\n\n❌ Unfortunately, the video exceeds Telegram limits."
    VideoError = "<code>{url}</code>\n\n⚠️ An error occurred during the download."
