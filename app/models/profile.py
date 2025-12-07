"""Professional info of the user to be used in finding the job."""

from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship


class Profile(Base):
    """The professional data whcih is used to find the proper vacancy."""

    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    current_position = Column(String, default=False)
    desired_position = Column(String)
    years_of_experience = Column(Integer)
    skills = Column(ARRAY(String))
    preferred_salary = Column(Integer)
    preferred_region = Column(String)
    languages = Column(ARRAY(String))
    education_level = Column(String)

    user = relationship('User', back_populates='profile')
