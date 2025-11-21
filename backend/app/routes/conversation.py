from uuid import UUID

from fastapi import APIRouter
from typing import List, Sequence
from app.dependencies import ConversationServiceDep
from app.models.message import MMessage
from app.schemas.conversation import SConversationRead, SConversationReadFull
from app.schemas.message import SMessageRead

router = APIRouter()

@router.get("", response_model=SConversationReadFull)
async def get_conversation(user_id: UUID, conversation_id: UUID, service: ConversationServiceDep):
    response = await service.get_conversation_info(user_id, conversation_id)
    return response

@router.get("/all", response_model=List[SConversationRead])
async def get_all_conversations(user_id: UUID, service: ConversationServiceDep):
    response = await service.get_conversations(user_id)
    return response

@router.post("/create")
async def create_conversation(user_id: UUID, title: str, service: ConversationServiceDep):
    response = await service.create_conversation(user_id, title)
    return response

@router.get("/messages")
async def conversation_messages(user_id: UUID, conversation_id: UUID, service: ConversationServiceDep):
    messages: Sequence[MMessage] = await service.get_conversation_messages(user_id, conversation_id)
    return [SMessageRead.model_validate(message) for message in messages]

@router.get("/messages/last")
async def conversation_last_message(user_id: UUID, conversation_id: UUID, service: ConversationServiceDep):
    response = await service.get_conversation_last_message(user_id, conversation_id)
    return response
