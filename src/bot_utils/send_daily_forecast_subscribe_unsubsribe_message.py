from telegram import Update
from src.llm.chains import (
    daily_forecast_subscribe_inquiry_chain,
    daily_forecast_unsubscribe_inquiry_chain,
)
from src.bot_utils.language import get_language, get_subscribe, get_unsubscribe
from src.models.user import User
from src.bot_utils.send_text import send_text
from src.bot_utils.update_get_user_data import get_user_first_name


async def send_daily_forecast_subscribe_unsubscribe_message(user: User, update: Update):
    user_name = get_user_first_name(update)
    user_language = get_language(update)
    if user.daily_forecast:
        unsubscribe_message = daily_forecast_unsubscribe_inquiry_chain.invoke(
            {
                "user_name": user_name,
                "user_language": user_language,
            }
        )
        unsubscribe_button_text = get_unsubscribe(update)
        await send_text(
            update,
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
        subscribe_button_text = get_subscribe(update)
        await send_text(
            update,
            subscribe_message,
            subscribe_button_text,
        )
