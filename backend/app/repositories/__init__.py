from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import RepositoryError

class BaseRepository:
    def __init__(self, db_session: AsyncSession, model):
        self.db: AsyncSession = db_session
        self.model = model

    # =========================================
    # > CREATE
    # =========================================
    async def create(self, data: dict):
        try:
            instance = self.model(**data)
            self.db.add(instance)
            await self.db.commit()
            await self.db.refresh(instance)
            return instance
        except Exception as e:
            await self.db.rollback()
            raise RepositoryError(f"Failed to create {self.model.__name__}", e)

    # =========================================
    # > READ
    # =========================================
    async def get_by_id(self, id: int):
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise RepositoryError(f"Failed to fetch {self.model.__name__} by ID", e)

    async def get_all(self, reverse: bool = False):
        try:
            stmt = select(self.model).order_by(
                desc(self.model.created_at) if reverse else self.model.created_at
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepositoryError(f"Failed to fetch all {self.model.__name__} entries", e)

    # =========================================
    # > UPDATE
    # =========================================
    async def update(self, instance, new_data: dict):
        try:
            for field, value in new_data.items():
                if hasattr(instance, field):
                    setattr(instance, field, value)

            self.db.add(instance)
            await self.db.commit()
            await self.db.refresh(instance)
            return instance

        except IntegrityError as e:
            await self.db.rollback()
            raise RepositoryError(f"Integrity error while updating {self.model.__name__}", e)

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RepositoryError(f"Database error while updating {self.model.__name__}", e)

        except Exception as e:
            await self.db.rollback()
            raise RepositoryError(f"Unexpected error while updating {self.model.__name__}", e)

    # =========================================
    # > DELETE
    # =========================================
    async def delete(self, instance) -> bool:
        try:
            await self.db.delete(instance)
            await self.db.commit()
            return True

        except IntegrityError as e:
            await self.db.rollback()
            raise RepositoryError(f"Integrity error while deleting {self.model.__name__}", e)

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RepositoryError(f"Database error while deleting {self.model.__name__}", e)

        except Exception as e:
            await self.db.rollback()
            raise RepositoryError(f"Unexpected error while deleting {self.model.__name__}", e)

    async def delete_by_id(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        if not instance:
            raise RepositoryError(f"{self.model.__name__} with ID {id} not found")
        return await self.delete(instance)
