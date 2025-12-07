from app.models import Resume
from sqlalchemy.orm import Session
import datetime


def save_resume(db: Session, telegram_id: str, resume_json: dict):
    """Save the resume in json form."""
    resume = Resume(
        telegram_id=telegram_id,
        hh_resume_id=resume_json.get('id'),
        raw_json=resume_json,
        parsed_at=datetime.datetime.utcnow()
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume
