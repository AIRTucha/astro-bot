from .base import Base

from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    date_of_birth_text: Mapped[str] = mapped_column(String(60), nullable=True)

    language: Mapped[str] = mapped_column(String(2), default="en")

    daily_forecast: Mapped[bool] = mapped_column(Boolean, default=True)

    daily_forecasts = relationship(
        "DailyForecast", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, date_of_birth: {self.dateOfBirth}, language: {self.language}"
