from typing import List, Literal, Sequence
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Query

from app.dependencies import get_conversation_service, get_current_user
from app.models.message import MMessage
from app.schemas.conversation import (SConversationCreate, SConversationRead,
                                      SConversationReadFull)
from app.schemas.message import SMessageRead
from app.services.conversation import ConversationService

router = APIRouter()

@router.post("")
async def create_conversation(
    data: SConversationCreate = Body(..., description="Conversation create data"),
    service: ConversationService = Depends(get_conversation_service),
    current_user = Depends(get_current_user)
):
    response = await service.create_conversation(current_user.public_id, data.title)
    return response

@router.get("", response_model=List[SConversationRead])
async def get_conversations(
    limit: int = Query(50, ge=1, le=100),
    order: Literal["asc", "desc"] = Query("asc"),
    service: ConversationService = Depends(get_conversation_service),
    current_user = Depends(get_current_user)
):
    response = await service.get_conversations(current_user.public_id)
    return response

@router.get("/{conversation_id}", response_model=SConversationReadFull)
async def get_conversation(
    conversation_id: UUID = Path(..., description="Conversation UUID"), 
    service: ConversationService = Depends(get_conversation_service),
    current_user = Depends(get_current_user)
):
    response = await service.get_conversation_info(current_user.public_id, conversation_id)
    return response

@router.get("/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: UUID = Path(..., description="Conversation UUID"),
    limit: int = Query(50, ge=1, le=100),
    order: Literal["asc", "desc"] = Query("asc"),
    service: ConversationService = Depends(get_conversation_service),
    current_user = Depends(get_current_user)
):
    messages: Sequence[MMessage] = await service.get_conversation_messages(current_user.public_id, conversation_id)
    return [SMessageRead.model_validate(message) for message in messages]
