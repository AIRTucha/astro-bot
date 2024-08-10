from .base import Base

from sqlalchemy import Integer, Text, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Advice(Base):
    __tablename__ = "advices"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    situation = mapped_column(Text, nullable=False)
    advice: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )
    user = relationship("User", back_populates="advices")

    def __repr__(self):
        return f"id: {self.id}, situation: {self.situation}, advice: {self.advice}, user_id: {self.user_id}"
