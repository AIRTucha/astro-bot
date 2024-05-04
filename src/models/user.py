from .base import Base

from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    date_of_birth_text: Mapped[str] = mapped_column(String(60))

    daily_forecast: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, date_of_birth: {self.dateOfBirth}, language: {self.language}"
