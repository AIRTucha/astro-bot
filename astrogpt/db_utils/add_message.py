from datetime import datetime
from sqlalchemy.orm import Session
from astrogpt.models.messages import Message


def add_message(session: Session, user_id: int, message: str, from_user: bool):
    # Create a new message instance
    new_message = Message(
        user_id=user_id, text=message, timestamp=datetime.now(), from_user=from_user
    )

    # Add the message to the session and commit it
    session.add(new_message)
    session.commit()
    return new_message
