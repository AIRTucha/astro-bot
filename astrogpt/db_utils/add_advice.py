from datetime import datetime
from sqlalchemy.orm import Session
from astrogpt.models.advice import Advice


def add_advice(session: Session, user_id: int, situation: str, advice: str):
    # Create a new advice instance
    new_advice = Advice(
        user_id=user_id, situation=situation, timestamp=datetime.now(), advice=advice
    )

    # Add the advice to the session and commit it
    session.add(new_advice)
    session.commit()
    return new_advice
