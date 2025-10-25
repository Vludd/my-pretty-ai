from uuid import UUID

from fastapi import APIRouter
from typing import Sequence
from app.services.conversation_service import ChatService
from app.models.message import MMessage
from app.schemas.message import SMessageRead
from app.dependencies import UserRepo, ConversationRepo, MessageRepo

router = APIRouter()
service = ChatService()

@router.get("")
async def get_conversations(
    user_id: UUID,
    user_repo: UserRepo,
    conversation_repo: ConversationRepo
):
    response = await service.get_conversations(user_id, user_repo, conversation_repo)
    return response

@router.get("/{conversation_id}/messages")
async def get_messages(
    user_id: UUID,
    conversation_id: UUID,
    user_repo: UserRepo,
    conversation_repo: ConversationRepo,
    message_repo: MessageRepo
):
    messages: Sequence[MMessage] = await service.get_conversation_messages(user_id, conversation_id, user_repo, conversation_repo, message_repo)
    return [SMessageRead.model_validate(message) for message in messages]

@router.post("/create")
async def create_conversation(
    user_id: UUID,
    title: str,
    user_repo: UserRepo,
    conversation_repo: ConversationRepo
):
    response = await service.create(user_id, title, user_repo, conversation_repo)
    return response
