from uuid import UUID
from sqlalchemy import asc, select, desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import MMessage
from app.repositories import BaseRepository

class MessageRepository(BaseRepository):
    async def get_all_by_conversation(self, conversation_id: int, reverse=False):
        stmt = select(self.model).order_by(
            desc(self.model.created_at) if reverse else self.model.created_at
        ).where(self.model.conversation_id == conversation_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_latest_by_conversation(self, conversation_id: int, reverse=False):
        stmt = (
            select(self.model)
            .where(self.model.conversation_id == conversation_id)
            .order_by(
                asc(self.model.created_at) if reverse else desc(self.model.created_at)
            )
            .limit(1)
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().first()

