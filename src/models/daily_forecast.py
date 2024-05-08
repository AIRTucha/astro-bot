from .base import Base

from sqlalchemy import Integer, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.user import User


class DailyForecast(Base):
    __tablename__ = "daily_forecasts"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    forecast_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[Date] = mapped_column(Date, nullable=False, index=True)

    user: Mapped[User] = relationship(
        Integer,
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    user = relationship("User", back_populates="daily_forecasts")

    def __repr__(self):
        return f"id: {self.id}, forecast_text: {self.forecast_text}, user_id: {self.user_id}"
