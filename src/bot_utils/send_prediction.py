from telegram import ReplyKeyboardMarkup, KeyboardButton, Update

from src.llm.chains import prediction_chain
from src.models.user import User
from src.bot_utils.send_daily_forecast_subscribe_unsubsribe_message import (
    send_daily_forecast_subscribe_unsubscribe_message,
)
from src.bot_utils.send_text import send_text
from src.bot_utils.update_get_user_data import get_user_first_name
from src.bot_utils.language import get_language, get_subscribe


async def send_prediction(user: User, update: Update, birthday_text: str) -> None:
    user_name = get_user_first_name(update)
    user_language = get_language(update)
    prediction = prediction_chain.invoke(
        {
            "user_name": user_name,
            "birth_day": birthday_text,
            "user_language": user_language,
        }
    )
    await send_text(update, prediction, get_subscribe(update))
    await send_daily_forecast_subscribe_unsubscribe_message(user, update)
