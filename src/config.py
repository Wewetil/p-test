import os
from dotenv import load_dotenv
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Здесь весь конфиг. Часть берется с виртуального окружения. """

    APP_TITLE: str = 'Async service'  # название проекта
    APP_DESCRIPTION: str = 'Homework Positive Technologies'  # описание проекта
    APP_VERSION: str = '0.0.1'  # версия проекта
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")

    class Config:
        env_file = '.env'


settings = Settings()
