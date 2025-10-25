from uuid import UUID
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import MMessage as MODEL

from app.utils.logger import logger

class MessageRepository:
    def __init__(self, db_session: AsyncSession):
        self.db: AsyncSession = db_session
        self.model = MODEL

    async def create(self, data: dict) -> MODEL:
        try:
            conversation = self.model(**data)
            self.db.add(conversation)
            await self.db.commit()
            await self.db.refresh(conversation)
            return conversation
        except Exception as e:
            raise
    
    async def get_all_by_conversation(self, conversation_id: int, reverse = False):
        stmt = select(self.model).order_by(
            desc(self.model.created_at) if reverse else self.model.created_at
        ).where(self.model.conversation_id == conversation_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, id: int) -> MODEL | None:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_public_id(self, public_id: UUID) -> MODEL | None:
        stmt = select(self.model).where(self.model.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update(self, model: MODEL, new_data: dict) -> MODEL | None:
        try:
            for field, value in new_data.items():
                if hasattr(model, field):
                    setattr(model, field, value)

            self.db.add(model)
            await self.db.flush()
            await self.db.commit()
            await self.db.refresh(model)
            return model

        except IntegrityError as e:
            print(f"Integrity error while updating {self.model.__name__}: {e}")
            await self.db.rollback()
            return None
        except SQLAlchemyError as e:
            logger.error(f"Database error while updating {self.model.__name__}: {e}")
            await self.db.rollback()
            return None
        except Exception as e:
            logger.error(f"Unexpected error while updating {self.model.__name__}: {e}")
            await self.db.rollback()
            raise
        
    async def delete(self, instance: MODEL) -> bool:
        try:
            await self.db.delete(instance)
            await self.db.commit()
            return True

        except IntegrityError as e:
            logger.warning(f"Integrity error while deleting {self.model.__name__}: {e}")
            await self.db.rollback()
            return False

        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting {self.model.__name__}: {e}")
            await self.db.rollback()
            raise

        except Exception as e:
            logger.critical(f"Unexpected error while deleting {self.model.__name__}: {e}")
            await self.db.rollback()
            raise
    
    async def delete_by_id(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        try:
            await self.db.delete(instance)
            await self.db.commit()
            return True

        except IntegrityError as e:
            logger.warning(f"Integrity error while deleting {self.model.__name__}: {e}")
            await self.db.rollback()
            return False

        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting {self.model.__name__}: {e}")
            await self.db.rollback()
            raise

        except Exception as e:
            logger.critical(f"Unexpected error while deleting {self.model.__name__}: {e}")
            await self.db.rollback()
            raise
