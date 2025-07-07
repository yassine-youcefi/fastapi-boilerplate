from fastapi import APIRouter
from src.user.routes.v1.user_routers import userRouter

api_router = APIRouter()
api_router.include_router(userRouter, prefix="/user", tags=["User"])
