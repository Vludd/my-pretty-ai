from uuid import UUID
from sqlalchemy import select, desc

from app.repositories import BaseRepository
from app.models.conversation import MConversation

from app.core.exceptions import RepositoryError

class ConversationRepository(BaseRepository):
    async def get_by_public_id(self, public_id: UUID) -> MConversation | None:
        try:
            stmt = select(self.model).where(self.model.public_id == public_id)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise RepositoryError("Failed to fetch conversation by public ID", e)
        
        
    async def get_all_by_user(self, user_id: int, reverse = False):
        try:
            stmt = (
                select(self.model)
                .where(self.model.user_id == user_id)
                .order_by(
                    desc(self.model.created_at) 
                    if reverse 
                    else self.model.created_at
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepositoryError("Failed to fetch user conversations", e)
