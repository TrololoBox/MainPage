from functools import lru_cache

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    database_url: str = Field("sqlite:///./data.db", env="DATABASE_URL")
    secret_key: str = Field("change-me", env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(120, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    pdf_storage_root: str = Field("archive", env="PDF_STORAGE_ROOT")
    reminder_hours: int = Field(24, env="REMINDER_HOURS")

    class Config:
        env_file = ".env"

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
