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


class Messages(Enum):
    API_Finding = "<code>{url}</code>\n\n🟡 Checking if API is working."
    API_Found = "<code>{url}</code>\n\n🟢 API is working. Preparing your video."
    API_NotFound = "<code>{url}</code>\n\n🔴 Unfortunately, our API is not working now. We will still try to download your video. Check /api for more info."

    VideoDownloaded = "<code>{url}</code>\n\nUnfortunately, the video exceeds Telegram limits. Please, download it from a temporary link below."
    ErrorOccured = "<code>{url}</code>\n\nOops! This video might be age-restricted or too large to download."

    Promo = (
        "Hi! I'm <b>@free_yt_dl_bot</b> — 100% free, no ads, no forced subscriptions.\n\n"
        "If you like my work, support me by checking out my "
        "<b><a href='https://t.me/anekobtw_c'>Telegram news channel</a></b> 😊\n\n"
        "<b>This message will self-delete in 15 seconds.</b>"
    )  # fmt: skip

    Caption = "<b><i><a href='https://t.me/free_yt_dl_bot'>via</a> | <a href='{url}'>link</a></i></b>"

    Start = """
Hello, @{username}! Just send the link to the video.

ℹ️ <b>We don’t collect any data.</b>

❗ <b>If the bot isn’t working, don’t worry</b> — your request will be processed automatically once we're back online.

🙏 <b>Please don’t block the bot</b> — it needs to message you when the download is ready.
"""

    Api = """
API status: {status}

<b>Why do we need the API?</b>

Telegram bots can't send videos larger than 50 MB.  
Our custom API bypasses this by:

• Enabling <b>faster downloads</b>  
• Supporting <b>best quality videos</b>  
• Offering <b>unlimited storage</b>
"""

    def f(self, **kwargs) -> str:
        return self.value.format(**kwargs)
