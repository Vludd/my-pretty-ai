from fastapi import APIRouter
from app.dependencies import TTSServiceDep

router = APIRouter()

@router.post("/models")
async def completion(service: TTSServiceDep):
    response = await service.get_models()
    return response
