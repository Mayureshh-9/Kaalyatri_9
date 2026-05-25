from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:12345@localhost:5432/KaalYatri"
    
    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Company
    COMPANY_NAME: str = "KaalYatri"
    COMPANY_TAGLINE: str = "The Time Travellers"
    OWNER_EMAIL: str = "abc@gmail.com"
    FRONTEND_ORIGIN: str = "http://localhost:4200"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()