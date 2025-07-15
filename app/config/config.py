from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration using Pydantic BaseSettings.
    Loads variables from environment and .env file.
    """

    # --- FastAPI App Config ---
    PROJECT_NAME: str = "fastapi-boilerplate"  # The name of the project
    DEBUG: bool = True  # Enable debug mode
    ENVIRONMENT: str = "dev"  # Environment: dev, test, prod
    BASE_URL: str = "http://localhost:8000"  # Base URL for the app
    DOCS_URL: str = "/docs"  # Swagger docs URL
    REDOC_URL: str = "/redoc"  # ReDoc docs URL
    OPENAPI_URL: str = "/openapi.json"  # OpenAPI schema URL
    API_V1_PREFIX: str = "/api/v1"  # API version prefix
    ALLOWED_ORIGINS: List[str] = ["*"]  # CORS allowed origins
    ALLOW_CREDENTIALS: bool = True  # CORS allow credentials
    ALLOW_METHODS: List[str] = ["*"]  # CORS allowed methods
    ALLOW_HEADERS: List[str] = ["*"]  # CORS allowed headers

    # --- Database Config ---
    DB_USER: str  # Database username
    DB_PASSWORD: str  # Database password
    DB_HOST: str  # Database host
    DB_PORT: str  # Database port
    DB_NAME: str  # Database name
    DB_TEST_NAME: str = "fastapi_test_db"  # Test database name
    ECHO_SQL: bool = True  # SQLAlchemy echo SQL
    DB_POOL_SIZE: int = 10  # DB connection pool size
    DB_MAX_OVERFLOW: int = 5  # DB max overflow
    DB_TIMEOUT: int = 30  # DB connection timeout (seconds)
    SERVER_TIMEZONE: str = "UTC+4"  # Server timezone

    # --- Redis Config ---
    REDIS_HOST: str = "redis"  # Redis host
    REDIS_PORT: int = 6379  # Redis port
    REDIS_DB: int = 0  # Redis DB index
    REDIS_URL: str = "redis://redis:6379/0"  # Default Redis URL format

    # --- Celery Config ---
    CELERY_BROKER_URL: str  # Celery broker URL
    CELERY_RESULT_BACKEND: str = REDIS_URL  # Celery result backend

    # --- JWT/Auth Config ---
    JWT_SECRET: str  # JWT secret key
    JWT_ALGORITHM: str = "HS256"  # JWT algorithm
    JWT_ACCESS_EXPIRES_IN: int = 36000  # Access token expiry (seconds)
    JWT_REFRESH_EXPIRES_IN: int = 604800  # Refresh token expiry (seconds)

    # --- AWS S3 Config ---
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION: str
    S3_BUCKET: str
    S3_ENDPOINT_URL: str = "https://s3.{S3_REGION}.amazonaws.com"

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

    @property
    def ASYNC_TEST_DATABASE_URL(self) -> str:
        """Get the async test database URL (with asyncpg driver)"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_TEST_NAME}"
        )


settings = Settings()
