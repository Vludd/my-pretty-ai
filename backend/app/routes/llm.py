from uuid import UUID

from fastapi import APIRouter
from app.dependencies import LLMServiceDep

router = APIRouter()

@router.post("/completion")
async def completion(user_id: UUID, conversation_id: UUID, text: str, service: LLMServiceDep):
    response = await service.completion(user_id, conversation_id, text)
    return response

@router.post("/load/conversation")
async def load_conversation(user_id: UUID, conversation_id: UUID, service: LLMServiceDep):
    response = await service.load_conversation(user_id, conversation_id)
    return response
