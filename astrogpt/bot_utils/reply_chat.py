from astrogpt.bot_utils.chat import Chat

from astrogpt.logger.logger import logger
from telegram import (
    Update,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    User,
)
from sqlalchemy.orm import Session
from astrogpt.db_utils.get_user import get_user


def format_name(user: User | None) -> str:
    user_name = ""

    if user is None:
        return "Unknown User"

    if user.first_name is not None:
        user_name += user.first_name

    if user.last_name is not None:
        user_name += f" {user.last_name}"

    if user_name == "":
        if user.username is not None:
            user_name = user.username
        else:
            user_name = "Unknown User"

    return user_name


class ReplyChat(Chat):
    def __init__(self, update: Update):
        if (
            update.message is None
            or update.message.from_user is None
            or update.message.from_user.id is None
            or update.message.from_user.language_code is None
        ):
            logger.error("Update message is malformed %v", update.to_dict())
            raise ValueError("Update message is malformed")

        self.user_name = format_name(update.message.from_user)
        self.id = update.message.from_user.id
        self.language = update.message.from_user.language_code
        self.message = update.message

    def refresh_state(self, session: Session) -> None:
        user = get_user(session, self.id)

        if not (user is None):
            self.user_name = user.name
            self.language = user.language if user.language is not None else "en"

    def get_user_name(self) -> str:
        return self.user_name

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

    async def set_typing_action(self) -> None:
        try:
            await self.message.reply_chat_action("typing")
        except Exception as e:
            logger.error("Error setting typing action %s", e)
            pass
