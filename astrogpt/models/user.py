from .base import Base
from typing import Optional

from sqlalchemy import String, BigInteger, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    date_of_birth_text: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)

    language: Mapped[Optional[str]] = mapped_column(String(2), default="en")

    daily_forecast: Mapped[bool] = mapped_column(Boolean, default=True)

    daily_forecasts = relationship(
        "DailyForecast", back_populates="user", cascade="all, delete-orphan"
    )

    messages = relationship(
        "Message", back_populates="user", cascade="all, delete-orphan"
    )

    advices = relationship(
        "Advice", back_populates="user", cascade="all, delete-orphan"
    )

    warnings = relationship(
        "Warning", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, date_of_birth_text: {self.date_of_birth_text}, language: {self.language}"

    def isRegistered(self):
        return (
            self.date_of_birth_text is not None
            and self.language is not None
            and self.target_topics is not None
            and self.hobbies is not None
            and self.self_description is not None
        )
