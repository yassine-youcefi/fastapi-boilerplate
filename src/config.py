import os
from dotenv import load_dotenv # type: ignore
from pydantic_settings import BaseSettings # type: ignore

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastQR-Dine Backend"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRES_IN: int = os.getenv("JWT_EXPIRES_IN", 36000)
    ECHO_SQL: bool = "true"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 5
    DATABASE_URL: str = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

settings = Settings()
