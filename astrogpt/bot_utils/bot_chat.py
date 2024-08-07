from astrogpt.bot_utils.chat import Chat

from astrogpt.models.user import User
from telegram import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    Bot,
)
from astrogpt.db_utils.update_user import update_user_daily_forecast_subscription
from astrogpt.models.engine import engine
from sqlalchemy.orm import Session


class BotChat(Chat):
    def __init__(self, bot: Bot, user: User):
        self.bot = bot
        self.user = user

    def get_user_name(self) -> str:
        return self.user.name

    def get_language_code(self) -> str:
        return self.user.language if self.user.language is not None else "en"

    def get_user_id(self) -> int:
        return self.user.id

    async def send_text(self, text: str, *button_texts: str) -> None:
        try:
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
        except Exception as e:
            err_str = str(e).lower()
            if "bot was blocked by the user" in err_str:
                with Session(engine) as session:
                    update_user_daily_forecast_subscription(
                        session, self.user.id, is_subscribed=False
                    )

    def get_message_text(self) -> str:
        return ""
