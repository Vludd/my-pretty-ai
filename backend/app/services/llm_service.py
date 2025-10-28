import httpx

from uuid import UUID
from typing import List, Sequence
from fastapi.exceptions import HTTPException

from app.models.message import MMessage
from app.types.llm import ContextRole
from app.dependencies import UserRepo, ConversationRepo, MessageRepo, LLM_URL
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
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                data = { "text": text }
                response = await client.post(f"{LLM_URL}/completion", json=data)
                
                if response.status_code == 404:
                    logger.error(f"LLM Service request error: {response.text}")
                    raise HTTPException(
                        status_code=404,
                        detail=response.text
                    )

                elif response.status_code == 400:
                    logger.error(f"LLM Service request error: {response.text}")
                    raise HTTPException(
                        status_code=400,
                        detail=response.text
                    )

                elif not response.is_success:
                    logger.error(f"LLM Service request error: {response.text}")
                    raise HTTPException(
                        status_code=502,
                        detail=response.text
                    )
                
                llm_answer = response.json()["reply"]
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
                
                return response.json()
            
            except httpx.ConnectTimeout:
                logger.error("LLM Service request timeout")
                raise HTTPException(
                    status_code=504,
                    detail="LLM Service request timeout"
                )

            except httpx.ConnectError:
                logger.error("LLM Service unavailable")
                raise HTTPException(
                    status_code=503,
                    detail="LLM Service unavailable"
                )

            except Exception as e:
                logger.exception("Unexpected error when calling LLM Service")
                raise HTTPException(
                    status_code=500,
                    detail="Unexpected error when calling LLM Service"
                )
    
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
        
        context: list[dict] = []
        messages: Sequence[MMessage] = await message_repo.get_all_by_conversation(exists_conversation.id) # type: ignore
        if messages:
            for message in messages:
                message_role = ContextRole.ASSISTANT if bool(message.sender_type == SenderType.AI) else ContextRole.USER
                
                context_message = {
                    "role": message_role.value,
                    "content": str(message.content)
                }
                
                context.append(context_message)
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(f"{LLM_URL}/context/load", json=context)
                
                if response.status_code == 404:
                    logger.error(f"LLM Service request error: {response.text}")
                    raise HTTPException(
                        status_code=404,
                        detail=response.text
                    )

                elif response.status_code == 400:
                    logger.error(f"LLM Service request error: {response.text}")
                    raise HTTPException(
                        status_code=400,
                        detail=response.text
                    )

                elif not response.is_success:
                    logger.error(f"LLM Service request error: {response.text}")
                    raise HTTPException(
                        status_code=502,
                        detail=response.text
                    )
                
                return {"detail": "Context has been loaded"}
            
            except httpx.ConnectTimeout:
                logger.error("LLM Service request timeout")
                raise HTTPException(
                    status_code=504,
                    detail="LLM Service request timeout"
                )

            except httpx.ConnectError:
                logger.error("LLM Service unavailable")
                raise HTTPException(
                    status_code=503,
                    detail="LLM Service unavailable"
                )

            except Exception as e:
                logger.exception("Unexpected error when calling LLM Service")
                raise HTTPException(
                    status_code=500,
                    detail="Unexpected error when calling LLM Service"
                )
    
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
