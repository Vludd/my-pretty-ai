from uuid import UUID
from sqlalchemy import select, desc

from app.core.exceptions import RepositoryError
from app.models.prompt import MPrompt
from app.repositories import BaseRepository

class PromptRepository(BaseRepository):
    async def get_by_public_id(self, public_id: UUID) -> MPrompt | None:
        try:
            stmt = select(self.model).where(self.model.public_id == public_id)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise RepositoryError("Failed to fetch prompt by public ID", e)

    async def get_all_by_user(self, user_id: int):
        try:
            stmt = select(self.model).where(
                (self.model.is_default == True) | (self.model.user_id == user_id)
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepositoryError("Failed to fetch user prompts", e)
        
    async def get_default_prompt(self):
        try:
            stmt = select(self.model).where(self.model.is_default == True)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise RepositoryError("Failed to fetch default prompt", e)
    
    async def create_default_prompt(self, data: dict):
        exists = await self.get_default_prompt()
        if exists:
            return
        
        await self.create(data)
