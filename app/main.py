import logging

from fastapi import FastAPI
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.config import Config

from app.auth.routes.auth_routers import auth_router
from app.dependencies import get_redis_cache
from app.exceptions import custom_http_exception_handler, custom_validation_exception_handler
from app.user.routes.user_routers import user_router

# =========================
# Logging Configuration
# =========================
logging.basicConfig(level=logging.DEBUG)

# =========================
# Environment & App Config
# =========================
config = Config(".env")
ENVIRONMENT = config("ENVIRONMENT", cast=str, default="dev")
SHOW_DOCS_ENVIRONMENT = ("dev", "test")

app_configs = {
    "title": "Fastapi Boilerplate",
    "description": "A boilerplate for FastAPI applications with user authentication and Redis caching.",
    "version": "0.0.1",
    "debug": ENVIRONMENT in SHOW_DOCS_ENVIRONMENT,
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
    "docs_url": "/docs" if ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None,
    "redoc_url": "/redoc" if ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None,
}
if ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
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
    if ENVIRONMENT in SHOW_DOCS_ENVIRONMENT:
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
            allow_origins=["https://your-production-domain.com"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["Authorization", "Content-Type"],
        )

    # Exception handlers
    app.add_exception_handler(Exception, custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
    app.add_exception_handler(FastAPIRequestValidationError, custom_validation_exception_handler)

    # Routers
    app.include_router(user_router, prefix="/user", tags=["User"])
    app.include_router(auth_router, prefix="/user/auth", tags=["Auth"])

    # Startup/Shutdown events
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


@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok"}
