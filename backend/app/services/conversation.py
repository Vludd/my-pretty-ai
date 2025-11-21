from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.conversation import SConversationCreate, SConversationReadFull

from app.models.user import MUser
from app.models.conversation import MConversation
from app.models.message import MMessage

from app.core.repository_factory import RepositoryFactory

import app.core.exceptions as ex

class ConversationService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.user_repo = RepositoryFactory.get_repository(MUser, db_session)
        self.conversation_repo = RepositoryFactory.get_repository(MConversation, db_session)
        self.message_repo = RepositoryFactory.get_repository(MMessage, db_session)
        
    async def get_conversation_info(self, user_id: UUID, conversation_id: UUID):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        exists_conversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not exists_conversation:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if exists_conversation.user_id != exists_user.id:
            raise ex.ForbiddenException("User doesn't have access to this conversation", log_level="warning")
        
        conversation_full_info = SConversationReadFull(
            public_id=exists_conversation.public_id,
            title=exists_conversation.title,
            messages=None,
            last_message=None,
            created_at=exists_conversation.created_at,
            updated_at=exists_conversation.updated_at
        ).model_dump()
        
        messages = await self.message_repo.get_all_by_conversation(exists_conversation.id)
        last_message = messages[-1]
        
        conversation_full_info["messages"] = messages
        conversation_full_info["last_message"] = last_message
        
        return conversation_full_info
        
    async def create_conversation(self, user_id: UUID, title: str):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        conversation_data = SConversationCreate(title=title).model_dump()
        conversation_data["user_id"] = exists_user.id
        
        created_conversation = await self.conversation_repo.create(conversation_data)
        if not created_conversation:
            raise ex.InternalServerException("Conversation is not created!")
    
        return {"public_id": created_conversation.public_id}
    
    async def get_conversation_messages(self, user_id: UUID, conversation_id: UUID):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        exists_conversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not exists_conversation:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if exists_conversation.user_id != exists_user.id:
            raise ex.ForbiddenException("User doesn't have access to this conversation", log_level="warning")
        
        messages = await self.message_repo.get_all_by_conversation(exists_conversation.id) # type: ignore
        return messages
    
    async def get_conversation_last_message(self, user_id: UUID, conversation_id: UUID):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        exists_conversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not exists_conversation:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if exists_conversation.user_id != exists_user.id:
            raise ex.ForbiddenException("User doesn't have access to this conversation", log_level="warning")
        
        last_message = await self.message_repo.get_latest_by_conversation(exists_conversation.id) # type: ignore
        return last_message
    
    async def get_conversations(self, user_id: UUID):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        exists_conversations = await self.conversation_repo.get_all_by_user(exists_user.id) # type: ignore
        return exists_conversations
