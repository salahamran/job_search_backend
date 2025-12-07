"""Reusable pydantic schems for models."""
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """The base models for User model."""

    first_name: str
    last_name: str
    age: int
    city: str
    email: EmailStr
    phone: str
    telegram_id: str
    hh_profile_url: str


class UserCreate(UserBase):
    """Used for creating a new user."""


class UserUpdate(UserBase):
    """Used for updating user info."""

    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    city: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    telegram_id: str | None = None
    hh_profile_url: str | None = None


class UserRead(UserBase):
    """Used for reading user data from DB."""

    id: int

    class Config:
        from_attributes = True
