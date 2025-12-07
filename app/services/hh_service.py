import httpx
from app.models import Resume
from datetime import datetime


async def get_hh_resumes(acces_token: str):
    """Collect the uers resume from hhru in json."""
    headers = {'Authorization': f'Bearer {acces_token}'}

    async with httpx.AsyncClient() as client:
        resp = await client.get('https://api.hh.ru/resumes/mine', headers=headers)

    if resp.status_code != 200:
        return None

    return resp.json()
