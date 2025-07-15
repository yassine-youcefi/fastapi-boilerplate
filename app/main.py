import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.auth.routes.auth_routers import auth_router
from app.config.config import settings
from app.dependencies import get_redis_cache
from app.exceptions import custom_http_exception_handler, custom_validation_exception_handler
from app.integrations.celery_app import create_celery_app
from app.integrations.database import engine
from app.user.routes.user_routers import user_router

# =========================
# Logging Configuration
# =========================
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}',
)
logger = logging.getLogger("fastapi_boilerplate")

# =========================
# App Config from Settings
# =========================
SHOW_DOCS_ENVIRONMENT = ("dev", "test")

app_configs = {
    "title": settings.PROJECT_NAME,
    "description": "A boilerplate for FastAPI applications with user authentication and Redis caching.",
    "version": "0.0.1",
    "debug": settings.DEBUG,
    "openapi_tags": [
        {
            "name": "User",
            "description": "APIs related to user and account management.",
        },
        {
            "name": "Auth",
            "description": "APIs related to user authentication and token management.",
        },
    ],
    "docs_url": settings.DOCS_URL if settings.ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None,
    "redoc_url": settings.REDOC_URL if settings.ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None,
    "openapi_url": settings.OPENAPI_URL if settings.ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None,
}
if settings.ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
    app_configs["openapi_url"] = None
    app_configs["docs_url"] = None
    app_configs["redoc_url"] = None


# =========================
# App Factory
# =========================
def create_app() -> FastAPI:
    """App factory for FastAPI application."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        logger.info("Starting FastAPI application.")
        try:
            await get_redis_cache()
        except Exception as e:
            logger.error(f"Redis connection failed at startup: {e}")
        yield
        # Shutdown
        if hasattr(get_redis_cache, "_instance"):
            await get_redis_cache._instance.close()

    app = FastAPI(lifespan=lifespan, **app_configs)

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )

    # Exception handlers
    app.add_exception_handler(Exception, custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
    app.add_exception_handler(FastAPIRequestValidationError, custom_validation_exception_handler)

    # Routers (add API versioning prefix)
    app.include_router(user_router, prefix="/user", tags=["User"])
    app.include_router(auth_router, prefix="/user/auth", tags=["Auth"])

    return app


# =========================
# App Instance & Health Endpoint
# =========================
app = create_app()
celery = create_celery_app()


@app.get("/health", include_in_schema=False)
async def health_check():
    redis_status = "unknown"
    db_status = "unknown"
    try:
        redis_cache = await get_redis_cache()
        if await redis_cache.ping():
            redis_status = "ok"
        else:
            redis_status = "unreachable"
    except Exception as e:
        redis_status = f"error: {str(e)}"
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {"status": "ok", "redis": redis_status, "database": db_status}
