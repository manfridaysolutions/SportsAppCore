from pydantic_settings import BaseSettings
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

    class Config:
        env_file = ".env"          # auto-load in VS Code
        env_file_encoding = "utf-8"


settings = Settings()
