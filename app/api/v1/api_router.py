from fastapi import APIRouter
from app.user.routes.v1.user_routers import user_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/user", tags=["User"])
