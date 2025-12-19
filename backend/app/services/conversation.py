from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as ex
from app.core.repository_factory import RepositoryFactory
from app.models.conversation import MConversation
from app.models.message import MMessage
from app.models.user import MUser
from app.schemas import SMessageResponse
from app.schemas.conversation import (SConversationCreate, SConversationRead,
                                      SConversationReadFull,
                                      SConversationUpdate)
from app.schemas.message import SMessageRead


class ConversationService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.user_repo = RepositoryFactory.get_repository(MUser, db_session)
        self.conversation_repo = RepositoryFactory.get_repository(MConversation, db_session)
        self.message_repo = RepositoryFactory.get_repository(MMessage, db_session)
        
    async def get_conversation_info(
        self, 
        user: MUser, 
        conversation_id: UUID
    ) -> SConversationReadFull:
        conversation: MConversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not conversation:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.deleted:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.user_id != user.id:
            raise ex.ForbiddenException("User doesn't have access to this conversation", log_level="warning")
        
        full_info = SConversationReadFull(
            public_id=conversation.public_id,
            title=conversation.title,
            messages=None,
            last_message=None,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        ).model_dump()
        
        messages = await self.message_repo.get_all_by_conversation(conversation.id)
        last_message = messages[-1]
        
        full_info["messages"] = messages
        full_info["last_message"] = last_message
        
        return SConversationReadFull(**full_info)
        
    async def create_conversation(
        self, 
        user: MUser, 
        data: SConversationCreate
    ) -> SConversationRead:
        conversation_data = SConversationCreate(title=data.title).model_dump()
        conversation_data["user_id"] = user.id
        
        created_conversation = await self.conversation_repo.create(conversation_data)
        if not created_conversation:
            raise ex.InternalServerException("Conversation is not created!")
    
        return SConversationRead.model_validate(created_conversation)
    
    async def get_conversation_messages(
        self, 
        user: MUser, 
        conversation_id: UUID
    ) -> list[SMessageRead]:
        conversation: MConversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not conversation:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.deleted:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.user_id != user.id:
            raise ex.ForbiddenException("User doesn't have access to this conversation", log_level="warning")
        
        messages = await self.message_repo.get_all_by_conversation(conversation.id) # type: ignore
        return [SMessageRead.model_validate(m) for m in messages]
    
    async def get_conversation_last_message(
        self, 
        user: MUser, 
        conversation_id: UUID
    ) -> SMessageRead:
        conversation: MConversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not conversation:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.deleted:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.user_id != user.id:
            raise ex.ForbiddenException("User doesn't have access to this conversation", log_level="warning")
        
        last_message = await self.message_repo.get_latest_by_conversation(conversation.id) # type: ignore
        return SMessageRead.model_validate(last_message)
    
    async def get_conversations(
        self, 
        user: MUser
    ) -> list[SConversationRead]:
        conversations = await self.conversation_repo.get_all_by_user(user.id) # type: ignore
        return [SConversationRead.model_validate(c) for c in conversations]
    
    async def update_conversation(
        self, 
        user: MUser, 
        conversation_id: UUID, 
        data: SConversationUpdate
    ) -> SConversationRead:
        conversation: MConversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not conversation:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.deleted:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.user_id != user.id:
            raise ex.ForbiddenException("User doesn't have access to this conversation", log_level="warning")
        
        updated_converstaion = await self.conversation_repo.update(conversation, data.model_dump(exclude_unset=True))
        if not updated_converstaion:
            raise ex.InternalServerException("Conversation is not updated!")
    
        return SConversationRead.model_validate(updated_converstaion)
    
    async def hard_delete_conversation(
        self, 
        user: MUser, 
        conversation_id: UUID
    ) -> SMessageResponse:
        conversation: MConversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not conversation:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.user_id != user.id:
            raise ex.ForbiddenException("User doesn't have access to this conversation", log_level="warning")
        
        deleted = await self.conversation_repo.delete(conversation)
        if not deleted:
            raise ex.InternalServerException("Conversation is not deleted!")
        
        return SMessageResponse(detail="Conversation has been deleted")

    async def archive_conversation(
        self,
        user: MUser,
        conversation_id: UUID
    ):
        conversation: MConversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not conversation:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.deleted:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.user_id != user.id:
            raise ex.ForbiddenException("User doesn't have access to this conversation", log_level="warning")
        
        archived = await self.conversation_repo.update(conversation, { "deleted": True })
        if not archived:
            raise ex.InternalServerException("Conversation is not archived!")

    async def restore_conversation(
        self,
        user: MUser,
        conversation_id: UUID
    ):
        conversation: MConversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not conversation:
            raise ex.NotFoundException("Conversation is not found!", log_level="warning")
        
        if conversation.user_id != user.id:
            raise ex.ForbiddenException("User doesn't have access to this conversation", log_level="warning")
        
        if not conversation.deleted:
            return
        
        restored = await self.conversation_repo.update(conversation, { "deleted": False })
        if not restored:
            raise ex.InternalServerException("Conversation is not restored!")
    