# environment variables (Settings)

import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    HH_CLIENT_ID: str = os.getenv('HH_CLIENT_ID')
    HH_CLIENT_SECRET: str = os.getenv('HH_CLIENT_SECRET')
    HH_REDIRECT_URI: str = "https://inga-unoral-craig.ngrok-free.dev/auth/hh/callback"
    HH_AUTH_URL: str = "https://hh.ru/oauth/authorize"
    HH_TOKEN_URL: str = "https://hh.ru/oauth/token"
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    URL_DATABASE: str = os.getenv('URL_DATABASE')


    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../../.env")
        env_file_encoding = "utf-8"


settings = Settings()
