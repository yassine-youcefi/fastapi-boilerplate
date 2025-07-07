from fastapi import FastAPI
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from app.user.routes.v1.user_routers import user_router
from app.user.exceptions import custom_http_exception_handler, custom_validation_exception_handler


def create_app() -> FastAPI:
    """App factory for FastAPI application."""
    app = FastAPI(
        title="FASTQR DINE API",
        description="API for managing digital restaurant orders.",
        version="0.0.1",
        debug=True
    )
    # Exception handlers
    app.add_exception_handler(Exception, custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
    app.add_exception_handler(FastAPIRequestValidationError, custom_validation_exception_handler)
    # Include user router
    app.include_router(user_router, prefix="/api/v1/user", tags=["User"])

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}

    return app


app = create_app()
