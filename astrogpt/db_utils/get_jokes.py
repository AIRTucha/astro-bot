from sqlalchemy.orm import Session
from sqlalchemy import desc
from astrogpt.models.messages import Message
from astrogpt.models.joke import Joke


joke_example = [
    """
Why did the Aries cross the road?
To prove they could do it faster and better than anyone else!
""",
    """
Why do Leos love Instagram?
Because they get to share their greatness with the world, one post at a time.
""",
    """
How do you spot a Sagittarius at the airport?
They’re the ones with the biggest smile and the smallest luggage.
""",
]


def get_jokes(session: Session, count=3) -> list[str]:
    jokes = session.query(Joke).order_by(desc(Joke.timestamp)).limit(count).all()
    joke_strings = [joke.astrologic_joke for joke in jokes]
    return (joke_example + joke_strings)[-count:]
