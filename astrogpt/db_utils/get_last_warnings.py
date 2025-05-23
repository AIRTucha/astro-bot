from sqlalchemy.orm import Session
from sqlalchemy import desc
from astrogpt.models.warning import Warning
from datetime import datetime, timedelta


# Assuming `session` is an active SQLAlchemy session
def get_warnings(session: Session, user_id: int, limit: int = 10):
    three_hours = datetime.now() - timedelta(hours=3)
    return (
        session.query(Warning)
        .filter(Warning.user_id == user_id)
        .filter(Warning.timestamp > three_hours)
        .order_by(desc(Warning.timestamp))
        .limit(limit)
        .all()
    )
