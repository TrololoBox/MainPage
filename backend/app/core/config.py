import os
from dataclasses import dataclass
from functools import lru_cache
from pydantic import validator


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    secret_key: str = os.getenv("SECRET_KEY", "change-me")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "14"))
    pdf_storage_root: str = os.getenv("PDF_STORAGE_ROOT", "archive")
    reminder_hours: int = int(os.getenv("REMINDER_HOURS", "24"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    service_name: str = os.getenv("SERVICE_NAME", "excursion-consent-api")
    otlp_endpoint: str = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "")
    enable_tracing: bool = os.getenv("ENABLE_TRACING", "true").lower() == "true"

    @validator("database_url")
    def validate_database_url(cls, value: str) -> str:  # noqa: N805
        if not value:
            raise ValueError("DATABASE_URL must not be empty")
        return value

    @validator("secret_key")
    def validate_secret_key(cls, value: str) -> str:  # noqa: N805
        if len(value) < 16:
            raise ValueError("SECRET_KEY must be at least 16 characters long")
        return value

    @validator("pdf_storage_root")
    def validate_pdf_storage_root(cls, value: str) -> str:  # noqa: N805
        if not value.strip():
            raise ValueError("PDF_STORAGE_ROOT must not be empty")
        return value

    @validator("access_token_expire_minutes", "reminder_hours")
    def validate_positive_int(cls, value: int, field):  # noqa: N805
        if value <= 0:
            raise ValueError(f"{field.name} must be greater than zero")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
