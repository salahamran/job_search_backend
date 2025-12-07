"""User models for the API, must be before starting the service."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    """
    The information which must be collected from.

    user to start the job search.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, default="")   # empty string
    last_name = Column(String, default="")
    age = Column(Integer, default=0)          # integer default
    city = Column(String, default="")
    email = Column(String, default="")
    phone = Column(String, default="")
    telegram_id = Column(String, default="")
    hh_profile_url = Column(String, default="")
    hh_access_token = Column(String, nullable=True)
    hh_refresh_token = Column(String, nullable=True)


    profile = relationship(
        'Profile', back_populates='user', uselist=False)
    preference = relationship(
        'Preference', back_populates='user', uselist=False)
    resumes = relationship(
        'Resume', back_populates='user')
