from fastapi import APIRouter
from app.routes.stt import router as stt_router

api_router = APIRouter()
api_router.include_router(stt_router, tags=["STT"])
