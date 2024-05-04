from telegram import ReplyKeyboardRemove, KeyboardButton, Update
from src.llm.chains import welcome_chain, welcome_again_chain

from src.models.user import User
from src.bot_utils.send_daily_forecast_subscribe_unsubsribe_message import (
    send_daily_forecast_subscribe_unsubscribe_message,
)
from src.bot_utils.update_get_user_data import get_user_first_name
from src.bot_utils.language import get_language
from src.bot_utils.send_text import send_text


async def send_welcome_message(update: Update):
    user_name = get_user_first_name(update)
    user_language = get_language(update)
    await send_text(
        update,
        welcome_chain.invoke(
            {
                "user_name": user_name,
                "user_language": user_language,
            }
        ),
    )


async def send_welcome_again_message(user: User, update: Update):
    user_name = get_user_first_name(update)
    user_language = get_language(update)
    welcome_message = welcome_again_chain.invoke(
        {
            "user_name": user_name,
            "user_language": user_language,
        }
    )
    await send_text(
        update,
        welcome_message,
    )
    await send_daily_forecast_subscribe_unsubscribe_message(user, update)
