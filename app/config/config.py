from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Application configuration using Pydantic BaseSettings.
    Loads variables from environment and .env file.
    """
    PROJECT_NAME: str = "FastQR-Dine Backend"
    APP_ENV: str = "development"
    DEBUG: bool = True
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_IN: int = 36000
    ECHO_SQL: bool = True
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 5
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_TIMEOUT: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Get the async database URL (with asyncpg driver)"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Get the sync database URL (with psycopg2 driver)"""
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
