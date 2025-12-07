"""Generic CRUD helper functions for all models."""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Type, TypeVar, List


ModelType = TypeVar('ModelType')


def create_from_schema(db: Session, model: Type[ModelType], schema):
    """
    Create a new object in the database from a Pydantic schema.

    Args:
        db (Session): Active SQLAlchemy session.
        model (Base): SQLAlchemy model class.
        schema (BaseModel): Pydantic schema with validated data.

    Returns:
        ModelType: The created database object.
    """
    obj = model(**schema.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_object_or_404(db: Session, model: Type[ModelType], object_id: int):
    """Retrieve a single object by its ID, or raise 404 if not found."""
    obj = db.query(model).filter(model.id == object_id).first()
    if not obj:
        raise HTTPException(
            status_code=404, detail=f'{model.__name__} not found')
    return obj


def get_all_objects(db: Session, model: Type[ModelType]) -> List[ModelType]:
    """Retrieve all objects for a given model."""
    return db.query(model).all()


def delete_objact(db: Session, model: Type[ModelType], object_id: int):
    """Delete an object by ID, raising 404 if not found."""
    obj = get_object_or_404(db, model, object_id)
    db.delete(obj)
    db.commit()
    return {"detail": f"{model.__name__} deleted succsessfully."}
