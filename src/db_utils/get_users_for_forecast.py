from datetime import timedelta, date
from sqlalchemy.orm import Session
from typing import List

from src.models.user import User
from src.models.daily_forecast import DailyForecast


async def get_users_for_forecast(
    session: Session,
) -> List[User]:
    day_ago = date.today() - timedelta(days=1)
    recent_forecast_subquery = (
        session.query(DailyForecast)
        .filter(DailyForecast.created_at > day_ago)
        .distinct()
        .subquery()
    )
    return (
        session.query(User)
        .filter(User.daily_forecast == (True))
        .outerjoin(
            recent_forecast_subquery, User.id == recent_forecast_subquery.c.user_id
        )
        .filter(recent_forecast_subquery.c.user_id.is_(None))
        .limit(10)
        .all()
    )
