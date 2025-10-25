from uuid import UUID

from fastapi import APIRouter
from app.services.llm_service import LLMService
from app.dependencies import UserRepo, ConversationRepo, MessageRepo

router = APIRouter()
service = LLMService()

@router.post("/completion")
async def completion(
    user_id: UUID,
    conversation_id: UUID,
    text: str,
    user_repo: UserRepo,
    conversation_repo: ConversationRepo,
    message_repo: MessageRepo
):
    response = await service.completion(user_id, conversation_id, text, user_repo, conversation_repo, message_repo)
    return response

@router.post("/load/conversation")
async def load_conversation(
    user_id: UUID,
    conversation_id: UUID,
    user_repo: UserRepo,
    conversation_repo: ConversationRepo,
    message_repo: MessageRepo
):
    response = await service.load_conversation(user_id, conversation_id, user_repo, conversation_repo, message_repo)
    return response
