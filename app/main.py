from fastapi import FastAPI
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from starlette.config import Config
from fastapi import Request
from app.user.routes.user_routers import user_router
from app.auth.routes.auth_routers import auth_router
from app.exceptions import custom_http_exception_handler, custom_validation_exception_handler

# Load environment configuration
config = Config(".env")
ENVIRONMENT = config("ENVIRONMENT", cast=str, default="dev")
SHOW_DOCS_ENVIRONMENT = ("dev", "test")  # Only show docs in dev and test

app_configs = {
    "title": "Fastapi Boilerplate",
    "description": "API for managing digital restaurant orders.",
    "version": "0.0.1",
    "debug": True
}
if ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
    app_configs["openapi_url"] = None
    app_configs["docs_url"] = None
    app_configs["redoc_url"] = None


def create_app() -> FastAPI:
    """App factory for FastAPI application."""
    app = FastAPI(**app_configs)
    # Exception handlers
    app.add_exception_handler(Exception, custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
    app.add_exception_handler(FastAPIRequestValidationError, custom_validation_exception_handler)

    # Include routers
    app.include_router(user_router, prefix="/user", tags=["User"])
    app.include_router(auth_router, prefix="/user/auth", tags=["Auth"])

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}

    return app


app = create_app()
