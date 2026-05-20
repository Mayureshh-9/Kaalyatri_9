import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "kaalyatri-time-travel-secret-2026")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/kaalyatri",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    OWNER_EMAIL = os.environ.get("OWNER_EMAIL", "abc@gmail.com")
    FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:4200")

    COMPANY_NAME = "KaalYatri"
    COMPANY_TAGLINE = "The Time Travellers"
