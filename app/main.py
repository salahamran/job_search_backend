from fastapi import FastAPI
from app.routers import user_router, login_router, resume_router
from app.core.database import engine, Base


app = FastAPI(title='job search API')
Base.metadata.create_all(bind=engine)
app.include_router(user_router.router)
app.include_router(login_router.login_router)
app.include_router(resume_router.router)
