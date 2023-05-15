import os
from typing import List
import json

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # Database connection
    HOST: str = os.getenv('HOST')
    PORT: int = os.getenv('PORT')
    USERNAME: str = os.getenv('USERNAME')
    PASSWORD: str = os.getenv('PASSWORD')
    DATABASE: str = os.getenv('DATABASE')
    FIRST_SUPERUSER_EMAIL: str = os.getenv('FIRST_SUPERUSER_EMAIL')
    FIRST_SUPERUSER_PASSWORD: str = os.getenv('FIRST_SUPERUSER_PASSWORD')
    SMS_SID: str = os.getenv('SMS_SID')
    SMS_AUTH_TOKEN: str = os.getenv('SMS_AUTH_TOKEN')
    
    PHONE: List[str] = json.loads(os.getenv('PHONE'))
    SQLALCHEMY_DATABASE_URL = f'mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

    class Config:
        case_sensitive = True


settings = Settings()
