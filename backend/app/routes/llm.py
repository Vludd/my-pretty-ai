from typing import List
from uuid import UUID

from fastapi import APIRouter
from app.dependencies import LLMServiceDep
from app.schemas.prompt import SPromptCreate, SPromptRead, SPromptUpdate

router = APIRouter()

@router.post("/completion")
async def completion(user_id: UUID, conversation_id: UUID, text: str, service: LLMServiceDep):
    response = await service.completion(user_id, conversation_id, text)
    return response

@router.post("/context/load")
async def context_load(user_id: UUID, conversation_id: UUID, service: LLMServiceDep, prompt_id: UUID | None = None):
    response = await service.load_context(user_id, conversation_id, prompt_id)
    return response

@router.post("/load/conversation", deprecated=True)
async def load_conversation(user_id: UUID, conversation_id: UUID, service: LLMServiceDep):
    response = await service.load_conversation(user_id, conversation_id)
    return response
    
@router.post("/prompt", response_model=SPromptRead, description="Create user prompt")
async def create_prompt(user_id: UUID, data: SPromptCreate, service: LLMServiceDep):
    response = await service.create_prompt(user_id, data)
    return response

@router.get("/prompts", response_model=List[SPromptRead], description="Get all user prompts")
async def get_all_prompts(user_id: UUID, service: LLMServiceDep):
    response = await service.get_prompts(user_id)
    return response

@router.get("/prompt", response_model=SPromptRead, description="Get user prompt")
async def get_prompt(user_id: UUID, prompt_id: UUID, service: LLMServiceDep):
    response = await service.get_prompt(user_id, prompt_id)
    return response

@router.put("/prompt", response_model=SPromptRead, description="Update user prompt")
async def update_prompt(user_id: UUID, prompt_id: UUID, data: SPromptUpdate, service: LLMServiceDep):
    response = await service.update_prompt(user_id, prompt_id, data)
    return response

@router.delete("/prompt", description="Delete user prompt")
async def delete_prompt(user_id: UUID, prompt_id: UUID, service: LLMServiceDep):
    await service.delete_prompt(user_id, prompt_id)
    return {"detail": "Prompt deleted!"}

@router.post("/prompts/export")
async def export_prompts(user_id: UUID, service: LLMServiceDep):
    pass

@router.post("/prompts/import")
async def import_prompts(user_id: UUID, service: LLMServiceDep):
    pass
    