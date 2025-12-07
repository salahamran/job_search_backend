"""API routes for users."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.crud import user_crud

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user router."""
    return user_crud.create_user(db, user)


@router.get('/', response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    """Get all users."""
    return user_crud.get_all_users(db)


@router.get('/{user_id}', response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID."""
    return user_crud.get_user(db, user_id)


@router.put('/{user_id}', response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Update a user by ID."""
    return user_crud.update_user(db, user_id, user)


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID."""
    return user_crud.delete_user(db, user_id)

