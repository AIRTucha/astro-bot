from astrogpt.llm.chains import prediction_chain
from astrogpt.models.user import User
from astrogpt.bot_utils.language import get_language
from astrogpt.db_utils.add_daily_forecast import add_daily_forecast
from astrogpt.models.engine import engine
from sqlalchemy.orm import Session
from astrogpt.db_utils.get_last_daily_forecasts import get_last_forecasts
from astrogpt.models.daily_forecast import DailyForecast
from astrogpt.logger.logger import logger
from typing import List

from astrogpt.bot_utils.chat import Chat

previous_forecasts_title = """"
Previous forecasts:


"""


def format_forecast(forecast: DailyForecast) -> str:
    date_format = "%m/%d/%Y"
    return f"{forecast.timestamp .strftime(date_format)} {forecast.forecast_text}"


def format_last_forecasts(forecasts: List[DailyForecast]) -> str:
    if len(forecasts) == 0:
        return "It is the first forecast for the user."
    return previous_forecasts_title + "\n".join([format_forecast(f) for f in forecasts])


def replace_none_with_missing(text: str | None) -> str:
    return text if text is not None else "MISSING"


async def generate_daily_forecast(user: User, chat: Chat) -> None:
    user_name = chat.get_user_name()
    user_language = get_language(chat)
    with Session(engine) as session:
        last_forecasts = get_last_forecasts(session, user.id, 3)
        prediction = prediction_chain.invoke(
            {
                "user_name": user_name,
                "user_birthday": replace_none_with_missing(user.date_of_birth_text),
                "user_language": user_language,
                "previous_predictions": format_last_forecasts(last_forecasts),
            }
        )
        logger.info("User %s forecast received", user.id)
        add_daily_forecast(session, user.id, prediction)
        return prediction
