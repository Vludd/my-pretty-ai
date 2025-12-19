from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies import PromptsServiceDep, get_current_user
from app.models.user import MUser
from app.schemas.prompt import SPromptCreate, SPromptRead, SPromptUpdate

router = APIRouter()
    
@router.post("", response_model=SPromptRead, description="Create user prompt")
async def create_prompt(
    data: SPromptCreate, 
    service: PromptsServiceDep,
    current_user: MUser = Depends(get_current_user)
):
    response = await service.create_prompt(current_user.public_id, data)
    return response

@router.get("", response_model=List[SPromptRead], description="Get all user prompts")
async def get_prompts(
    service: PromptsServiceDep,
    current_user: MUser = Depends(get_current_user)
):
    response = await service.get_prompts(current_user.public_id)
    return response

@router.get("/{prompt_id}", response_model=SPromptRead, description="Get user prompt")
async def get_prompt(
    prompt_id: UUID, 
    service: PromptsServiceDep,
    current_user: MUser = Depends(get_current_user)
):
    response = await service.get_prompt(current_user.public_id, prompt_id)
    return response

@router.patch("/{prompt_id}", response_model=SPromptRead, description="Update user prompt")
async def update_prompt(
    prompt_id: UUID, 
    data: SPromptUpdate, 
    service: PromptsServiceDep,
    current_user: MUser = Depends(get_current_user)
):
    response = await service.update_prompt(current_user.public_id, prompt_id, data)
    return response

@router.delete("", description="Delete user prompt")
async def delete_prompt(
    prompt_id: UUID, 
    service: PromptsServiceDep,
    current_user: MUser = Depends(get_current_user)
):
    await service.delete_prompt(current_user.public_id, prompt_id)
    return {"detail": "Prompt deleted!"}

@router.post("/export")
async def export_prompts(
    user_id: UUID, 
    service: PromptsServiceDep,
    current_user: MUser = Depends(get_current_user)
):
    pass

@router.post("/import")
async def import_prompts(
    user_id: UUID, 
    service: PromptsServiceDep,
    current_user: MUser = Depends(get_current_user)
):
    pass
