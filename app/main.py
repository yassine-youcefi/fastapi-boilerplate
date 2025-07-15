import logging

from fastapi import FastAPI
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes.auth_routers import auth_router
from app.config.config import settings
from app.dependencies import get_redis_cache
from app.exceptions import custom_http_exception_handler, custom_validation_exception_handler
from app.integrations.celery_app import create_celery_app
from app.user.routes.user_routers import user_router

# =========================
# Logging Configuration
# =========================
logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)

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
    "docs_url": "/docs" if settings.ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None,
    "redoc_url": "/redoc" if settings.ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None,
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
    app = FastAPI(**app_configs)

    # CORS configuration
    if settings.ENVIRONMENT in SHOW_DOCS_ENVIRONMENT:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[settings.BASE_URL],  # You can add a comma-separated list in settings if needed
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["Authorization", "Content-Type"],
        )

    # Exception handlers
    app.add_exception_handler(Exception, custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
    app.add_exception_handler(FastAPIRequestValidationError, custom_validation_exception_handler)

    # Routers (add API versioning prefix)
    app.include_router(user_router, prefix="/user", tags=["User"])
    app.include_router(auth_router, prefix="/user/auth", tags=["Auth"])

    # Startup/Shutdown events (to be refactored to lifespan in next step)
    @app.on_event("startup")
    async def startup_event():
        try:
            await get_redis_cache()
        except Exception as e:
            logging.error(f"Redis connection failed at startup: {e}")

    @app.on_event("shutdown")
    async def shutdown_event():
        if hasattr(get_redis_cache, "_instance"):
            await get_redis_cache._instance.close()

    return app


# =========================
# App Instance & Health Endpoint
# =========================
app = create_app()
celery = create_celery_app()


@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok"}
