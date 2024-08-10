from datetime import datetime
from sqlalchemy.orm import Session
from astrogpt.models.joke import Joke


def add_joke(session: Session, joke: str) -> Joke:
    # Create a new message instance
    new_message = Joke(astrologic_joke=joke, timestamp=datetime.now())

    # Add the message to the session and commit it
    session.add(new_message)
    session.commit()
    return new_message
