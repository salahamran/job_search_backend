"""Resume info and the attachments."""

from sqlalchemy import Column, String, Text, DateTime, Integer, JSON, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship
import datetime

class Resume(Base):
    """The raw data which was collected from users, files etc."""

    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # <-- ADD THIS
    telegram_id = Column(String, index=True)
    hh_resume_id = Column(String, nullable=True)   # id from hh.ru
    raw_json = Column(JSON)                        # raw HH response
    text = Column(Text, nullable=True)             # extracted plain text (optional)
    skills = Column(JSON, nullable=True)           # list
    languages = Column(JSON, nullable=True)
    education = Column(JSON, nullable=True)
    experience = Column(JSON, nullable=True)
    parsed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship('User', back_populates='resumes')
