from datetime import datetime
from sqlalchemy.orm import Session
from src.models.daily_forecast import DailyForecast


def add_daily_forecast(session: Session, user_id: int, forecast_text: str):
    # Create a new DailyForecast instance
    new_forecast = DailyForecast(
        user_id=user_id, forecast_text=forecast_text, created_at=datetime.now()
    )

    # Add the new forecast to the session and commit it
    session.add(new_forecast)
    session.commit()
    return new_forecast
