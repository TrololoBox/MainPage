import os
from dataclasses import dataclass
from functools import lru_cache
import json
from typing import Dict
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
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "60"))
    feature_flags: Dict[str, bool] = None
    environment: str = os.getenv("ENVIRONMENT", "dev")

    def __post_init__(self):
        self.feature_flags = self._parse_feature_flags(os.getenv("FEATURE_FLAGS"))

    @staticmethod
    def _parse_feature_flags(raw_flags: str | None) -> Dict[str, bool]:
        defaults = {
            "newsletter_form": True,
            "feedback_form": True,
            "beta_tools_banner": False,
        }

        if not raw_flags:
            return defaults

        try:
            parsed = json.loads(raw_flags)
        except json.JSONDecodeError as exc:
            raise ValueError("FEATURE_FLAGS must be valid JSON") from exc

        if not isinstance(parsed, dict):
            raise ValueError("FEATURE_FLAGS must be a JSON object with boolean values")

        cleaned: Dict[str, bool] = {}
        for key, value in parsed.items():
            if not isinstance(value, bool):
                raise ValueError("All FEATURE_FLAGS values must be boolean")
            cleaned[key] = value

        return {**defaults, **cleaned}

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

    @validator("environment")
    def validate_environment(cls, value: str) -> str:  # noqa: N805
        allowed = {"dev", "stage", "prod"}
        if value not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {', '.join(sorted(allowed))}")
        return value

    @validator("access_token_expire_minutes", "reminder_hours", "cache_ttl_seconds")
    def validate_positive_int(cls, value: int, field):  # noqa: N805
        if value <= 0:
            raise ValueError(f"{field.name} must be greater than zero")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
