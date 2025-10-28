from fastapi import APIRouter
from app.routes.tts import router as tts_router

api_router = APIRouter()
api_router.include_router(tts_router, tags=["TTS"])
