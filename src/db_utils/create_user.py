from src.models.user import User
from sqlalchemy.orm import Session
from telegram import Update
from src.bot_utils.update_get_user_data import (
    get_user_id,
    get_user_first_name,
    get_user_last_name,
)


def create_user(session: Session, update: Update):
    user_id = get_user_id(update)
    user_first_name = get_user_first_name(update)
    user_last_name = get_user_last_name(update)
    user = User(
        id=user_id,
        name=f"{user_first_name} {user_last_name}",
    )
    session.add(user)
    session.commit()
