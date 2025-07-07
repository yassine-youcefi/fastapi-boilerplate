from fastapi import APIRouter
from app.user.routes.v1.user_routers import userRouter
from app.config.config import Settings, settings

api_router = APIRouter()
api_router.include_router(userRouter, prefix="/user", tags=["User"])
