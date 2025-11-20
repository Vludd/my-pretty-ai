import httpx

from uuid import UUID
from typing import List, Sequence, Union
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from app.models.user import MUser
from app.models.conversation import MConversation
from app.models.message import MMessage
from app.models.prompt import MPrompt

from app.core.repository_factory import RepositoryFactory

from app.types.llm import ContextRole
from app.config import LLM_URL
from app.schemas.message import SMessageCreate
from app.schemas.prompt import DefaultLayer, LayerWithOptions, SPromptCreate, BaseLayer, SPromptUpdate
from app.types.messages import SenderType
from app.utils.logger import logger

prompts_limit = 20

class LLMService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.user_repo = RepositoryFactory.get_repository(MUser, db_session)
        self.conversation_repo = RepositoryFactory.get_repository(MConversation, db_session)
        self.message_repo = RepositoryFactory.get_repository(MMessage, db_session)
        self.prompt_repo = RepositoryFactory.get_repository(MPrompt, db_session)
        
    async def completion(self, user_id: UUID, conversation_id: UUID, text: str):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        exists_conversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not exists_conversation:
            logger.error("Conversation is not found!")
            raise HTTPException(status_code=404, detail="Conversation is not found!")
        
        message_data = SMessageCreate(
            content=text,
            sender_type=SenderType.USER
        ).model_dump()
        
        message_data["conversation_id"] = exists_conversation.id
        
        created_user_message = await self.message_repo.create(message_data)
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
                
                created_llm_message = await self.message_repo.create(message_data)
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
    
    async def load_conversation(self, user_id: UUID, conversation_id: UUID):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        exists_conversation = await self.conversation_repo.get_by_public_id(conversation_id)
        if not exists_conversation:
            logger.error("Conversation is not found!")
            raise HTTPException(status_code=404, detail="Conversation is not found!")
        
        context: list[dict] = []
        messages: Sequence[MMessage] = await self.message_repo.get_all_by_conversation(exists_conversation.id) # type: ignore
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
    
    async def create_prompt(
        self, 
        user_id: UUID, 
        data: SPromptCreate
    ):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        exists_prompts = await self.prompt_repo.get_all()
        
        if len(exists_prompts) >= prompts_limit:
            raise HTTPException(status_code=403, detail=f"There can be no more than {prompts_limit} custom prompts")
        
        prompt_data = SPromptCreate(
            name=data.name,
            layers=data.layers
        ).model_dump()
        
        prompt_data["user_id"] = exists_user.id
        
        created_user_prompt = await self.prompt_repo.create(prompt_data)
        if not created_user_prompt:
            logger.error("User Prompt is not created!")
            raise HTTPException(status_code=500, detail="User Prompt is not created!")
        
        return created_user_prompt
        
    async def get_prompts(self, user_id: UUID):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        exists_prompts = await self.prompt_repo.get_all_by_user(exists_user.id)
        return exists_prompts
        
    async def get_prompt(self, user_id: UUID, prompt_id: UUID):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        exists_prompt = await self.prompt_repo.get_by_public_id(prompt_id)
        if not exists_prompt:
            logger.error("Prompt is not found!")
            raise HTTPException(status_code=404, detail="Prompt is not found!")
   
        if not exists_prompt.user_id == exists_user.id:
            logger.warning("User does not have access to this prompt")
            raise HTTPException(status_code=403, detail="User does not have access to this prompt!")
        
        return exists_prompt
    
    async def update_prompt(
        self, 
        user_id: UUID, 
        prompt_id: UUID,
        data: SPromptUpdate
    ):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        exists_prompt = await self.prompt_repo.get_by_public_id(prompt_id)
        if not exists_prompt:
            logger.error("Prompt is not found!")
            raise HTTPException(status_code=404, detail="Prompt is not found!")
        
        if not exists_prompt.user_id == exists_user.id:
            logger.warning("User does not have access to this prompt")
            raise HTTPException(status_code=403, detail="User does not have access to this prompt!")
        
        if exists_prompt.is_default:
            logger.warning("Default prompt cannot be updated!")
            raise HTTPException(status_code=403, detail="Default prompt cannot be updated!")
        
        new_prompt_data = SPromptUpdate(
            name=data.name if data.name else exists_prompt.name,
            layers=data.layers if data.layers else exists_prompt.layers
        )
            
        updated_prompt = await self.prompt_repo.update(exists_prompt, new_prompt_data.model_dump(exclude_unset=True))
        if not updated_prompt:
            logger.warning("Prompt is not updated")
            raise HTTPException(status_code=500, detail="Prompt is not updated!")
        
        return updated_prompt
    
    async def delete_prompt(self, user_id: UUID, prompt_id: UUID):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        exists_prompt = await self.prompt_repo.get_by_public_id(prompt_id)
        if not exists_prompt:
            logger.error("Prompt is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        if not exists_prompt.user_id == exists_user.id:
            logger.warning("User does not have access to this prompt")
            raise HTTPException(status_code=403, detail="User does not have access to this prompt!")
        
        if exists_prompt.is_default:
            logger.warning("Default prompt cannot be deleted!")
            raise HTTPException(status_code=403, detail="Default prompt cannot be deleted!")
        
        is_deleted = await self.prompt_repo.delete_by_id(exists_prompt.id)
        if not is_deleted:
            logger.error("Prompt is not deleted!")
            raise HTTPException(status_code=500, detail="Prompt is not deleted!")
        
        return is_deleted
