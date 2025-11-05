from uuid import UUID
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import MUser
from app.repositories import BaseRepository

class UserRepository(BaseRepository):
    async def get_by_public_id(self, public_id: UUID) -> MUser | None:
        stmt = select(self.model).where(self.model.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> MUser | None:
        stmt = select(self.model).where(self.model.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
