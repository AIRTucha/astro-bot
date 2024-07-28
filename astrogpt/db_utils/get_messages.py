from sqlalchemy.orm import Session
from sqlalchemy import desc
from astrogpt.models.messages import Message


def get_messages(session: Session, user_id: int, count=5) -> list[Message]:
    return (
        session.query(Message)
        .filter(Message.user_id == user_id)
        .order_by(desc(Message.id))
        .limit(count)
        .all()
    )
