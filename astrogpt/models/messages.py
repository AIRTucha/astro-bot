from .base import Base

from sqlalchemy import Integer, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from astrogpt.models.user import User
from datetime import date


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    user = relationship("User", back_populates="messages")

    from_user = mapped_column(Boolean, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, message: {self.forecast_text}, user_id: {self.user_id}"
