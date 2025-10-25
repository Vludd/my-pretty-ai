from uuid import UUID
from fastapi.exceptions import HTTPException
from app.dependencies import UserRepo, ConversationRepo, MessageRepo
from app.schemas.conversation import SConversationCreate
from app.utils.logger import logger

class ChatService:
    async def create(
        self, 
        user_id: UUID,
        title: str,
        user_repo: UserRepo,
        conversation_repo: ConversationRepo
    ):
        exists_user = await user_repo.get_by_public_id(user_id)
        if not exists_user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        conversation_data = SConversationCreate(
            title=title
        ).model_dump()
        
        conversation_data["user_id"] = exists_user.id
        
        created_conversation = await conversation_repo.create(conversation_data)
        if not created_conversation:
            logger.error("Conversation is not created!")
            raise HTTPException(status_code=500, detail="Conversation is not created!")
    
        return {"public_id": created_conversation.public_id}
    
    async def get_conversation_messages(
        self,
        user_id: UUID,
        conversation_id: UUID,
        user_repo: UserRepo,
        conversation_repo: ConversationRepo,
        message_repo: MessageRepo
    ):
        exists_user = await user_repo.get_by_public_id(user_id)
        if not exists_user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        exists_conversation = await conversation_repo.get_by_public_id(conversation_id)
        if not exists_conversation:
            logger.error("Conversation is not found!")
            raise HTTPException(status_code=404, detail="Conversation is not found!")
        
        messages = await message_repo.get_all_by_conversation(exists_conversation.id) # type: ignore
        return messages
    
    async def get_conversations(
        self,
        user_id: UUID,
        user_repo: UserRepo,
        conversation_repo: ConversationRepo
    ):
        exists_user = await user_repo.get_by_public_id(user_id)
        if not exists_user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        exists_conversations = await conversation_repo.get_all_by_user(exists_user.id) # type: ignore
        return exists_conversations
