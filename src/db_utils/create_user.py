from src.models.user import User
from sqlalchemy.orm import Session
from telegram import Update


def create_user(session: Session, update: Update):
    user = User(
        id=update.message.from_user.id,
        name=f"{update.message.from_user.first_name} {update.message.from_user.last_name}",
    )
    session.add(user)
    session.commit()
