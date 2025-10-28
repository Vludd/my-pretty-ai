from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, StreamingResponse

from app.dependencies import tts

router = APIRouter()

@router.post("/generate")
async def generate(text: str, request: Request):
    return StreamingResponse(tts.generate_stream(text), media_type="audio/wav")
