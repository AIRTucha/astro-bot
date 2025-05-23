from sqlalchemy.orm import Session
from sqlalchemy import desc
from astrogpt.models.daily_forecast import DailyForecast


# Assuming `session` is an active SQLAlchemy session
def get_last_forecasts(session: Session, user_id: int, limit: int = 3):
    return (
        session.query(DailyForecast)
        .filter(DailyForecast.user_id == user_id)
        .order_by(desc(DailyForecast.id))
        .limit(limit)
        .all()
    )
