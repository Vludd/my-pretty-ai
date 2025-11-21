from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.conversation import ConversationService
from app.services.llm import LLMService
from app.services.tts import TTSService
from app.services.user import UserService

from app.database import get_db

DBSessionDep = Annotated[AsyncSession, Depends(get_db)]

def get_conversation_service(db: DBSessionDep) -> ConversationService: return ConversationService(db)
def get_llm_service(db: DBSessionDep) -> LLMService: return LLMService(db)
def get_tts_service(db: DBSessionDep) -> TTSService: return TTSService(db)
def get_user_service(db: DBSessionDep) -> UserService: return UserService(db)

ConversationServiceDep = Annotated[ConversationService, Depends(get_conversation_service)]
LLMServiceDep = Annotated[LLMService, Depends(get_llm_service)]
TTSServiceDep = Annotated[TTSService, Depends(get_tts_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
