from sqlalchemy import update
from astrogpt.models.user import User
from sqlalchemy.orm import Session


def update_user_birthday(session: Session, user: User, birthday: str):
    stmt = update(User).where(User.id == user.id).values(date_of_birth_text=birthday)
    session.execute(stmt)
    session.commit()
    user.date_of_birth_text = birthday
    return


def update_user_language(session: Session, user: User, language: str):
    stmt = update(User).where(User.id == user.id).values(language=language)
    session.execute(stmt)
    session.commit()
    user.language = language
    return


def update_user_target_topics(session: Session, user: User, target_topics: str):
    stmt = update(User).where(User.id == user.id).values(target_topics=target_topics)
    session.execute(stmt)
    session.commit()
    user.target_topics = target_topics
    return


def update_user_hobbies(session: Session, user: User, hobbies: str):
    stmt = update(User).where(User.id == user.id).values(hobbies=hobbies)
    session.execute(stmt)
    session.commit()
    user.hobbies = hobbies
    return


def update_user_self_description(session: Session, user: User, self_description: str):
    stmt = (
        update(User).where(User.id == user.id).values(self_description=self_description)
    )
    session.execute(stmt)
    session.commit()
    user.self_description = self_description
    return


def update_user_daily_forecast_subscription(
    session: Session, user_id: int, is_subscribed: bool
):
    stmt = update(User).where(User.id == user_id).values(daily_forecast=is_subscribed)
    session.execute(stmt)
    session.commit()
    return
