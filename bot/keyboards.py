"""
Keyboards
"""

from aiogram import types
from youtubesearchpython import VideosSearch


def get_results_kb(results: VideosSearch) -> types.InlineKeyboardMarkup:
    """Returns a keyboard with the first 10 videos"""
    buttons = [[types.InlineKeyboardButton(text=f"{result.get('duration')} | {result.get('title')}", callback_data=f"https://www.youtube.com/watch?v={result.get('id')}")] for result in results.resultComponents]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_options_keyboard(url: str) -> types.InlineKeyboardMarkup:
    """Returns a keyboard with options what to do with the video"""
    buttons = [
        [types.InlineKeyboardButton(text="🎥 Скачать видео (Только shorts)", callback_data=f"videodl_{url}")],
        [types.InlineKeyboardButton(text="🎵 Скачать аудио", callback_data=f"audiodl_{url}")],
        [types.InlineKeyboardButton(text="🖼 Скачать превью", callback_data=f"thumbnaildl_{url}")],
        [types.InlineKeyboardButton(text="❌ Удалить это сообщение", callback_data="delete_message")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
