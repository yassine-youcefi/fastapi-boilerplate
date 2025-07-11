import logging

from fastapi import FastAPI
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.config import Config

from app.auth.routes.auth_routers import auth_router
from app.config.config import settings
from app.exceptions import custom_http_exception_handler, custom_validation_exception_handler
from app.user.routes.user_routers import user_router
from app.utils.redis_cache import RedisCache

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
    "description": "API for managing digital restaurant orders.",
    "version": "0.0.1",
    "debug": True,
}
if ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
    app_configs["openapi_url"] = None
    app_configs["docs_url"] = None
    app_configs["redoc_url"] = None

# =========================
# Redis Cache
# =========================
redis_cache = RedisCache(url=settings.REDIS_URI)


def get_redis_cache() -> RedisCache:
    return redis_cache


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
        await redis_cache.connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        await redis_cache.close()

    # Example cache endpoint (can be removed in production)
    @app.get("/cache-example")
    async def cache_example():
        cached = await redis_cache.get("example_key")
        if cached:
            return {"cached": True, "value": cached}
        await redis_cache.set("example_key", "hello from redis!", expire=60)
        return {"cached": False, "value": "hello from redis!"}

    return app


# =========================
# App Instance & Health Endpoint
# =========================
app = create_app()


@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok"}
