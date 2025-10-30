from fastapi import APIRouter
from app.routes.tts import router as tts_router
from app.routes.models import router as models_router
from app.routes.config import router as config_router

api_router = APIRouter()
api_router.include_router(tts_router, tags=["TTS"])
api_router.include_router(models_router, tags=["Models"])
api_router.include_router(config_router, tags=["Config"])