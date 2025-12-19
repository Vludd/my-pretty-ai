import logging
from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as ex
from app.core.repository_factory import RepositoryFactory
from app.models.conversation import MConversation
from app.models.message import MMessage
from app.models.prompt import MPrompt
from app.models.user import MUser
from app.modules.prompt_manager.parser import build_system_context
from app.schemas.prompt import SPromptCreate, SPromptUpdate

logger = logging.getLogger(__name__)

prompts_limit = 20

class PromptService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.user_repo = RepositoryFactory.get_repository(MUser, db_session)
        self.prompt_repo = RepositoryFactory.get_repository(MPrompt, db_session)
        
    async def create_prompt(
        self, 
        user_id: UUID, 
        data: SPromptCreate
    ):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        exists_prompts = await self.prompt_repo.get_all()
        
        if len(exists_prompts) >= prompts_limit:
            raise ex.ForbiddenException("There can be no more than {prompts_limit} custom prompts", log_level="warning")
        
        prompt_data = SPromptCreate(
            name=data.name,
            layers=data.layers
        ).model_dump()
        
        prompt_data["user_id"] = exists_user.id
        
        created_user_prompt = await self.prompt_repo.create(prompt_data)
        if not created_user_prompt:
            raise ex.InternalServerException("User Prompt is not created!", log_level="warning")
        
        return created_user_prompt
        
    async def get_prompts(self, user_id: UUID):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        exists_prompts = await self.prompt_repo.get_all_by_user(exists_user.id)
        return exists_prompts
        
    async def get_prompt(self, user_id: UUID, prompt_id: UUID):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        exists_prompt = await self.prompt_repo.get_by_public_id(prompt_id)
        if not exists_prompt:
            raise ex.NotFoundException("Prompt is not found!", log_level="warning")
   
        if not exists_prompt.user_id == exists_user.id and not exists_prompt.is_default:
            raise ex.ForbiddenException("User does not have access to this prompt!", log_level="warning")
        
        return exists_prompt
    
    async def update_prompt(
        self, 
        user_id: UUID, 
        prompt_id: UUID,
        data: SPromptUpdate
    ):
        exists_user = await self.user_repo.get_by_public_id(user_id)
        if not exists_user:
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        exists_prompt = await self.prompt_repo.get_by_public_id(prompt_id)
        if not exists_prompt:
            raise ex.NotFoundException("Prompt is not found!", log_level="warning")
        
        if exists_prompt.is_default:
            raise ex.ForbiddenException("Default prompt cannot be updated!", log_level="warning")
        
        if not exists_prompt.user_id == exists_user.id:
            raise ex.ForbiddenException("User does not have access to this prompt!", log_level="warning")
        
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
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        exists_prompt = await self.prompt_repo.get_by_public_id(prompt_id)
        if not exists_prompt:
            raise ex.NotFoundException("Prompt is not found!", log_level="warning")
        
        if exists_prompt.is_default:
            raise ex.ForbiddenException("Default prompt cannot be deleted!", log_level="warning")
        
        if not exists_prompt.user_id == exists_user.id:
            raise ex.ForbiddenException("User does not have access to this prompt!", log_level="warning")
        
        is_deleted = await self.prompt_repo.delete_by_id(exists_prompt.id)
        if not is_deleted:
            raise ex.InternalServerException("Prompt is not deleted!", log_level="warning")
        
        return is_deleted
