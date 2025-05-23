from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from typing import List

from astrogpt.models.user import User
from astrogpt.models.daily_forecast import DailyForecast


async def get_users_for_forecast(
    session: Session,
) -> List[User]:
    day_ago = datetime.now() - timedelta(days=1)
    recent_forecast_subquery = (
        session.query(DailyForecast)
        .filter(DailyForecast.timestamp > day_ago)
        .distinct()
        .subquery()
    )
    return (
        session.query(User)
        .filter(User.daily_forecast == (True))
        .filter(User.date_of_birth_text != None)
        .outerjoin(
            recent_forecast_subquery, User.id == recent_forecast_subquery.c.user_id
        )
        .filter(recent_forecast_subquery.c.user_id.is_(None))
        .limit(10)
        .all()
    )
