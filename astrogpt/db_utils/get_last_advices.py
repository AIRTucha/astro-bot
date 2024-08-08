from sqlalchemy.orm import Session
from sqlalchemy import desc
from astrogpt.models.advice import Advice


# Assuming `session` is an active SQLAlchemy session
def get_last_advices(session: Session, user_id: int, limit: int = 3):
    return (
        session.query(Advice)
        .filter(Advice.user_id == user_id)
        .order_by(desc(Advice.timestamp))
        .limit(limit)
        .all()
    )
