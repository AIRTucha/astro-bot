from sqlalchemy.orm import Session
from sqlalchemy import desc
from astrogpt.models.messages import Message
from datetime import datetime, timedelta


def get_messages(session: Session, user_id: int, count=5) -> list[Message]:
    since = datetime.now() - timedelta(minutes=20)
    return (
        session.query(Message)
        .filter(Message.user_id == user_id)
        .filter(Message.timestamp > since)
        .order_by(desc(Message.timestamp))
        .limit(count)
        .all()
    )
