from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Environment
    env: str = Field(default="development")

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://testservice1:sportsapp@localhost:5432/testdb1"
    )

    # App
    app_name: str = "SportsAppService"
    log_level: str = "info"

# Use ONLY this block for V2 configuration:
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # <-- This fixes the 'workspacefolder' crash!
    )


settings = Settings()
