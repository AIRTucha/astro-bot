from sqlalchemy.orm import Session
from sqlalchemy import desc
from astrogpt.models.daily_forecast import DailyForecast
from datetime import datetime, timedelta


def get_forecast_for_today(session: Session, user_id: int):
    try:
        today = datetime.now() - timedelta(days=1)
        return (
            session.query(DailyForecast)
            .filter(DailyForecast.user_id == user_id)
            .filter(DailyForecast.timestamp > today)
            .one()
        )
    except:
        return None
