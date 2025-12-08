import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    secret_key: str = os.getenv("SECRET_KEY", "change-me")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "14"))
    pdf_storage_root: str = os.getenv("PDF_STORAGE_ROOT", "archive")
    reminder_hours: int = int(os.getenv("REMINDER_HOURS", "24"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
