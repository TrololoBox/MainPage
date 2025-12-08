import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    secret_key: str = os.getenv("SECRET_KEY", "change-me")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    pdf_storage_root: str = os.getenv("PDF_STORAGE_ROOT", "archive")
    reminder_hours: int = int(os.getenv("REMINDER_HOURS", "24"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    service_name: str = os.getenv("SERVICE_NAME", "excursion-consent-api")
    otlp_endpoint: str = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "")
    enable_tracing: bool = os.getenv("ENABLE_TRACING", "true").lower() == "true"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
