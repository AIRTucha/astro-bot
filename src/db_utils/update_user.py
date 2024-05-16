from sqlalchemy import update
from src.models.user import User
from sqlalchemy.orm import Session


def update_user_birthday(session: Session, user: User, birthday: str):
    stmt = update(User).where(User.id == user.id).values(date_of_birth_text=birthday)
    session.execute(stmt)
    session.commit()
    user.date_of_birth_text = birthday
    return


def update_user_daily_forecast_subscription(
    session: Session, user_id: int, is_subscribed: bool
):
    stmt = update(User).where(User.id == user_id).values(daily_forecast=is_subscribed)
    session.execute(stmt)
    session.commit()
    return
