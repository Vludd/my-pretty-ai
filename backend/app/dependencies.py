from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import UserRepository, ConversationRepository, MessageRepository

from app.database import get_db

from app.data.configs.llm_config_schema import SLLMConfig
from app.core.ai_engine import LLMEngine

llm_config = SLLMConfig()
LLM = LLMEngine(
    llm_config, 
    layers_order=["system", "about", "rules", "safety", "personality", "relationship", "context", "time_context", "erotic"],
    layer_variants={
        "personality": "sadodere",
        "relationship": "friend"
    }
)

DBSessionDep = Annotated[AsyncSession, Depends(get_db)]

def get_user_repo(db: DBSessionDep) -> UserRepository: return UserRepository(db)
def get_conversation_repo(db: DBSessionDep) -> ConversationRepository: return ConversationRepository(db)
def get_message_repo(db: DBSessionDep) -> MessageRepository: return MessageRepository(db)

UserRepo = Annotated[UserRepository, Depends(get_user_repo)]
ConversationRepo = Annotated[ConversationRepository, Depends(get_conversation_repo)]
MessageRepo = Annotated[MessageRepository, Depends(get_message_repo)]
