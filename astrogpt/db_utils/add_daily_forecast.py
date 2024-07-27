from datetime import datetime
from sqlalchemy.orm import Session
from astrogpt.models.daily_forecast import DailyForecast
from astrogpt.db_utils.add_message import add_message


def add_daily_forecast(session: Session, user_id: int, forecast_text: str):
    add_message(
        session=session, user_id=user_id, message=forecast_text, from_user=False
    )
    # Create a new DailyForecast instance
    new_forecast = DailyForecast(
        user_id=user_id, forecast_text=forecast_text, created_at=datetime.now()
    )

    # Add the new forecast to the session and commit it
    session.add(new_forecast)
    session.commit()
    return new_forecast
