from src.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.bot_utils.chat import Chat


def get_user(session: Session, user_id: int) -> User | None:
    stm = select(User).where(User.id == user_id)
    return session.scalar(stm)


def get_user_from_chat(session: Session, chat: Chat) -> User | None:
    user_id = chat.get_user_id()
    stm = select(User).where(User.id == user_id)
    return session.scalar(stm)
