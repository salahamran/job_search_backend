from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.crud.user_crud import get_user_by_telegram
from app.crud.resume_crud import save_resume
from app.services.hh_service import get_hh_resumes

router = APIRouter(prefix='/resume')


@router.get('/fetch')
async def fetch_resume(telegram_id: str, db=Depends(get_db)):
    user = get_user_by_telegram(db, telegram_id)
    if not user or not user.hh_access_token:
        return {'error': 'User not authorized with HH'}

    hh_data = await get_hh_resumes(user.hh_access_token)
    if not hh_data:
        return {'error': 'Cannot fetch resume'}

    resume = save_resume(db, telegram_id, hh_data)
    return {'succes': True, 'resume_id': resume.id}
