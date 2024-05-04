from .base import Base

from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy import Integer


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    date_of_birth_text = Column(String(60))

    daily_forecast = Column(Boolean, default=False)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, date_of_birth: {self.dateOfBirth}, language: {self.language}"
