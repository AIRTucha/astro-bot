from .base import Base

from sqlalchemy import Integer, Text, DateTime, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )
    user = relationship("User", back_populates="messages")

    from_user = mapped_column(Boolean, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, message: {self.text}, user_id: {self.user_id}"
    
    def __str__(self):
        return f'{self.timestamp} {'User' if self.from_user else 'Bot'}: {self.text}'
