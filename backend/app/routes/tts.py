from uuid import UUID

from fastapi import APIRouter
from app.services.tts_service import TTSService
from app.dependencies import UserRepo, ConversationRepo, MessageRepo

router = APIRouter()
service = TTSService()

@router.post("/models")
async def completion():
    response = await service.get_models()
    return response

# @router.post("/load/conversation")
# async def load_conversation(
#     user_id: UUID,
#     conversation_id: UUID,
#     user_repo: UserRepo,
#     conversation_repo: ConversationRepo,
#     message_repo: MessageRepo
# ):
#     response = await service.load_conversation(user_id, conversation_id, user_repo, conversation_repo, message_repo)
#     return response
