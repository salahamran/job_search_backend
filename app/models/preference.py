"""Matching Preferences."""

from sqlalchemy import Column, String, DateTime, Boolean, ARRAY, Integer, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship


class Preference(Base):
    """The data whcih matched with what user provides."""

    __tablename__ = 'preferences'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    job_sources = Column(ARRAY(String))
    notify_via_telegram = Column(Boolean)
    auto_apply = Column(Boolean)
    created_at = Column(DateTime)

    user = relationship('User', back_populates='preference')
