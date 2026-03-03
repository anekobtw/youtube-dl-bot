# `youtube-dl-bot`

![version](https://img.shields.io/badge/Version-3.8.0-blue)
![license](https://img.shields.io/badge/License-CC-red)
![python](https://img.shields.io/badge/Python-3.10%2B-blue)

A Telegram bot for downloading videos from different platforms directly in your chats.

**Live Bot**: [@free_yt_dl_bot](https://t.me/free_yt_dl_bot)

## Setup

### Docker (Recommended)
```
$ docker build -t youtube-dl-bot .
$ docker run -d --name youtube-dl-bot-container -e TOKEN=your_telegram_bot_token_here youtube-dl-bot
```

### Manual

1. Install Python

2. Install [ffmpeg](https://ffmpeg.org/download.html)

3. Acquire bot token from [@BotFather](https://t.me/BotFather)

4. Create a `.env` file with:

```
TOKEN=your_telegram_bot_token_here
``` 

5. Clone and install dependencies:

```bash
$ git clone https://github.com/anekobtw/youtube-dl-bot.git
$ poetry install
```

6. Run the bot

```bash
$ cd src
$ poetry run python main.py
```

## Contributing
Pull requests, bug reports, and feature suggestions are welcome! Please read our [Code of Conduct](https://github.com/anekobtw/youtube-dl-bot/blob/main/CODE_OF_CONDUCT.md)

## License
The project is under MIT licence.

> // Maintained with ❤️ by [@anekobtw](https://github.com/anekobtw)
