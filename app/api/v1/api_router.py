from fastapi import APIRouter
from app.user.routes.user_routers import user_router
from app.config.config import Settings, settings

api_router = APIRouter()
api_router.include_router(user_router, prefix="/user", tags=["User"])
