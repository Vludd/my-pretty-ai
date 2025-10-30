from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse, StreamingResponse

from app.utils import load_tts_models, refresh_tts_models_cache

router = APIRouter()

@router.get("/models", description="Get a list of TTS models")
async def get_models(
    lang: str | None = Query(None, description="Language filer. Examples: en, ru, fr"),
    downloaded: bool | None = Query(None, description="Downloading status filter")
):
    models = load_tts_models()

    filtered = [
        m for m in models
        if (lang is None or m["language"] == lang)
        and (downloaded is None or m["downloaded"] == downloaded)
    ]
    return {"models": filtered, "total": len(filtered)}

@router.post("/models/refresh", description="Force refresh list of TTS models")
async def refresh_models():
    result = refresh_tts_models_cache()
    return result
