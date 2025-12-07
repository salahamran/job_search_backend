from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from app.core.database import Base
import datetime


class HHToken(Base):
    """Saveing the generated token from hhru."""

    __tablename__ = 'hh_tokens'
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, index=True)
    access_token = Column(String)
    refresh_token = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    scope = Column(String, nullable=True)
    raw = Column(JSON)
    created_at = Column(DateTime, default=datetime.timezone.utc)
