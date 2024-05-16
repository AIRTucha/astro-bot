from telegram import ReplyKeyboardMarkup, KeyboardButton, Update

from src.llm.chains import prediction_chain
from src.models.user import User
from src.bot_utils.send_daily_forecast_subscribe_unsubsribe_message import (
    send_daily_forecast_subscribe_unsubscribe_message,
)
from src.bot_utils.language import get_language, get_subscribe
from src.db_utils.add_daily_forecast import add_daily_forecast
from src.models.engine import engine
from sqlalchemy.orm import Session
from src.db_utils.get_last_daily_forecasts import get_last_forecasts
from src.models.daily_forecast import DailyForecast
from typing import List

from src.bot_utils.chat import Chat

previous_forecasts_title = """"
Previous forecasts:


"""


def format_forecast(forecast: DailyForecast) -> str:
    date_format = "%m/%d/%Y"
    return f"{forecast.created_at.strftime(date_format)} {forecast.forecast_text}"


def format_last_forecasts(forecasts: List[DailyForecast]) -> str:
    if len(forecasts) == 0:
        return "It is the first forecast for the user."
    return previous_forecasts_title + "\n".join([format_forecast(f) for f in forecasts])


async def send_daily_forecast(user: User, chat: Chat) -> None:
    user_name = chat.get_user_name()
    user_language = get_language(chat)
    with Session(engine) as session:
        last_forecasts = get_last_forecasts(session, user.id, 3)

        prediction = prediction_chain.invoke(
            {
                "user_name": user_name,
                "birth_day": user.date_of_birth_text,
                "user_language": user_language,
                "previous_predictions": format_last_forecasts(last_forecasts),
            }
        )
        add_daily_forecast(session, user.id, prediction)

        await chat.send_text(prediction, get_subscribe(chat))
        await send_daily_forecast_subscribe_unsubscribe_message(user, chat)
