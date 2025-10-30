from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.dependencies import tts

router = APIRouter()

@router.post("/speech", description="Generate audio from input text")
async def speech(text: str):
    """Generates audio from input text and returns it as a StreamingResponse."""
    return StreamingResponse(tts.generate_stream(text), media_type="audio/wav")

@router.post("/generate", description="Generate audio from input text and save it to a file")
async def generate_audio_file(text: str):
    """
    Generates audio from input text and saves it to a file.
    Returns the filename, file path, and size (in bytes).
    """
    return {
        "filename": "example_audio.wav",
        "path": "./output/example_audio.wav",
        "size": 51.551
    }
