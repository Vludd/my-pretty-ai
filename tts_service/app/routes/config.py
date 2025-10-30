from fastapi import APIRouter
from app.core.tts_config import load_config

router = APIRouter()

@router.get("/config", description="Get a current config for TTS (In Dev)")
async def get_config():
    """Get a current config (IN DEV)"""
    return load_config()
