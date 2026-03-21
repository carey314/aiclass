from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.stages import router as stages_router
from app.api.v1.lessons import router as lessons_router
from app.api.v1.media import router as media_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)
api_v1_router.include_router(stages_router)
api_v1_router.include_router(lessons_router)
api_v1_router.include_router(media_router)
