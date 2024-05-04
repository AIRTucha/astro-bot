from src.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from telegram import Update
from src.bot_utils.update_get_user_data import get_user_id


def get_user(session: Session, user_id: int) -> User | None:
    stm = select(User).where(User.id == user_id)
    return session.scalar(stm)


def get_user_from_update(session: Session, update: Update) -> User | None:
    user_id = get_user_id(update)
    stm = select(User).where(User.id == user_id)
    return session.scalar(stm)
