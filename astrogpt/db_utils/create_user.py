from astrogpt.models.user import User
from sqlalchemy.orm import Session

from astrogpt.bot_utils.chat import Chat


def create_user(session: Session, chat: Chat):
    user_id = chat.get_user_id()
    user_name = chat.get_user_name()
    language_code = chat.get_language_code()
    user = User(
        id=user_id,
        name=user_name,
        language=language_code,
    )
    session.add(user)
    session.commit()
