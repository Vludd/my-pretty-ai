import tempfile
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse, StreamingResponse

from app.dependencies import stt

router = APIRouter()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail=f"Неверный тип файла: {file.content_type}")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        text = stt.transcribe(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при расшифровке: {e}")

    return JSONResponse({"text": text})
