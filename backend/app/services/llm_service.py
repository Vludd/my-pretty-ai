from uuid import UUID
from typing import Sequence
from fastapi.exceptions import HTTPException

from app.models.message import MMessage
from app.schemas.llm import SContextMessage
from app.types.llm import ContextRole
from app.dependencies import LLM, UserRepo, ConversationRepo, MessageRepo
from app.schemas.message import SMessageCreate
from app.types.messages import SenderType
from app.utils.logger import logger

class LLMService:
    async def completion(
        self, 
        user_id: UUID,
        conversation_id: UUID,
        text: str, 
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
        
        message_data = SMessageCreate(
            content=text,
            sender_type=SenderType.USER
        ).model_dump()
        
        message_data["conversation_id"] = exists_conversation.id
        
        created_user_message = await message_repo.create(message_data)
        if not created_user_message:
            logger.error("User Message is not created!")
            raise HTTPException(status_code=500, detail="User Message is not created!")
        
        reply = await LLM.generate(text)
        if not reply:
            logger.error("Error while LLM completion")
            raise HTTPException(status_code=500, detail="Error while LLM completion")
        
        llm_answer = reply.get("reply")
        if not llm_answer:
            logger.error("Response received, but unable to retrieve response content")
            raise HTTPException(status_code=500, detail="Response received, but unable to retrieve response content")
        
        message_data = SMessageCreate(
            content=llm_answer,
            sender_type=SenderType.AI
        ).model_dump()
        
        message_data["conversation_id"] = exists_conversation.id
        
        created_llm_message = await message_repo.create(message_data)
        if not created_llm_message:
            logger.error("AI Message is not created!")
            raise HTTPException(status_code=500, detail="AI Message is not created!")
        
        return reply
    
    async def load_conversation(
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
        
        context: list[SContextMessage] = []
        messages: Sequence[MMessage] = await message_repo.get_all_by_conversation(exists_conversation.id) # type: ignore
        if messages:
            for message in messages:
                message_role = ContextRole.ASSISTANT if bool(message.sender_type == SenderType.AI) else ContextRole.USER
                
                context_message = SContextMessage(
                    role=message_role,
                    content=str(message.content)
                )
                
                context.append(context_message)
        
        await LLM.load_conversation(context)
        return {"details": "Conversation loaded!"}
    
    # async def create_user(self, data: SUserCreate, user_repo: UserRepo) -> SUserRead:
    #     if data.password != data.password_verify:
    #         raise HTTPException(status_code=400, detail="Passwords do not match")
        
    #     hashed_password = argon2.hash(data.password)
        
    #     user_dict = data.model_dump(exclude={"password", "password_verify"})
    #     user_dict["password_hash"] = hashed_password
        
    #     created_user = await user_repo.create(user_dict)
    #     if not created_user:
    #         logger.error("Users is not created!")
    #         raise HTTPException(status_code=500, detail="Users is not created!")

    #     return SUserRead.model_validate(created_user)
    
    # async def login_user(self, data: SUserLogin, user_repo: UserRepo):
    #     exists_user = await user_repo.get_by_username(data.username)
    #     if not exists_user:
    #         raise HTTPException(status_code=500, detail="User is not registered")
        
    #     if not exists_user.password_hash: # type: ignore
    #         raise HTTPException(status_code=400, detail="User account is broken")
        
    #     verified = argon2.verify(data.password, exists_user.password_hash)
    #     if not verified:
    #         raise HTTPException(status_code=400, detail="Incorrect username or password")
        
    #     update_data = SUserUpdate(
    #         last_login_at=datetime.now(timezone.utc)
    #     ).model_dump(exclude_unset=True)
        
    #     updated_user = await user_repo.update(exists_user, update_data)
    #     if not updated_user:
    #         raise HTTPException(status_code=500, detail="Error while updating user")
        
    #     return {"public_id": str(exists_user.public_id)}
    
    # async def register_user(self, data: SUserCreate, user_repo: UserRepo) -> str:
    #     if data.password != data.password_verify:
    #         raise HTTPException(status_code=400, detail="Passwords do not match")
        
    #     hashed_password = argon2.hash(data.password)
        
    #     user_dict = data.model_dump(exclude={"password", "password_verify"})
    #     user_dict["password_hash"] = hashed_password
    #     user_dict["last_login_at"] = datetime.now(timezone.utc)
        
    #     try:
    #         created_user = await user_repo.create(user_dict)
    #         if not created_user:
    #             logger.error("Users is not created!")
    #             raise HTTPException(status_code=500, detail="Users is not created!")
            
    #         return str(created_user.public_id)
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Error: {e}")
