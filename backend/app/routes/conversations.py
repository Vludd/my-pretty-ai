from typing import List, Literal, Sequence
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Query, Response

from app.dependencies import get_conversation_service, get_current_user
from app.models.user import MUser
from app.schemas import SMessageResponse
from app.schemas.conversation import (SConversationCreate, SConversationRead,
                                      SConversationReadFull,
                                      SConversationUpdate)
from app.schemas.message import SMessageRead
from app.services.conversation import ConversationService

router = APIRouter()

@router.post("", response_model=SConversationRead)
async def create_conversation(
    data: SConversationCreate = Body(..., description="Conversation create data"),
    service: ConversationService = Depends(get_conversation_service),
    current_user: MUser = Depends(get_current_user)
):
    response = await service.create_conversation(current_user, data)
    return response

@router.get("", response_model=List[SConversationRead])
async def get_conversations(
    limit: int = Query(50, ge=1, le=100),
    order: Literal["asc", "desc"] = Query("asc"),
    service: ConversationService = Depends(get_conversation_service),
    current_user: MUser = Depends(get_current_user)
):
    response = await service.get_conversations(current_user)
    return response

@router.get("/{conversation_id}", response_model=SConversationReadFull)
async def get_conversation(
    conversation_id: UUID = Path(..., description="Conversation UUID"), 
    service: ConversationService = Depends(get_conversation_service),
    current_user: MUser = Depends(get_current_user)
):
    response = await service.get_conversation_info(current_user, conversation_id)
    return response

@router.patch("/{conversation_id}", response_model=SConversationRead)
async def update_conversation(
    data: SConversationUpdate = Body(..., description="Conversation update data"),
    conversation_id: UUID = Path(..., description="Conversation UUID"), 
    service: ConversationService = Depends(get_conversation_service),
    current_user: MUser = Depends(get_current_user)
):
    response = await service.update_conversation(current_user, conversation_id, data)
    return response

@router.patch("/{conversation_id}/restore", response_model=SMessageResponse)
async def restore_conversation(
    conversation_id: UUID = Path(..., description="Conversation UUID"), 
    service: ConversationService = Depends(get_conversation_service),
    current_user: MUser = Depends(get_current_user)
):
    await service.restore_conversation(current_user, conversation_id)
    return Response(status_code=200)

@router.delete("/{conversation_id}/archive", response_model=SMessageResponse)
async def arhive_conversation(
    conversation_id: UUID = Path(..., description="Conversation UUID"), 
    service: ConversationService = Depends(get_conversation_service),
    current_user: MUser = Depends(get_current_user)
):
    await service.archive_conversation(current_user, conversation_id)
    return Response(status_code=204)

@router.get("/{conversation_id}/messages", response_model=list[SMessageRead])
async def get_conversation_messages(
    conversation_id: UUID = Path(..., description="Conversation UUID"),
    limit: int = Query(0, ge=0, le=100),
    order: Literal["asc", "desc"] = Query("asc"),
    service: ConversationService = Depends(get_conversation_service),
    current_user: MUser = Depends(get_current_user)
):
    messages = await service.get_conversation_messages(current_user, conversation_id)
    return messages
