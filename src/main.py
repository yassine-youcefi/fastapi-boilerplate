from fastapi import FastAPI, Depends
from src.api.v1.api_router import api_router


def create_app() -> FastAPI:
    """App factory for FastAPI application."""
    app = FastAPI(
        title="FASTQR DINE API",
        description="API for managing digital restaurant orders.",
        version="0.0.1",
        debug=True
    )
    # Include central API router
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}

    return app


app = create_app()
