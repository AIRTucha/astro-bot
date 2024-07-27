from sqlalchemy.orm import Session
from sqlalchemy import desc
from astrogpt.models.messages import Message


# Assuming `session` is an active SQLAlchemy session
def get_messages(session: Session, user_id: int, limit: int = 10):
    return (
        session.query(Message)
        .filter(Message.user_id == user_id)
        .order_by(desc(Message.created_at))
        .limit(limit)
        .all()
    )
