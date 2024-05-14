from src.models.user import User
from sqlalchemy.orm import Session

from src.bot_utils.chat import Chat


def create_user(session: Session, chat: Chat):
    user_id = chat.get_user_id()
    user_name = chat.get_user_name()
    user = User(
        id=user_id,
        name=user_name,
    )
    session.add(user)
    session.commit()
