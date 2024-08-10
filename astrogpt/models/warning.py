from .base import Base

from sqlalchemy import Integer, Text, DateTime, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

import enum


class WarningType(str, enum.Enum):
    hacking_attempt = "hacking_attempt"
    inappropriate_behavior = "inappropriate_behavior"
    repetitive_unrelated_input = "repetitive_unrelated_input"
    inappropriate_language = "inappropriate_language"
    output_manipulation = "output_manipulation"


class Warning(Base):
    __tablename__ = "warnings"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    warning: Mapped[WarningType] = mapped_column(Enum(WarningType), nullable=False)
    warning_explanation: Mapped[str] = mapped_column(Text, nullable=False)

    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )
    user = relationship("User", back_populates="warnings")

    def __repr__(self):
        return f"id: {self.id}, warning: {self.warning}, warning_explanation: {self.warning_explanation}, user_id: {self.user_id}"
