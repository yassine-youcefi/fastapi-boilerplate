from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration using Pydantic BaseSettings.
    Loads variables from environment and .env file.
    """

    PROJECT_NAME: str = "fastapi-boilerplate"
    DEBUG: bool = True
    ENVIRONMENT: str = "dev"  # Add this line to match .env
    BASE_URL: str = "http://localhost:8000"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRES_IN: int = 36000
    JWT_REFRESH_EXPIRES_IN: int = 604800

    ECHO_SQL: bool = True
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 5
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_TIMEOUT: int = 30
    SERVER_TIMEZONE: str = "UTC+4"

    # Redis configuration
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"  # Default Redis URL format

    # Celery configuration
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str = REDIS_URL

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Get the async database URL (with asyncpg driver)"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Get the sync database URL (with psycopg2 driver)"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URI(self) -> str:
        """Get the Redis URI"""
        if self.REDIS_URL:
            return self.REDIS_URL
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


settings = Settings()
