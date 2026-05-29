from app.core.settings import settings


class AppConfig:
    ENV = settings.env
    DATABASE_URL = settings.database_url
    APP_NAME = settings.app_name
    LOG_LEVEL = settings.log_level


config = AppConfig()
