from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.crud.base import (
    create_from_schema,
    get_object_or_404, get_all_objects)


def create_user(db: Session, user_data: UserCreate):
    """Create a new user."""
    return create_from_schema(db, User, user_data)


def get_user(db: Session, user_id: int):
    """Get a user by ID or raise 404."""
    return get_object_or_404(db, User, user_id)


def get_all_users(db: Session):
    """Return a list of all users."""
    return get_all_objects(db, User)


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """Update an existing user."""
    user = get_object_or_404(db, User, user_id)

    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    """Delete a user by ID."""
    user = get_object_or_404(db, User, user_id)
    db.delete(user)
    db.commit()
    return {'detail': 'User deleted successfully'}


def get_user_by_telegram(db: Session, telegram_id: str):
    """Return the user with given telegram_id."""
    return db.query(User).filter(User.telegram_id == telegram_id).first()
