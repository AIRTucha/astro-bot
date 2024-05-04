from src.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from telegram import Update


def get_user(session: Session, user_id: int) -> User:
    stm = select(User).where(User.id == user_id)
    return session.scalar(stm)


def get_user_from_update(session: Session, update: Update) -> User:
    stm = select(User).where(User.id == update.message.from_user.id)
    return session.scalar(stm)
