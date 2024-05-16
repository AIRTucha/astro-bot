from src.bot_utils.chat import Chat

from src.logger.logger import logger
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


class ReplyChat(Chat):
    def __init__(self, update: Update):
        update._bot
        if (
            update.message is None
            or update.message.from_user is None
            or update.message.from_user.first_name is None
            or update.message.from_user.last_name is None
            or update.message.from_user.id is None
            or update.message.from_user.language_code is None
        ):
            logger.error("Update message is malformed %v", update.to_dict())
            raise ValueError("Update message is malformed")
        self.first_name = update.message.from_user.first_name
        self.last_name = update.message.from_user.last_name
        self.id = update.message.from_user.id
        self.language = update.message.from_user.language_code
        self.message = update.message

    def get_user_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_language_code(self) -> str:
        return self.language

    def get_user_id(self) -> int:
        return self.id

    async def send_text(self, text: str, *button_texts: str) -> None:
        if len(button_texts) == 0:
            await self.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        else:
            keyboard = [[KeyboardButton(text) for text in button_texts]]
            await self.message.reply_text(
                text,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=keyboard,
                    resize_keyboard=True,
                    one_time_keyboard=True,
                ),
            )

    def get_message_text(self) -> str:
        return self.message.text if self.message.text is not None else ""
