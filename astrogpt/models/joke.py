from .base import Base

from sqlalchemy import Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Joke(Base):
    __tablename__ = "jokes"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    astrologic_joke = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    def __repr__(self):
        return f"id: {self.id}, astrologic_joke: {self.astrologic_joke}"
