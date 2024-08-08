from sqlalchemy.orm import Session
from sqlalchemy import desc
from astrogpt.models.messages import Message
from astrogpt.models.joke import Joke

joke_example = [
    """
First date
Her: So what do you do?
Him: I'm currently trying to eliminate all cancers
Her: Wow, impressive
Him: Then I'Il move on to Virgos
""",
    """
What sign are you most compatible
with?

The dollar sign.
""",
    """
man I swear it only takes 1 mercury retrograde for someone to start
believing in astrology Imao
""",
]


def get_jokes(session: Session, count=3) -> list[str]:
    jokes = session.query(Joke).order_by(desc(Joke.timestamp)).limit(count).all()
    joke_strings = [joke.astrologic_joke for joke in jokes]
    return (joke_example + joke_strings)[-count:]
