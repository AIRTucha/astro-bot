from src.bot_utils.chat import Chat

from src.models.user import User
from telegram import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    Bot,
)


class BotChat(Chat):
    def __init__(self, bot: Bot, user: User):
        self.bot = bot
        self.user = user

    def get_user_name(self) -> str:
        return self.user.name

    def get_language_code(self) -> str:
        return self.user.language

    def get_user_id(self) -> int:
        return self.user.id

    async def send_text(self, text: str, *button_texts: str) -> None:
        if len(button_texts) == 0:
            await self.bot.send_message(
                chat_id=self.user.id, text=text, reply_markup=ReplyKeyboardRemove()
            )
        else:
            keyboard = [[KeyboardButton(text) for text in button_texts]]
            await self.bot.send_message(
                chat_id=self.user.id,
                text=text,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=keyboard,
                    resize_keyboard=True,
                    one_time_keyboard=True,
                ),
            )

    def get_message_text(self) -> str:
        return ""
