import sqlite3
from typing import Literal


class UsersDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.curr = self.conn.cursor()

        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS users(
            user_id INT,
            lang CHAR(2)
        )"""
        )

    def create_user(self, user_id: int, lang: Literal["ru", "en"]) -> None:
        if not self.get_lang(user_id):
            self.curr.execute("INSERT INTO users VALUES (?, ?)", (user_id, lang))
            self.conn.commit()

    def get_lang(self, user_id: int) -> str | None:
        self.curr.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
        row = self.curr.fetchone()
        return row[0] if row is not None else None

    def update_user(self, user_id: int, lang: Literal["ru", "en"]) -> None:
        if self.get_lang(user_id):
            self.curr.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
            self.conn.commit()
        else:
            self.create_user(user_id, lang)
