from fastapi import APIRouter, HTTPException, Depends
from urllib.parse import urlencode
from app.core.confing import settings
import httpx
from fastapi import Depends
from app.core.database import get_db
from app.models import User

from app.crud.user_crud import get_user_by_telegram
from app.crud.resume_crud import save_resume
from app.services.hh_service import get_hh_resumes


login_router = APIRouter(prefix='/auth/hh')


@login_router.get("/login")
def hh_login(telegram_id: str, db=Depends(get_db)):
    # 1. Check if user exists
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    # 2. Create HH auth URL
    params = {
        "response_type": "code",
        "client_id": settings.HH_CLIENT_ID,
        "redirect_uri": settings.HH_REDIRECT_URI,
        "state": telegram_id,
    }
    url = f"{settings.HH_AUTH_URL}?{urlencode(params)}"
    return {"auth_url": url}



@login_router.get("/callback")
async def hh_callback(code: str, state: str, db=Depends(get_db)):
    telegram_id = state   # The telegram user ID we passed in ?state=

    # === 1. Exchange Auth Code for Token ===
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": settings.HH_CLIENT_ID,
        "client_secret": settings.HH_CLIENT_SECRET,
        "redirect_uri": settings.HH_REDIRECT_URI,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(settings.HH_TOKEN_URL, data=data)
        token_data = resp.json()

    if "access_token" not in token_data:
        raise HTTPException(400, "Cannot exchange code")

    # === 2. Save tokens to user ===
    user = get_user_by_telegram(db, telegram_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.hh_access_token = token_data["access_token"]
    user.hh_refresh_token = token_data.get("refresh_token")
    db.commit()

    # === 3. Fetch resume immediately ===
    hh_resumes = await get_hh_resumes(user.hh_access_token)

    if not hh_resumes:
        message_text = (
            "✅ Authorization complete, but I couldn't find any resumes "
            "attached to your HH.ru account."
        )
    else:
        # If HH returns multiple resumes, take the first one
        items = hh_resumes.get("items", [])
        if not items:
            raise HTTPException(400, "User has no resumes in HH.ru")

        resume_json = items[0]   # first resume

        save_resume(db, telegram_id, resume_json)

        # Person's name from resume
        name = resume_json.get("first_name") or user.first_name or "friend"

        message_text = (
            f"✅ {name}, your HH.ru authorization is complete!\n"
            f"📄 I have successfully collected your resume."
        )

    # === 4. Notify Telegram ===
    telegram_api_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": telegram_id,
        "text": message_text
    }

    async with httpx.AsyncClient() as client:
        await client.post(telegram_api_url, data=payload)

    return {"success": True, "message": "HH authorization & resume collected"}
