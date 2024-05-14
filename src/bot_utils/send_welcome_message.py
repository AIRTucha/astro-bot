from telegram import ReplyKeyboardRemove, KeyboardButton, Update
from src.llm.chains import welcome_chain, welcome_again_chain

from src.models.user import User
from src.bot_utils.send_daily_forecast_subscribe_unsubsribe_message import (
    send_daily_forecast_subscribe_unsubscribe_message,
)
from src.bot_utils.language import get_language

from src.bot_utils.chat import Chat


async def send_welcome_message(chat: Chat):
    user_name = chat.get_user_name()
    user_language = get_language(chat)
    await chat.send_text(
        welcome_chain.invoke(
            {
                "user_name": user_name,
                "user_language": user_language,
            }
        ),
    )


async def send_welcome_again_message(user: User, chat: Chat):
    user_name = chat.get_user_name()
    user_language = get_language(chat)
    welcome_message = welcome_again_chain.invoke(
        {
            "user_name": user_name,
            "user_language": user_language,
        }
    )
    await chat.send_text(
        welcome_message,
    )
    await send_daily_forecast_subscribe_unsubscribe_message(user, chat)
