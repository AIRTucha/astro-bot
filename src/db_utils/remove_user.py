from src.models.user import User
from sqlalchemy import delete


def remove_user(session, user_id):
    stm = delete(User).where(User.id == user_id)
    session.execute(stm)
    session.commit()
