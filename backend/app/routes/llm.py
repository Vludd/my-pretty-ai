from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies import LLMServiceDep, get_current_user
from app.models.user import MUser
from app.schemas.prompt import SPromptCreate, SPromptRead, SPromptUpdate

router = APIRouter()

@router.post("/completion")
async def completion(
    conversation_id: UUID, 
    text: str, 
    service: LLMServiceDep,
    current_user: MUser = Depends(get_current_user)
):
    response = await service.completion(current_user.public_id, conversation_id, text)
    return response

@router.post("/context/load")
async def context_load(
    conversation_id: UUID,
    service: LLMServiceDep,
    prompt_id: UUID | None = None,
    current_user: MUser = Depends(get_current_user)
):
    response = await service.load_context(current_user.public_id, conversation_id, prompt_id)
    return response
