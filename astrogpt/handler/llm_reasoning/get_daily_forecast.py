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
from astrogpt.handler.llm_reasoning.action_result import ActionResult
from astrogpt.bot_utils.chat import Chat
from astrogpt.bot_utils.generate_daily_forecast import generate_daily_forecast
from astrogpt.db_utils.get_forecast_for_today import get_forecast_for_today

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


async def get_daily_forecast(
    session: Session, user: User, chat: Chat
) -> List[ActionResult]:

    forecast = get_forecast_for_today(session=session, user_id=user.id)
    if forecast is None:
        prediction = await generate_daily_forecast(user, chat)
        return [
            ActionResult(
                "Daily Forecast Generation",
                f"New daily forecast: {prediction}",
            )
        ]
    else:
        return [
            ActionResult(
                "Daily Forecast Generation",
                f"Daily forecast was already generated for today: {forecast} \n Give user with a very brief recap of todays forecast and tell that new one will be available tomorrow.",
            )
        ]
