from telegram import Update
from src.llm.chains import (
    daily_forecast_subscribe_inquiry_chain,
    daily_forecast_unsubscribe_inquiry_chain,
)
from src.bot_utils.language import get_language, get_subscribe, get_unsubscribe
from src.models.user import User
from src.bot_utils.chat import Chat


async def send_daily_forecast_subscribe_unsubscribe_message(user: User, chat: Chat):
    user_name = chat.get_user_name()
    user_language = get_language(chat)
    if user.daily_forecast:
        unsubscribe_message = daily_forecast_unsubscribe_inquiry_chain.invoke(
            {
                "user_name": user_name,
                "user_language": user_language,
            }
        )
        unsubscribe_button_text = get_unsubscribe(chat)
        await chat.send_text(
            unsubscribe_message,
            unsubscribe_button_text,
        )
    else:
        subscribe_message = daily_forecast_subscribe_inquiry_chain.invoke(
            {
                "user_name": user_name,
                "user_language": user_language,
            }
        )
        subscribe_button_text = get_subscribe(chat)
        await chat.send_text(
            subscribe_message,
            subscribe_button_text,
        )
