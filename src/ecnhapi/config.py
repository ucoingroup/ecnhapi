"""Runtime configuration helpers for the eCNH API service."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and optional .env files."""

    app_name: str = "eCNH API"
    environment: str = "development"
    api_prefix: str = "/v1"
    cn_holidays_csv: str = ""
    docs_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ECNHAPI_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
