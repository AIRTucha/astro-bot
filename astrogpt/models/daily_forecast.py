from .base import Base

from sqlalchemy import Integer, Text, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class DailyForecast(Base):
    __tablename__ = "daily_forecasts"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    forecast_text: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )
    user = relationship("User", back_populates="daily_forecasts")

    def __repr__(self):
        return f"id: {self.id}, forecast_text: {self.forecast_text}, user_id: {self.user_id}"
