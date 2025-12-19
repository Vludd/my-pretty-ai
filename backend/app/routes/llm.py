from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies import LLMServiceDep, get_current_user
from app.schemas.prompt import SPromptCreate, SPromptRead, SPromptUpdate

router = APIRouter()

@router.post("/completion")
async def completion(
    user_id: UUID, 
    conversation_id: UUID, 
    text: str, 
    service: LLMServiceDep,
    current_user = Depends(get_current_user)
):
    response = await service.completion(user_id, conversation_id, text)
    return response

@router.post("/context/load")
async def context_load(
    user_id: UUID,
    conversation_id: UUID,
    service: LLMServiceDep,
    prompt_id: UUID | None = None,
    current_user = Depends(get_current_user)
):
    response = await service.load_context(user_id, conversation_id, prompt_id)
    return response

@router.post("/load/conversation", deprecated=True)
async def load_conversation(
    user_id: UUID, 
    conversation_id: UUID, 
    service: LLMServiceDep,
    current_user = Depends(get_current_user)
):
    response = await service.load_conversation(user_id, conversation_id)
    return response
